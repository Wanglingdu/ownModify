# DeepRop项目组
## 试用系统自动启动服务
> 需求说明:用户为医生群体，电脑小白，要求程序能一键点击启动，程序崩溃后能自动重启

- 开始时间: 2017/9/21 22:04
- Deadline: 2017/9/23

### 环境说明
1. Ubuntu16.04 + docker + Nvidia 1050

### 实现构想
1. 使用shell脚本实现

### 实现步骤
#### 实现双击sh脚本能够执行
1. Ubuntu16.04下的文件管理器使用的是nautilus,它对可执行文件的默认打开方式是display,也就是用文本编辑器打开，可以打开nautilus然后点编辑来更改首选项，但是我这里没找到编辑这个设置选项．一个通用的方法是使用dconf系统配置软件，在终端输入dconf-editor，然后回车。如果没有安装dconf-editor系统会提示你进行安装，然后可以再次输入dconf-editor，然后会出现一个窗口用来修改一些系统配置．左侧栏中找到org->gnome->nautilus->preferences，然后右边会有executable-text-activation选项，默认是display，改为ask之后关闭窗口即可。再次双击bash文件之后系统就会弹出对话框供你选择，是diskplay还是run in terminal.选择你想要的就行了．测试文件如下:
```bash
#!/bin/bash
echo "hello,world"
read -n 1 -p "press enter to quit"
# 最后一句是等待输入，不加这个你可能点击之后看不到什么反应，因为窗口执行完后自动关闭了．
```

2. 使用bash实现启动python脚本
> 首先看一下bash的基础教程[shell 教程－菜鸟教程](http://www.runoob.com/linux/linux-shell-variable.html)

- 
