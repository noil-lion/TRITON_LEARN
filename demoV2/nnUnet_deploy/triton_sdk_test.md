# triton_sdk测试

## docker file 文件
```
# triton-DockerFile
ARG FROM_IMAGE_NAME=nvcr.io/nvidia/pytorch:21.11-py3  # 基镜像依旧是pytorch 21.11
FROM ${FROM_IMAGE_NAME} 

ADD ./triton/requirements.txt .    # 添加trtiton requirements文件
RUN pip install --disable-pip-version-check -r requirements.txt
RUN apt-get update && apt-get install -y libb64-dev libb64-0d

ADD ./requirements.txt .   # 添加训练基环境文件
RUN pip install --disable-pip-version-check -r requirements.txt
RUN pip install monai==0.8.0 --no-dependencies

RUN curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
RUN unzip -qq awscliv2.zip
RUN ./aws/install
RUN rm -rf awscliv2.zip aws

WORKDIR /workspace/nnunet_pyt
ADD . /workspace/nnunet_pyt 
```

## triton requirements文件
```
# triton/requirements.txt
networkx==2.5
onnx==1.8.0
onnxruntime==1.5.2
pycuda>=2019.1.2
PyYAML>=5.2
tqdm>=4.44.1
tabulate>=0.8.7
natsort>=7.0.0
# use tags instead of branch names - because there might be docker cache hit causing not fetching most recent changes on branch
model_navigator @ git+https://github.com/triton-inference-server/model_navigator.git@v0.1.0#egg=model_navigator
```

## 设置环境变量
```
# source triton/scripts/setup_environment.sh
WORKDIR="$(pwd)"
export WORKSPACE_DIR=${WORKDIR}/workspace
export DATASETS_DIR=${WORKSPACE_DIR}/datasets_dir/01_3d/
export CHECKPOINT_DIR=${WORKSPACE_DIR}/checkpoint_dir
export MODEL_REPOSITORY_PATH=${WORKSPACE_DIR}/model_store
export SHARED_DIR=${WORKSPACE_DIR}/shared_dir

echo "Preparing directories"  # 创建目录
mkdir -p ${WORKSPACE_DIR}
mkdir -p ${DATASETS_DIR}
mkdir -p ${CHECKPOINT_DIR}
mkdir -p ${MODEL_REPOSITORY_PATH}
mkdir -p ${SHARED_DIR}

echo "Setting up environment"  # 设置环境变量
export MODEL_NAME=nnunet
export TRITON_LOAD_MODEL_METHOD=explicit
export TRITON_INSTANCES=1
export TRITON_SERVER_URL=127.0.0.1
```

## 构建指令
```
git clone https://github.com/NVIDIA/DeepLearningExamples.git

cd DeepLearningExamples/PyTorch/Segmentation/nnUNet

source triton/scripts/setup_environment.sh

bash triton/scripts/docker/triton_inference_server.sh  # 可选

mv data ../data
mv results ../results

bash triton/scripts/docker/build.sh  # 构建部署容器

bash triton/scripts/docker/interactive.sh  # 交互
```