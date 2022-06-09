# Signing file and verifying signature using RSA encrypting with asymmetric keys

This program allows selecting any file from your system and perform digital signing and it's verification. \
First, file has to be chosen. Right after opening, a hash is found using SHA-256 hashing.

This enables button `Generate RSA key pair`, which generates `private.pem` and `public.pem` files. Make sure not to modify them. 
The source of randomness is a YouTube 24/7 livestream found at [link](https://www.youtube.com/watch?v=h3MuIUNCCzI). 
During execution a part of transport stream is downloaded as `live_chunk.mp4`, a `.wav` 
file is created from it as well and saved as `audio.wav` and then processed. 
After processing files are removed. 

After keys are generated, a signing operation can be performed. Program uses hash of previously selected file
and private key from `private.pem` file. 

To verify file, use `Verify a signature` button. Window will open asking you to select a file.
SHA-256 hash of given file is found and verification is performed using public key stored in `public.pem`.  

# Basic setup instructions
Note: It is highly recommended to run program in virtual environment to ensure proper functioning. But you can also follow
steps below.

Using terminal:

1. Install required packages using `pip3`:
```
pip3 install pycryptodome imageio streamlink tk m3u8 urllib3 wave numpy opencv-python moviepy
```
2. Navigate to folder with cloned repository.
3. Run program:
```
py signature.py
```
# Setup in virtual environment
Running program inside virtual environment ensures that it does not mess your other python packages.
If you want to run the program inside virtual environment follow these steps:
1. Make sure virtualenv is installed. If not use:
```
py -m pip install --user virtualenv
```
2. Create virtual environment:
```
py -m venv <venv location and name>
```
3. Activate the venv:
```
.\path\to\venv\Scripts\activate
```
4. You can confirm you’re in the virtual environment by checking the location of your Python interpreter:
```
where python
```

5. Install required packages using `pip3`:
```
pip3 install pycryptodome imageio streamlink tk m3u8 urllib3 wave numpy opencv-python moviepy
```
If you encounter problem with permission of some packages, try running above command with `--no-cache-dir` option.

6. Run program:
- Use terminal:
```
py signature.py
```
- Or simply double-click on `signature.py`.

If you want to switch projects or otherwise leave your virtual environment, simply run:
```
deactivate
```

More about virtual environments can be found [here](https://packaging.python.org/en/latest/guides/installing-using-pip-and-virtual-environments/).

# Sample images:
![image1](https://github.com/qubrat/DS_verifier_Custom_RNG/blob/d28c2e5f461e2f464e4746a489f9b6ad207fbb41/images/signature.png)

![image2](https://github.com/qubrat/DS_verifier_Custom_RNG/blob/d28c2e5f461e2f464e4746a489f9b6ad207fbb41/images/signature1.png)
