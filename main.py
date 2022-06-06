import hashlib
import os

import randomsource
from tkinter import *
from tkinter import filedialog

window = Tk()
window.title("File encryption")

filepath = "None"
path_label = ''
status_label = ''
status_value = ''


def open_file():
    global filepath
    global path_label
    global status_label
    global status_value
    filepath = filedialog.askopenfilename(title="Choose file")

    h = hashlib.sha3_256()

    with open(filepath, 'rb') as file:
        chunk = 0
        while chunk != b'':
            chunk = file.read(1024)
            h.update(chunk)

    hash_text = str(h.hexdigest())

    # Update filepath label
    path_label = Label(window, text=filepath, width=40)
    path_label.grid(row=1, columnspan=3, ipady=5)

    # Update status bar
    status_label = Label(window, text="Hashcode of  chosen file: ", anchor=E, bg="#cfcfcf")
    status_label.grid(row=3, column=0, columnspan=3, ipady=2, sticky=W + E)

    status_value = Label(window, text=hash_text, anchor=E, bg="#cfcfcf")
    status_value.grid(row=4, column=0, columnspan=3, ipady=2, sticky=W + E)

    randomsource.execute()


def main():
    # noinspection PyTypeChecker
    # Labels
    global filepath
    global path_label
    global status_label
    global status_value

    chosen_label = Label(window, text="Chosen file:", width=40)
    chosen_label.grid(row=0, columnspan=3, ipady=5)

    path_label = Label(window, text=filepath, width=40)
    path_label.grid(row=1, columnspan=3, ipady=5)

    # Buttons
    choose_file_button = Button(window, command=open_file, text="Choose a file", width=20, bg="#bee3fe", borderwidth=0)
    encrypt_button = Button(window, text="Encrypt chosen file", width=20, bg="#bcfecb", borderwidth=0)
    decrypt_button = Button(window, text="Decrypt chosen file", width=20, bg="#ffdfba", borderwidth=0)
    choose_file_button.grid(row=2, column=0, ipady=4)
    encrypt_button.grid(row=2, column=1, ipady=4)
    decrypt_button.grid(row=2, column=2, ipady=4)

    # Status bar
    status_label = Label(window, text="Perform an action my dude,", anchor=E, bg="#cfcfcf")
    status_label.grid(row=3, column=0, columnspan=3, ipady=2, sticky=W + E)
    status_value = Label(window, text="I'm waiting", anchor=E, bg="#cfcfcf")
    status_value.grid(row=4, column=0, columnspan=3, ipady=2, sticky=W + E)

    window.mainloop()


if __name__ == "__main__":
    main()
