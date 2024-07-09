import torch
import torch.nn as nn
from torchvision import models

class ShipDetectionModel(nn.Module):
    def __init__(self, num_classes, num_types):
        super(ShipDetectionModel, self).__init__()
        self.backbone = models.resnet50(pretrained=True)    # 使用预训练的ResNet50作为骨干网络
        self.backbone.fc = nn.Identity()                    # 移除ResNet的全连接层，保留特征提取部分
        self.fc_bbox = nn.Linear(2048, 4)                   # 定义用于回归任务的全连接层，输出4个值（边界框的坐标）
        self.fc_class = nn.Linear(2048, num_classes)        # 定义用于分类任务的全连接层，输出num_classes个值（类别概率）
        self.fc_type = nn.Linear(2048, num_types)           # 定义用于类型任务的全连接层，输出num_types个值（类型概率）

    def forward(self, x):
        features = self.backbone(x)             # 提取输入图像的特征
        bbox = self.fc_bbox(features)           # 通过全连接层预测边界框的坐标
        ship_class = self.fc_class(features)    # 通过全连接层预测船只的类别
        ship_type = self.fc_type(features)      # 通过全连接层预测船只的类型
        return bbox, ship_class, ship_type

def load_model(model_name, num_classes, num_types):
    # 根据模型名称加载相应的模型
    if model_name == "resnet50":
        return ShipDetectionModel(num_classes, num_types)
    else:
        raise ValueError(f"模型 {model_name} 不存在")    # 如果模型名称不存在，抛出异常
