import tkinter as tk
import windnd
from tkinter.messagebox import showinfo


def dragged_files(files):
    msg = '\n'.join((item.decode('gbk') for item in files))
    showinfo("Drag file path", msg)


if __name__ == '__main__':
    rootWindow = tk.Tk()
    windnd.hook_dropfiles(rootWindow, func=dragged_files)
    rootWindow .mainloop()