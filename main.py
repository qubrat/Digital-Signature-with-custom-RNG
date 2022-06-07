from typing import Any

from Crypto import Hash
from Crypto.Signature import pkcs1_15
from Crypto.Hash import SHA256
from tkinter import *
from tkinter import filedialog
from Crypto.PublicKey import RSA
import randomsource

window = Tk()
window.title("File encryption")

filepath = "None"
path_label = ""
status_label = ""
status_value = ""
sign_button = ""
generate_keys_button = ""
verify_button = ""
hash_object: Hash
signature: bytes


def open_file():
    global filepath
    filepath = filedialog.askopenfilename(title="Choose file")
    hash_text = str(hash_file(filepath).hexdigest())
    save_hash_text(hash_text, filepath)

    # Update filepath label
    path_label["text"] = filepath

    # Update status bar
    status_label["text"] = "Hashcode of chosen file:"
    status_value["text"] = hash_text

    # Update buttons availability
    generate_keys_button["state"] = "normal"


def hash_file(file):
    global hash_object
    hash_object = SHA256.new()

    with open(file, "rb") as file:
        chunk = 0
        while chunk != b"":
            chunk = file.read(1024)
            hash_object.update(chunk)

    return hash_object


def save_hash_text(hashcode, path):
    with open("hashcode.txt", "w") as file:
        file.write("This is file containing hashcode of file: " + path + ": \n")
        file.write(hashcode)
        file.write("\n\nSave this to verify if program is working correctly.\n")


def generate_keys():
    # Check if file chosen
    if filepath == "None" or filepath == "":
        status_label["text"] = "Error: no file selected."
    else:
        # Update labels
        status_label["text"] = "Generating RSA key pair..."
        status_value["text"] = ""
        key = RSA.generate(2048, randomsource.execute())

        # Generate private key
        print("Generating private key...")
        private_key = key.export_key()
        file_out = open("private.pem", "wb")
        file_out.write(private_key)
        file_out.close()
        print("Done.")
        # Generate public key
        print("Generating public key...")
        public_key = key.public_key().export_key()
        file_out = open("public.pem", "wb")
        file_out.write(public_key)
        file_out.close()
        # Update labels
        status_label["text"] = "Generated RSA key pair."
        status_value["text"] = ""
        print("Done.")
        # Update buttons availability
        sign_button["state"] = "normal"


def sign_file():
    # Check if file chosen
    if filepath == "None" or filepath == "":
        status_label["text"] = "Error: no file selected."
    else:
        global hash_object
        global signature
        status_label["text"] = "Signing file..."
        private_key = RSA.importKey(open("private.pem").read())
        signer = pkcs1_15.new(private_key)
        signature = signer.sign(hash_object)

        status_label["text"] = "Signed."
        verify_button["state"] = "normal"


def verify_file():
    # Check if file chosen
    if filepath == "None" or filepath == "":
        status_label["text"] = "Error: no file selected."
    else:
        global hash_object
        global signature
        status_label["text"] = "Signing file..."
        public_key = RSA.importKey(open("public.pem").read())
        verifier = pkcs1_15.new(public_key)
        verifier.verify(hash_object, signature)

        status_label["text"] = "Verified."


def main():
    # Labels
    global filepath
    global path_label
    global status_label
    global status_value
    global generate_keys_button
    global sign_button
    global verify_button

    chosen_label = Label(window, text="Chosen file:", width=60)
    chosen_label.grid(row=0, columnspan=2, ipady=5)

    path_label = Label(window, text=filepath, width=60)
    path_label.grid(row=1, columnspan=2, ipady=5)

    # Buttons
    choose_file_button = Button(window, command=open_file, text="Choose a file", width=30, bg="#bee3fe", borderwidth=1)
    generate_keys_button = Button(window, command=generate_keys, text="Generate RSA keys", width=30, bg="#bee3fe",
                                  borderwidth=1, state="disabled")
    sign_button = Button(window, command=sign_file, text="Sign chosen file", width=30, bg="#bcfecb", borderwidth=1,
                         state="disabled")
    verify_button = Button(window, command=verify_file, text="Verify a signature", width=30, bg="#ffdfba", borderwidth=1, state="disabled")
    choose_file_button.grid(row=2, column=0, ipady=4)
    generate_keys_button.grid(row=2, column=1, ipady=4)
    sign_button.grid(row=3, column=0, ipady=4)
    verify_button.grid(row=3, column=1, ipady=4)

    # Status bar
    status_label = Label(window, text="Perform an action my dude,", anchor=E, bg="#cfcfcf")
    status_label.grid(row=4, column=0, columnspan=2, ipady=2, sticky=W + E)
    status_value = Label(window, text="I'm waiting", anchor=E, bg="#cfcfcf")
    status_value.grid(row=5, column=0, columnspan=2, ipady=2, sticky=W + E)

    window.mainloop()


if __name__ == "__main__":
    main()
