''' Download emails as documents '''
import imaplib
import email
import dateutil.parser
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
        self.username = username
        self.password = password
        stat, (msg,) = mail.login(self.username, self.password)
        print(msg.decode('utf-8'))
        self.mailbox = mail

    def search(self, folder, query):
        """ Load a folder and find Emails by Header """
        self.folder = folder
        stat, (msg,) = self.mailbox.select('"{}"'.format(self.folder))
        if stat != 'OK':
            raise RuntimeError(stat, msg.decode('utf-8'))

        self.query = query
        result, (ids,) = self.mailbox.search(None, 'HEADER {0}'.format(self.query))
        id_list = ids.split() # ids is a space separated string

        assert(len(id_list) > 0)
        for cid in id_list:
            self.emails.append(self.parse_email(cid))

    def parse_email(self, email_id):
        """ Extract {Subject, Date, Content, Type} from email """
        payload = {"ID": email_id}
        result, data = self.mailbox.fetch(email_id, "(RFC822)")
        raw_email = data[0][1]

        email_message = email.message_from_string(raw_email.decode('utf-8'))
        payload['Date'] = dateutil.parser.parse(email_message['Date'])
        payload['Subject'] = email_message['Subject']
        payload['Type'], payload['Content'] = get_first_text_block(email_message)
        return payload

    def save(self, directory):
        """ Output content from email into local files """
        if not path.exists(directory):
            makedirs(directory)

        for payload in self.emails:
            fpart = 'enote_{d}.{t}'.format(
                            d=payload['Date'].strftime('%m%d%Y%H%M'),
                            t='txt' if payload['Type'] == 'text' else 'html')
            filename = path.join(directory, fpart)
            print(filename)
            with open(filename, 'w+') as fid:
                fid.write(payload['Content'])
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
