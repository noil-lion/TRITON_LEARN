
# 模型转换
模型转换使用的是技术路线时checkpoint->onnx->engin(plan)文件。
1. 技术路线是先将checkpoint文件转为onnx文件类型，指定输入维度(dummpy_input)，使用python脚本加载checkpoint文件，并转换为onnx格式，在启动tensorrt容器，使用trtexec工具模型转换，构建tensorrt推理引擎。
* 查看trtexec的tensorrt版本
```
$ dpkg -l | grep TensorRT

```
* 查看docker镜像中tensorrt版本  
本例基于docker镜像文件支持tensorrt后端引擎模型执行。可通过官方镜像版本发布查看内部包含的tensorrt版本
```
https://docs.nvidia.com/deeplearning/triton-inference-server/release-notes/rel_22-04.html#rel_22-04
```

* 执行模型转换
```
//单卡
$ docker run --gpus '"device=0"' -it --rm -v /work:/work nvcr.io/nvidia/tensorrt:22.04-py3
$ trtexec --onnx=/work/wuzihao/triton/model_repository/nnUnet_onnx/1/model.onnx --explicitBatch --saveEngine=/work/wuzihao/triton/model_repository/nnUnet_onnx/1/model.engin --workspace=1024 --best
$ //静态batchsize的engine生成。
$ trtexec   --onnx=/work/wuzihao/triton/model_repository/nnUnet_onnx/1/model.onnx \
            --explicitBatch  \
            --workspace=4096 \
            --best \
            --saveEngine=/work/wuzihao/triton/model_repository/nnUnet_onnx/1/model.engin 
```

#  模型部署测试

1. 配置文件编写
2. 模型仓库构建
3. tritonserver启动
4. tritonserver-sdk启动
5. model-perf测试
```
root@8d3d08540d36:/workspace# perf_analyzer -m BraTS_onnx --percentile=95 
*** Measurement Settings ***
  Batch size: 1
  Using "time_windows" mode for stabilization
  Measurement window: 5000 msec
  Using synchronous calls for inference
  Stabilizing using p95 latency

Request concurrency: 1
  Client: 
    Request count: 18
    Throughput: 3.6 infer/sec
    p50 latency: 241996 usec
    p90 latency: 422606 usec
    p95 latency: 461593 usec
    p99 latency: 571785 usec
    Avg HTTP time: 288135 usec (send/recv 75544 usec + response wait 212591 usec)
  Server: 
    Inference count: 21
    Execution count: 21
    Successful request count: 21
    Avg request latency: 178392 usec (overhead 866 usec + queue 814 usec + compute input 8326 usec + compute infer 136394 usec + compute output 31992 usec)

Failed to obtain stable measurement within 10 measurement windows for concurrency 1. Please try to increase the --measurement-interval.
Inferences/Second vs. Client p95 Batch Latency
Concurrency: 1, throughput: 3.6 infer/sec, latency 461593 usec
root@8d3d08540d36:/workspace# perf_analyzer -m BraTS --percentile=95 
*** Measurement Settings ***
  Batch size: 1
  Using "time_windows" mode for stabilization
  Measurement window: 5000 msec
  Using synchronous calls for inference
  Stabilizing using p95 latency

Request concurrency: 1
  Client: 
    Request count: 30
    Throughput: 6 infer/sec
    p50 latency: 149090 usec
    p90 latency: 246616 usec
    p95 latency: 280101 usec
    p99 latency: 390144 usec
    Avg HTTP time: 164001 usec (send/recv 67233 usec + response wait 96768 usec)
  Server: 
    Inference count: 35
    Execution count: 35
    Successful request count: 35
    Avg request latency: 73781 usec (overhead 130 usec + queue 199 usec + compute input 10209 usec + compute infer 32360 usec + compute output 30883 usec)

Inferences/Second vs. Client p95 Batch Latency
Concurrency: 1, throughput: 6 infer/sec, latency 280101 usec
```
