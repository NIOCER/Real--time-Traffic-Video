import cv2

cap = cv2.VideoCapture(r'D:\AUT\COMP702 笔记\Project\frames\video.mp4')
bgsubmog = cv2.bgsegm.createBackgroundSubtractorMOG()  # 去除背景

# 视频形态学
kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
# 保存车辆中心点信息
cars = []
# 统计车的数量
car_n = 0

while True:
    ret, frame = cap.read()

    if ret:
        '''
        视频预处理阶段
        '''
        # 灰度处理
        # 图像灰度化处理可以作为图像处理的预处理步骤，为之后的图像分割、图像识别和图像分析等上层操作做准备。
        cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # 高斯去噪- 高斯滤波是一种线性平滑滤波，适用于消除高斯噪声，广泛应用于图像去噪。
        # 可以简单地理解为，高斯滤波去噪就是对整幅图像像素值进行加权平均，针对每一个像素点的值，都由其本身值和邻域内的其他像素值经过加权平均后得到。
        blur = cv2.GaussianBlur(frame, (3, 3), 5)  # GaussianBlur()函数介绍. 高斯滤波 是一种线性平滑滤波，适用于消除高斯噪声，广泛应用于图像处理的减噪过程。
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
    cv2.putText(frame, "Cars Count:" + str(car_n), (500, 60), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 4)
    cv2.imshow('video', frame)

    key = cv2.waitKey(1)
    if key == 27:  # Esc退出
        break

cap.release()
cv2.destroyAllWindows()
