from tkinter import *  # Call GUI library, suitable for small GUI program writing
from tkinter.ttk import Progressbar  # Call read bar
from tkinter.filedialog import askopenfilename  # Call Read File Path
from tqdm import tqdm
from time import sleep
import matplotlib.pyplot as plt
import cv2
import os  # OS is a tool for working with files or folders
import re  # re is about finding a match

window = Tk()
font = cv2.FONT_HERSHEY_SIMPLEX


class mainframe(Frame):

    def __init__(self, master=None):
        super().__init__(master)  # super () calls Frame method
        self.master = master
        self.pack()
        self.createWidget()

    def createWidget(self):  # Start creating components

        mainmenu = Menu(window)  # Create the main menu
        menuFile = Menu(mainmenu)
        menuEdit = Menu(mainmenu)
        menuHelp = Menu(mainmenu)

        # Add submenu to main menu bar
        mainmenu.add_cascade(label="File(F)", menu=menuFile)
        mainmenu.add_cascade(label="Edit(E)", menu=menuEdit)
        mainmenu.add_cascade(label="Help(H)", menu=menuHelp)

        # Add menu items
        menuFile.add_command(label="Open", accelerator="Ctrl+O", command=self.open_file)
        menuFile.add_command(label="Save", accelerator="Ctrl+S")
        menuFile.add_separator()  # Diversion Split Line
        menuFile.add_command(label="Exit", accelerator="Ctrl+Q", command=self.exit)

        window['menu'] = mainmenu  # Add the main menu bar to the root window

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
        bar1.title("Loading")
        with tqdm(total=100000, desc='Example', leave=True, ncols=100, unit='B', unit_scale=True) as tqbar:

            # Window entry
            barload = Progressbar(bar1, length=350)  # Length 350
            barload.pack(pady=10)  # Up and down spacing 10
            Button(bar1, text='Cancel', command=bar1.destroy).pack()  # Shutdown button
            barload['value'] = 0  # Set the progress bar value (set the initial value to zero)
            barload['maximum'] = 350  # Set the maximum progress bar

            for i in range(350):
                barload['value'] += 50
                barload.update()  # Update progress bar values
                sleep(0)

            for i in range(10):
                tqbar.update(10000)  # Update the progress bar

            bar1.destroy()

            while play_file.isOpened():  # ret = return; return true or false
                ret, frame = play_file.read()
                cv2.namedWindow("Traffic video", 0)  # 0 means you can resize while drawing windows
                cv2.resizeWindow("Traffic video", 800, 600)  # Set length and width
                cv2.imshow('Traffic video', frame)  # Video by Frame

                if cv2.waitKey(20) == 27:  # Esc Keyboard Exit
                    # If you set WaitKey (0), you are waiting indefinitely for the keyboard to enter, which means you can press any key to continue
                    break
                    cv2.destroyAllWindows()  # Used to delete windows

                if cv2.getWindowProperty('Traffic video', cv2.WND_PROP_VISIBLE) < 1:  # Click close the window to exit the program
                    break
                    cv2.destroyAllWindows()  # Used to delete windows

    def load_video(self):

        path = askopenfilename()  # Access to File Path
        file = cv2.VideoCapture(path)  # Turn on Video

        bar1 = Tk()
        bar1.geometry('400x80')
        bar1.title("Loading")
        with tqdm(total=100000, desc='Example', leave=True, ncols=100, unit='B', unit_scale=True) as tqbar:

            # Window entry
            barload = Progressbar(bar1, length=350)  # Length 350
            barload.pack(pady=10)  # Up and down spacing 10
            Button(bar1, text='Cancel', command=bar1.destroy).pack()  # Shutdown button
            barload['value'] = 0  # Set the progress bar value (set the initial value to zero)
            barload['maximum'] = 350  # Set the maximum progress bar

            for i in range(350):
                barload['value'] += 50
                barload.update()  # Update progress bar values

            for i in range(10):
                tqbar.update(10000)  # Update progress bar values

            bar1.destroy()

            while file.isOpened():  # ret = return; return true or false
                ret, frame = file.read()
                cv2.namedWindow("Traffic video", 0)  # 0 means you can resize while drawing windows
                cv2.resizeWindow("Traffic video", 800, 600)  # Set length and width
                cv2.imshow('Traffic video', frame)  # Video by Frame

                if cv2.waitKey(20) == 27:  # Esc Keyboard Exit Program
                    # If you set WaitKey (0), you are waiting indefinitely for the keyboard to enter, which means you can press any key to continue
                    break
                    cv2.destroyAllWindows()  # Used to delete windows

                if cv2.getWindowProperty('Traffic video', cv2.WND_PROP_VISIBLE) < 1:  # Click close the window to exit the program
                    break
                    cv2.destroyAllWindows()  # Used to delete windows

    def analysis_video(self):

        path = askopenfilename()  # Access to File Path
        file = cv2.VideoCapture(path)  # Open the file

        bar1 = Tk()
        bar1.geometry('400x80')
        bar1.title("Loading")

        bgsubmog = cv2.bgsegm.createBackgroundSubtractorMOG()  # remove background
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))  # Video Morphology

        cars = []  # Save vehicle hub information
        car_n = 0  # Counting cars

        with tqdm(total=100000, desc='Example', leave=True, ncols=100, unit='B', unit_scale=True) as tqbar:

            # Window entry
            barload = Progressbar(bar1, length=350)  # Length 350
            barload.pack(pady=10)  # Up and down spacing 10
            Button(bar1, text='Cancel', command=bar1.destroy).pack()  # Shutdown button
            barload['value'] = 0  # Set the progress bar value (set the initial value to zero)
            barload['maximum'] = 350  # Set the maximum progress bar

            for i in range(350):
                barload['value'] += 50
                barload.update()  # Update progress bar values
                sleep(0)

            for i in range(10):
                tqbar.update(10000)  # Update the progress bar

            bar1.destroy()

        while file.isOpened():

            ret, frame = file.read()
            if ret:
                '''
                Video pre-processing phase
                '''
                # Greyscale Treatment
                # Image grayscale processing can be used as a preprocessing step for image segmentation, image recognition, and image analysis.
                cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

                # Gaussian denoising -Gaussian filtering is a linear smoothing filter which is suitable for eliminating Gaussian noise and widely used in image denoising.
                # It can simply be understood that Gaussian filter denoising is the weighted averaging of pixel values across an image, with values for each pixel being obtained by weighted averaging their own values and those of other pixels in the neighborhood.
                blur = cv2.GaussianBlur(frame, (3, 3), 5)  # Gaussian Blur () Gaussian filter is a linear smoothing filter which is suitable for eliminating Gaussian noise and widely used in image processing.
                mask = bgsubmog.apply(blur)  # remove background
                cv2.imshow('video', mask)

                # Corrosion -can be more accurate in colour tracing, with less colour interference
                erode = cv2.erode(mask, kernel)  # erode()coupled with Gaussian blurring, can make the image more colourful

                # Expansions are morphological operations, called morphologies, that change the shape of an object, figuratively understand something: corrosion = thinning expansions = getting fat
                dilate = cv2.dilate(erode, kernel, 3)

                # Closed operations
                close = cv2.morphologyEx(dilate, cv2.MORPH_CLOSE, kernel)  # cv2. MorphologyEx undergoes various morphological changes
                close = cv2.morphologyEx(close, cv2.MORPH_CLOSE, kernel)

                # use cv2. findContours () function to find the outline of the detection object.
                contours, h = cv2.findContours(close, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE, )

                # draw a line
                # cv2.line(image, start_point, end_point, color, thickness)
                # cv2.line(frame, (20, 500), (1300, 550), (0, 255, 255), 3)

                for (i, c) in enumerate(contours):  # enumerate()Data Objects Traversed
                    (x, y, w, h) = cv2.boundingRect(c)  # cv2.boundingRect()This function gets some information about the minimum rectangular border of an image

                    # Filter small test box
                    isshow = (w >= 90) and (h >= 90)
                    if not isshow:
                        continue

                    # Save Hub information
                    # cv2.rectangle Contains parameters： (img, pt1, pt2, color, thickness=None, lineType=None, shift=None)
                    # cv2.rectangle(Read the picture variable, (top left) (bottom right), (color), (line width)
                    cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)
                    centre_p = (x + int(w / 2), y + int(h / 2))
                    cars.append(centre_p)

                    # cv2.circle(frame, centre_p, 5, (0, 0, 255), -1)
                    for (x, y) in cars:
                        if 593 < y < 607:
                            car_n += 1
                            cars.remove((x, y))

            # cv2.putText(img，text，org, fontFace, fontScale, color, thinckness, lineType, bottomLeftOrigin)
            cv2.putText(frame, "Cars Count:" + str(car_n), (500, 60), cv2.FONT_HERSHEY_SIMPLEX, 1,
                        (0, 0, 255), 4)

            cv2.imshow('video', frame)

            key = cv2.waitKey(1)
            if key == 27:  # Esc Keyboard Exit Program
                # If you set WaitKey (0), you are waiting indefinitely for the keyboard to enter, which means you can press any key to continue
                break
            if cv2.getWindowProperty('video', cv2.WND_PROP_VISIBLE) < 1:  # Click close the window to exit the program
                break


if __name__ == '__main__':
    window.geometry('600x400')
    window.title("Real-time-Traffic-Video")
    main = mainframe(master=window)
    window.mainloop()
