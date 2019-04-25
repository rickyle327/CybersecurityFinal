import string
import secrets
import cryptography
from cryptography.fernet import Fernet
from pymongo import MongoClient
from pprint import pprint

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
    plength = input("How long would you like the password to be? ")
    message = passwordgenerator(int(plength)).encode()
    f = Fernet(readkey())
    encrypted = f.encrypt(message)
    return encrypted


# First decrypts the file based on the key written to key.key, then decodes to get original password.
def decryptpassword(encryptedpassword = ""):
    f = Fernet(readkey())
    decrypted = f.decrypt(encryptedpassword).decode()
    return decrypted


# Connects to the MongoDB and returns the connection.
def connectdb():
    client = MongoClient("mongodb+srv://gabriel:Citrine0407@passwordmanager-biqpk.mongodb.net/test?retryWrites=true")
    db = client.passwordobjects
    return db


# Adds a website account to the database
def addaccount(db):
    websiteurl = input("Please enter the website url you have the account for: ")
    username = input("Please enter the username for the account: ")
    accountobject = {
        'websiteurl': websiteurl,
        'username': username,
        'password': encryptpassword()
    }
    # Check if user already made an account for this website
    if (db.account.find_one({'websiteurl': accountobject.get('websiteurl')})):
        print("An account for this website already exists.")
    else:
        result = db.account.insert_one(accountobject)


# Retrieves the password from the database based on website
def retrievepassword(db):
    websiteurl = input("Please enter the website url you want the password for: ")
    if (db.account.find_one({'websiteurl': websiteurl})):
        encodeddata = db.account.find_one({'websiteurl': "www.google.com"})
        presult = decryptpassword(encodeddata.get('password'))
        uresult = encodeddata.get('username')
        print("Your username is: " + uresult)
        print("Your password is: " + presult)
    else:
        print("Couldn't find an account for that website.")


def deleteaccount(db):
    websiteurl = input("Please enter the website url you want to delete the account for: ")
    if (db.account.delete_one({'websiteurl': websiteurl}).deleted_count != 0):
        print("Successfully deleted account for " + websiteurl)
    else:
        print("Could not find account for " + websiteurl)


def main():
    db = connectdb()
    print("Welcome to the password manager!")
    print("Manager supports the following commands:")
    print("addaccount - adds an account using a website url, a username, and a randomly generated password.")
    print("getpassword - will retrieve the password from the database for usage.")
    print("deleteaccount - will delete a saved account from the database.")
    print("quit - quits application.")
    while (1):
        choice = input("$: ")
        if (choice == "addaccount"):
            addaccount(db)
        elif (choice == "getpassword"):
            retrievepassword(db)
        elif (choice == "deleteaccount"):
            deleteaccount(db)
        elif (choice == "quit"):
            return
        else:
            print("Bad choice, please try again.")


if __name__ == '__main__':
    main()