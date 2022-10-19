from tkinter import *  # 调用GUI库, 适合小型GUI程序编写
from tkinter.ttk import Progressbar  # 调用读取条
from tkinter.filedialog import askopenfilename  # 调用读取文件路径
from tqdm import tqdm
from time import sleep
import matplotlib.pyplot as plt
import cv2
import os  # os便是对文件或文件夹操作的一个工具
import re  # re便是寻找匹配内容

window = Tk()
font = cv2.FONT_HERSHEY_SIMPLEX


class mainframe(Frame):

    def __init__(self, master=None):
        super().__init__(master)  # super()调用Frame方法
        self.master = master
        self.pack()
        self.createWidget()

    def createWidget(self):  # 开始创建组件

        mainmenu = Menu(window)  # 创建主菜单
        menuFile = Menu(mainmenu)
        menuEdit = Menu(mainmenu)
        menuHelp = Menu(mainmenu)

        # 将子菜单加入到主菜单栏
        mainmenu.add_cascade(label="File(F)", menu=menuFile)
        mainmenu.add_cascade(label="Edit(E)", menu=menuEdit)
        mainmenu.add_cascade(label="Help(H)", menu=menuHelp)

        # 添加菜单项
        menuFile.add_command(label="打开", accelerator="Ctrl+O", command=self.open_file)
        menuFile.add_command(label="保存", accelerator="Ctrl+S")
        menuFile.add_separator()  # 调剂分割线
        menuFile.add_command(label="退出", accelerator="Ctrl+Q", command=self.exit)

        window['menu'] = mainmenu  # 将主菜单栏加到根窗口

        bt01 = Button(self, text="Play Video", width=10, height=1, command=self.load_video, font="Times")
        bt02 = Button(self, text="Analysis Video", width=10, height=1, command=self.analysis_video, font="Times")
        btqu = Button(self, text="Exit", width=10, height=1, command=window.destroy, font="Times")

        bt01.grid(row=0, column=0, padx=15, pady=15)
        bt02.grid(row=0, column=2, padx=15, pady=15)
        btqu.grid(row=0, column=4, padx=15, pady=15)

    def exit(self):
        window.quit()

    def open_file(self):

        file = askopenfilename()
        play_file = cv2.VideoCapture(file)
        bar1 = Tk()
        bar1.geometry('400x80')
        bar1.title("读取中")
        with tqdm(total=100000, desc='Example', leave=True, ncols=100, unit='B', unit_scale=True) as tqbar:

            # 窗口进度条
            barload = Progressbar(bar1, length=350)  # 长度为350
            barload.pack(pady=10)  # 上下间距为10
            Button(bar1, text='取消', command=bar1.destroy).pack()  # 关闭按钮
            barload['value'] = 0  # 设置进度条值(设初值为零)
            barload['maximum'] = 350  # 设置进度条最大值

            for i in range(350):
                barload['value'] += 50
                barload.update()  # 更新进度条值
                sleep(0)

            for i in range(10):
                tqbar.update(10000)  # 更新进度条

            bar1.destroy()

            while play_file.isOpened():  # ret = return; return true or false
                ret, frame = play_file.read()
                cv2.namedWindow("Traffic video", 0)  # 0表示可以调整大小， 同时绘制窗口
                cv2.resizeWindow("Traffic video", 800, 600)  # 设置长和宽
                cv2.imshow('Traffic video', frame)  # frame框架下展示视频

                if cv2.waitKey(20) == 27:  # Esc键盘退出程序
                    # 如果设置waitKey(0),则表示无限期的等待键盘输入，代表按任意键继续
                    break
                    cv2.destroyAllWindows()  # 用来删除窗口的

                if cv2.getWindowProperty('Traffic video', cv2.WND_PROP_VISIBLE) < 1:  # 点击窗口关闭，退出该程序
                    break
                    cv2.destroyAllWindows()  # 用来删除窗口的

    def load_video(self):

        path = askopenfilename()  # 获取文件路径
        file = cv2.VideoCapture(path)  # 打开视频

        bar1 = Tk()
        bar1.geometry('400x80')
        bar1.title("读取中")
        with tqdm(total=100000, desc='Example', leave=True, ncols=100, unit='B', unit_scale=True) as tqbar:

            # 窗口进度条
            barload = Progressbar(bar1, length=350)  # 长度为350
            barload.pack(pady=10)  # 上下间距为10
            Button(bar1, text='取消', command=bar1.destroy).pack()  # 关闭按钮
            barload['value'] = 0  # 设置进度条值(设初值为零)
            barload['maximum'] = 350  # 设置进度条最大值

            for i in range(350):
                barload['value'] += 50
                barload.update()  # 更新进度条值

            for i in range(10):
                tqbar.update(10000)  # 更新进度条

            bar1.destroy()

            while file.isOpened():  # ret = return; return true or false
                ret, frame = file.read()
                cv2.namedWindow("Traffic video", 0)  # 0表示可以调整大小， 同时绘制窗口
                cv2.resizeWindow("Traffic video", 800, 600)  # 设置长和宽
                cv2.imshow('Traffic video', frame)  # frame框架下展示视频

                if cv2.waitKey(20) == 27:  # Esc键盘退出程序
                    # 如果设置waitKey(0),则表示无限期的等待键盘输入，代表按任意键继续
                    break
                    cv2.destroyAllWindows()  # 用来删除窗口的

                if cv2.getWindowProperty('Traffic video', cv2.WND_PROP_VISIBLE) < 1:  # 点击窗口关闭，退出该程序
                    break
                    cv2.destroyAllWindows()  # 用来删除窗口的

    def analysis_video(self):

        path = askopenfilename()  # 获取文件路径
        file = cv2.VideoCapture(path)  # 打开文件

        bar1 = Tk()
        bar1.geometry('400x80')
        bar1.title("读取中")

        bgsubmog = cv2.bgsegm.createBackgroundSubtractorMOG()  # 去除背景
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))  # 视频形态学

        cars = []  # 保存车辆中心点信息
        car_n = 0  # 统计车的数量

        with tqdm(total=100000, desc='Example', leave=True, ncols=100, unit='B', unit_scale=True) as tqbar:

            # 窗口进度条
            barload = Progressbar(bar1, length=350)  # 长度为350
            barload.pack(pady=10)  # 上下间距为10
            Button(bar1, text='取消', command=bar1.destroy).pack()  # 关闭按钮
            barload['value'] = 0  # 设置进度条值(设初值为零)
            barload['maximum'] = 350  # 设置进度条最大值

            for i in range(350):
                barload['value'] += 50
                barload.update()  # 更新进度条值
                sleep(0)

            for i in range(10):
                tqbar.update(10000)  # 更新进度条

            bar1.destroy()

        while file.isOpened():

            ret, frame = file.read()
            if ret:
                '''
                视频预处理阶段
                '''
                # 灰度处理
                # 图像灰度化处理可以作为图像处理的预处理步骤，为之后的图像分割、图像识别和图像分析等上层操作做准备。
                cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

                # 高斯去噪- 高斯滤波是一种线性平滑滤波，适用于消除高斯噪声，广泛应用于图像去噪。
                # 可以简单地理解为，高斯滤波去噪就是对整幅图像像素值进行加权平均，针对每一个像素点的值，都由其本身值和邻域内的其他像素值经过加权平均后得到。
                blur = cv2.GaussianBlur(frame, (3, 3), 5)  # GaussianBlur()高斯滤波 是一种线性平滑滤波，适用于消除高斯噪声，广泛应用于图像处理的减噪过程。
                mask = bgsubmog.apply(blur)  # 背景去除
                cv2.imshow('video', mask)

                # 腐蚀-可以是色彩追踪更加精准, 少了很多的颜色干扰
                erode = cv2.erode(mask, kernel)  # erode()图像腐蚀,加上高斯模糊,就可以使得图像的色彩更加突出

                # 膨胀属于形态学操作，所谓的形态学，就是改变物体的形状，形象理解一些：腐蚀=变瘦 膨胀=变胖
                dilate = cv2.dilate(erode, kernel, 3)

                # 闭操作
                close = cv2.morphologyEx(dilate, cv2.MORPH_CLOSE, kernel)  # cv2.morphologyEx() 进行各类形态学的变化
                close = cv2.morphologyEx(close, cv2.MORPH_CLOSE, kernel)

                # 使用cv2.findContours ()函数来查找检测物体的轮廓。
                contours, h = cv2.findContours(close, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE, )

                # 画一条线
                # cv2.line(image, start_point, end_point, color, thickness)
                # cv2.line(frame, (20, 500), (1300, 550), (0, 255, 255), 3)

                for (i, c) in enumerate(contours):  # enumerate()遍历的数据对象
                    (x, y, w, h) = cv2.boundingRect(c)  # cv2.boundingRect()这个函数可以获得一个图像的最小矩形边框一些信息

                    # 过滤小的检测框
                    isshow = (w >= 90) and (h >= 90)
                    if not isshow:
                        continue

                    # 保存中心点信息
                    # cv2.rectangle 包含的参数有： (img, pt1, pt2, color, thickness=None, lineType=None, shift=None)
                    # cv2.rectangle(读取图片变量， （左上角点坐标）（右下角点坐标），（颜色），（线宽）)
                    cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)
                    centre_p = (x + int(w / 2), y + int(h / 2))
                    cars.append(centre_p)

                    # cv2.circle(frame, centre_p, 5, (0, 0, 255), -1)
                    for (x, y) in cars:
                        if 593 < y < 607:
                            car_n += 1
                            cars.remove((x, y))

            # cv2.putText(img，text，org, fontFace, fontScale, color, thinckness, lineType, bottomLeftOrigin)
            # cv2.putText(图片,显示的文字,检测框左上角坐标,字体,字体大小,颜色,字体粗细）
            cv2.putText(frame, "Cars Count:" + str(car_n), (500, 60), cv2.FONT_HERSHEY_SIMPLEX, 1,
                        (0, 0, 255), 4)

            cv2.imshow('video', frame)

            key = cv2.waitKey(1)
            if key == 27:  # Esc键盘退出程序
                # 如果设置waitKey(0),则表示无限期的等待键盘输入，代表按任意键继续
                break
            if cv2.getWindowProperty('video', cv2.WND_PROP_VISIBLE) < 1:  # 点击窗口关闭，退出该程序
                break


if __name__ == '__main__':
    window.geometry('600x400')
    window.title("视频读取的程序")
    main = mainframe(master=window)
    window.mainloop()
