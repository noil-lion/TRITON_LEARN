# 由onnx文件构建tensorrt引擎
## 使用trtexec工具进行序列化引擎构建
trtexec有两个主要用途：  

* 测试网络性能 - 可以使用 trtexec 工具来测试保存为 UFF 文件、ONNX 文件、Caffe prototxt 格式的模型推理的性能，trtexec 工具有许多选项用于指定输入和输出、性能计时的迭代、允许的精度等。
* 序列化引擎生成 - 可以将UFF、ONNX、Caffe格式的模型构建成engine。

## ONNX->engine
