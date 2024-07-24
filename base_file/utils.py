import contextlib
import cv2
import numpy as np
import os
import pandas as pd
import random
import torch
import yaml


__version__ = "1.0"  # 设置模块的版本号为1.0


# 用于存储和操作命名空间数据的类
class Namespace(object):
    # 初始化函数
    def __init__(self, *args, **kwargs):
        self.add(*args, **kwargs)  # 初始化时调用add方法，添加传入的参数

    # 使对象可迭代，返回对象属性的迭代器
    def __iter__(self):
        return self.__dict__.__iter__()

    # 返回对象的字符串表示形式
    def __str__(self, quote=""):
        return "\n".join(self.__print(self.__dict__, quote=quote))

    # 通过键获取值
    def __getitem__(self, item):
        return self.__dict__[item]

    # 通过键设置值
    def __setitem__(self, key, value):
        self.__dict__[key] = value

    # 返回对象属性的键值对
    def items(self):
        return self.__dict__.items()

    # 添加项目到命名空间
    def add(self, *args, **kwargs):
        """
        :param args: str表示要加载的yaml文件路径或要添加的项目字典
        :param kwargs: 要添加的项目
        :return: None
        """
        for arg in args:
            if isinstance(arg, str):
                with open(arg, "r") as f:
                    arg = yaml.safe_load(f)
            if isinstance(arg, dict):
                self.__dict__ = {**self.__dict__, **arg}
            else:
                raise TypeError("Expected %s got %s" % (dict, type(arg)))
        self.__dict__ = {**self.__dict__, **self.__convert(kwargs)}

    # 将对象保存到文件中
    def save(self, filename, quote=""):
        with open(filename, "w") as f:
            f.write(self.__str__(quote=quote))

    # 将字典中的字典转换为Namespace对象
    @staticmethod
    def __convert(dictionary):
        for k, v in dictionary.items():
            if isinstance(v, dict):
                dictionary[k] = Namespace(v)
        return dictionary

    # 生成对象的字符串表示形式
    def __print(self, dictionary, tab="  ", level=0, list_lim=10, quote=""):
        """
        :param dictionary: [dict] 要打印的对象
        :param tab: [str] 用于缩进的字符串
        :param level: [int] 缩进的级别
        :param list_lim: [int] 列表中项目的数量，超过此数量则使用多行
        :param quote: [str] 用于引用的字符
        :return: 包含对象内容的字符串列表
        """
        lines = []
        for key, item in dictionary.items():
            item = self.__format_item(item, quote)
            # 如果项目是字典，写入键，然后递归调用
            if isinstance(item, Namespace):
                lines.append("%s%s:" % ((level * tab), key))
                lines += self.__print(item, level=level + 1, quote=quote)
            # 如果项目是numpy数组，写入键和数组形状
            elif isinstance(item, np.ndarray):
                lines.append(
                    "%s%s: %s numpy.ndarray of type %s"
                    % ((level * tab), key, item.shape, item.dtype)
                )
            # 如果项目是列表，如果列表包含列表/元组/Namespace或长度超过list_lim，则分行写入
            elif isinstance(item, list):
                if (
                    any(
                        [
                            any([isinstance(i, t) for t in (list, tuple, Namespace)])
                            for i in item
                        ]
                    )
                    or len(item) > list_lim
                ):
                    lines.append("%s%s:" % ((level * tab), key))
                    for i in item:
                        if isinstance(i, Namespace):
                            lines += [
                                (
                                    "%s  %s" % ((level + 1) * tab, line)
                                    if j
                                    else "%s- %s" % ((level + 1) * tab, line)
                                )
                                for j, line in enumerate(self.__print(i, quote=quote))
                            ]
                        else:
                            lines.append("%s- %s" % ((level + 1) * tab, i))
                else:
                    lines.append("%s%s: %s" % ((level * tab), key, item))
            else:
                lines.append("%s%s: %s" % ((level * tab), key, item))
        return lines

    # 格式化项目
    def __format_item(self, item, quote):
        if isinstance(item, list) or isinstance(item, tuple):
            return [self.__format_item(i, quote) for i in item]
        else:
            return "%s%s%s" % (quote, item, quote) if isinstance(item, str) else item


