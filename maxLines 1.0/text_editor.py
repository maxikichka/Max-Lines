from tkinter import *
import pyautogui
from tkinter.filedialog import asksaveasfile
from tkinter.filedialog import askopenfilename
from tkinter import ttk
import re
from tkinter import filedialog
import os
from io import StringIO
import sys
from PIL import ImageTk, Image
from tkinter import messagebox
import webbrowser

text_boxes = []
tabs_list = []

text_size = 11


#data
keywords = ['False', 'None', 'True', 'and', 'as', 'assert', 'async', 'await', 'break', 'class', 'continue', 'def', 'del', 'elif', 'else', 'except', 'finally', 'for', 'from', 'global', 'if', 'import', 'in', 'is', 'lambda', 'nonlocal', 'not', 'or', 'pass', 'raise', 'return', 'try', 'while', 'with', 'yield']
builtins = ['__build_class__', '__import__', 'abs', 'all', 'any', 'ascii', 'bin', 'breakpoint', 'callable', 'chr', 'compile', 'delattr', 'dir', 'divmod', 'eval', 'exec', 'format', 'getattr', 'globals', 'hasattr', 'hash', 'hex', 'id', 'input', 'isinstance', 'issubclass', 'iter', 'len', 'locals', 'max', 'min', 'next', 'oct', 'ord', 'pow', 'print', 'repr', 'round', 'setattr', 'sorted', 'sum', 'vars', 'open']
definitions = []

def decrease_text_size(*args):
    global text_size
    text_size -= 1
    text_boxes[tabControl.index(tabControl.select())].config(font=("Courier", text_size))

def increase_text_size(*args):
    global text_size
    text_size += 1
    text_boxes[tabControl.index(tabControl.select())].config(font=("Courier", text_size))


def search_google(*args):

    query = text_boxes[tabControl.index(tabControl.select())].get(SEL_FIRST, SEL_LAST)
    
    webbrowser.open("https://www.google.com/search?q=" + query)

def comment_block(*args):
    if text_boxes[tabControl.index(tabControl.select())].tag_ranges(SEL):
        text = text_boxes[tabControl.index(tabControl.select())].get("1.0", END).split("\n")

        highlighted = text_boxes[tabControl.index(tabControl.select())].get(SEL_FIRST, SEL_LAST).split("\n")

        #high_i = text.index(highlighted[0])


        for i in range(len(highlighted)):

            if len(highlighted[i]) < 1:
                continue
                
            if i <= len(highlighted) - 1 and highlighted[i][0] == "#":
                text_boxes[tabControl.index(tabControl.select())].delete(str(i + 1) + ".0", str(i + 1) + ".1")


            else:
                if i <= len(highlighted) - 1:
                    text_boxes[tabControl.index(tabControl.select())].insert(str(i + 1) + ".0", "#")

    else:
        return

def run_code(*args):

    code = text_boxes[tabControl.index(tabControl.select())].get("1.0", END)

    old_stdout = sys.stdout
    sys.stdout = mystdout = StringIO()

    try:
    
        exec("import time\nstart = time.time()\n" + code + "end = time.time()\nprint('[Finished in ' + str(end-start) + ']')")
        sys.stdout = old_stdout

        message = mystdout.getvalue()

    except Exception as err:
        message = err
    

    output.insert(INSERT, message)

    


    print(message)

