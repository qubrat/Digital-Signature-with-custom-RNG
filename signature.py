# pip install pycryptodome imageio streamlink tk m3u8 urllib3 wave numpy opencv-python moviepy

from tkinter import *
from tkinter import filedialog

from Crypto import Hash
from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA
from Crypto.PublicKey.RSA import RsaKey
from Crypto.Signature import pkcs1_15

import randomsource

window = Tk()
window.title("Digital signature")

filepath = ""
path_label = ""
status_label = ""
status_value = ""
sign_button = ""
generate_keys_button = ""
verify_button = ""
hash_object: Hash
signature: bytes
key: RsaKey


def open_file():
    global filepath
    filepath = filedialog.askopenfilename(title="Choose file")

    try:
        hash_text = hash_file(filepath).hexdigest()
        path_label["text"] = filepath

        # Update status bar
        status_label["fg"] = "black"
        status_label["text"] = "SHA-256 hash of chosen file:"
        status_value["text"] = hash_text

        # Update buttons availability
        generate_keys_button["state"] = "normal"

    except FileNotFoundError:
        print("Error: no file selected.")
        status_label["text"] = "Error: no file selected."
        status_label["fg"] = "#bc1c1c"
        status_value["text"] = ""
        path_label["text"] = "Please, select a file."


def hash_file(file):
    global hash_object
    hash_object = SHA256.new()

    with open(file, "rb") as file:
        chunk = 0
        while chunk != b"":
            chunk = file.read(1024)
            hash_object.update(chunk)

    return hash_object


def generate_keys():
    # Check if file chosen
    global key
    if filepath == "None" or filepath == "":
        status_label["text"] = "Error: no file selected."
        status_label["fg"] = "#bc1c1c"
    else:
        # Update labels
        status_label["fg"] = "black"
        status_label["text"] = "Generating RSA key pair..."
        status_value["text"] = ""
        # try:
        status_label["fg"] = "black"

        random_data = randomsource.Source()
        key = RSA.generate(2048, random_data.execute)
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
        print("You can sign a file now.")
        # Update buttons availability
        sign_button["state"] = "normal"

        # except TypeError:
        #     print("Key generation failed, sorry, shit happens. Try again.")
        #     status_label["text"] = "Key generation failed, sorry, shit happens. Try again."


def sign_file():
    # Check if file chosen
    if filepath == "None" or filepath == "":
        print("Error: no file selected.")
        status_label["text"] = "Error: no file selected."
        status_label["fg"] = "#bc1c1c"
    else:
        global hash_object
        global signature
        status_label["fg"] = "black"
        print("Signing file...")
        status_label["text"] = "Signing file..."
        private_key = RSA.importKey(open("private.pem").read())
        signer = pkcs1_15.new(private_key)
        signature = signer.sign(hash_object)

        print("Signed.")
        status_label["text"] = "Signed."
        verify_button["state"] = "normal"


def verify_file():
    global filepath
    filepath = filedialog.askopenfilename(title="Choose file")
    # Check if file chosen
    if filepath == "None" or filepath == "":
        print("Error: no file selected.")
        status_label["text"] = "Error: no file selected."
        status_label["fg"] = "#bc1c1c"
    else:
        status_label["fg"] = "black"
        hash_object_to_verification = hash_file(filepath)
        hash_text = hash_object_to_verification.hexdigest()

        # Update filepath label
        path_label["text"] = filepath
        # Update status bar
        status_label["text"] = "SHA-256 hash of file chosen to verification:"
        status_value["text"] = hash_text
        print("Verifying file...")
        status_label["text"] = "Verifying file..."
        # Get public key stored previously and initiate verifier using this key
        public_key = RSA.importKey(open("public.pem").read())
        verifier = pkcs1_15.new(public_key)
        try:
            verifier.verify(hash_object_to_verification, signature)
            print("Verified. All good my dude.")
            status_label["text"] = "Verified. All good my dude."
            status_label["fg"] = "#006300"

        except ValueError:
            print("Signature is not valid.")
            status_label["text"] = "Signature is not valid."
            status_label["fg"] = "#bc1c1c"


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
    sign_frame = LabelFrame(window, text="Signing a file", padx=5, pady=5)
    choose_file_button = Button(sign_frame, command=open_file, text="Select a file", width=30, bg="#bee3fe", borderwidth=1)
    sign_button = Button(sign_frame, command=sign_file, text="Sign chosen file", width=30, bg="#bcfecb", borderwidth=1,
                         state="disabled")
    choose_file_button.grid(row=0, column=0, ipady=5)
    sign_button.grid(row=0, column=1, ipady=5)

    verify_frame = LabelFrame(window, text="Verifying signature", padx=5, pady=5)
    choose_signature_button = Button(verify_frame, command=open_file, text="Select a signature", width=30, bg="#bee3fe", borderwidth=1)
    verify_button = Button(verify_frame, command=verify_file, text="Verify a signature", width=30, bg="#ffdfba",
                           borderwidth=1, state="disabled")
    choose_signature_button.grid(row=0, column=0, ipady=5)
    verify_button.grid(row=0, column=1, ipady=5)

    sign_frame.grid(row=2, pady=10, padx=20)
    verify_frame.grid(row=3, pady=10, padx=20)

    # Status bar
    status_label = Label(window, text="Perform an action my dude,", anchor=E, bg="#cfcfcf")
    status_label.grid(row=4, column=0, columnspan=2, ipady=2, sticky=W + E)
    status_value = Label(window, text="I'm waiting", anchor=E, bg="#cfcfcf")
    status_value.grid(row=5, column=0, columnspan=2, ipady=2, sticky=W + E)

    window.mainloop()


if __name__ == "__main__":
    main()
