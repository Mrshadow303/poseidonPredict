import torch
from torchvision import transforms
import os
import cv2
import numpy as np
from model import load_model

# 参数
model_name = "resnet50"              # 使用的预训练模型名称
num_types = 4                        # 船舶类型的数量
num_classes = 10                     # 船舶类别的数量
model_save_path = 'type18.7500_class12.5000%.pth'     # 已训练好的模型路径
DATA_DIR = os.getcwd()               # 程序文件路径

# 定义 ship_type 和 ship_class 的映射
ship_type_mapping = {0: "Corvette", 1: "Frigate", 2: "Destroyer", 3: "Ferry"}
ship_class_mapping = {
    0: "Ada",
    1: "Independence",
    2: "Visby",
    3: "Alvaro De Bazan",
    4: "Jiangkai II",
    5: "Oliver Hazard Perry",
    6: "Akizuki",
    7: "Sejong Daewang",
    8: "Zumwalt",
    9: "Armourique",
}

# 设置设备
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(f"正在使用 {device} 进行预测")

# 加载模型
model = load_model(model_name, num_classes, num_types).to(device)
model.load_state_dict(torch.load(os.path.join(DATA_DIR, model_save_path)))
model.eval()

# 定义图像转换
transform = transforms.Compose([
    transforms.ToPILImage(),
    transforms.Resize((224, 224)),
    transforms.ToTensor()
])

# 创建保存预测结果的文件夹
output_dir = os.path.join(DATA_DIR, "predictions")
os.makedirs(output_dir, exist_ok=True)

# 预测并保存结果函数
def predict_and_save(image_path, output_path):
    image = cv2.imread(image_path)
    if image is None:
        print(f"无法读取图像: {image_path}")
        return

    original_image = image.copy()

    # 将单通道图像转换为三通道图像
    if image.ndim == 2:
        image = np.stack((image,) * 3, axis=-1)

    image = transform(image).unsqueeze(0).to(device)

    with torch.no_grad():
        outputs_bbox, outputs_class, outputs_type = model(image)

    outputs_bbox = outputs_bbox.cpu().numpy()[0]
    outputs_class = torch.argmax(outputs_class, dim=1).cpu().numpy()[0]
    outputs_type = torch.argmax(outputs_type, dim=1).cpu().numpy()[0]

    # 将预测结果转换为对应的类别名称
    class_name = ship_class_mapping[outputs_class]
    type_name = ship_type_mapping[outputs_type]

    # 绘制边界框和类别信息
    x1, y1, x2, y2 = outputs_bbox
    cv2.rectangle(original_image, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 2)
    cv2.putText(original_image, f"Class: {class_name}", (int(x1), int(y1) - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (36, 255, 12), 2)
    cv2.putText(original_image, f"Type: {type_name}", (int(x1), int(y1) - 30), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (36, 255, 12), 2)

    # 保存结果图像
    cv2.imwrite(output_path, original_image)

    print(f"预测结果 - 边界框: {outputs_bbox}, 船舶类别: {class_name}, 船舶类型: {type_name}")
    print(f"结果已保存至: {output_path}")

# 测试样例
test_image_path = os.path.join(DATA_DIR, "irships/images/000000000.png")  # 需将此路径修改为你的测试图像路径
output_image_path = os.path.join(output_dir, "000000000_pred.png")
predict_and_save(test_image_path, output_image_path)
