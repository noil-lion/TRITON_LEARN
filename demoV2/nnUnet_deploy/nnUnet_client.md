# nnUnet的triton客户端构建

## 客户端实例-TritonInferRequest
1. 层级结构  
依赖Triton官方提供的库及对应实现:  
common.cpp->common.h,  
grpc_client.h->common.h,  
TritonInferRequest.h->grpc_client.h + ITKCommon.h(输入数据接口类)  

2. TritonInferRequest.h
推理请求发起及接收模块的头文件.这里解析一下其基本组成.   
* InferOptionBase结构体
推理选项信息结构体定义
```
struct InferOptionBase {
  // model folder info in triton server  在服务器中的模型文件夹信息
  std::string modelName;                 //模型名
  std::string modelVersion;              //模型版本号
  std::string url;                       //模型路径
  // model info in triton server         模型信息
  std::string outputName;                //输出名
  std::string inputName;                 //输入名
  std::string inputDatatype;             //输入数据类型
  // The shape of the input              输入输出维度
  int inputC;                             
  int outputC;
  // The format of the input NCDHW         NCDHW输入格式
  std::string inputFormat;
  int maxBatchSize;                        //最大batch

  std::vector<int> patchSize;              //前处理参数
  float probThreshold;                     //后处理参数
  int overlapSize;                         //overlap裁剪重叠尺寸
  // "max" or "avg"
  std::string overlapMethod;               //重构时overlap处理方法,是最大化法还是平均法
};
```
* 定义TritonInferRequest类及类方法:
```
 protected:
  std::unique_ptr<tClient::InferenceServerGrpcClient> grpcClient_;
  tClient::InferInput* input;           //输入
  tClient::InferRequestedOutput* output;  //输出
  tClient::Headers httpHeaders;           //http头
  tClient::Error err;                     //错误

  ThreeUcMaskType::Pointer outputMask_;   //输出mask
  std::vector<int> dimOrder_;             //dimorder
  InferOptionBase option_;                //推理选项
  VolumeInfo rawImageInfo_;               //原始图像信息
  bool verbose_;
```
包含构造函数和析构函数:
```
public:
    TritonInferRequest(InferOptionBase& option, std::vector<int>& dimOrder, bool verbose = false);
    ~TritonInferRequest();
```
客户端初始化函数  
```
void initialize();
```
推理执行函数,函数声明为patchwise的推理,前处理及推理request发送将在该函数中定义.
```
void inferPatchwise(ThreeFlImageType::Pointer rawImage, std::vector<std::vector<std::vector<int>>> patchIndexes, std::string activation = "none");
```
后处理函数,将网络预测结果进行重构拼接
```
bool inferResultToMaskBuffer(std::unique_ptr<tClient::InferResult> result, std::vector<std::vector<std::vector<int>>> batchPatchIndexes, int patchNum,
                               std::string activation, int requestIndex, std::vector<int> outputDataDimOrder, float* gaussianMapsBuffer, float* dataBuffer,
                               float* aggregatedGaussianBuffer);
```

## TritonInferRequest.cpp
依赖于TritonInferRequest.h文件
1. TritonInferRequest构造函数
```
TritonInferRequest::TritonInferRequest(InferOptionBase& option, std::vector<int>& dimOrder, bool verbose) {
  option_ = option;      //选项赋值
  verbose_ = verbose;    //
  dimOrder_ = dimOrder;  //维度order
}

```

2. 初始化initialize函数实现  

```
std::string modelName = option_.modelName;
std::string modelVersion = option_.modelVersion;
std::string url = option_.url;

// 1. Create the inference client for the server. 
err = tClient::InferenceServerGrpcClient::Create(&grpcClient_, url, verbose_);   //client端实例创建

// 2. Initialize the inputs with the data.
std::vector<int64_t> rawPatchShape = {option_.patchSize[2], option_.patchSize[1], option_.patchSize[0]};  //patch形状确定
std::vector<int64_t> shape = {option_.maxBatchSize, option_.inputC, rawPatchShape[dimOrder_[0]], rawPatchShape[dimOrder_[1]], rawPatchShape[dimOrder_[2]]};  //输入数据维度确定

err = tClient::InferInput::Create(&input, option_.inputName, shape, option_.inputDatatype); //创建输入对象实例

//3. 初始化请求输出对象实例
err = tClient::InferRequestedOutput::Create(&output, option_.outputName);  //创建赋值给output
if (!err.IsOk()) { THROW_RETURNCODE(IBOT_RETURNCODE::MODEL_INFERENCE_ERROR, "unable to get output: " + err.Message()); }  //错误判断
```
3. inferPatchwise:patchwise级的推理请求发送函数实现.
```
void TritonInferRequest::inferPatchwise(ThreeFlImageType::Pointer rawImage, std::vector<std::vector<std::vector<int>>> patchIndexes, std::string activation) {}

//1. 获取原始数据图像信息并进行patch分割

```
