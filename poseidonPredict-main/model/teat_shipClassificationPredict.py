import requests
import json

# 定义 Flask 应用的 URL
url = 'http://127.0.0.1:5000/predict'

# 定义要发送的图像文件路径
image_path = 'images\\000004468.png'

# 打开图像文件并读取其内容
with open(image_path, 'rb') as image_file:
    image_data = image_file.read()

# 发送 POST 请求到 Flask 应用的 /predict 接口
response = requests.post(url, files={'image': image_data})

# 检查响应状态码
if response.status_code == 200:
    # 解析并打印返回的 JSON 数据
    predictions = response.json()
    print(json.dumps(predictions, indent=4))
else:
    # 打印错误信息
    print(f"Error: {response.status_code}")
    print(response.text)
