import torch
import torchvision
import torchvision.transforms as transforms
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
import time
import sys

from pytorch_mvm_class import *
## To Indranil & Mustafa: This is for using 'for loops' in mvm_tensor. Just execute with '-i' at command line
ind = False
for i in range(len(sys.argv)):
    if sys.argv[i] == '-i':
        ind = True


normalize = transforms.Normalize( mean = [0.485, 0.456, 0.406], std = [0.229, 0.224, 0.225]) 
trainset = torchvision.datasets.CIFAR100(root='./data', train=True, download=True, transform =transforms.Compose([transforms.ToTensor(), normalize]))
trainloader = torch.utils.data.DataLoader(trainset, batch_size=64, shuffle=True, num_workers=4)


class Net(nn.Module):
    def __init__(self):
        super(Net, self).__init__()
        self.conv3_64    = nn.Conv2d(3,64,3, padding = 1)
        self.conv64_64   = nn.Conv2d(64,64,3, padding = 1)#, ind=ind)
        self.conv64_128  = nn.Conv2d(64,128,3, padding = 1)#, ind=ind)
        self.conv128_128 = nn.Conv2d(128,128,3, padding = 1)#, ind=ind)
        self.conv128_256 = nn.Conv2d(128,256,3, padding = 1)#, ind=ind)
        self.conv256_256 = nn.Conv2d(256,256,3, padding = 1)#, ind=ind)
        self.conv256_512 = nn.Conv2d(256,512,3, padding = 1)#, ind=ind)
        self.conv512_512 = nn.Conv2d(512,512,3, padding = 1)#, ind=ind)
        """
        self.conv3_64    = Conv2d_mvm(3,64,3, padding = 1, ind=ind)
        self.conv64_64   = Conv2d_mvm(64,64,3, padding = 1, ind=ind)
        self.conv64_128  = Conv2d_mvm(64,128,3, padding = 1, ind=ind)
        self.conv128_128 = Conv2d_mvm(128,128,3, padding = 1, ind=ind)
        self.conv128_256 = Conv2d_mvm(128,256,3, padding = 1, ind=ind)
        self.conv256_256 = Conv2d_mvm(256,256,3, padding = 1, ind=ind)
        self.conv256_512 = Conv2d_mvm(256,512,3, padding = 1, ind=ind)
        self.conv512_512 = Conv2d_mvm(512,512,3, padding = 1, ind=ind)
        """

        self.relu = nn.ReLU(True)
        self.pool = nn.MaxPool2d(2,2)

        self.linear1 = nn.Linear(512,512)
        print(self.linear1.weight.data.shape)
        self.classifier = nn.Sequential(
            nn.Linear(512, 512),
            nn.ReLU(True),
            nn.Linear(512, 512),
            nn.ReLU(True),
            nn.Linear(512, 100),
        )


        for m in self.modules():
            if isinstance(m, Conv2d_mvm) or isinstance(m, nn.Conv2d):
                n = m.kernel_size[0] * m.kernel_size[1] * m.out_channels
                std = np.sqrt(2./n)
                m.weight.data.normal_(0, std)
                m.bias.data.zero_()
#                print("normalized")
        device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")

    def forward(self, x):
        print("1st layer")
        x = self.relu(self.conv3_64(x))
        
        print("2nd layer")
        x = self.relu(self.conv64_64(x))
        
        x = self.pool(x)

        x = self.relu(self.conv64_128(x))
        print("3rd layer")
        x = self.relu(self.conv128_128(x))
        print("4th layer")
        x = self.pool(x)

        x = self.relu(self.conv128_256(x))
        print("5th layer")
        x = self.relu(self.conv256_256(x))
        print("6th layer")
        x = self.relu(self.conv256_256(x))
        print("7th layer")
        x = self.pool(x)

        x = self.relu(self.conv256_512(x))
        print("8th layer")
        x = self.relu(self.conv512_512(x))
        print("9th layer")
        x = self.relu(self.conv512_512(x))
        print("10th layer")
        x = self.pool(x)


        x = self.relu(self.conv512_512(x))
        print("11tj layer")
        x = self.relu(self.conv512_512(x))
        print("12th layer")
        x = self.relu(self.conv512_512(x))
        print("13th layer")
        x = self.pool(x)
        print(x.shape)
        x = x.view(x.size(0), -1)
        print(x.shape)
        x = self.classifier(x)
        
        return x


net = Net()

device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
net.to(device)
#print(net.conv1.weight.shape)
criterion = nn.CrossEntropyLoss()
optimizer = optim.SGD(net.parameters(), lr=0.001, momentum=0.9)

for itr in range(1):
    forward = 0
    for i, data in enumerate(trainloader):
        inputs, labels = data
        torch.cuda.synchronize()
        input_begin = time.perf_counter()
        inputs, labels = inputs.to(device), labels.to(device)   
        #print(time.perf_counter()-input_begin)

        torch.cuda.synchronize()
        forward_begin = time.perf_counter() 
        outputs = net(inputs)

        forward_time = time.perf_counter() - forward_begin
        #print(forward_time)

        forward += forward_time
        break

