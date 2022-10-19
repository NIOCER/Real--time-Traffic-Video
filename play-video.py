import cv2

file = cv2.VideoCapture(r'D:\AUT\COMP702 RND\Resources\路口文件\汇泉路车站大街路口南向抓拍机_云存储15821040_1460613894_1.mp4')  # r responsible for character transfer

while file.isOpened():  # ret = return; return true or false

    ret, frame = file.read()
    cv2.namedWindow("Traffic video", 0)  # 0 means you can resize while drawing windows
    cv2.resizeWindow("Traffic video", 800, 600)  # Set length and width
    cv2.imshow('Traffic video', frame)  # Video by Frame

    if cv2.waitKey(20) == 27:  # Esc Keyboard Exit Program
        # If you set WaitKey (0), you are waiting indefinitely for the keyboard to enter, which means you can press any key to continue
        break
        cv2.destroyAllWindows() # Used to delete windows

    if cv2.getWindowProperty('Traffic video', cv2.WND_PROP_VISIBLE) < 1:  # Click close the window to exit the program
        break
        cv2.destroyAllWindows()  # Used to delete windows