# 定义 ship_type 和 ship_class 的映射,暂未取用
ship_type_mapping = {"Corvette": 0, "Frigate": 1, "Destroyer": 2, "Ferry": 3}
ship_class_mapping = {
    "Ada": 0,
    "Independence": 1,
    "Visby": 2,
    "Alvaro De Bazan": 3,
    "Jiangkai II": 4,
    "Oliver Hazard Perry": 5,
    "Akizuki": 6,
    "Sejong Daewang": 7,
    "Zumwalt": 8,
    "Armourique": 9,
}


class DataSet(object):

    # 初始化函数
    def __init__(
        self,
        root,
        metadata="metadata.csv",
        sea_intensity_range=(5, 30),
        sky_intensity_range=(2, 30),
        clutter_intensity_range=None,
        clutter_height_range=(0.2, 0.7),
        clutter_probability=0.5,
        augment_sea="augment/sea",
        augment_sky="augment/sky",
        augment_clutter="augment/clutter",
        cache_sea_images=True,
        cache_sky_images=True,
        cache_clutter_images=True,
        blur=3,
    ):
        print("IRShips Dataloader, version %s" % __version__)
        print("Initialising dataset...")

        # 主要数据变量
        self._metadata = None  # 私有占位符，用于数据框
        self._metadata_file = None  # 私有占位符，用于存储元数据路径
        self.indices = None  # 用于索引数据框的占位符
        self.root = root
        self.key = Namespace("/".join((root, "key.yaml")))
        self.load_metadata(metadata=metadata)


        # 设置数据增强选项
        self.sea_intensity_range = sea_intensity_range
        self.cloud_intensity_range = sky_intensity_range
        self.clutter_probability = clutter_probability
        self.clutter_height_range = clutter_height_range
        if clutter_intensity_range is None:
            self.clutter_intensity_range = {
                "ice": (0, 5),
                "structure": (20, 70),
                "landscape": (15, 60),
            }
        else:
            self.clutter_intensity_range = clutter_intensity_range

        # 初始化变量以存储真实世界图像
        self.sea_images = None
        self.sky_images = None
        self.clutter_images = None

        # 缓存选项
        self._cache_sea_images = cache_sea_images
        self._cache_sky_images = cache_sky_images
        self._cache_clutter_images = cache_clutter_images

        # 设置数据增强图像
        self.blur = blur
        self.augment_sea = augment_sea
        self.augment_sky = augment_sky
        self.augment_clutter = augment_clutter
        print("Done")

    # 获取数据集中的训练标签
    def __getitem__(self, index: int):
        """
        :param index: int 要检索实例的索引
        :return: 包含图像数据和标签数据的Namespace元组
        """
        index = self.indices[index]

        # 读取图像和标签
        image_path = os.path.join(self.root, "images", self.metadata.iloc[index].filename)
        label_path = os.path.join(self.root, "labels", self.metadata.iloc[index].labelname)

        image = cv2.imread(image_path, cv2.IMREAD_UNCHANGED)
        label = cv2.imread(label_path, cv2.IMREAD_UNCHANGED)

        # 查找水平图像的海平面
        sea_level = get_sea_level(image) if self.metadata.iloc[index]['pitch'] == 0 else 0

        # 构建图像和标签的 Namespace
        image_namespace = Namespace(
            dataset="IRShips",
            type_id=self.key["Type"].index(self.metadata.iloc[index].ship_type),
            class_id=self.key["Class"].index(self.metadata.iloc[index].ship_class),
            image=image,
            sea_level=sea_level,
            pitch=self.metadata.iloc[index]['pitch'],
            is_input=True,
        )

        label_namespace = Namespace(
            dataset="IRShips",
            type_id=self.key["Type"].index(self.metadata.iloc[index].ship_type),
            class_id=self.key["Class"].index(self.metadata.iloc[index].ship_class),
            image=label,
            is_input=False,
        )


        # 添加海洋、云和杂乱
        if self.augment_sea:
            image_namespace = self.__add_sea(image_namespace, label_namespace)
        if image_namespace.pitch == 0:
            if self.augment_sky:
                image_namespace = self.__add_sky(image_namespace, label_namespace)
            if self.augment_clutter:
                image_namespace = self.__add_clutter(image_namespace, label_namespace)

        # 应用高斯模糊
        if isinstance(self.blur, int) and self.blur > 0:
            image_namespace.image = cv2.GaussianBlur(image_namespace.image, (self.blur, self.blur), 0)

        # 将图像数据类型转换为浮点型，并归一化
        image_namespace.image = image_namespace.image.astype(np.float32) / 255.0

        x1, y1, x2, y2 = self.metadata.iloc[index][["x1", "y1", "x2", "y2"]].values
        ship_class = ship_class_mapping[self.metadata.iloc[index]["ship_class"]]
        ship_type = ship_type_mapping[self.metadata.iloc[index]["ship_type"]]
        #print(f"ship_class: {ship_class}, ship_type: {ship_type}")
        try:
            # 返回数据、是否加载和是否转换
            return {
                "image": image_namespace.image,
                "label": label_namespace.image,
                "shipBox": torch.tensor([x1, y1, x2, y2], dtype=torch.float32),
                # "shipClass": torch.tensor(ship_class, dtype=torch.long),
                # "shipType": torch.tensor(ship_type, dtype=torch.long),
                "shipClass": ship_class,
                "shipType": ship_type,
                "image_name": self.metadata.iloc[index].filename,
            }
        except ValueError as e:
            print(f"创建tensor时出错: {e}")

    # 获取数据集的长度
    def __len__(self):
        return len(self.indices)

    # 加载元数据
    def load_metadata(self, metadata=None):
        print("Loading metadata")
        if metadata is not None:
            self._metadata_file = metadata
        self.metadata = pd.read_csv("/".join((self.root, self._metadata_file)))
        # ----------------------------------------------
        # 测试，仅取部分数据
        # use_data_count = 1000  # 取数据的个数
        # if use_data_count is not None:
        #     # self.metadata = self.metadata.sample(frac=1).reset_index(
        #     #     drop=True
        #     # )  # 打乱数据
        #     self.metadata = self.metadata.head(use_data_count)  # 取参数个数据

    # 打乱数据集索引
    def shuffle(self):
        random.shuffle(self.indices)

    # 对数据集索引进行排序
    def sort(self):
        self.indices.sort()

    # 获取元数据
    @property
    def metadata(self):
        return self._metadata

    # 设置元数据
    @metadata.setter
    def metadata(self, new_value):
        """
        :param new_value: pd.dataframe of IRShips metadata
        :return: None
        """
        self._metadata = new_value
        self.indices = list(range(len(self._metadata)))
        print("Indexed %i instances" % len(self.indices))

    # 获取海洋增强图像路径
    @property
    def augment_sea(self):
        return self._augment_sea

    # 设置海洋增强图像路径
    @augment_sea.setter
    def augment_sea(self, new_value):
        """
        :param new_value: string : 海洋增强图像的路径
        :return: None
        """
        self.sea_images = (
            None if new_value is None else self.__load_sea_images(new_value)
        )
        self._augment_sea = new_value

    # 获取天空增强图像路径
    @property
    def augment_sky(self):
        return self._augment_sky

    # 设置天空增强图像路径
    @augment_sky.setter
    def augment_sky(self, new_value):
        self.sky_images = (
            None if new_value is None else self.__load_sky_images(new_value)
        )
        self._augment_sky = new_value

    # 获取杂乱增强图像路径
    @property
    def augment_clutter(self):
        return self._augment_clutter

    # 设置杂乱增强图像路径
    @augment_clutter.setter
    def augment_clutter(self, new_value):
        self.clutter_images = (
            None if new_value is None else self.__load_clutter_images(new_value)
        )
        self._augment_clutter = new_value

    # 获取海洋图像缓存选项
    @property
    def cache_sea_images(self):
        return self._cache_sea_images

    # 设置海洋图像缓存选项
    @cache_sea_images.setter
    def cache_sea_images(self, new_value):
        self._cache_sea_images = new_value  # 设置变量
        if self.sea_images is not None:  # 如果海洋增强图像已经加载
            (
                print("Caching sea images...")
                if self.cache_sea_images
                else print("Indexing sea images...")
            )
            self.augment_sea = self._augment_sea  # 重新加载它们
            print("Done")

    # 获取天空图像缓存选项
    @property
    def cache_sky_images(self):
        return self._cache_sky_images

    # 设置天空图像缓存选项
    @cache_sky_images.setter
    def cache_sky_images(self, new_value):
        self._cache_sky_images = new_value  # 设置变量
        if self.sky_images is not None:  # 如果天空增强图像已经加载
            (
                print("Caching sky images...")
                if self.cache_sea_images
                else print("Indexing sky images...")
            )
            self.augment_sky = self._augment_sky  # 重新加载它们
            print("Done")

    # 获取杂乱图像缓存选项
    @property
    def cache_clutter_images(self):
        return self._cache_clutter_images

    # 设置杂乱图像缓存选项
    @cache_clutter_images.setter
    def cache_clutter_images(self, new_value):
        self._cache_clutter_images = new_value  # 设置变量
        if self.clutter_images is not None:  # 如果杂乱增强图像已经加载
            (
                print("Caching sea images...")
                if self.cache_clutter_images
                else print("Indexing sea images...")
            )
            self.augment_clutter = self._augment_clutter  # 重新加载它们
            print("Done")

    # 加载图像的静态方法
    @staticmethod
    def __load_images(directory, cache_images, load_flag=-1):
        images = []
        for image_name in os.listdir(directory):
            image_path = "%s/%s" % (directory, image_name)
            if cache_images:
                image = cv2.imread(image_path, load_flag)
                if image is not None:
                    images.append(image)
                else:
                    raise FileNotFoundError("Unable to load image: %s" % image_path)
            else:
                if os.path.isfile(image_path):
                    images.append(image_path)
                else:
                    raise FileNotFoundError("Unable to find image: %s" % image_path)
        return images

    # 加载海洋增强图像
    def __load_sea_images(self, directory):
        h = self.__load_images(
            "%s/%s/horizontal" % (self.root, directory),
            self.cache_sea_images,
            cv2.IMREAD_GRAYSCALE,
        )
        print(
            "\tLoaded %i images for sea-state augmentation (horizontal perspective)"
            % len(h)
        )
        e = self.__load_images(
            "%s/%s/elevated" % (self.root, directory),
            self.cache_sea_images,
            cv2.IMREAD_GRAYSCALE,
        )
        print(
            "\tLoaded %i images for sea-state augmentation (elevated perspective)"
            % len(e)
        )
        return {"horizontal": h, "elevated": e}

    # 加载天空增强图像
    def __load_sky_images(self, directory):
        sky_images = self.__load_images(
            "%s/%s" % (self.root, directory),
            self.cache_sky_images,
            cv2.IMREAD_GRAYSCALE,
        )
        print("\tLoaded %i images for sky-state augmentation" % len(sky_images))
        return sky_images

    # 加载杂乱增强图像
    def __load_clutter_images(self, directory):
        ice = self.__load_images(
            "%s/%s/ice" % (self.root, directory),
            self.cache_clutter_images,
            cv2.IMREAD_GRAYSCALE,
        )
        ice = [(i, "ice") for i in ice]
        print("\tLoaded %i images for clutter augmentation (ice)" % len(ice))
        struct = self.__load_images(
            "%s/%s/structure" % (self.root, directory),
            self.cache_clutter_images,
            cv2.IMREAD_GRAYSCALE,
        )
        struct = [(i, "structure") for i in struct]
        print("\tLoaded %i images for clutter augmentation (structure)" % len(struct))
        land = self.__load_images(
            "%s/%s/landscape" % (self.root, directory),
            self.cache_clutter_images,
            cv2.IMREAD_GRAYSCALE,
        )
        land = [(i, "landscape") for i in land]
        print("\tLoaded %i images for clutter augmentation (landscapes)" % len(land))
        return ice + land + struct

    # 添加海洋图像
    def __add_sea(self, image, label):
        with contextlib.suppress(TypeError):
            intensity_range = np.random.randint(*self.sea_intensity_range)

        sea_image = random.choice(
            self.sea_images["horizontal" if image.pitch == 0 else "elevated"]
        )
        if not self.cache_sea_images:
            sea_image = cv2.imread(sea_image, cv2.IMREAD_GRAYSCALE)

        mask = label.image[image.sea_level :, ...].copy()
        image_lower = image.image[image.sea_level :, ...]

        sea_image = process_sea(
            sea_image,
            shape=image_lower.shape[0:2],
            average_intensity=int(np.mean(image_lower)),
            intensity_range=intensity_range,
        )

        image.image[image.sea_level :, ...] = superimpose(image_lower, sea_image, mask)
        return image

    # 添加天空图像
    def __add_sky(self, image, label):
        if image.sea_level:
            with contextlib.suppress(TypeError):
                intensity_range = np.random.randint(*self.cloud_intensity_range)

            mask = label.image[0 : image.sea_level, ...].copy()
            image_top = image.image[0 : image.sea_level, ...]
            background_temp = int(np.mean(image_top))

            sky_image = random.choice(self.sky_images)
            if not self.cache_sky_images:
                sky_image = cv2.imread(sky_image, cv2.IMREAD_GRAYSCALE)

            clouds = process_sky(
                sky=sky_image,
                shape=image_top.shape[0:2],
                lower=background_temp,
                upper=background_temp + intensity_range,
            )

            image.image[0 : image.sea_level, ...] = superimpose(image_top, clouds, mask)
        return image

    # 添加杂乱图像
    def __add_clutter(self, image, label):
        if np.random.random() < self.clutter_probability and image.sea_level:

            intensity = self.clutter_intensity_range
            for key, item in self.clutter_intensity_range.items():
                with contextlib.suppress(TypeError):
                    intensity[key] = np.random.randint(*item)

            with contextlib.suppress(TypeError):
                clutter_height = get_random_value(*self.clutter_height_range)
            clutter_height = max(10, int(clutter_height * image.sea_level))

            orig_image = image.image.copy()

            clutter_image, clutter_type = random.choice(self.clutter_images)
            if not self.cache_clutter_images:
                clutter_image = cv2.imread(clutter_image, cv2.IMREAD_GRAYSCALE)

            intensity = self.clutter_intensity_range[clutter_type]
            with contextlib.suppress(TypeError):
                intensity = np.random.randint(*intensity)

            clutter = process_clutter(
                clutter_image, image.image.shape, intensity, clutter_height
            )
            y0 = image.sea_level - clutter.shape[0]
            ship_mask = label.image[y0 : image.sea_level :, ...].copy()
            clutter_mask = clutter.copy()
            clutter_mask[clutter > 0] = 1
            clutter_mask = 1 - clutter_mask
            image.image[y0 : image.sea_level, ...] = superimpose(
                image.image[y0 : image.sea_level, ...], clutter, clutter_mask
            )
            image.image[y0 : image.sea_level, ...] = superimpose(
                orig_image[y0 : image.sea_level, ...], clutter, ship_mask
            )
        return image


