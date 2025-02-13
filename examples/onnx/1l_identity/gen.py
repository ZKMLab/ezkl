import torch
from torch import nn
import json


class MyModel(nn.Module):
    def __init__(self):
        super(MyModel, self).__init__()

    def forward(self, x):
        return x


circuit = MyModel()

x = 0.1*torch.rand(1, *[2], requires_grad=True)

# Flips the neural net into inference mode
circuit.eval()

# Export the model
torch.onnx.export(circuit,               # model being run
                  # model input (or a tuple for multiple inputs)
                  x,
                  # where to save the model (can be a file or file-like object)
                  "network.onnx",
                  export_params=True,        # store the trained parameter weights inside the model file
                  opset_version=10,          # the ONNX version to export the model to
                  do_constant_folding=True,  # whether to execute constant folding for optimization
                  input_names=['input'],   # the model's input names
                  output_names=['output'],  # the model's output names
                  dynamic_axes={'input': {0: 'batch_size'},    # variable length axes
                                'output': {0: 'batch_size'}})

data_array = ((x).detach().numpy()).reshape([-1]).tolist()

data = dict(input_data=[data_array])

# Serialize data into file:
json.dump(data, open("input.json", 'w'))
