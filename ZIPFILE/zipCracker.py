import zipfile
from threading import Thread
import argparse
#Run 1
"""
zFile = zipfile.ZipFile("EV.zip")
zFile.extractall(pwd="secret")
"""

#Run 2
"""
zFile = zipfile.ZipFile("EV.zip")
try:
    zFile.extractall(pwd="secret")
except Exception, e:
    print e
"""

#Run 3
"""
zFile = zipfile.ZipFile("EV.zip")
passFile = open("Dictionary.zip")
for p in passFile.readlines():
    password = p.strip("\n")
    try:
        zFile.extractall(pwd=password)
        print("[+] Password = {r}".format(r = password))
        exit(0)
    except Exception, e:
        pass
"""

#Run 4
"""
def extractFile(zFile,password):
    try:
        zFile.extractall(pwd=password)
        return password
    except:
        return
def main():
    zFile = zipfile.ZipFile("EV.zip")
    passFile = open("Dictionary.txt")
    for line in passFile.readlines():
        password = line.strip("\n")
        guess = extractFile(zFile,password)
        if guess:
            print("[+] Password = {r}".format(r = guess))
            break
if __name__ == "__main__":
    main()
"""

#Run 5 (Multi Threading)
"""
def extractFile(zFile, password):
    try:
        zFile.extractall(pwd= password)
        print("[+] Password = {r}".format(r = password))
    except:
        pass
def main():
    zFile = zipfile.ZipFile("EV.zip")
    passFile = open("Dictionary.txt")
    for p in passFile.readlines():
        password = p.strip("\n")
        t = Thread(target = extractFile, args =(zFile,password))
        t.start()
if __name__ == "__main__":
    main()
"""

#Run 6

def extractFile(zFile,password):
    try:
        zFile.extractall(pwd=password)
        print("[+] Password = {r}".format(r = str(password, "utf-8")))
    except:
        pass
def main():
    parser = argparse.ArgumentParser("usage%prog -f <zipfile> -d <dictionary>")
    parser.add_argument('-f', dest = 'zname', type=str,help = 'specify zip file')
    parser.add_argument('-d', dest = 'dname', type=str,help = 'specify dictionary file')
    args = parser.parse_args()
    if (args.zname == None) | (args.dname == None):
        print(parser.usage)
        exit(0)
    else:
        zname = args.zname
        dname = args.dname
    zFile = zipfile.ZipFile(zname)
    passFile = open(dname)
    for line in passFile.readlines():
        password = bytes(line.strip("\n"), "utf-8")
        t = Thread(target=extractFile, args = (zFile, password))
        t.start()
if __name__ == "__main__":
    main()