def open_selcted_file(*args):

    try:
    
        filename = files_list[tree.index(tree.curselection())]

    except NameError:
        return

    filepath = path_list[tree.index(tree.curselection())]


    add_tab(filename)

    text_bar = Scrollbar(tabs_list[-1]) 
  
    text_bar.pack(side = RIGHT, fill = Y)

    

    text_boxes.append(Text(tabs_list[-1], undo=True, maxundo=-1, autoseparators=True, yscrollcommand = text_bar.set))

    text_binds()

    text_boxes[-1].config(font=("Courier", text_size))

    '''
    if filepath.endswith(".ico") or filepath.endswith(".png") or filepath.endswith(".jpg"):
        img = Image.open(filepath)
        img = ImageTk.PhotoImage(img)
        panel = Label(text_boxes[-1], image=img)
        panel.image = img
        panel.pack()
    '''

    text_boxes[-1].pack(fill = BOTH, expand = True)

    text_bar.config(command = text_boxes[-1].yview)

    try:
        read_file = open(filepath, "rb")
        read_file.close()
    except PermissionError:
        return
    
    try:
        read_file = open(filepath, "r")
        text_boxes[-1].insert("1.0", read_file.read())

        read_file.close()
    except UnicodeDecodeError:
        if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.tiff', '.bmp', '.gif', '.ico')):
            img = Image.open(filepath)
            img = ImageTk.PhotoImage(img)
            panel = Label(text_boxes[-1], image=img)
            panel.image = img
            panel.pack()
            
        else:
            output_binary = messagebox.askyesno(title="File Type Not Supported", message="Mline will show this file as a binary, which may cause your editor to go unresponsive. Proceed?")
            if output_binary:
                read_file = open(filepath, "rb")
                text_boxes[-1].insert("1.0", read_file.read())
                read_file.close()
            else:
                tabControl.forget(text_boxes[tabControl.index(tabControl.select())])
                return
                


def open_tree():

    global files_list, path_list

    files_list = []
    path_list = []

    count = 1

    tree.insert(1, "Loading your project folder")

    tree.insert(2, "please wait...")
    
    startpath = filedialog.askdirectory()



    tree.delete(0, END)


    for root, dirs, files in os.walk(startpath):
        level = root.replace(startpath, '').count(os.sep)
        indent = ' ' * 4 * (level)

        tree.insert(count, '{}{}/'.format(indent, "0" + os.path.basename(root)))
        
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

    #j = 0

    lines = code.split("\n")

    for i in range(len(lines)):

        #print(i)
##        for j in range(len(lines[i])):
##            if lines[i][j] == "#":
##                text_boxes[tabControl.index(tabControl.select())].tag_add(i, str(i + 1) + "." + str(j), str(i + 1) + "." + str(len(lines[i])))
##                text_boxes[tabControl.index(tabControl.select())].tag_configure(i, foreground="red")
##                break
##            elif lines[i][j] == '"':
##                text_boxes[tabControl.index(tabControl.select())].tag_add(i, str(i + 1) + "." + str(j), str(i + 1) + "." + str(lines[i].find('"', j + 1, len(lines[i])) + 1))
##                text_boxes[tabControl.index(tabControl.select())].tag_configure(i, foreground="green")
##                j = lines[i].find('"', j + 2, len(lines[i])) + 1
##
##            elif lines[i][j] == "'":
##                text_boxes[tabControl.index(tabControl.select())].tag_add(i, str(i + 1) + "." + str(j), str(i + 1) + "." + str(lines[i].find("'", j + 1, len(lines[i])) + 1))
##                text_boxes[tabControl.index(tabControl.select())].tag_configure(i, foreground="green")
##                j = lines[i].find("'", j + 2, len(lines[i])) + 1


        j = 0
        while j < len(lines[i]):
            #print(j)
            if lines[i][j] == "#":
                text_boxes[tabControl.index(tabControl.select())].tag_add(j, str(i + 1) + "." + str(j), str(i + 1) + "." + str(len(lines[i])))
                text_boxes[tabControl.index(tabControl.select())].tag_configure(j, foreground="red")
                break
            elif lines[i][j] == '"':
                text_boxes[tabControl.index(tabControl.select())].tag_add(j, str(i + 1) + "." + str(j), str(i + 1) + "." + str(lines[i].find('"', j + 1, len(lines[i])) + 1))
                text_boxes[tabControl.index(tabControl.select())].tag_configure(j, foreground="green")
                #j += ((lines[i].find('"', j, len(lines[i])) + 1) - j)
                #j += 3

            elif lines[i][j] == "'":
                text_boxes[tabControl.index(tabControl.select())].tag_add(j, str(i + 1) + "." + str(j), str(i + 1) + "." + str(lines[i].find("'", j + 1, len(lines[i])) + 1))
                text_boxes[tabControl.index(tabControl.select())].tag_configure(j, foreground="green")
                #j = lines[i].find("'", j, len(lines[i])) + 1
                #j += ((lines[i].find('"', j, len(lines[i])) + 1) - j)
            j += 1



