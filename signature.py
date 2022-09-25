# pip install pycryptodome imageio streamlink tk m3u8 urllib3 wave numpy opencv-python moviepy

from tkinter import *
from tkinter import filedialog
from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA
from Crypto.Signature import pkcs1_15
import TRNG
import data_creator
import video_processor
from os import remove

window = Tk()
window.title("Digital signature")

filepath = ""
path_label = ""
status_label = ""
status_value = ""
sign_button = ""
generate_keys_button = ""
verify_button = ""
signature: bytes
sign: bytes


def printGreen(text): print("\033[92m{}\033[00m".format(text))


def printYellow(text): print("\033[93m{}\033[00m".format(text))


def printRed(text): print("\033[91m{}\033[00m".format(text))


def printCyan(text): print("\033[95m{}\033[00m".format(text))


# ------------------OPENING FILE------------------

def open_file():
    global filepath
    filepath = filedialog.askopenfilename(title="Choose file")
    printYellow("Selected file:")
    print(filepath)

    try:
        path_label["text"] = filepath
        # Update buttons availability
        sign_button["state"] = "normal"

    except FileNotFoundError:
        printRed("Error: no file selected.")
        status_label["text"] = "Error: no file selected."
        status_label["fg"] = "#bc1c1c"
        status_value["text"] = ""
        path_label["text"] = "Please, select a file."

    except TypeError:
        printRed("Error: no file selected.")
        status_label["text"] = "Error: no file selected."
        status_label["fg"] = "#bc1c1c"
        status_value["text"] = ""
        path_label["text"] = "Please, select a file."


def hash_file(file):
    hash_object = SHA256.new()

    with open(file, "rb") as file:
        chunk = 0
        while chunk != b"":
            chunk = file.read(1024)
            hash_object.update(chunk)

    return hash_object


# ------------------SIGNING FILE------------------

def sign_file(if_online):
    # Check if file chosen
    if filepath == "None" or filepath == "":
        printRed("Error: no file selected.")
        status_label["text"] = "Error: no file selected."
        status_label["fg"] = "#bc1c1c"
    else:
        global signature

        try:
            printCyan("Signing file...")
            status_label["text"] = "Signing file..."
            status_label["fg"] = "black"

            generate_keys(if_online)
            private_key = RSA.importKey(open("private.pem").read())
            signer = pkcs1_15.new(private_key)
            signature = signer.sign(hash_file(filepath))

            with open("signature.pem", "wb") as file_out:
                file_out.write(signature)

        except InterruptedError:
            printRed("No video file selected!")
            printYellow("    Please select a file when file selection window shows up.")


def generate_keys(online_video):
    # Check if file chosen
    if filepath == "None" or filepath == "":
        status_label["text"] = "Error: no file selected."
        status_label["fg"] = "#bc1c1c"
    else:
        # Update labels
        status_label["fg"] = "black"
        status_label["text"] = "Generating RSA key pair..."
        status_value["text"] = ""
        try:
            status_label["fg"] = "black"
            if online_video.get() == 1:
                file = video_processor.get_video()
                data = TRNG.trng_algorithm(file, 1)
                random_bytes = data_creator.DataCreator(data)
                key = RSA.generate(2048, random_bytes.execute)
                export_keys(key)
                printGreen("Signed.")
                status_label["text"] = "Signed."
            else:
                file = filedialog.askopenfilename(title="Choose video file")
                data = TRNG.trng_algorithm(file)
                random_bytes = data_creator.DataCreator(data)
                key = RSA.generate(2048, random_bytes.execute)
                export_keys(key)
                printGreen("File signed. Signature has been saved in 'signature.pem' file.")
                status_label["text"] = "File signed. Signature has been saved in 'signature.pem' file."

        except OSError:
            printRed("Error: no video file selected.")
            printYellow("    Please, select a video file to generate keys!")
            status_label["text"] = "Error: no video file selected."
            status_label["fg"] = "#bc1c1c"
            status_value["text"] = "Please, select a video file to generate keys!"

        except AttributeError:
            printYellow("Key generation failed, no video file selected.")
            status_label["text"] = "Key generation failed, no video file selected."

        except TypeError:
            if online_video.get() == 1:
                remove(filepath)
            printYellow("Key generation failed.")
            printYellow("Try again.")
            status_label["text"] = "Key generation failed. Try again."


