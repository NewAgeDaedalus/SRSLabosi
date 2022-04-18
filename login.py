import os
from sys import argv
from utils import *
from pathlib import Path
from Crypto.Protocol.KDF import scrypt
from Crypto.Hash import HMAC, SHA256
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes


path = os.path.expanduser('~')+'/.Usermgmt/data'
userPasswToChangePath = os.path.expanduser('~')+'/.Usermgmt/change'

def toChange(username:str):
     with open(userPasswToChangePath, 'r') as file:
        line = file.readline()
        while line != "":
            if line[:-1] == username:
                return True
            line = file.readline()

def removeFromChange(username):
    with open(userPasswToChangePath,'r') as fileR:
        lines = fileR.readlines()
        with open(userPasswToChangePath, 'w') as fileW:
            for line in lines:
                if line[:-1] != username:
                    fileW.write(line)

def changePasswd(username:str):
    if not checkIfAlreadyExists(username, path):
        exit("%s does not exist" % username)
    newPassword = makePassword()
    salt = get_random_bytes(100)
    key = scrypt(newPassword, salt, 32, 2**14, 8,1,1)
    cipher = HMAC.new(key, digestmod=SHA256)
    cipher.update(newPassword.encode('utf-8','ignore'))
    tag = cipher.hexdigest()
    with open(path, 'r') as fileR:
        lines = fileR.readlines()
        with open(path,"w") as fileW:
            i = 0
            while lines[i][:-1] != username:
                fileW.write(lines[i])
                i+=1
            fileW.write(username+"\n")
            fileW.write(salt.hex()+'\n')
            fileW.write(tag+'\n')
            i+=3
            for line in lines[i:]:
                fileW.write(line)

def main():
    try:
        username = argv[1]
    except(IndexError):
        exit("No username given")
    print("Hello %s!" % username)
    password = getpass("Password:")
    salt = ""
    origTag = ""
    usernameDoesNotExist = True
    with open(path, 'r') as file:
        lines = file.readlines()
        for i in range(0, len(lines), 2):
            if lines[i][:-1] == username:
                salt = bytes.fromhex(lines[i+1])
                origTag = bytes.fromhex(lines[i+2])
                usernameDoesNotExist = False
    key = scrypt(password, salt, 32,2**14,8,1,1) 
    cipher = HMAC.new(key,digestmod=SHA256)
    cipher.update(password.encode('utf-8', 'ignore'))
    tag = cipher.digest()
    if tag == origTag:
        #Na cudnom je mjestu ova provjera tako
        #za zastitu od timing attacka
        if usernameDoesNotExist:
            exit("Failed Login")
        print("Succecsfull login")
        if toChange(username):
            print("The admin wants you to change your password")
            print("Please enter a new password")
            changePasswd(username)
            removeFromChange(username)
    else:
        exit("Failed login")

if __name__ == "__main__":
    main()
