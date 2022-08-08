# Triton Server构建
Triton服务器采用的是Cmake和Docker构建。为了简化构建过程，Triton 提供了一个 build.py脚本。

## 使用docke构建


## 构建不适用docker
## pytorch后端的约定规则
***
### 命名规则
1. 输入单纯为张量时：
命名与Torchscript 模型的前向函数定义为 forward(self, input0, input1)参数要同名。
通用命名规则\<name>_<index>.
2. 输入为张量字典时：也就是类似json格式数据作为输入
这样的话，配置命名需要遵守名称name为键名称'A'命名规则。
> {'A': tensor1, 'B': tensor2}

### 配置规则
输入和输出形状由max_batch_size和输入输出的dims维度属性组合指定。  
对于尺寸可变的输入输出模型，可以在配置列表中将其配置为-1.
> dim[4, -1]//可变二维张量输入