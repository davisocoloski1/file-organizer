from platform import win32_edition
from time import sleep
from tkinter.ttk import Progressbar
from tkinter import Button, Label, Entry, Tk, Frame
from tkinter.ttk import Progressbar
from app import App

app = App()

root = Tk()
root.title("File Organizer")
root.update_idletasks()
root.minsize(width=300, height=150)

content = Frame(root, bd=10)
content.grid(column=0, row=0, sticky="nsew")
root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(0, weight=1)

# Labels
label = Label(content, text="File Organizer", font=("Arial", 12), anchor="center")
label.grid(column=1, row=0, columnspan=3, sticky="we", pady=5)

label2 = Label(content, text="Origin Directory: ", font=("Arial", 12))
label2.grid(column=0, row=1)

label3 = Label(content, text="Destination: ", font=("Arial", 12))
label3.grid(column=0, row=2)

# Progress Bar
progress_bar = Progressbar(content, length=100, mode="determinate")
progress_bar.grid(column=1, row=4, columnspan=2, sticky="we", pady=5)

# Inputs
moving_to_label = Entry(content, bd=2, width=20, font=("Arial", 12), state="disabled", cursor="arrow")
moving_to_label.grid(column=1, row=2, sticky="we", pady=5)

input_dir = Entry(content, bd=2, width=20, font=("Arial", 12))
input_dir.grid(column=1, row=1, sticky="w")
input_dir.focus_set()

# Buttons
find_dir_button = Button(content, text="Search", command=lambda: app.open_file_dialog(input_dir))
find_dir_button.grid(column=2, row=1, padx=5, sticky="we")

select_new_dir = Button(content, text="Move to", command=lambda: app.open_file_dialog(label=moving_to_label))
select_new_dir.grid(column=2, row=2, pady=5, padx=5, sticky="we")

organize_button = Button(content, text="Organize Files", width=20, command=lambda: app.organize_files(input_dir.get(), moving_to_label.get(), root, progress_bar))
organize_button.grid(column=1, row=3, sticky="we")

copy_path_button = Button(content, text="Copy Path", width=20, command=lambda: app.copy_path(input_dir.get()))
copy_path_button.grid(column=2, row=3, padx=5, sticky="we")

if __name__ == '__main__':
    root.mainloop()
