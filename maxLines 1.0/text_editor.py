from tkinter import *
import pyautogui
from tkinter.filedialog import asksaveasfile
from tkinter.filedialog import askopenfilename
from tkinter import ttk
import re
from tkinter import filedialog
import os

cur_text = ""
text_boxes = []
tabs_list = []


#data
keywords = ['False', 'None', 'True', 'and', 'as', 'assert', 'async', 'await', 'break', 'class', 'continue', 'def', 'del', 'elif', 'else', 'except', 'finally', 'for', 'from', 'global', 'if', 'import', 'in', 'is', 'lambda', 'nonlocal', 'not', 'or', 'pass', 'raise', 'return', 'try', 'while', 'with', 'yield']
builtins = ['__build_class__', '__import__', 'abs', 'all', 'any', 'ascii', 'bin', 'breakpoint', 'callable', 'chr', 'compile', 'delattr', 'dir', 'divmod', 'eval', 'exec', 'format', 'getattr', 'globals', 'hasattr', 'hash', 'hex', 'id', 'input', 'isinstance', 'issubclass', 'iter', 'len', 'locals', 'max', 'min', 'next', 'oct', 'ord', 'pow', 'print', 'repr', 'round', 'setattr', 'sorted', 'sum', 'vars', 'open']
definitions = []

def open_tree(event):

    files_list = []
    
    startpath = filedialog.askdirectory()

    for root, dirs, files in os.walk(startpath):
        level = root.replace(startpath, '').count(os.sep)
        indent = ' ' * 4 * (level)
        #print('{}{}/'.format(indent, os.path.basename(root)))
        files_list.append('{}{}/'.format(indent, os.path.basename(root)))
        
        subindent = ' ' * 4 * (level + 1)
        for f in files:
            #print('{}{}'.format(subindent, f))
            files_list.append('{}{}'.format(subindent, f))
        
        


    for i in range(len(files_list)):
        tree.insert(i + 1, files_list[i])


    
    

def highlighting_syntax(code):
    #print("hi")
    #keywords
    #builtins
    #comments
    #strings
    #definitions

    #pattern = re.compile("")

    #print(re.search(pattern, code))

    code.find("#")
    
    
    

def delete_tab(event):
    if len(tabs_list) == 1:
        win.destroy()
    tabControl.forget(tabControl.select())

def delete_line(event):
    pos = text_boxes[tabControl.index(tabControl.select())].index(CURRENT)
    coors = pos.split(".")
    text_boxes[tabControl.index(tabControl.select())].delete(coors[0] + ".0", coors[0] + ".100")

def save():
    
    cur_text = text_boxes[tabControl.index(tabControl.select())].get("1.0", END)
    selected_tab = tabControl.tab(tabControl.select(), "text")

    if selected_tab == "Untitled":
        save_as()
        return
    
    win.title(selected_tab)
    
    write_file = open(selected_tab, "w")

    write_file.write(text_boxes[tabControl.index(tabControl.select())].get("1.0", END))

    write_file.close()
    text_boxes[tabControl.index(tabControl.select())].edit_modified(False)

def save_shortcut(event):
    
    cur_text = text_boxes[tabControl.index(tabControl.select())].get("1.0", END)
    selected_tab = tabControl.tab(tabControl.select(), "text")

    if selected_tab == "Untitled":
        save_as()
        return
    
    win.title(selected_tab)
    
    write_file = open(selected_tab, "w")

    write_file.write(text_boxes[tabControl.index(tabControl.select())].get("1.0", END))

    write_file.close()
    text_boxes[tabControl.index(tabControl.select())].edit_modified(False)


'''def undo(event):
    print("hi")
    text_boxes[tabControl.index(tabControl.select())].delete("1.0", END)
    text_boxes[tabControl.index(tabControl.select())].insert("1.0", cur_text)
'''
def changes_made(event):
    #print("hi")
    #print(text_boxes[tabControl.index(tabControl.select())].edit_modified())
    if text_boxes[tabControl.index(tabControl.select())].edit_modified() != 0:
        win.title("*" + tabControl.tab(tabControl.select(), "text"))
        code = text_boxes[tabControl.index(tabControl.select())].get("1.0", END)
        highlighting_syntax(code)

def change_tab(event):
    selected_tab = tabControl.tab(tabControl.select(), "text")

    print(selected_tab)
    win.title(selected_tab)

def text_binds():
    #text_boxes[tabControl.index(tabControl.select())]
    text_boxes[-1].bind("<Control_L><space>", command_prompt)
    #text_boxes[tabControl.index(tabControl.select())].bind("<<Modified>>", changes_made)
    text_boxes[-1].bind("<Key>", changes_made)
    #text_boxes[tabControl.index(tabControl.select())].bind("<Control_L>s", undo)
    text_boxes[-1].bind("<Control-s>", save_shortcut)
    
    text_boxes[-1].bind("<Control-d>", delete_line)

    text_boxes[-1].bind("<Control-w>", delete_tab)


    
    

def new_file():
    global text_box
    add_tab("Untitled")
    text_boxes.append(Text(tabs_list[-1], undo=True, maxundo=-1, autoseparators=True))

    text_binds()

    text_boxes[-1].pack()

def tabs():
    global tabControl
    #style = ttk.Style()
    #ttk.Style().configure("TButton", padding=6, relief="flat", background="#ccc")
    tabControl = ttk.Notebook(win)
    tabControl.bind("<<NotebookTabChanged>>", change_tab)
    



def add_tab(tab_name):
    global tab
    tabs_list.append(ttk.Frame(tabControl))
    tabControl.add(tabs_list[-1], text=tab_name)
    tabControl.grid(column=2, row=0)
    tabs_list[-1].bind("<Button-2>", delete_tab)


def open_file():
    #global text_box
    filename = askopenfilename()
    file_content = open(filename, "r")
    add_tab(filename)
    text_boxes.append(Text(tabs_list[-1], undo=True, maxundo=-1, autoseparators=True))

    text_binds()

    text_boxes[-1].pack()

    text_boxes[-1].insert("1.0", file_content.read())

    cur_text = text_boxes[-1].get("1.0", END)

def save_as():
    files = [('All Files', '*.*'),  
             ('Python Files', '*.py'), 
             ('Text Document', '*.txt')] 
    file_saved = asksaveasfile(filetypes = files, defaultextension = files)
    if file_saved is None:
        return
    file_saved.write(text_boxes[tabControl.index(tabControl.select())].get("1.0", END))
    file_saved.close()

def menus():
    menu = Menu(win)
    win.config(menu=menu)
    fileMenu = Menu(menu)
    menu.add_cascade(label="File", menu=fileMenu)
    fileMenu.add_command(label="New", command=new_file)
    fileMenu.add_command(label="Save as", command=save_as)
    fileMenu.add_command(label="Save", command=save)
    fileMenu.add_command(label="Open", command=open_file)
    fileMenu.add_separator()

def command_prompt(event):
    command = pyautogui.prompt(text='Line Column', title='Coordinate to go to' , default='0 0')
    line = int(command.split(" ")[0])
    column = int(command.split(" ")[1])
    text_boxes[tabControl.index(tabControl.select())].mark_set("insert", "%d.%d" % (line, column))
    text_boxes[tabControl.index(tabControl.select())].see(str(line) + "." + str(column))
win = Tk()

win.title("Mline")

tabs()

open_project = Button(win, text="Open project")

open_project.grid(column=1, sticky=N)

tree = Listbox(win)

tree.grid(column=1, sticky=N)

menus()



win.mainloop()
