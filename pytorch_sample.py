import torch
import torchvision
import torchvision.transforms as transforms
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
import sys

from pytorch_mvm_class import *

## To Indranil & Mustafa: This is for using 'for loops' in mvm_tensor. Just execute with '-i' at command line
ind = False
for i in range(len(sys.argv)):
    if sys.argv[i] == '-i':
        ind = True

inputs = torch.tensor([[[[-1.,0,1],[2,1,0],[1,2,1]],[[2,3,1],[2,0,1],[4,2,1]],[[3,2,1],[0,2,1],[5,3,2]]], [[[1.,0,1],[-2,1,0],[1,-2,1]],[[2,-3,1],[-2,0,-1],[4,-2,-1]],[[-3,2,1],[0,2,1],[-5,3,2]]]])/10
#inputs = torch.tensor([[[[1.,0,1],[2,1,0],[1,2,1]],[[2,3,1],[2,0,1],[4,2,1]],[[3,2,1],[0,2,1],[5,3,2]]], [[[-1.,0,1],[2,1,0],[1,2,1]],[[2,3,1],[2,0,1],[4,2,1]],[[3,2,1],[0,2,1],[5,3,2]]]])

labels = torch.tensor([1, 1])
weights = torch.tensor([[[[-2.,1],[-1,2]],[[-4,2],[0,1]],[[-1,0],[-3,-2]]],[[[2.,1],[1,2]],[[3,2],[1,1]],[[1,2],[3,2]]]])/10
trainloader = [[inputs, labels]]
trainset = torchvision.datasets.CIFAR10(root='./data', train=True, download=True, transform =transforms.Compose([transforms.ToTensor()]))
trainloader = torch.utils.data.DataLoader(trainset, batch_size=1, shuffle=True, num_workers=4)
inputs, labels = next(iter(trainloader))
#trainset = torchvision.datasets.CIFAR10(root='./data', train=True, download=True, transform =transforms.Compose([transforms.ToTensor()]))
#trainloader = torch.utils.data.DataLoader(trainset, batch_size=1, shuffle=True, num_workers=4)


#inputs = torch.rand(64,64,32,32).sub(0.5).mul(0.5)
#weights = torch.rand(64,64,3,3).sub(0.5).mul(0.5)


#weights_lin = torch.rand(10,288).sub_(0.5).mul_(0.5)


#inputs_lin = torch.tensor([[-1.,0,1,2,-2],[5, 4, 3, 2, 1]])/10
#weights_lin = torch.tensor([[-1.,0,1,2,-2],[5, 4, 3, 2, 1],[-1, -2, -3, -4, -5]])/10

class Net(nn.Module):
    def __init__(self):
        super(Net, self).__init__()

        self.conv1 = nn.Conv2d(3,64,3, bias=False, stride =1 )
        self.conv2 = nn.Conv2d(64,64,3, bias=False, stride =2 )
        self.avgpool = nn.AvgPool2d(14)
        self.linear = nn.Linear(64,10, bias = False)
        #print(self.linear.weight.data.shape)
        #self.linear.weight.data = torch.clone(weights_lin)

    def forward(self, x):
        #self.conv1.weight.data = torch.clone(weights_conv[0])
        print(self.conv1.weight.data[0][0][0])
        x = self.conv1(x)

        #self.conv2.weight.data = torch.clone(weights_conv[1])
        print(self.conv2.weight.data[0][0][0])
        x = self.conv2(x)
        #pdb.set_trace()
        x = self.avgpool(x)
        x = x.view(x.size(0), -1)
        x = self.linear(x)
        return x


class my_Net(nn.Module):
    def __init__(self):
        super(my_Net, self).__init__()
        self.conv1 = Conv2d_mvm(3,64,3, bit_slice = 4, stride=1, bit_stream = 4, bias=False, ind=ind)   # --> my custom module for mvm
        self.conv2 = Conv2d_mvm(64,64,3, bit_slice = 4, stride=2, bit_stream = 4, bias=False, ind=ind)
        self.avgpool = nn.AvgPool2d(14)
        self.linear = Linear_mvm(64,10, bit_slice = 4, bit_stream = 4, bias=False, ind=ind)
        #self.linear.weight.data = torch.clone(weights_lin)

    def forward(self, x):
        self.conv1.weight.data = torch.clone(weights_conv[0])
        print(self.conv1.weight.data[0][0][0])
        x = self.conv1(x)

        self.conv2.weight.data = torch.clone(weights_conv[1])
        print(self.conv2.weight.data[0][0][0])
        x = self.conv2(x)
        x = self.avgpool(x)
        x = x.view(x.size(0),-1)
        self.linear.weight.data = torch.clone(weights_lin)
        x = self.linear(x)
        return x


net = Net()
mynet = my_Net()


device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
net.to(device)
mynet.to(device)
inputs = inputs.to(device)
weights_conv = []
for m in net.modules():
    
  #  print (m)for m in model.modules():
    if isinstance(m, nn.Conv2d):
        n = m.kernel_size[0] * m.kernel_size[1] * m.out_channels
        m.weight.data.normal_(0, math.sqrt(2. / n))
        weights_conv.append(m.weight.data.clone())
    elif isinstance(m, nn.Linear):
            stdv = 1. / math.sqrt(m.weight.data.size(1))
            m.weight.data.uniform_(-stdv, stdv)
            weights_lin = m.weight.data.clone()
            if m.bias is not None:
               m.bias.data.uniform_(-stdv, stdv)


torch.cuda.synchronize()
begin = time.time()
result_net = net(inputs)

torch.cuda.synchronize()
end = time.time()
print(end-begin)
result_mynet = mynet(inputs)

torch.cuda.synchronize()
end2 = time.time()
print(end2-end)


print(result_net[0])

print(result_mynet[0])
print(torch.norm(result_net-result_mynet))