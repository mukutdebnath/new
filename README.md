# PUMA Functional Simulator

## System requirements

Below you can find the system requirements and versions tested.

| Requirement | Version                    |
| ----------- | -------------------------- |
| Python      | 3.7.3                      |
| PyTorch      | 1.1.0                      |


## Quick start

`pytorch_sample.py` has a simple example inputs and weights matrix, and a simple network.
By the command `python pytorch_sample.py`, you can run the code. 

Conv2d_mvm is the custom module defined in pytorch_mvm_class.py

To run with physical crossbar models, use `-i` command like:
```bash
python pytorch_sample -i
```
And then for loops in mvm_tensor will work. 


## Supported configuration parameters

| parameters      | Meaning                                      | default value        |
| --------------- | -------------------------------------------- | -------------------- |
| bit_slice       | # of bit-slicing for weight (1, 2, 4, 8)     |       2              |
| bit_stream      | # of bit-stream for input (1, 2, 4, 8)       |       1              |
| weight_bits     | # of bits for fixed point of weight (16, 32) |      16              |
| weight_bit_frac | # of bits for fraction part of weight        |  16 -> 12 / 32 -> 24 |
| input_bits      | # of bits for fixed point of input (16, 32)  |      16              |
| input_bit_frac  | # of bits for fraction part of input         |  16 -> 12 / 32 -> 24 |
| adc_bit         | # of adc bits (1, 2, ... )                   |       9              |
| acm_bits        | # of bit of output                           |      16              |
| acm_bit_frac    | # of bits for fraction partof output         |  16 -> 12 / 32 -> 24 |


## Running NN models

CIFAR-100:
```bash
python3 pytorch_sample_cifar100.py -i <True for nonideal, False for ideal> -b <batch-size> --pretrained models/resnet20fp_cifar10.pth.tar --evaluate
```

Required model files:
- resnet20.py
- resnet20_mvm.py
- \_\_init\_\_.py

Note: resnet20_mvm.py has specifications for frac_bits for weights and inputs. Please change it inside the file. 

ImageNet
```bash
python3 pytorch_sample_imnet.py -i <True for nonideal, False for ideal> -b <batch-size> --pretrained models/resnet18_imnet_fp.pth.ar --evaluate
```
Required model files:
- resnet18_imnet.py
- resnet18_imnet_mvm.py
- \_\_init\_\_.py

Note: resnet18_imnet_mvm.py has specifications for frac_bits for weights and inputs. Please change it inside the file.


## Authors

Aayush Ankit, Dong-Eun Kim
