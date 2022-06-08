# Signing file and verifying signature using RSA encrypting with asymmetric keys

This program allows selecting any file from your system and perform digital signing and it's verification. \
First, file has to be chosen. Right after opening, a hash is found. \
This enables button `Generate RSA key pair`, which generates `private.pem` and `public.pem` files. Make sure not to modify them. \
After keys are generated, a signing operation can be performed. Program uses hash of previously selected file
and private key from `private.pem` file.
