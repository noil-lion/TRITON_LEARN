triton服务启动指令，配置端口映射，并指定仓库地址:
cd /work/wuzihao/triton
CPU版:
docker run --rm -p40183:8000 -p40184:8001 -p40185:8002 -v /work/wuzihao/triton/model_repository:/models nvcr.io/nvidia/tritonserver:22.04-py3 tritonserver --model-repository=/models --strict-model-config=false
GPU版：
docker run --gpus "device=1" --rm -p40183:8000 -p40184:8001 -p40185:8002 -v /work/wuzihao/triton/model_repository:/models nvcr.io/nvidia/tritonserver:22.04-py3 tritonserver --model-repository=/models --strict-model-config=false

启动服务后，测试是否可连接
curl -v localhost:40184/v2/health/ready

启动客户端，发起推理请求
grpc版：
python client_grpc.py

http版：
python client_http.py

测试结果
Input: np.random.random([1, 1, 128, 160, 112]).astype(np.float32)

CPU版

grpc
grpc infer: 3.2185842990875244, 3.6354119777679443,  4.292175769805908
http
http infer: 10.05390453338623, 12.498617887496948, 11.113388538360596

GPU版
资源：
| Processes:                                                                  |
|  GPU   GI   CI        PID   Type   Process name                  GPU Memory |
|        ID   ID                                                   Usage      |
|    1   N/A  N/A   2367018      C   tritonserver                     3715MiB |
grpc
grpc infer: 0.27219104766845703
http
http infer: 6.692427396774292
