''' Download emails as documents '''
import sys
import imaplib
import email
from os import path, makedirs

class MyNotes:
    def __init__(self):
        self.mailbox = None # imaplib instance
        self.credentials = {'User': '', 'Pass': ''}
        self.folder = '' # Inbox, Sent, etc.
        self.query = '' # To email@site.com
        self.dest = '.' # Local directory
        self.emails = [] # {Subject, Date, Payload, ContentType, Saved}

    def login(self, username, password):
        """ Login to Gmail account """
        mail = imaplib.IMAP4_SSL('imap.gmail.com')
        self.username = username if username
        self.password = password if password
        stat, (msg,) = mail.login(self.username, self.password)
        print(msg.decode('utf-8'))
        self.mailbox = mail

    def search(self, folder, query):
        """ Load a folder and find Emails by Header """
        self.folder = folder if folder
        stat, (msg,) = self.mailbox.select('"{}"'.format(self.folder))
        if stat != 'OK':
            raise RuntimeError(stat, msg.decode('utf-8'))

        self.query = query if query
        result, (ids,) = self.mailbox.search(None, 'HEADER {0}'.format(self.query))
        id_list = ids.split() # ids is a space separated string

        assert(len(id_list) > 0)
        for cid in id_list:
            self.emails.append(self.parse_email(cid))

    def parse_email(self, email_id):
        """ Extract {Subject, Date, Payload, Content} from email """
        data = {}
        result, data = self.mailbox.fetch(email_id, "(RFC822)")
        raw_email = data[0][1]

        email_message = email.message_from_string(raw_email.decode('utf-8'))
        data['Date'] = email_message['Date']
        data['Subject'] = email_message['Subject']
        data['Content'], data['Payload'] = get_first_text_block(email_message)

    def save(directory):
        """ Output content from email into local files """
        if not path.exists(directory):
            makedirs(directory)

        filename = path.join(directory, 'enote_{d}.txt'.format(d="10102016"))
        with open(filename, 'w+') as fid:
            fid.write(payload)
        print('Save: {}'.format(filename))

    def archive(folder):
        """ Move emails to a new location, or delete them """
        raise NotImplemented()


def get_first_text_block(email_message_instance):
    maintype = email_message_instance.get_content_maintype()
    if maintype == 'multipart':
        for part in email_message_instance.get_payload():
            if part.get_content_maintype() == 'text':
                return maintype, part.get_payload()
    elif maintype == 'text':
        return maintype, email_message_instance.get_payload()


def main(username, password, folder, search, directory):
    notes = MyNotes()
    notes.login(usernam, password)
    notes.search(folder, search)
    notes.save(directory)


if __name__ == "__main__":
    usernm = sys.argv[1]
    passwd = sys.argv[2]
    foldr = sys.argv[3]
    srch = sys.argv[4]
    dest = sys.argv[5]
    main(usernm, passwd, foldr, srch, dest)
