# 模型转换
1. 执行模型转换
```
$ docker run --gpus '"device=4"' -it --rm -v /work:/work nvcr.io/nvidia/tensorrt:22.04-py3
$ trtexec --onnx=/work/wuzihao/triton/model_repository/nnUnet_onnx/1/model.onnx --explicitBatch --saveEngine=/work/wuzihao/triton/model_repository/nnUnet_onnx/1/model.engin --workspace=1024 --best
$ //静态batchsize的engine生成。
$ trtexec   --onnx=/work/wuzihao/demo/model_trans/results/BraTS2020.onnx \
            --explicitBatch \
            --workspace=4096 \
            --best \
            --saveEngine=/work/wuzihao/demo/model_trans/results/BraTS2020.engin 
```


## 模型性能测试报告
1. 启动tritonserver—sdk
   ```
   docker run -it --gpus '"device=0"' \
        -v /var/run/docker.sock:/var/run/docker.sock \
        -v /work:/work \
        -v /work/wuzihao/demo/model_trans/:/work/wuzihao/demo/model_trans \
        --net=host nvcr.io/nvidia/tritonserver:22.04-py3-sdk
   ```

2. 使用model-analyzer监测模型性能
   ```
   // 自动搜索config最佳配置参数
   model-analyzer profile \
        --model-repository /work/wuzihao/triton/model_repository \
        --profile-models BraTS --triton-launch-mode=docker \
        --output-model-repository-path /work/wuzihao/demo/model_trans/output \
        --run-config-search-max-model-batch-size 1 \
        --override-output-model-repository
   ```

3. 分析模型性能
> model-analyzer analyze --analysis-models nnUnet

4. 选择较优配置文件生成性能报告
> model-analyzer report --report-model-configs nnUnet_config_3,nnUnet_config_default,nnUnet_config_4 --export-path /workspace

5. 将结果复制到host端
```
cp -r ./summaries/ /work/wuzihao/
cp -r ./detailed/ /work/wuzihao/
```

## error
* trt模型部署时报错
```
E0915 01:26:07.509052 1 logging.cc:43] 1: [stdArchiveReader.cpp::StdArchiveReader::40] Error Code 1: Serialization (Serialization assertion stdVersionRead == serializationVersion failed.Version tag does not match. Note: Current Version: 205, Serialized Engine Version: 213)
E0915 01:26:07.509101 1 logging.cc:43] 4: [runtime.cpp::deserializeCudaEngine::50] Error Code 4: Internal Error (Engine deserialization failed.)
```
序列化引擎和反序列化引擎版本不一致。
* 查看trtexec的tensorrt版本
```
$ dpkg -l | grep TensorRT

```
* 查看docker镜像中tensorrt版本  
本例基于docker镜像文件支持tensorrt后端引擎模型执行。可通过官方镜像版本发布查看内部包含的tensorrt版本
```
https://docs.nvidia.com/deeplearning/triton-inference-server/release-notes/rel_22-04.html#rel_22-04
```
