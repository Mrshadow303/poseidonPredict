from flask import Flask, request, jsonify
import torch
from ultralytics import YOLO
from PIL import Image
import io

# 创建 Flask 应用
app = Flask(__name__)

# 加载训练好的 YOLOv8 模型
model = YOLO('best.pt')

@app.route('/predict', methods=['POST'])
def predict():
    if 'image' not in request.files:
        return jsonify({'error': 'No image provided'}), 400

    # 获取上传的图像
    file = request.files['image']
    image_bytes = file.read()
    image = Image.open(io.BytesIO(image_bytes))

    # 使用 YOLO 模型进行推理
    results = model(image)

    # 处理结果，例如返回检测到的目标框和分类
    predictions = []
    for result in results:
        for box in result.boxes:
            predictions.append({
                'class': int(box.cls),
                'confidence': float(box.conf),
                'box': [float(x) for x in box.xyxy[0]]  # bounding box coordinates
            })

    # 返回推理结果
    return jsonify({'predictions': predictions})

# 启动 Flask 应用
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