# 获取海洋水平线
def get_sea_level(image, label=None, threshold=5):
    image = image[:, 0]
    image -= image[0]
    image[image > 0] = 1
    i = np.flip(np.arange(image.shape[0]))
    sea_level = np.argmax(image * i) + 1
    if sea_level < threshold and label is not None:
        sea_level = find_extents(label, normalize=False)[3]
    return int(sea_level) if int(sea_level) > 1 else 0


# 获取随机值
def get_random_value(lower, upper):
    return lower + np.random.random() * (upper - lower)


# 选择图像
def choose_image(directory):
    try:
        filenames = os.listdir(directory)
    except FileNotFoundError:
        print("choose_image : No such directory : %s" % directory)
    filename = random.choice(filenames)
    return cv2.imread("/".join((directory, filename)), cv2.IMREAD_GRAYSCALE), filename


# 叠加图像
def superimpose(image_1, image_2, mask):
    assert image_1.shape == image_2.shape
    mask[mask > 0] = 1
    image_2[mask > 0] = 0
    image_2 += image_1 * mask
    return image_2


# 查找范围
def find_extents(image, normalize=False):
    image[image < 50] = 0
    image[image > 0] = 255
    x = np.argwhere(image.any(axis=0))[:, 0]
    y = np.argwhere(image.any(axis=1))[:, 0]
    if normalize:
        x = x / image.shape[1]
        y = y / image.shape[0]
    return np.array((x[0], y[0], x[-1], y[-1]))