def delete_tab(*args):
    tabControl.forget(tabControl.select())

def delete_line(*args):
    pos = text_boxes[tabControl.index(tabControl.select())].index(CURRENT)
    coors = pos.split(".")
    text_boxes[tabControl.index(tabControl.select())].delete(coors[0] + ".0", coors[0] + ".100")

def save(*args):

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

    #print(event.char)

    if event.char == ".":
        Listbox(text_boxes[tabControl.index(tabControl.select())]).pack(pady=25, padx=25)
    
    if text_boxes[tabControl.index(tabControl.select())].edit_modified() != 0:
        win.title("*" + tabControl.tab(tabControl.select(), "text"))
        code = text_boxes[tabControl.index(tabControl.select())].get("1.0", END)
        highlighting_syntax(code)

def change_tab(*args):
    selected_tab = tabControl.tab(tabControl.select(), "text")

    #print(selected_tab)
    win.title(selected_tab)

def text_binds():
    text_boxes[-1].bind("<F5>", run_code)
    #text_boxes[tabControl.index(tabControl.select())]
    text_boxes[-1].bind("<Control_L><space>", command_prompt)
    #text_boxes[tabControl.index(tabControl.select())].bind("<<Modified>>", changes_made)
    text_boxes[-1].bind("<Key>", changes_made)
    #text_boxes[tabControl.index(tabControl.select())].bind("<Control_L>s", undo)
    text_boxes[-1].bind("<Control-s>", save)
    
    text_boxes[-1].bind("<Control-d>", delete_line)

    text_boxes[-1].bind("<Control-w>", delete_tab)


    text_boxes[-1].bind("<Alt-slash>", comment_block)

    text_boxes[-1].bind("<Control-b>", search_google)

    text_boxes[-1].bind("<Control_L><Shift_L>", save_as)

    text_boxes[-1].bind("<Control-equal>", increase_text_size)


    text_boxes[-1].bind("<Control-minus>", decrease_text_size)






def new_file(*args):
    global text_box
    add_tab("Untitled")

    text_bar = Scrollbar(tabs_list[-1]) 
  
    text_bar.pack(side = RIGHT, fill = Y)


    line_numbers = Text(tabs_list[-1], width=2)

    line_numbers.pack(side = LEFT, fill = BOTH)
    
    
    text_boxes.append(Text(tabs_list[-1], bg="black", fg="white", insertbackground='white', undo=True, maxundo=-1, autoseparators=True, yscrollcommand = text_bar.set))

    text_binds()

    text_boxes[-1].config(font=("Courier", text_size))

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
    
    


def open_file(*args):
    #global text_box
    filename = askopenfilename()
    file_content = open(filename, "rb")
    add_tab(filename)

    text_bar = Scrollbar(tabs_list[-1]) 
  
    text_bar.pack(side = RIGHT, fill = Y)
    
    
    text_boxes.append(Text(tabs_list[-1], undo=True, maxundo=-1, autoseparators=True, yscrollcommand = text_bar.set))

    text_binds()

    text_boxes[-1].config(font=("Courier", text_size))

    text_boxes[-1].pack(fill = BOTH, expand = True)

    text_boxes[-1].insert("1.0", file_content.read())

    text_bar.config(command = text_boxes[-1].yview)



    highlighting_syntax(text_boxes[tabControl.index(tabControl.select())].get("1.0", END))
    


def save_as(*args):
    files = [('All Files', '*.*'),  
             ('Python Files', '*.py'), 
             ('Text Document', '*.txt')] 
    file_saved = asksaveasfile(filetypes = files, defaultextension = files)
    #print(file_saved.get())
    if file_saved is None:
        return
    file_saved.write(text_boxes[tabControl.index(tabControl.select())].get("1.0", END))
    file_saved.close()


    tabControl.tab(tabs_list[tabControl.index(tabControl.select())], text=file_saved.name)

    change_tab()


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

win.bind("<Control-o>", open_file)

win.bind("<Control-n>", new_file)



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

output = Text(win, height=5)

output.pack()



win.mainloop()
