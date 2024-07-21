import cv2
from utils import Dataloader

# 初始化数据集
dataset = Dataloader(root="irships")

# 使用len关键字获取数据集的长度
print("\n数据集长度: %i" % len(dataset))

print("\n打乱数据集")
dataset.shuffle()

print("\n让我们遍历数据集:")

# 最后，你可以像这样遍历数据集...
for i, (inp, lab) in enumerate(dataset):

    print("图像 %i:\n--------------" % i)
    print(inp, "\n")  # 'inp' 包含元数据和输入图像

    print("标签 %i:\n--------------" % i)
    print(lab, "\n")  # 'lab' 包含元数据和对象范围 (x1, y1, x2, y2)

    cv2.imshow("IRShips 图像", inp.image)  # 显示当前图像
    print("按 'q' 退出或按其他键继续...\n")
    if (cv2.waitKey(0) & 0xFF) == ord("q"):
        cv2.destroyAllWindows()
        break
