''' Download emails as documents '''
import sys
import imaplib
import email
from os import path, makedirs


def get_first_text_block(email_message_instance):
    maintype = email_message_instance.get_content_maintype()
    if maintype == 'multipart':
        for part in email_message_instance.get_payload():
            if part.get_content_maintype() == 'text':
                return part.get_payload()
    elif maintype == 'text':
        return email_message_instance.get_payload()

def parse_email(raw_email):
    email_message = email.message_from_string(raw_email)

    print('To: ', email_message['To'])
    print('From: ', email.utils.parseaddr(email_message['From']))
    print('Date: ', email_message['Date'])
    print(email_message.items()) # print all headers
    return get_first_text_block(email_message)

def main(username, password, folder, search, directory):
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
    payload = parse_email(raw_email.decode('utf-8'))

    if not path.exists(directory):
        makedirs(directory)

    filename = path.join(directory, 'enote_{d}.txt'.format(d="10102016"))
    with open(filename, 'w+') as fid:
        fid.write(payload)
    print('Save: {}'.format(filename))

if __name__ == "__main__":
    usernm = sys.argv[1]
    passwd = sys.argv[2]
    foldr = sys.argv[3]
    srch = sys.argv[4]
    dest = sys.argv[5]
    main(usernm, passwd, foldr, srch, dest)
