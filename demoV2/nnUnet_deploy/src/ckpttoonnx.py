import torch
from torch import nn
import  pickle
from nnunet.training.model_restore import load_model_and_checkpoint_files
import os
import numpy as np
 
if __name__ == "__main__":
 
    #convert .model to .onnx
    Model_path = "/work/wuzihao/DeepLearningExamples-master/PyTorch/Segmentation/nnUNet/results/checkpoints"
    folds='all'
    checkpoint_name = "model_final_checkpoint" 
 
    trainer, params = load_model_and_checkpoint_files(Model_path, folds=folds, mixed_precision=True, checkpoint_name=checkpoint_name)  
    net = trainer.network
   
    checkpoint = torch.load(os.path.join( Model_path , folds, checkpoint_name +".model"))
 
    net.load_state_dict(checkpoint['state_dict'])
    net.eval()
    dummy_input = torch.randn(1, 4, 512, 512).to("cuda")
    torch.onnx.export(
        net,
        dummy_input,
        'dynamic-1.onnx',
        input_names=['input'],
        output_names=['output'],
        dynamic_axes = {'input': {0: 'batch_size'},'output': {0: 'batch_size'}}
        )
