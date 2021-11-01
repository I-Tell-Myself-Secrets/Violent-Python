import argparse
from pexpect import pxssh
class Client:
    def __init__(self,host,user,password):
        self.host = host
        self.user = user
        self.password = password
        self.session = self.connect()
    def connect(self):
        try:
            s = pxssh.pxssh()
            s.login(self.host,self.user,self.password)
            return s
        except Exception as e:
            print(e)
            print("[-] Error connecting!")
    def send_command(self,cmd):
        self.session.sendline(cmd)
        if str(cmd).__contains__("sudo"):
            self.session.sendline(self.password)
        self.session.prompt()
        return self.session.before
def botnetCommand(command):
    for client in botNet:
        output = client.send_command(str(command))
        print("[*] Output from " + client.host)
        print("[+] "+str(output))
def addClient(host,user,password):
    client = Client(host,user,password)
    botNet.append(client)
botNet = []
#addClient("127.0.0.1", "root", "toor")
#addClient("10.10.10.130", "root", "toor")
botnetCommand("uname -v")
botnetCommand("sudo cat /etc/issue")
