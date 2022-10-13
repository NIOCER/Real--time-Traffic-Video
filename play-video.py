import cv2

file = cv2.VideoCapture(r'D:\AUT\COMP702 RND\Resources\路口文件\汇泉路车站大街路口南向抓拍机_云存储15821040_1460613894_1.mp4')  # r负责转字符

while file.isOpened():  # ret = return; return true or false

    ret, frame = file.read()
    cv2.namedWindow("Traffic video", 0)  # 0表示可以调整大小， 同时绘制窗口
    cv2.resizeWindow("Traffic video", 800, 600)  # 设置长和宽
    cv2.imshow('Traffic video', frame)  # frame框架下展示视频

    if cv2.waitKey(20) == 27:  # Esc键盘退出程序
        # 如果设置waitKey(0),则表示无限期的等待键盘输入，代表按任意键继续
        break
        cv2.destroyAllWindows() # 用来删除窗口的

    if cv2.getWindowProperty('Traffic video', cv2.WND_PROP_VISIBLE) < 1:  # 点击窗口关闭，退出该程序
        break
        cv2.destroyAllWindows()  # 用来删除窗口的