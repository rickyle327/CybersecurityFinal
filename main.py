import string
import secrets
import cryptography
from cryptography.fernet import Fernet


# Random generates a password of length n with letters, numbers and symbols.
def passwordgenerator(n=100):
    return ''.join(secrets.choice(string.ascii_letters + string.digits + string.punctuation) for _ in range(n))


# Creates a key which we can use to encrypt/decrypt
def makekey():
    key = Fernet.generate_key()
    return key;


# Writes a generated key to a file called key.key
def writekey():
    file = open('key.key', 'wb')
    file.write(makekey())
    file.close()


# Reads written key from key.key
def readkey():
    file = open('key.key', 'rb')
    key = file.read()
    file.close()
    return key


# First encodes a random genned password, and then encrypts with the key written to key.key
def encryptpassword():
    message = passwordgenerator(10).encode()
    print(message)
    f = Fernet(readkey())
    encrypted = f.encrypt(message)
    return encrypted


# First decrypts the file based on the key written to key.key, then decodes to get original password.
def decryptpassword(encryptedpassword = ""):
    f = Fernet(readkey())
    decrypted = f.decrypt(encryptedpassword).decode()
    print(decrypted)
    return decrypted


def main():
    decryptpassword(encryptpassword())


if __name__ == '__main__':
    main()