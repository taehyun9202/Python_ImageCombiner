import os
import tkinter.ttk as ttk
import tkinter.messagebox as msgbox
from tkinter import *
from tkinter import filedialog
from PIL import Image
import keyboard
import time
from PIL import ImageGrab #python image library

root = Tk()
root.title("Image Combiner")


# div1

file_frame = Frame(root)
file_frame.pack(fill="both", padx=5, pady=5)

def add_file():
    files = filedialog.askopenfilenames(title="Select image files",
        filetypes = (("PNG file", "*.png"), ("JPG file", "*.jpg"), ("All File", "*.*")),
        initialdir = r"C:\Users\TylerN\Coding\python\python_stack\python\gui")

    for file in files:
        # print(file)
        list_file.insert(END, file)

def del_file():
    for index in reversed(list_file.curselection()): # need to delete from the back for multiple delete 
        list_file.delete(index)

# save directory (folder)
def browse_path():
    selected_folder = filedialog.askdirectory()
    if selected_folder == "":
        return
    txt_path.delete(0, END)
    txt_path.insert(END, selected_folder)
    # print(selected_folder)

def merge_image():
    # print(cmb_width.get(), cmb_space.get(), cmb_format.get())
    # print(list_file.get(0, END))
    try: 
        img_width = cmb_width.get()
        if img_width == "Original":
            img_width = -1
        else:
            img_width = int(img_width)

        img_space = cmb_space.get()
        if img_space == "Narrow":
            img_space = 30
        elif img_space == "Normal":
            img_space = 60
        elif img_space == "Wide":
            img_space = 90
        else:
            img_space = 0

        img_format = cmb_format.get().lower()


        images = [Image.open(x) for x in list_file.get(0, END)]

        images_sizes = []
        if img_width > -1:
            images_sizes = [(int(img_width), int(img_width * x.size[1] / x.size[0])) for x in images]
        else:
            images_sizes = [(x.size[0], x.size[1]) for x in images]
    
        # widths = [x.size[0] for x in images]
        # heights = [x.size[1] for x in images]
        widths, heights = zip(*(images_sizes))

        max_width, total_height = max(widths), sum(heights)
        # print(max_width, total_height)

        if img_space > 0:
            total_height += (img_space * (len(images) - 1))
        result_img = Image.new("RGB", (max_width, total_height), (255, 255, 255))
        y_offset = 0 # y coordination

        for index, img  in enumerate(images):
            if img_width > -1:
                img = img.resize(images_sizes[index])

            result_img.paste(img, (0, y_offset))
            y_offset += (img.size[1] + img_space)

            progress = (index + 1) / len(images) * 100 # percentage
            p_var.set(progress)
            progressbar.update()

        file_name = "combined." + img_format
        dest_path = os.path.join(txt_path.get(), file_name)
        result_img.save(dest_path)
        msgbox.showinfo("Info", "Combine finished")
    
    except Exception as err:
        msgbox.showerror("Error", err)


def start():
    # print(cmb_width.get(), cmb_space.get(), cmb_format.get())
    if list_file.size() < 2:
        msgbox.showwarning("Warning!","Add more than 1 image")

    elif len(txt_path.get()) == 0:
        msgbox.showwarning("Warning", "Select saving directory")

    else:
        merge_image()


btn_add_file = Button(file_frame, text="Add file", width=10, height=2, padx=5, pady=5, command=add_file)
btn_add_file.pack(side="left", padx=5, pady=5)

btn_delete_file = Button(file_frame, text="Delete file", width=10, height=2, padx=5, pady=5, command=del_file)
btn_delete_file.pack(side="right", padx=5, pady=5)


# div2

list_frame = Frame(root)
list_frame.pack(fill="both", padx=5, pady=5)

scrollbar = Scrollbar(list_frame)
scrollbar.pack(side="right", fill="y", padx=5, pady=5)

list_file = Listbox(list_frame, selectmode="extended", height=10, yscrollcommand=scrollbar.set)
list_file.pack(side="left", fill="both", expand=True, padx=5, pady=5)
scrollbar.config(command=list_file.yview)


# div3

path_frame = LabelFrame(root, text="Save location")
path_frame.pack(fill="both", padx=5, pady=5)

txt_path = Entry(path_frame)
txt_path.pack(side="left", fill="x", expand=True, ipady=4, padx=5, pady=5)

btn_path = Button(path_frame, text="Find Path", width=10, command=browse_path)
btn_path.pack(side="right", padx=5, pady=5)


# div4

frame_option = LabelFrame(root, text="Option")
frame_option.pack(padx=5, pady=5)


# image width option

lbl_width = Label(frame_option, text="Width", width=8)
lbl_width.pack(side="left", padx=5, pady=5)

opt_width = ["Original", "1024", "800", "640"]
cmb_width = ttk.Combobox(frame_option, state="readonly", values=opt_width, width=10)
cmb_width.current(0)
cmb_width.pack(side="left", padx=5, pady=5)


# space option

lbl_space = Label(frame_option, text="Space", width=8)
lbl_space.pack(side="left", padx=5, pady=5)

opt_space = ["None", "Narrow", "Normal", "Wide"]
cmb_space = ttk.Combobox(frame_option, state="readonly", values=opt_space, width=10)
cmb_space.current(0)
cmb_space.pack(side="left", padx=5, pady=5)


# format option

lbl_format = Label(frame_option, text="Format", width=8)
lbl_format.pack(side="left", padx=5, pady=5)

opt_format = ["PNG", "JPG", "BMP"]
cmb_format = ttk.Combobox(frame_option, state="readonly", values=opt_format, width=10)
cmb_format.current(0)
cmb_format.pack(side="left", padx=5, pady=5)


# progress bar
progress_frame = LabelFrame(root, text="Progress")
progress_frame.pack(fill="both", padx=5, pady=5)

p_var = DoubleVar()
progressbar = ttk.Progressbar(progress_frame, maximum=100, variable=p_var)
progressbar.pack(fill="both", padx=5, pady=5)


# run frame
run_frame = Frame(root)
run_frame.pack(fill="both", padx=5, pady=5)

btn_start = Button(run_frame, pady=5, padx=5, text="Start", width=10, command=start)
btn_start.pack(side="left", padx=5, pady=5)

btn_close = Button(run_frame, pady=5, padx=5, text="Close", width=10, command=root.quit)
btn_close.pack(side="right", padx=5, pady=5)


def screenshot():
    cur_time = time.strftime("_%m%d%Y_%H%M%S")
    img = ImageGrab.grab()  # screenshot
    img.save("image{}.png".format(cur_time))

keyboard.add_hotkey("`", screenshot)

root.resizable(False, False)
root.mainloop()

