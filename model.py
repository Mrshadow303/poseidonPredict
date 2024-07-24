# model.py 定义了ShipDetectionModel类，用于构建Ship Detection模型。
import torch
import torch.nn as nn
from torchvision import models

class ShipDetectionModel(nn.Module):
    def __init__(self, backbone, num_classes, num_types):
        super(ShipDetectionModel, self).__init__()
        self.backbone = backbone                      # 使用传入的骨干网络
        self.backbone.fc = nn.Identity()              # 移除骨干网络的全连接层，保留特征提取部分
        self.fc1 = nn.Linear(2048, 1024)              # 增加一个全连接层
        self.bn1 = nn.BatchNorm1d(1024)               # 增加Batch Normalization
        self.dropout1 = nn.Dropout(0.5)               # 增加Dropout层
        self.fc_bbox = nn.Linear(1024, 4)             # 定义用于回归任务的全连接层，输出4个值（边界框的坐标）
        self.fc_class = nn.Linear(1024, num_classes)  # 定义用于分类任务的全连接层，输出num_classes个值（类别概率）
        self.fc_type = nn.Linear(1024, num_types)     # 定义用于类型任务的全连接层，输出num_types个值（类型概率）

    def forward(self, x):
        features = self.backbone(x)                   # 提取输入图像的特征
        x = self.fc1(features)
        x = self.bn1(x)
        x = self.dropout1(x)
        bbox = self.fc_bbox(x)                        # 通过全连接层预测边界框的坐标
        ship_class = self.fc_class(x)                 # 通过全连接层预测船只的类别
        ship_type = self.fc_type(x)                   # 通过全连接层预测船只的类型
        return bbox, ship_class, ship_type

def load_model(model_name, num_classes, num_types):
    # 根据模型名称加载相应的模型
    if model_name == "resnet50":
        backbone = models.resnet50(pretrained=True)
    elif model_name == "resnet34":
        backbone = models.resnet34(pretrained=True)
    elif model_name == "resnet18":
        backbone = models.resnet18(pretrained=True)
    else:
        raise ValueError(f"模型 {model_name} 不存在")  # 如果模型名称不存在，抛出异常

    return ShipDetectionModel(backbone, num_classes, num_types)