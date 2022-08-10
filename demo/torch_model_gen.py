import os
import torch
from torch import nn


class MyNet(nn.Module):

    def __init__(self):
        super(MyNet, self).__init__()
        self.embedding = nn.Embedding(100, 8)
        self.fc = nn.Linear(8, 4)
        self.fc_list = nn.Sequential(*[nn.Linear(8, 8) for _ in range(4)])

    def forward(self, input_ids):
        word_emb = self.embedding(input_ids)
        output1 = self.fc(word_emb)
        output2 = self.fc_list(word_emb)
        return output1, output2


def create_modelfile(model_version_dir, version_policy=None):
    # your model net

    # 定义输入的格式
    example_input0 = torch.tensor([[1, 2, 3], [4, 5, 6]], dtype=torch.long)

    my_model = MyNet()

    traced = torch.jit.trace(my_model, (example_input0))

    try:
        os.makedirs(model_version_dir)
    except OSError as ex:
        pass  # ignore existing dir

    traced.save(model_version_dir + "/model.pt")


create_modelfile("/work/wuzihao/triton/model_repository/mymodel_pt/1")