import pexpect

PROMPT = ['# ', '>>> ', '> ', '\$ ']
def send_command(child, cmd):
    child.sendline(cmd)
    child.expect(PROMPT)
    print(child.before)
def connect(user, host, password):
    ssh_newkey = "Are you sure you wish to continue connecting"
    connStr = user + "@" + host
    child = pexpect.spawn("ssh " + connStr)
    ret = child.expect([pexpect.TIMEOUT, ssh_newkey,connStr + "'s password:"])
    if ret == 0:
        print("[-] Error connecting")
        return
    elif ret == 1:
        child.sendline("yes")
        ret = child.expect([pexpect.TIMEOUT, connStr + "'s password:"])
        if ret == 0:
            print("[--] Error Connecting")
            return
    child.sendline(password)
    child.expect(PROMPT)
    return child

def main():
    host = "127.0.0.1"
    user = ""
    password = ""
    child = connect(user,host,password)
    #Must have super user priviliges to execute what is below this line
    send_command(child, 'cat /etc/shadow | grep everchosen')
if __name__ == "__main__":
    main()
