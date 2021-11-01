import argparse
import socket
from threading import Thread
from threading import Semaphore

screenlock = Semaphore(value = 1)
def connScan(tgtHost,tgtPort):
    try:
        connSkt = socket.socket(AF_INET, SOCK_STREAM)
        connSkt.connect((tgtHost, tgtPort))
        connSkt.send("ViolentPython\n")
        results = connSkt.recv(100)
        screenlock.acquire()
        print("[+] TCP open {r}".format(r = tgtPort))
        print("[+] {r}".format(r = results))
        connSkt.close()
    except:
        screenlock.acquire()
        print("[-] TCP close {r}".format(r = tgtPort))
    finally:
        screenlock.release()
def portScan(tgtHost, tgtPorts):
    try:
        tgtIP = socket.gethostbyname(tgtHost)
        print(tgtIP)
    except:
        print("[-] Cannot resolve {r}. Unknown host".format(r = tgtHost))
        return
    try:
        tgtName = socket.gethostbyaddr(tgtIP)
        print("Scan results for {a}".format(a = tgtName[0]))
    except:
        print("Scan results for {a}".format(a = tgtIP))
    socket.setdefaulttimeout(1)
    for tgtPort in tgtPorts:
        print("Scanning port {r}".format(r = tgtPort))
        #connScan(tgtHost, int(tgtPort))
        t = Thread(target = connScan, args=(tgtHost, int(tgtPort)))
        t.start()
def main():
    parser = argparse.ArgumentParser("usage %prog -H <target host> -p <target port>")
    parser.add_argument("-H", dest = "tgtHost", type = str, help = "specify target host")
    parser.add_argument("-p", dest = "tgtPort", type = str, help = "specify target port")
    args = parser.parse_args()
    tgtHost = args.tgtHost
    tgtPorts = str(args.tgtPort).split(",")
    if (tgtHost == None) | (tgtPorts[0] == None):
        print(parser.usage)
        exit(0)
    portScan(tgtHost,tgtPorts)
if __name__ == "__main__":
    main()