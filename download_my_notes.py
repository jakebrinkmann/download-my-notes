''' Download emails as documents '''
import sys
import imaplib

def main(username, password):
    mail = imaplib.IMAP4_SSL('imap.gmail.com')
    stat, (msg,) = mail.login(username, password)
    print(msg.decode('utf-8'))

if __name__ == "__main__":
    usernm = sys.argv[1]
    passwd = sys.argv[2]
    main(usernm, passwd)
