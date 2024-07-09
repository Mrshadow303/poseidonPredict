import torch
import torch.nn as nn
import torch.optim as optim
from torchvision import transforms
from torch.utils.data import DataLoader, Dataset
import pandas as pd
import numpy as np
from PIL import Image
from model import load_model
import os
from tqdm import tqdm  # 进度条库

# 参数
num_types = 4                        # 船舶类型的数量
num_classes = 10                     # 船舶类别的数量
num_epochs = 10                      # 训练轮数
model_name = "resnet50"              # 使用的预训练模型名称
model_save_path = 'best_model.pth'   # 之前保存的模型路径，用来继续训练
continue_training = False            # 是否继续训练之前的模型
best_accuracy = 0.0                  # 初始化最佳准确率
DATA_DIR = os.getcwd()               # 程序文件路径

# 定义 ship_type 和 ship_class 的映射
ship_type_mapping = { 'Corvette':0,'Frigate':1,'Destroyer':2,'Ferry':3,}
ship_class_mapping = {'Ada':0,'Independence':1,'Visby':2,'Alvaro De Bazan':3,'Jiangkai II':4,'Oliver Hazard Perry':5,
                      'Akizuki':6,'Sejong Daewang':7,'Zumwalt':8,'Armourique':9,}

# 设置设备
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(f"正在使用 {device} 进行训练")

# 定义数据集
class ShipDataset(Dataset):
    # def __init__(self, preprocessed_dir, labels_dir, metadata_file, transform=None):
        # self.preprocessed_dir = preprocessed_dir  # 预处理后的数据文件夹
    def __init__(self, images_dir, labels_dir, metadata_file, transform=None):
        self.images_dir = images_dir  # 原图文件夹
        self.labels_dir = labels_dir
        self.metadata = pd.read_csv(metadata_file, nrows=10000) #取10000条数据，测试
        self.transform = transform

        # 将 ship_class 和 ship_type 转换为数值类型
        self.metadata['ship_class'] = self.metadata['ship_class'].map(ship_class_mapping)
        self.metadata['ship_type'] = self.metadata['ship_type'].map(ship_type_mapping)

        # 检查是否有 NaN 值
        if self.metadata['ship_class'].isnull().any():
            raise ValueError("Some ship_class values are not mapped correctly.")
        if self.metadata['ship_type'].isnull().any():
            raise ValueError("Some ship_type values are not mapped correctly.")

    def __len__(self):
        return len(self.metadata)

    def __getitem__(self, idx):
        img_name = self.metadata.iloc[idx]['filename']
        # img_path = os.path.join(self.preprocessed_dir, f"{img_name}.pt")
        img_path = os.path.join(self.images_dir, img_name)
        label_path = os.path.join(self.labels_dir, self.metadata.iloc[idx]['labelname'])
        # image = torch.load(img_path)              # 加载预处理后的图像
        image = Image.open(img_path).convert('RGB') # 不加载预处理后的图像，直接加载原图
        label = Image.open(label_path).convert('L')
        x1, y1, x2, y2 = self.metadata.iloc[idx][['x1', 'y1', 'x2', 'y2']].values
        ship_class = self.metadata.iloc[idx]['ship_class']
        ship_type = self.metadata.iloc[idx]['ship_type']

        if self.transform:
            image = self.transform(image)
            label = self.transform(label)

        return image, label, torch.tensor([x1, y1, x2, y2], dtype=torch.float32), torch.tensor(ship_class, dtype=torch.long), torch.tensor(ship_type, dtype=torch.long)

# 数据变换
transform = transforms.Compose([
    transforms.Resize((256, 512)),  # 原分辨率(512, 1024)，这里降低是为了提高训练效率
    transforms.ToTensor()
])

# # 预处理数据，保存为 pt 文件，主要是图片太多，将预处理提出来，加快训练速度，但对磁盘消耗极大，30万张图预计消耗500g的磁盘空间
# preprocessed_dir = os.path.join(DATA_DIR, 'preprocessed_images')  # 创建一个文件夹保存预处理后的数据
# os.makedirs(preprocessed_dir, exist_ok=True)

# metadata_file = os.path.join(DATA_DIR, 'irships/metadata.csv')
# metadata = pd.read_csv(metadata_file)

# for idx, row in metadata.iterrows():
#     img_name = row['filename']
#     img_path = os.path.join(DATA_DIR, 'irships/images', img_name)
#     image = Image.open(img_path).convert('RGB')
#     image = transform(image)
#     torch.save(image, os.path.join(preprocessed_dir, f"{img_name}.pt"))
#     if idx % 100 == 0:
#         print(f"Processed {idx}/{len(metadata)} images")

# print("All images preprocessed and saved.")

# 使用预处理后的数据进行训练
# train_dataset = ShipDataset(preprocessed_dir=preprocessed_dir,
#                             labels_dir=os.path.join(DATA_DIR, 'irships/labels'),
#                             metadata_file=metadata_file,
#                             transform=transform)

# 使用原始数据进行训练
train_dataset = ShipDataset(images_dir=os.path.join(DATA_DIR, 'irships/images'),
                            labels_dir=os.path.join(DATA_DIR, 'irships/labels'),
                            metadata_file=os.path.join(DATA_DIR, 'irships/metadata.csv'),
                            transform=transform)
train_loader = DataLoader(train_dataset, batch_size=64, shuffle=True)
#train_loader = DataLoader(train_dataset, batch_size=64, shuffle=True, num_workers=4)  # 多线程加速,但有更高的性能要求

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
        for images, labels, bboxes, ship_classes, ship_types in train_loader:
            images, bboxes, ship_classes, ship_types = images.to(device), bboxes.to(device), ship_classes.to(device), ship_types.to(device)
            optimizer.zero_grad()
            outputs_bbox, outputs_class, outputs_type = model(images)
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


# 预测
# def predict(model, image_path):
#     image = Image.open(image_path).convert('RGB')
#     image = transform(image).unsqueeze(0).to(device)
#     model.eval()
#     with torch.no_grad():
#         bbox, ship_class, ship_type = model(image)
#     return bbox.squeeze().tolist(), ship_class.argmax().item(), ship_type.argmax().item()

# 使用示例
# bbox, ship_class, ship_type = predict(model, os.path.join(DATA_DIR, 'irships/images/000000000.png'))
# print(f"Bounding Box: {bbox}")
# print(f"Ship Class: {ship_class}")
# print(f"Ship Type: {ship_type}")
