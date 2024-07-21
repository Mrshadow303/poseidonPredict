from io import BytesIO
import numpy as np
import os
from PIL import Image, ImageOps
import requests

# 本地导入
from utils import Namespace

# 用于从URL下载图像并进行处理
def download_from_urls(dictionary, root="."):
    # 遍历字典中的每一项
    for k, v in dictionary.items():
        # 构建目录路径
        directory = "/".join((root, k))
        # 如果值是列表，则下载图像
        if isinstance(v, list):
            os.makedirs(directory, exist_ok=True)
            print("Downloading images to %s" % directory)
            for i, item in ProgressBar(enumerate(v), prefix="Progress: "):
                # 下载图像
                try:
                    image = Image.open(BytesIO(requests.get(item["image_url"]).content))
                except:
                    msg = "\r  Unable to download image %i : %s"
                    print((msg % (i, item["image_url"])).ljust(70))
                    continue
                # 如果存在变换，则变换图像
                if "transforms" in item.keys():
                    image = transform_image(image, item["transforms"])
                # 保存图像
                try:
                    image.save("%s/%s.png" % (directory, str(i).zfill(4)))
                except SystemError:
                    msg = "\r  Unable to save image %i : %s (there may be a problem with the image transforms)."
                    print((msg % (i, item["image_url"])).ljust(70))
        else:
            # 如果值不是列表，则递归调用
            download_from_urls(v, root=directory)


def transform_image(image, transforms):
    # 遍历所有变换
    for transform in transforms:
        if transform["name"].lower() == "crop":
            image = image.crop(**transform["kwargs"])
        elif transform["name"].lower() == "grayscale":
            image = ImageOps.grayscale(image)
        elif transform["name"].lower() == "mask":
            mask = np.array(Image.open(**transform["kwargs"]))
            image = np.array(image)
            mask[mask > 0] = 1
            if image.ndim == 3:
                mask = mask[..., None]
            image = Image.fromarray(image * mask)
    return image


class ProgressBar(object):

    def __init__(self, iterable, prefix="", length=50, fill="█"):
        self._iterable = list(iterable)
        self.prefix = prefix
        self.length = length
        self.fill = fill

    def __getitem__(self, i):
        if len(self._iterable) > 0:
            p = i / len(self._iterable)  # 进度的小数表示
            f = int(self.length * p)  # 进度条的分数
            bar = self.fill * f + '-' * (self.length - f)  # 进度条字符串
            line = "%s|%s| %.1f%%" % (self.prefix, bar, p * 100)  # 打印的行
            print("\r%s" % line, end="\n" if i == len(self._iterable) else "\r")
        return self._iterable[i]


if __name__ == "__main__":
    import argparse
    import zipfile


    def unzip(path):
        print("Unzipping %s..." % path)
        with zipfile.ZipFile(path, "r") as f:
            f.extractall()
        print("Done")


    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--filepath", default="./12800324/urls.yaml", type=str, help="Path to YAML file of URLs")
    parser.add_argument("-o", "--output", default="irships/augment", type=str, help="Output directory")
    parser.add_argument("-m", "--masks", default="masks", type=str, help="Directory of masks")
    args = parser.parse_args()

    # if not os.path.isdir("irships/images") or not os.path.isdir("irships/labels"):
    #     unzip("irships.zip")  # 如果未解压，则解压IRShips
    # unzip(args.masks + ".zip")  # 如果未解压，则解压masks

    download_from_urls(Namespace(args.filepath), root=args.output)
