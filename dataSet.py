import os
import pandas as pd
import torch
from torch.utils.data import Dataset
from PIL import Image
from torchvision import transforms

# 定义 ship_type 和 ship_class 的映射
ship_type_mapping = {'Corvette': 0, 'Frigate': 1, 'Destroyer': 2, 'Ferry': 3}
ship_class_mapping = {
    'Ada': 0, 'Independence': 1, 'Visby': 2, 'Alvaro De Bazan': 3, 'Jiangkai II': 4,
    'Oliver Hazard Perry': 5, 'Akizuki': 6, 'Sejong Daewang': 7, 'Zumwalt': 8, 'Armourique': 9,
}

class ShipDataset(Dataset):
    def __init__(self, preprocessed_dir, labels_dir, metadata_file, transform=None, use_data_count=None,data_dir=None):
        self.preprocessed_dir = preprocessed_dir  # 预处理后的数据文件夹
    # def __init__(self, images_dir, labels_dir, metadata_file, transform=None):
    #     self.images_dir = images_dir  # 原图文件夹
        self.labels_dir = labels_dir
        self.metadata = pd.read_csv(metadata_file)
        self.data_dir = data_dir

        # 将 ship_class 和 ship_type 转换为数值类型
        self.metadata['ship_class'] = self.metadata['ship_class'].map(ship_class_mapping)
        self.metadata['ship_type'] = self.metadata['ship_type'].map(ship_type_mapping)

        # 检查是否有 NaN 值
        if self.metadata['ship_class'].isnull().any():
            raise ValueError("Some ship_class values are not mapped correctly.")
        if self.metadata['ship_type'].isnull().any():
            raise ValueError("Some ship_type values are not mapped correctly.")

        # 打乱数据并取参数个数据
        if use_data_count is not None:
            self.metadata = self.metadata.sample(frac=1).reset_index(drop=True)  # 打乱数据
            self.metadata = self.metadata.head(use_data_count)  # 取参数个数据
            # print("1"+"-"*40)
            # print(self.metadata.head())

        self.transform = transform

    def __len__(self):
        return len(self.metadata)

    def __getitem__(self, idx):
        img_name = self.metadata.iloc[idx]['filename']
        img_path = os.path.join(self.preprocessed_dir, f"{img_name}.pt")    # 预处理后的数据路径
        # img_path = os.path.join(self.images_dir, img_name)                # 直接训练，不加载预处理后的数据
        label_path = os.path.join(self.labels_dir, self.metadata.iloc[idx]['labelname'])

        image = torch.load(img_path)              # 加载预处理后的图像
        # image = Image.open(img_path).convert('RGB') # 不加载预处理后的图像，直接加载原图
        label = Image.open(label_path).convert('L')
        x1, y1, x2, y2 = self.metadata.iloc[idx][['x1', 'y1', 'x2', 'y2']].values
        ship_class = self.metadata.iloc[idx]['ship_class']
        ship_type = self.metadata.iloc[idx]['ship_type']

        if self.transform:
            # image = self.transform(image)     # 直接训练时在这里预处理图像
            label = self.transform(label)

        return image, label, torch.tensor([x1, y1, x2, y2], dtype=torch.float32), \
               torch.tensor(ship_class, dtype=torch.long), torch.tensor(ship_type, dtype=torch.long)

    # 预处理数据，保存为 pt 文件，主要是图片太多，将预处理提出来，加快训练速度，但对磁盘消耗极大，30万张图预计消耗500g的磁盘空间
    def preprocess_data(self):
        preprocessed_dir = os.path.join(self.data_dir, 'preprocessed_images')  # 创建一个文件夹保存预处理后的数据
        os.makedirs(preprocessed_dir, exist_ok=True)
        # print("2"+"-"*40)
        # print(self.metadata.head())

        for idx, row in self.metadata.iterrows():
            img_name = row['filename']
            img_path = os.path.join(self.data_dir, 'irships/images', img_name)
            image = Image.open(img_path).convert('RGB')
            image = self.transform(image)
            torch.save(image, os.path.join(preprocessed_dir, f"{img_name}.pt"))
            if idx % 100 == 0:
                print(f"Processed {idx}/{len(self.metadata)} images")

        print("All images preprocessed and saved.")