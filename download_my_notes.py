''' Download emails as documents '''
import sys
import imaplib

def main(username, password, folder, search):
    mail = imaplib.IMAP4_SSL('imap.gmail.com')
    stat, (msg,) = mail.login(username, password)
    print(msg.decode('utf-8'))

    stat, (msg,) = mail.select('"{}"'.format(folder))
    msg = msg.decode('utf-8')
    if stat != 'OK':
        raise RuntimeError(stat, msg)

    result, (ids,) = mail.search(None, 'HEADER {0}'.format(search))
    id_list = ids.split() # ids is a space separated string

    result, data = mail.fetch(id_list[-1], "(RFC822)")
    raw_email = data[0][1]
    print(raw_email.decode('utf-8'))

if __name__ == "__main__":
    usernm = sys.argv[1]
    passwd = sys.argv[2]
    foldr = sys.argv[3]
    srch = sys.argv[4]
    main(usernm, passwd, foldr, srch)