def export_keys(key):
    # Generate private key
    printCyan("Exporting private key...")
    private_key = key.export_key()
    with open("private.pem", "wb") as file_out:
        file_out.write(private_key)
    printGreen("Done.")

    # Generate public key
    printCyan("Exporting public key...")
    public_key = key.public_key().export_key()
    with open("public.pem", "wb") as file_out:
        file_out.write(public_key)
    printGreen("Done.")

    # Update labels
    status_label["text"] = "Generated RSA key pair."
    status_value["text"] = ""
    print("Generated RSA key pair.")


# ------------------VERIFYING SIGNATURE------------------

def select_signature_file():
    global filepath
    filepath = filedialog.askopenfilename(title="Choose signature file.")
    if filepath == "None" or filepath == "":
        printRed("Error: no file selected.")
        status_label["text"] = "Error: no file selected."
        status_label["fg"] = "#bc1c1c"
    else:
        path_label["text"] = filepath
        status_label["fg"] = "black"
        status_label["text"] = "Selected signature file:"
        status_value["text"] = filepath
        verify_button["state"] = "normal"
        printYellow("Selected signature file:")
        print(filepath)

        global sign
        signature_f = open(filepath, "rb")
        sign = signature_f.read()
        signature_f.close()


def verify_file():
    global filepath
    filepath = filedialog.askopenfilename(title="Choose file for verification")
    # Check if file chosen
    if filepath == "None" or filepath == "":
        printRed("Error: no file selected.")
        status_label["text"] = "Error: no file selected."
        status_label["fg"] = "#bc1c1c"
    else:
        hash_object_to_verification = hash_file(filepath)
        hash_text = hash_object_to_verification.hexdigest()

        # Update filepath label
        path_label["text"] = filepath
        # Update status bar
        status_label["text"] = "SHA-256 hash of file chosen to verification:"
        status_value["text"] = hash_text
        printCyan("Verifying file...")
        status_label["text"] = "Verifying file..."
        # Get public key stored previously and initiate verifier using this key
        public_key = RSA.importKey(open("public.pem").read())
        verifier = pkcs1_15.new(public_key)
        try:
            global sign
            verifier.verify(hash_object_to_verification, sign)
            printGreen("Verified. All good my dude.")
            status_label["text"] = "Verified. All good my dude."
            status_label["fg"] = "#006300"
            status_value["text"] = ""

        except ValueError:
            printRed("Signature is not valid.")
            status_label["text"] = "Signature is not valid."
            status_label["fg"] = "#bc1c1c"
            status_value["text"] = ""


# ------------------MAIN LOOP------------------

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

    # Sign frame
    sign_frame = LabelFrame(window, text="Signing a file", padx=5, pady=5)

    choose_file_button = Button(sign_frame, command=open_file, text="Select a file to sign", width=30, bg="#bee3fe",
                                borderwidth=1)
    sign_button = Button(sign_frame, command=lambda: sign_file(if_online_video), text="Sign chosen file", width=30,
                         bg="#bcfecb", borderwidth=1, state="disabled")

    if_online_video = IntVar()
    checkbox = Checkbutton(sign_frame, text="I want to use external video stream\n(takes longer to generate  keys)",
                           variable=if_online_video, onvalue=1,
                           offvalue=0)
    checkbox.deselect()

    choose_file_button.grid(row=0, column=0, ipady=5)
    sign_button.grid(row=0, column=1, ipady=5)
    checkbox.grid(row=1, columnspan=2, pady=3)

    # Verify frame
    verify_frame = LabelFrame(window, text="Verifying signature", padx=5, pady=5)
    choose_signature_button = Button(verify_frame, command=select_signature_file, text="Select a signature file",
                                     width=30,
                                     bg="#bee3fe", borderwidth=1)
    verify_button = Button(verify_frame, command=verify_file, text="Verify a signature", width=30, bg="#ffdfba",
                           borderwidth=1, state="disabled")
    choose_signature_button.grid(row=0, column=0, ipady=5)
    verify_button.grid(row=0, column=1, ipady=5)

    # Set frames
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
