# Triton inferrence Server简介
一款开源推理服务软件，简化AI推理。  
***
同时支持在GPU、x86 和 ARM CPU 或 AWS Inferentia 上跨云、数据中心、边缘和嵌入式设备进行推理。  

能部署来自多个深度学习和机器学习框架的任何AI模型。(TensorRT、TensorFlow、PyTorch、ONNX、OpenVINO、Python、RAPIDS FIL)  
***
## Triton 结构
### 基本元素
1. 模型仓库（model repository）
   基于文件系统存储要使用的模型仓库。
3. 并发执行
4. 动态批处理
5. Pipeline建模（BLS）
6. 推理协议（HTTP/GRPC）
7. 请求响应调度及批处理
8. 后端C API
9. python/C++库

![var](pic/Triton_arc.jpg)
