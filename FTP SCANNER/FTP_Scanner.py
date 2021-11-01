import ftplib

def annonLogin(hostname):
    try:
        ftp = ftplib.FTP(hostname)
        ftp.login('anonymous', 'me@your.com')
        print("[*] {a} FTP Anonymous Logon Succeded.".format(a = str(hostname)))
        ftp.quit()
        return True
    except Exception as e:
        print(e)
        print("[-] {a} FTP Anonymous Logon Failed.".format(a = str(hostname)))
        return False
host = "127.0.0.1"
annonLogin(host)
