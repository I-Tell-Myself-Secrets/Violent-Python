import nmap
import argparse

def nmapScan(tgtHost, tgtPort):
    nmScan = nmap.PortScanner()
    nmScan.scan(tgtHost,tgtPort)
    state = nmScan[tgtHost]["tcp"][int(tgtPort)]["state"]
    print("[*] {a} tcp/{b} {c}".format(a = tgtHost, b = tgtPort, c = state))
def main():
    parser = argparse.ArgumentParser("usage%prog -H <target host> -p <target port>")
    parser.add_argument("-H", dest="tgtHost", type=str, help="specify target host")
    parser.add_argument("-p",dest="tgtPort",type=str,help="specify target port")
    args = parser.parse_args()
    tgtHost = args.tgtHost
    tgtPort = str(args.tgtPort)
    if (tgtHost == None) | (tgtPort == None):
        print(parser.usage)
        exit(0)
    for port in tgtPort:
        nmapScan(tgtHost,port)
if __name__ == "__main__":
    main()
