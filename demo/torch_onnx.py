import os
import torch
from torch import nn
import torch.onnx


class MyNet(nn.Module):

    def __init__(self):
        super(MyNet, self).__init__()

        self.embedding = nn.Embedding(num_embeddings=100,
                                      embedding_dim=10)

    def forward(self, input0, input1):
        # tf.add(tf.multiply(x1, 0.5), 2)
        output0 = torch.add(torch.multiply(input0, 0.5), 2)

        output1 = self.embedding(input1)

        return output0, output1


def torch2onnx(model_version_dir, max_batch):
    # 定义输入的格式
    example_input0 = torch.zeros([max_batch, 2], dtype=torch.float32)
    example_input1 = torch.zeros([max_batch, 2], dtype=torch.int32)

    my_model = MyNet()

    try:
        os.makedirs(model_version_dir)
    except OSError as ex:
        pass  # ignore existing dir

    torch.onnx.export(my_model,
                      (example_input0, example_input1),
                      os.path.join(model_version_dir, 'model.onnx'),
                      # 输入节点的名称
                      input_names=("INPUT0", "INPUT1"),
                      # 输出节点的名称
                      output_names=("OUTPUT0", "OUTPUT1"),
                      # 设置batch_size的维度
                      dynamic_axes={"INPUT0": [0], "INPUT1": [0], "OUTPUT0": [0], "OUTPUT1": [0]},
                      verbose=True)

torch2onnx("/work/workspace/triton/model_repository/mymodel_onxx/1", max_batch=32)