```
poserdonPredict-main   项目后端
├──model               里面是船类识别的模型和脚本
│    ├──images         临时文件夹，存放用于测试的图片
│    ├──best.pt        训练好的yolov8模型权重
│    ├──shipClassificationPredict.py      flask服务器脚本，需要启动
└──src   真正的后端程序


poserdonPredict-vue 项目前端
└──src   
    ├──components       项目页面组件
    ├──router           路径配置文件
    └──store            动态路由
```

在启动项目时，需要依次启动flask服务文件（python，可以使用pycharm或vs code等启动）、后端程序（springboot程序，可用Idea启动）、前端程序（vue程序，可使用vs code启动）


