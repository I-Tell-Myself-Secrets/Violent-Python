
import crypt

def testPass(cryptoPasswd):
    salt = cryptoPasswd[0:2]
    dictionary = open("dictionary.txt", "r")
    for word in dictionary.readlines():
        word =  word.strip("\n")
        cryptword = crypt.crypt(word,salt)
        if(cryptword == cryptoPasswd):
            print("[+] Found the password {r}".format(r = word))
            return
    print("[x] Password was not found!")
    return

def main():
    passFile = open("password.txt", "r")
    for line in passFile.readlines():
        if ":" in line:
            user = line.split(":")[0]
            cryptoPasswd = line.split(":")[1]
            print("[*] Checking password for user {r}:".format(r = user))
            testPass(cryptoPasswd)

if __name__ == "__main__":
    main()
