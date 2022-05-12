import os
from sys import argv
from utils import *
from pathlib import Path
from login import changePasswd
from Crypto.Protocol.KDF import scrypt
from Crypto.Hash import HMAC, SHA256
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
import argparse 

path = os.path.expanduser('~')+'/.Usermgmt/data'
userPasswToChangePath = os.path.expanduser('~')+'/.Usermgmt/change'

def add_user(username:str):
    if checkIfAlreadyExists(username, path):
        exit("Username %s already exists" % username);
    password = makePassword() 
    salt = get_random_bytes(100);
    key = scrypt(password, salt, 32, 2**14, 8,1,1)
    cipher = HMAC.new(key,digestmod=SHA256)
    cipher.update(password.encode('utf-8', 'ignore'))
    tag = cipher.hexdigest()
    with open(path, "a") as file:
        file.write(username +"\n")
        file.write(salt.hex()+"\n")
        file.write(tag+"\n")

def deleteUser(username:str):
    if not checkIfAlreadyExists(username, path):
        exit("Username %s doesn't exist" % username)
    with open(path, "r") as fileR:
        lines = fileR.readlines()
        with open (path, 'w') as  fileW:
            for i in range(0, len(lines), 3):
                line = lines[i]
                if line[:-1] == username:
                    continue
                fileW.write(lines[i])
                fileW.write(lines[i+1])
                fileW.write(lines[i+2])

def forcepass(username:str):
    if not checkIfAlreadyExists(username, path):
        exit("Username %s doesn't exist" % username)
    with open(userPasswToChangePath, "r") as file:
        line = file.readline()[:-1]
        while line != "":
            if line == username:
                exit("User already ordered to change passwd")
            line = file.readline()[:-1]
    with open(userPasswToChangePath, 'a') as file:
        file.write(username+"\n")
        

def main():
    parser = argparse.ArgumentParser();
    parser.add_argument("--passwd", metavar = "changePasswd")
    parser.add_argument("--add", metavar = "add user")
    parser.add_argument("--delet",metavar ="delete user")
    parser.add_argument("--forcepass", metavar = "force user to change password")
    akcije = parser.parse_args()
    if akcije.add != None:
        add_user(akcije.add)
    elif akcije.passwd != None:
        changePasswd(akcije.passwd)
    elif akcije.delet != None:
        deleteUser(akcije.delet)
    elif akcije.forcepass != None:
        forcepass(akcije.forcepass)
    return 0;

if __name__ == "__main__":
    main()
