from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives import serialization
import argparse


parser = argparse.ArgumentParser()
parser.add_argument("-g", "--gen_key", action="store_true",
                    help="Generate pub and prive rsa key")

parser.add_argument("-e", "--encrypt", action="store_true",
                    help="Encrypt plain text")

parser.add_argument("-d", "--decrypt", action="store_true",
                    help="Decrypt encrypted text")


args = parser.parse_args()
if args.gen_key:
    print("Generate key")
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
    )


# pem_priv = private_key.private_bytes(
#    encoding=serialization.Encoding.PEM,
#    format=serialization.PrivateFormat.PKCS8,
#    encryption_algorithm=serialization.BestAvailableEncryption(b'mypassword')
# )

    pem_priv = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.TraditionalOpenSSL,
        encryption_algorithm=serialization.NoEncryption()
    )
    with open("prive.pem", "wb") as file:
        file.write(pem_priv)

    public_key = private_key.public_key()
    pem_pub = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )
    with open("pub.pem", "wb") as file:
        file.write(pem_pub)


if args.encrypt:
    print("Encrypt message")
    with open("message.txt", "rb") as file:
        message = file.read()

    with open("pub.pem", "rb") as key_file:
        load_public_key = serialization.load_pem_public_key(key_file.read())
    #message = b"encrypted data"
    ciphertext = load_public_key.encrypt(
        message,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    with open("encrypted.txt", "wb") as file:
        file.write(ciphertext)

if args.decrypt:
    print("Decrypt message")
    with open("encrypted.txt", "rb") as file:
        ciphertext = file.read()
    with open("prive.pem", "rb") as key_file:
        load_private_key = serialization.load_pem_private_key(
            key_file.read(),
            password=None,
        )
    plaintext = load_private_key.decrypt(
        ciphertext,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    print(plaintext)


# if plaintext == message:
#    print("ok")
#    print(plaintext)
#    print(ciphertext)