# 归一化图像
def normalize(image, lower=0, upper=255):
    image = image.astype(np.float32)
    image -= np.min(image)
    image *= (upper - lower) / max(np.max(image), 1)
    image += lower
    return image


# 获取缩放比例
def get_scale(orig_shape, min_shape):
    orig_shape = np.array(orig_shape)
    min_shape = np.array(min_shape)
    scale = max(min_shape / orig_shape)
    if scale < 1:
        scale = scale + np.random.random() * (1 - scale)
    return scale


# 处理海洋图像
def process_sea(sea, shape, average_intensity=20, intensity_range=30):
    scale = get_scale(orig_shape=sea.shape[0:2], min_shape=shape)
    sea = cv2.resize(sea, (0, 0), fx=scale, fy=scale)
    if np.random.random() > 0.5:
        sea = cv2.flip(sea, 1)
    sea = random_crop(sea, shape=shape)

    sea = sea.astype(np.float32)
    lower = int(average_intensity - intensity_range / 2)
    upper = int(average_intensity + intensity_range / 2)
    sea = normalize(sea, lower=lower, upper=upper)
    sea[sea < 0] = 0
    sea[sea > 255] = 255
    return sea.astype(np.uint8)


# 处理天空图像
def process_sky(sky, shape, lower=0, upper=255):
    scale = get_scale(orig_shape=sky.shape[0:2], min_shape=shape)
    sky = cv2.resize(sky, (0, 0), fx=scale, fy=scale)
    if np.random.random() > 0.5:
        sky = cv2.flip(sky, 1)
    sky = random_crop(sky, shape=shape)

    sky = sky.astype(np.float32)
    sky[sky < 10] = 0
    sky[sky < 10] = 0
    sky = normalize(sky, lower, upper)
    sky[sky < 0] = 0
    sky[sky > 255] = 255
    return sky.astype(np.uint8)


