from tkinter import *
from tkinterdnd2 import *
from tkinter.messagebox import showerror
import os,re


# Load tkdnd, which provides drag and drop support for objects within a single application, within the same window, or between windows. To enable an object to be dragged, you must create an event binding for it to start the drag and drop process
class TkDnD:
    def __init__(self, tkroot):
        # 'single underscore 'starts with member variables called protected variables, meaning that only class objects and subclass objects have access to them themselves; cannot be imported with' from xxx import * ';
        # "Double underline" begins with a private member, meaning that only class objects can access this data themselves, not even subclass objects.
        self._tkroot = tkroot
        tkroot.tk.eval('package require tkdnd')
        tkroot.dnd = self
        # make self an attribute of the parent window for easy access in child classes
    

    def bindsource(self, widget, type=None, command=None, arguments=None, priority=None):

        """
        Register widget as drag source; for details on type, command and arguments, see bindtarget().
        priority can be a value between 1 and 100, where 100 is the highest available priority (default: 50).
        If command is omitted, return the current binding for type; if both type and command are omitted,
        return a list of registered types for widget.
        """

        command = self._generate_callback(command, arguments)
        tkcmd = self._generate_tkcommand('bindsource', widget, type, command, priority)
        res = self._tkroot.tk.eval(tkcmd)
        if type == None:
            res = res.split()
        return res

    def bindtarget(self, widget, type=None, sequence=None, command=None, arguments=None, priority=None):

        """
        Register widget as drop target; type may be one of text/plain, text/uri-list, text/plain;charset=UTF-8 (see
        the man page tkDND for details on other (platform specific) types); sequence may be one of '<Drag>',
        '<DragEnter>', '<DragLeave>', '<Drop>' or '<Ask>' ; command is the callback associated with the specified
        event, argument is an optional tuple of arguments that will be passed to the callback; possible arguments
        include: %A %a %b %C %c %D %d %L %m %T %t %W %X %x %Y %y (see the tkDND man page for details); priority may
        be a value in the range 1 to 100 ; if there are bindings for different types, the one with the priority value
        will be proceeded first (default: 50). If command is omitted, return the current binding for type,
        where sequence defaults to '<Drop>'. If both type and command are omitted, return a list of registered types
        for widget.

        """

        command = self._generate_callback(command, arguments)
        tkcmd = self._generate_tkcommand('bindtarget', widget, type, sequence, command, priority)
        res = self._tkroot.tk.eval(tkcmd)

        if type == None:
            res = res.split()
        return res

    def clearsource(self, widget):
        """
        Unregister widget as drag source.
        """

        self._tkroot.tk.call('dnd', 'clearsource', widget)

    def cleartarget(self, widget):
        """
        Unregister widget as drop target.
        """

        self._tkroot.tk.call('dnd', 'cleartarget', widget)

    def drag(self, widget, actions=None, descriptions=None, cursorwindow=None, command=None, arguments=None):
        """
        Initiate a drag operation with source widget.
        """
        command = self._generate_callback(command, arguments)

        if actions:
            if actions[1:]:
                actions = '-actions {%s}' % ' '.join(actions)
            else:
                actions = '-actions %s' % actions[0]

        if descriptions:
            descriptions = ['{%s}' % i for i in descriptions]
            descriptions = '{%s}' % ' '.join(descriptions)

        if cursorwindow:
            cursorwindow = '-cursorwindow %s' % cursorwindow

        tkcmd = self._generate_tkcommand('drag', widget, actions, descriptions, cursorwindow, command)
        self._tkroot.tk.eval(tkcmd)

    def _generate_callback(self, command, arguments):
        '''
        Register command as tk callback with an optional list of arguments.
        '''

        cmd = None
        if command:
            cmd = self._tkroot._register(command)
            if arguments:
                cmd = '{%s %s}' % (cmd, ' '.join(arguments))
        return cmd

    def _generate_tkcommand(self, base, widget, *opts):
        '''
        Create the command string that will be passed to tk.
        '''

        tkcmd = 'dnd %s %s' % (base, widget)
        for i in opts:
            if i is not None:
                tkcmd += ' %s' % i

        return tkcmd


# Adds dragged files to listbox
def drop(files):
    print(files)
    # Drag file has special symbol solution
    if isinstance(files, str):
        # s = re.compile(r'[{](.*?)[}]').findall(files) # special symbol {} filter
        files = re.sub(u"{.*?}", "", files).split()  # Split multiple files by whitespace, so no whitespace in filenames

    for file in files:
        lb.insert("end", file)


# Open the selected file
def open_file():
    if not lb.curselection():
        showerror("ERROR", "Nothing selected！")
        return
    file = lb.get(lb.curselection())  # Gets the currently selected file path
    print(file)
    os.startfile(file)  # Open the file

if __name__ == '__main__':
    root = Tk()

    root.title("My tools")
    root.geometry()
    root.wm_resizable(False, False)  # No modification of length and width allowed

    dnd = TkDnD(root)

    lb = Listbox(root, height=7, width=60, selectmode=SINGLE)
    dnd.bindtarget(lb, 'text/uri-list', '<Drop>', drop, ('%D',))
    # These are events that bind when you drag a file into a box, and you can write your own functional tests
    # dnd.bindtarget(lb, 'text/uri-list', '<Drag>', lambda x:x, ('%A', ))
    # dnd.bindtarget(lb, 'text/uri-list', '<DragEnter>', drag, ('%A', ))

    lb.grid(row=0, rowspan=7, column=1, columnspan=5, padx=20)

    Button(root, text="Open the file", width=10, command=open_file).grid(row=7, column=5, padx=10, ipadx=10, pady=10)

    root.mainloop()

