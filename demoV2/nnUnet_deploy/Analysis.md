## Triton perf性能测试

启动客户端容器，此时会进入客户端容器内部的workspace文件夹，可在此进行发起请求和性能分析。
```
docker run -it --rm --net=host nvcr.io/nvidia/tritonserver:22.04-py3-sdk
```

```
perf_analyzer -m nnUnet --percentile=95  --concurrency=10
```

* 基于onnx模型
```
  root@8d3d08540d36:/workspace# perf_analyzer -m nnUnet_onnx --percentile=95  --measurement-interval=10000
*** Measurement Settings ***
  Batch size: 1
  Using "time_windows" mode for stabilization
  Measurement window: 10000 msec
  Using synchronous calls for inference
  Stabilizing using p95 latency

Request concurrency: 1
  Client:
    Request count: 535
    Throughput: 53.5 infer/sec
    p50 latency: 17466 usec
    p90 latency: 23158 usec
    p95 latency: 29602 usec
    p99 latency: 34782 usec
    Avg HTTP time: 18876 usec (send/recv 6329 usec + response wait 12547 usec)
  Server:
    Inference count: 635
    Execution count: 635
    Successful request count: 635
    Avg request latency: 9403 usec (overhead 72 usec + queue 78 usec + compute input 667 usec + compute infer 7544 usec + compute output 1042 usec)

Inferences/Second vs. Client p95 Batch Latency
Concurrency: 1, throughput: 53.5 infer/sec, latency 29602 usec

```
* 基于tensorrt模型
```
root@8d3d08540d36:/workspace# perf_analyzer -m nnUnet --percentile=95  --measurement-interval=10000
*** Measurement Settings ***
  Batch size: 1
  Using "time_windows" mode for stabilization
  Measurement window: 10000 msec
  Using synchronous calls for inference
  Stabilizing using p95 latency

Request concurrency: 1
  Client:
    Request count: 635
    Throughput: 63.5 infer/sec
    p50 latency: 15004 usec
    p90 latency: 17989 usec
    p95 latency: 21624 usec
    p99 latency: 28319 usec
    Avg HTTP time: 15610 usec (send/recv 5775 usec + response wait 9835 usec)
  Server:
    Inference count: 769
    Execution count: 769
    Successful request count: 769
    Avg request latency: 7394 usec (overhead 73 usec + queue 59 usec + compute input 1427 usec + compute infer 4396 usec + compute output 1439 usec)

Inferences/Second vs. Client p95 Batch Latency
Concurrency: 1, throughput: 63.5 infer/sec, latency 21624 usec
```
结论：在compute infer有了一定提升，4396 usec /7544 usec, 推理计算的平均延时降至原来的58.3%，但计算的输入输出延时在一定程度上增加，总的请求处理的平均延时为7394 usec/ 9403 usec,降至原先的78.6%，在吞吐量上，也有一定提升，

* 高并发
```
root@8d3d08540d36:/workspace# perf_analyzer -m nnUnet --percentile=95  --concurrency=10
*** Measurement Settings ***
  Batch size: 1
  Using "time_windows" mode for stabilization
  Measurement window: 5000 msec
  Using synchronous calls for inference
  Stabilizing using p95 latency

Request concurrency: 10
  Client:
    Request count: 1151
    Throughput: 230.2 infer/sec
    p50 latency: 45722 usec
    p90 latency: 63800 usec
    p95 latency: 74476 usec
    p99 latency: 103171 usec
    Avg HTTP time: 44099 usec (send/recv 13011 usec + response wait 31088 usec)
  Server:
    Inference count: 1360
    Execution count: 1360
    Successful request count: 1360
    Avg request latency: 11651 usec (overhead 59 usec + queue 5446 usec + compute input 1860 usec + compute infer 2941 usec + compute output 1345 usec)

Inferences/Second vs. Client p95 Batch Latency
Concurrency: 10, throughput: 230.2 infer/sec, latency 74476 usec
root@8d3d08540d36:/workspace# perf_analyzer -m nnUnet --percentile=95  --concurrency=10
*** Measurement Settings ***
  Batch size: 1
  Using "time_windows" mode for stabilization
  Measurement window: 5000 msec
  Using synchronous calls for inference
  Stabilizing using p95 latency

Request concurrency: 10
  Client:
    Request count: 1262
    Throughput: 252.4 infer/sec
    p50 latency: 38170 usec
    p90 latency: 57941 usec
    p95 latency: 66884 usec
    p99 latency: 116117 usec
    Avg HTTP time: 41146 usec (send/recv 12259 usec + response wait 28887 usec)
  Server:
    Inference count: 1464
    Execution count: 1464
    Successful request count: 1464
    Avg request latency: 15780 usec (overhead 76 usec + queue 9322 usec + compute input 1944 usec + compute infer 2837 usec + compute output 1601 usec)

Inferences/Second vs. Client p95 Batch Latency
Concurrency: 10, throughput: 252.4 infer/sec, latency 66884 usec
root@8d3d08540d36:/workspace# perf_analyzer -m nnUnet_onnx --percentile=95  --concurrency=10
*** Measurement Settings ***
  Batch size: 1
  Using "time_windows" mode for stabilization
  Measurement window: 5000 msec
  Using synchronous calls for inference
  Stabilizing using p95 latency

Request concurrency: 10
  Client:
    Request count: 627
    Throughput: 125.4 infer/sec
    p50 latency: 79382 usec
    p90 latency: 83123 usec
    p95 latency: 84783 usec
    p99 latency: 89577 usec
    Avg HTTP time: 79927 usec (send/recv 6711 usec + response wait 73216 usec)
  Server:
    Inference count: 752
    Execution count: 752
    Successful request count: 752
    Avg request latency: 70356 usec (overhead 50 usec + queue 62375 usec + compute input 591 usec + compute infer 6488 usec + compute output 852 usec)

Inferences/Second vs. Client p95 Batch Latency
Concurrency: 10, throughput: 125.4 infer/sec, latency 84783 usec
root@8d3d08540d36:/workspace# perf_analyzer -m nnUnet_onnx --percentile=95  --concurrency=10
*** Measurement Settings ***
  Batch size: 1
  Using "time_windows" mode for stabilization
  Measurement window: 5000 msec
  Using synchronous calls for inference
  Stabilizing using p95 latency

Request concurrency: 10
  Client:
    Request count: 562
    Throughput: 112.4 infer/sec
    p50 latency: 88684 usec
    p90 latency: 94148 usec
    p95 latency: 96037 usec
    p99 latency: 99301 usec
    Avg HTTP time: 89268 usec (send/recv 7500 usec + response wait 81768 usec)
  Server:
    Inference count: 673
    Execution count: 673
    Successful request count: 673
    Avg request latency: 76201 usec (overhead 96 usec + queue 67301 usec + compute input 811 usec + compute infer 6849 usec + compute output 1144 usec)

Inferences/Second vs. Client p95 Batch Latency
Concurrency: 10, throughput: 112.4 infer/sec, latency 96037 usec

```