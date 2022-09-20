# 基于BraTS脑瘤分割的nnUnet网络训练和部署实例

__概述__  
BraTS全名是Brain Tumor Segmentation，即脑部肿瘤分割。世界卫生组织（WHO）按细胞来源和行为对脑肿瘤进行分类，改善疾病诊断，治疗计划，监测和临床试验，需要可靠的脑肿瘤分割来检测肿瘤的位置和范围。

__挑战与困难__   
肿瘤几乎可以以任何形状和大小出现在不同的位置，对比度差，并且肿瘤的强度值可能与健康的脑组织的强度值重叠，肿瘤异质。  

Based:   
OS: Ubuntu 20.04;
EDITOR: VSCode 1.71.1;

Requirements:   
* GPU-A100
* nnUNet
* BraTS2020
* Pytorch
* Docker-nvidia
* TensorRT
* ONNX

Keywords: Medical Image Segmentation;nnUNet;Brain Tumor;TensorRT;Neural Network; Model Deployment & Acceleration.

## nnUNet-[start](./nnUnet_deploy/nnUNet.md)

## 数据集和预处理-[start](./nnUnet_deploy/DATASET.md)

## 模型训练与验证-[start](./nnUnet_deploy/Training.md)

## 模型部署与加速-[start](./nnUnet_deploy/DEPLOY.md)

## 性能测试和分析-[start](./nnUnet_deploy/Analysis.md)