# 处理杂乱图像
def process_clutter(clutter, shape, intensity, clutter_height):
    im_h, im_w = shape[0:2]
    scale = clutter_height / clutter.shape[0]
    wrap = np.any(clutter[:, 0]) or np.any(clutter[:, -1])
    if np.random.random() > 0.5:
        clutter = cv2.flip(clutter, 1)
    clutter = cv2.resize(clutter, (0, 0), fx=scale, fy=scale)
    if clutter.shape[1] < im_w:
        clutter = stretch_image(clutter, im_w, wrap=wrap)
    else:
        clutter = random_crop(clutter, shape=(clutter.shape[0], im_w))
    clutter = normalize(clutter, 0, intensity)
    return clutter


# 随机裁剪图像
def random_crop(
    image, scale=None, shape=None, resize=False, interpolation=cv2.INTER_LINEAR
):
    if scale is not None and shape is not None:
        print(
            "%s.random_crop : both a scale and a shape were given : only one can be prescribed"
        )
    elif scale is None and shape is None:
        print(
            "%s.random_crop : neither a scale nor a shape were given :  one (and only one) of these should be given"
        )
    im_h, im_w = image.shape[0:2]
    if scale is not None:
        with contextlib.suppress(TypeError):
            scale = get_random_value(*scale)
        if not 0 < scale <= 1:
            print(
                "%s.random_crop : 0 < scale <=1 must be true : got scale = %f"
                % (__name__, scale)
            )
        crop_w = int(im_w * scale)
        crop_h = int(im_h * scale)
    elif shape is not None:
        crop_h, crop_w = shape
    x0 = 0 if im_w - crop_w == 0 else np.random.randint(0, im_w - crop_w)
    y0 = 0 if im_h - crop_h == 0 else np.random.randint(0, im_h - crop_h)
    x1 = x0 + crop_w
    y1 = y0 + crop_h
    coords = (x0, y0, x1, y1)
    image = crop(image, coords, resize, interpolation)
    return image


# 裁剪图像
def crop(image, coords, resize=False, interpolation=cv2.INTER_LINEAR):
    x0, y0, x1, y1 = coords
    h, w = image.shape[0:2]
    image = image[y0:y1, x0:x1, ...]
    if resize:
        image = cv2.resize(image, (w, h), interpolation=interpolation)
    return image


# 拉伸图像
def stretch_image(image, width, wrap=False):
    h, w = image.shape[0:2]
    new_image = np.zeros((h, width), np.uint8)
    if wrap:
        for i in range(int(np.ceil(width / w))):
            x0 = i * w
            x1 = min(x0 + w, width)
            new_image[:, x0:x1] = (
                image[:, : x1 - x0] if i % 2 else image[:, ::-1][:, : x1 - x0]
            )
    else:
        x0 = np.random.randint(0, width - w)
        x1 = x0 + w
        new_image[:, x0:x1] = image
    return new_image
