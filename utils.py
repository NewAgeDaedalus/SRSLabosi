from getpass import getpass
#
#password is not allowed to be shown in terminal
def makePassword():
    passwd = getpass("Password:")
    repeatPasswd = getpass("Repeat password:")
    if passwd != repeatPasswd:
        exit("Passwords mismatch")
    return passwd 

def checkIfAlreadyExists(username:str, path):
    with open(path, 'r') as file:
        while 1337:
            line = file.readline()
            if line == "":
                return False
            if line[:-1] == username:
                return True
            for i in range(2):
                if file.readline() == "":
                    return False
    return False 

