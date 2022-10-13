from tkinter import *  # 调用GUI库, 适合小型GUI程序编写
from tkinter.filedialog import *
import numpy as np
import cv2

window = Tk()
window.geometry("600x450")

frm1=Frame(window)
frm1.pack(side='left')

frm2=Frame(window)
frm2.pack(side='right')

Label(frm1, text="right frame").pack()
Label(frm2, text="left frame").pack()

'''
frame = Frame(root)
frame.pack()

leftframe = Frame(root)
leftframe.pack(side=LEFT)

rightframe = Frame(root)
rightframe.pack(side=RIGHT)

label = Label(frame, text="Project Real- time Traffic Video generation")
label.pack()

button1 = Button(leftframe, text="Play video")
button1.pack(padx=3, pady=3)

button2 = Button(leftframe, text="Analysis video")
button2.pack(padx=3, pady=3)

button3 = Button(leftframe, text="Save video")
button3.pack(padx=3, pady=3)
'''

window.title("Test")
window.mainloop()   #调用组件的mainloop()方法，进入事件循环
