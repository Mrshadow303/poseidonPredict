import torch
import torch.nn as nn
import torch.optim as optim
from torchvision import transforms
from torch.utils.data import DataLoader
from base_file import utils
from model import load_model
import os
from tqdm import tqdm  # 进度条库
import cv2
import numpy as np

# 参数
num_types = 4                        # 船舶类型的数量
num_classes = 10                     # 船舶类别的数量
num_epochs = 1                       # 训练轮数
model_name = "resnet50"              # 使用的预训练模型名称
model_save_path = 'best_model.pth'   # 之前保存的模型路径，用来继续训练
continue_training = False            # 是否继续训练之前的模型
best_accuracy = 0.0                  # 初始化最佳准确率
use_data_count = 1000                # 训练时使用的数据数量，None 表示使用全部数据
DATA_DIR = os.getcwd()               # 程序文件路径

# 设置设备
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(f"正在使用 {device} 进行训练")

# 加载数据集
train_dataset = utils.DataSet(root=os.path.join(DATA_DIR, r"irships"),
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
                                blur=3,
                                )
train_loader = DataLoader(train_dataset, batch_size=64, shuffle=True)
# 加载模型
model = load_model(model_name, num_classes, num_types).to(device)

# 如果需要继续训练之前保存的模型，加载模型权重
if continue_training:
    model.load_state_dict(torch.load(os.path.join(DATA_DIR, model_save_path)))

criterion_bbox = nn.MSELoss()
criterion_class = nn.CrossEntropyLoss()
criterion_type = nn.CrossEntropyLoss()
optimizer = optim.Adam(model.parameters(), lr=0.001, weight_decay=0.0001)

# 训练循环
for epoch in range(num_epochs):
    model.train()
    running_loss = 0.0
    correct_class = 0
    correct_type = 0
    total = 0

    # 添加进度条显示
    with tqdm(total=len(train_loader), desc=f"Epoch {epoch+1}/{num_epochs}", unit="batch") as pbar:
        for batch in train_loader:
            images = []
            bboxes = []
            ship_classes = []
            ship_types = []

            for index in range(len(batch)):
                image = batch['image'][index]
                label = batch['label'][index]

                # 将单通道图像转换为三通道图像
                if image.ndim == 2:
                    image = np.stack((image,) * 3, axis=-1)

                images.append(image)

                x1, y1, x2, y2 = batch['shipBox'][index]
                ship_class = batch['shipClass'][index]
                ship_type = batch['shipType'][index]

                bboxes.append([x1, y1, x2, y2])
                ship_classes.append(ship_class)
                ship_types.append(ship_type)

            images = torch.stack([transforms.ToTensor()(img) for img in images]).to(device)
            bboxes = torch.tensor(bboxes, dtype=torch.float32).to(device)
            # print(f"ship_classes: {ship_classes}, ship_types: {ship_types}")
            ship_classes = torch.tensor(ship_classes, dtype=torch.long).to(device)
            ship_types = torch.tensor(ship_types, dtype=torch.long).to(device)

            optimizer.zero_grad()
            # 获取模型的输出
            outputs_bbox, outputs_class, outputs_type = model(images)

            # 计算损失
            loss_bbox = criterion_bbox(outputs_bbox, bboxes)
            loss_class = criterion_class(outputs_class, ship_classes)
            loss_type = criterion_type(outputs_type, ship_types)
            loss = loss_bbox + loss_class + loss_type
            loss.backward()
            optimizer.step()
            running_loss += loss.item()

            _, predicted_class = torch.max(outputs_class, 1)
            _, predicted_type = torch.max(outputs_type, 1)
            total += ship_classes.size(0)
            correct_class += (predicted_class == ship_classes).sum().item()
            correct_type += (predicted_type == ship_types).sum().item()

            # 更新进度条
            pbar.update(1)
            pbar.set_postfix({"Loss": running_loss / (pbar.n + 1), "Class Acc": 100 * correct_class / total, "Type Acc": 100 * correct_type / total})

    # 计算当前epoch的准确率
    class_accuracy = 100 * correct_class / total
    type_accuracy = 100 * correct_type / total
    print(f"Epoch {epoch+1}/{num_epochs}, Loss: {running_loss:.4f}, Class Accuracy: {class_accuracy:.2f}%, Type Accuracy: {type_accuracy:.2f}%")

    # 如果当前准确率高于最佳准确率，则保存模型
    if class_accuracy > best_accuracy:
        best_accuracy = class_accuracy
        torch.save(model.state_dict(), os.path.join(DATA_DIR, f"{class_accuracy:.4f}%.pth"))
        print(f"Best model saved with class accuracy: {best_accuracy:.4f}%")

# 强制保存最后一轮的模型
torch.save(model.state_dict(), os.path.join(DATA_DIR, f"final_{class_accuracy:.4f}%.pth"))
print("Final model saved.")