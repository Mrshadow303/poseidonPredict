import os
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader
import numpy as np
import cv2
from sklearn.model_selection import train_test_split
from base_file.utils import DataSet

# 定义一些超参数
EPOCHS = 10
BATCH_SIZE = 32
LEARNING_RATE = 0.001
DATA_DIR = os.getcwd()               # 程序文件路径

# 定义你的模型
class ShipDetectionModel(nn.Module):
    def __init__(self, num_classes, num_types):
        super(ShipDetectionModel, self).__init__()
        self.feature_extractor = nn.Sequential(
            # 这里使用简单的卷积层，你可以替换为更复杂的模型，例如ResNet50
            nn.Conv2d(1, 16, kernel_size=3, stride=1, padding=1),
            nn.ReLU(),
            nn.MaxPool2d(kernel_size=2, stride=2),
            nn.Conv2d(16, 32, kernel_size=3, stride=1, padding=1),
            nn.ReLU(),
            nn.MaxPool2d(kernel_size=2, stride=2)
        )
        self.fc = nn.Sequential(
            nn.Linear(32*128*64, 1024),  # 假设输入图像大小为256x128
            nn.ReLU(),
            nn.Linear(1024, 512),
            nn.ReLU(),
            nn.Linear(512, 4 + num_classes + num_types)  # 4个坐标 + 船的分类 + 船的类型
        )

    def forward(self, x):
        x = self.feature_extractor(x)
        x = x.view(x.size(0), -1)
        x = self.fc(x)
        return x

# 加载数据
dataSet = DataSet(root=os.path.join(DATA_DIR, r"irships"),
                                metadata="metadata.csv",
                                sea_intensity_range=(5, 30),
                                sky_intensity_range=(2, 30),
                                clutter_intensity_range=None,
                                clutter_height_range=(0.2, 0.7),
                                clutter_probability=0.5,
                                augment_sea="/augment/sea",
                                augment_sky="/augment/sky",
                                augment_clutter="/augment/clutter",
                                cache_sea_images=True,
                                cache_sky_images=True,
                                cache_clutter_images=True,
                                blur=3,)

train_data, val_data = train_test_split(dataSet, test_size=0.2, random_state=42)
train_loader = DataLoader(train_data, batch_size=BATCH_SIZE, shuffle=True)
val_loader = DataLoader(val_data, batch_size=BATCH_SIZE, shuffle=False)

# 初始化模型、损失函数和优化器
model = ShipDetectionModel(num_classes=len(dataSet.key['Class']), num_types=len(dataSet.key['Type']))
criterion = nn.MSELoss()
optimizer = optim.Adam(model.parameters(), lr=LEARNING_RATE)

# 训练模型
def train():
    model.train()
    for epoch in range(EPOCHS):
        running_loss = 0.0
        for images, labels in train_loader:
            optimizer.zero_grad()
            outputs = model(images)
            loss = criterion(outputs, labels)
            loss.backward()
            optimizer.step()
            running_loss += loss.item()
        print(f"Epoch [{epoch + 1}/{EPOCHS}], Loss: {running_loss / len(train_loader)}")

# 验证模型
def validate():
    model.eval()
    val_loss = 0.0
    with torch.no_grad():
        for images, labels in val_loader:
            outputs = model(images)
            loss = criterion(outputs, labels)
            val_loss += loss.item()
    print(f"Validation Loss: {val_loss / len(val_loader)}")

# 主函数
if __name__ == "__main__":
    for epoch in range(EPOCHS):
        train()
        validate()
        # 可以在这里保存模型
        torch.save(model.state_dict(), f"model_epoch_{epoch + 1}.pth")
