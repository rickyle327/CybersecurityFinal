import string
import secrets
import cryptography
from cryptography.fernet import Fernet


def passwordgenerator(n=100):
    return ''.join(secrets.choice(string.ascii_letters + string.digits + string.punctuation) for _ in range(n))


def makekey():
    key = Fernet.generate_key()
    return key;


def writekey():
    file = open('key.key', 'wb')
    file.write(makekey())
    file.close()


def readkey():
    file = open('key.key', 'rb')
    key = file.read()
    print(key)
    file.close()
    return key


def main():
    print(passwordgenerator())
    readkey()


if __name__ == '__main__':
    main()