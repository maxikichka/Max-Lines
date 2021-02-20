from tkinter import *
import pyautogui
from tkinter.filedialog import asksaveasfile
from tkinter.filedialog import askopenfilename
from tkinter import ttk
import re
from tkinter import filedialog
import os

text_boxes = []
tabs_list = []


#data
keywords = ['False', 'None', 'True', 'and', 'as', 'assert', 'async', 'await', 'break', 'class', 'continue', 'def', 'del', 'elif', 'else', 'except', 'finally', 'for', 'from', 'global', 'if', 'import', 'in', 'is', 'lambda', 'nonlocal', 'not', 'or', 'pass', 'raise', 'return', 'try', 'while', 'with', 'yield']
builtins = ['__build_class__', '__import__', 'abs', 'all', 'any', 'ascii', 'bin', 'breakpoint', 'callable', 'chr', 'compile', 'delattr', 'dir', 'divmod', 'eval', 'exec', 'format', 'getattr', 'globals', 'hasattr', 'hash', 'hex', 'id', 'input', 'isinstance', 'issubclass', 'iter', 'len', 'locals', 'max', 'min', 'next', 'oct', 'ord', 'pow', 'print', 'repr', 'round', 'setattr', 'sorted', 'sum', 'vars', 'open']
definitions = []

def open_selcted_file(event):
    filename = files_list[tree.index(tree.curselection())]

    filepath = path_list[tree.index(tree.curselection())]



    if filename.endswith(".py"):
        add_tab("🐍" + filename)
    else:
        add_tab(filename)

    text_bar = Scrollbar(tabs_list[-1]) 
  
    text_bar.pack(side = RIGHT, fill = Y)

    

    text_boxes.append(Text(tabs_list[-1], undo=True, maxundo=-1, autoseparators=True, yscrollcommand = text_bar.set))

    

    text_binds()

    text_boxes[-1].pack(fill = BOTH, expand = True)

    text_bar.config(command = text_boxes[-1].yview)

    try:
        read_file = open(filepath, "rb")
    except PermissionError:
        return

    try:
        text_boxes[-1].insert("1.0", read_file.read())
    except UnicodeDecodeError:
        return
    

    

    read_file.close()


def open_tree():

    global files_list, path_list

    files_list = []
    path_list = []

    count = 1
    
    startpath = filedialog.askdirectory()


    for root, dirs, files in os.walk(startpath):
        level = root.replace(startpath, '').count(os.sep)
        indent = ' ' * 4 * (level)

        tree.insert(count, '{}{}/'.format(indent, "📁" + os.path.basename(root)))
        
        files_list.append(os.path.basename(root))

        path_list.append(root)
        
        subindent = ' ' * 4 * (level + 1)

        count += 1

        
        for f in files:
            tree.insert(count, "{}{}".format(subindent, f))
            
            files_list.append(f)
            path_list.append(root + "/" + f)

            count += 1


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

    selected_tab = tabControl.tab(tabControl.select(), "text")

    if selected_tab == "Untitled":
        save_as()
        return
    
    win.title(selected_tab)
    
    write_file = open(selected_tab, "w")

    write_file.write(text_boxes[tabControl.index(tabControl.select())].get("1.0", END))

    write_file.close()
    text_boxes[tabControl.index(tabControl.select())].edit_modified(False)


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

    text_bar = Scrollbar(tabs_list[-1]) 
  
    text_bar.pack(side = RIGHT, fill = Y)
    
    text_boxes.append(Text(tabs_list[-1], undo=True, maxundo=-1, autoseparators=True, yscrollcommand = text_bar.set))

    text_binds()

    text_boxes[-1].pack(fill = BOTH, expand = True)


    text_bar.config(command = text_boxes[-1].yview)

def tabs():
    global tabControl
    #style = ttk.Style()
    #ttk.Style().configure("TButton", padding=6, relief="flat", background="#ccc")
    tabControl = ttk.Notebook(win)
    tabControl.bind("<<NotebookTabChanged>>", change_tab)
    tabControl.bind("<Button-2>", delete_tab)
    tabControl.pack(fill = BOTH, expand = True)


def add_tab(tab_name):
    global tab
    tabs_list.append(ttk.Frame(tabControl))
    tabControl.add(tabs_list[-1], text=tab_name)
    
    


def open_file():
    #global text_box
    filename = askopenfilename()
    file_content = open(filename, "rb")
    add_tab(filename)

    text_bar = Scrollbar(tabs_list[-1]) 
  
    text_bar.pack(side = RIGHT, fill = Y)
    
    
    text_boxes.append(Text(tabs_list[-1], undo=True, maxundo=-1, autoseparators=True, yscrollcommand = text_bar.set))

    text_binds()

    text_boxes[-1].pack(fill = BOTH, expand = True)

    text_boxes[-1].insert("1.0", file_content.read())

    text_bar.config(command = text_boxes[-1].yview)


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

win.wm_iconbitmap('imgs/logo.ico')

win.title("Mline")



open_project = Button(win, text="Open project", command=open_tree)

open_project.pack(side = TOP)

   
tree_bar = Scrollbar(win) 
  
tree_bar.pack(side = LEFT, fill = Y)

tree = Listbox(win, width=25, yscrollcommand = tree_bar.set)


tree.bind('<<ListboxSelect>>', open_selcted_file)

tree.pack(side = LEFT, fill = BOTH)

tree_bar.config( command = tree.yview )


tabs()

menus()



win.mainloop()
