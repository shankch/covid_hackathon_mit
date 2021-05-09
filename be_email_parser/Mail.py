import imaplib
import datetime
import email
import smtplib
from email.mime.text import MIMEText

"""GENERIC IMAP CLASS THAT CAN MANAGE AND IMAP4 INBOX"""


class Mail:
    def __init__(self, username, password, stmp_ssl_host, stmp_ssl_port, imap_server, imap_port):
        # set up email server for sending mail
        self.server = smtplib.SMTP(stmp_ssl_host, stmp_ssl_port)
        self.server.ehlo()
        self.server.starttls()
        self.server.ehlo()
        self.server.login(username, password)
        self.username = username
        self.all_requested = []
        self.verbose = False


        # sets up imap for reading thru inbox
        self.imap = self.login(username, password, imap_server, imap_port)

    # Returns an imap
    def login(self, username, password, imap_server, imap_port):
        login_attempts = 0
        while True:
            try:
                imap = imaplib.IMAP4_SSL(imap_server, imap_port)
                r, d = imap.login(username, password)
                assert r == 'OK', 'login failed: %s' % str(r)
                if self.verbose:
                    print(" > Signed in as %s" % username, d)
                return imap
            except Exception as err:
                print(" > Sign in error: %s" % str(err))
                login_attempts = login_attempts + 1
                if login_attempts < 3:
                    continue
                assert False, 'login failed'

    def send_email(self, targets, subject, msg):
        if self.verbose:
            print("SENDING EMAIL \n\tTO: %s\n\tSUBJECT: %s\n\tMSG: %s\n" % (targets,subject,msg))
        email_message = MIMEText(msg)
        email_message['Subject'] = subject
        email_message['From'] = self.username
        email_message['To'] = ', '.join(targets)
        self.server.sendmail(self.username, targets, email_message.as_string())

    def get_list(self):
        return self.imap.list()

    def select(self, select_str):
        if self.verbose:
            print("\tSELECTING MAILBOX: %s" % select_str)
        return self.imap.select(select_str)

    def inbox(self):
        return self.select("Inbox")

    def junk(self):
        return self.select("Junk")

    def logout(self):
        return self.imap.logout()

    def since_date(self, days):
        mydate = datetime.datetime.now() - datetime.timedelta(days=days)
        return mydate.strftime("%d-%b-%Y")

    def allIdsSince(self, days):
        r, d = self.imap.search(None, '(SINCE "' + self.since_date(days) + '")', 'ALL')
        return d[0].decode('utf8').split(' ')

    def allIdsToday(self):
        return self.allIdsSince(1)

    def readIdsSince(self, days):
        r, d = self.imap.search(None, '(SINCE "' + self.date_since(days) + '")', 'SEEN')
        return d[0].decode('utf8').split(' ')

    def readIdsToday(self):
        return self.readIdsSince(1)

    def unreadIdsSince(self, days):
        r, d = self.imap.search(None, '(SINCE "' + self.since_date(days) + '")', 'UNSEEN')
        return d[0].decode('utf8').split(' ')

    def unreadIdsToday(self):
        return self.unreadIdsSince(1)

    def allIds(self):
        r, d = self.imap.search(None, "ALL")
        if d[0] == b'':
            return []
        return d[0].decode('utf8').split(' ')

    def readIds(self):

        r, d = self.imap.search(None, "SEEN")
        if d[0] == b'':
            return []
        return d[0].decode('utf8').split(' ')

    def unreadIds(self):
        r, d = self.imap.search(None, "UNSEEN")
        if d[0] == b'':
            return []
        return d[0].decode('utf8').split(' ')

    def hasUnread(self):
        return self.unreadIds() != ['']

    def getIdswithWord(self, ids, word):
        stack = []
        for id in ids:
            self.getEmail(id)
            if word in self.mailbody().lower():
                stack.append(id)
        return stack

    def getEmail(self, id):
        r, d = self.imap.fetch(id, "(RFC822)")
        raw_email = d[0][1]
        email_message = email.message_from_string(raw_email.decode('utf8'))
        return email_message

    def unread(self):
        if self.verbose:
            print("\tPOPULATING all_requested with UNREAD MAIL")
        self.all_requested = []
        for ids in self.unreadIds():
            self.all_requested.append(self.getEmail(ids))
        return self.all_requested

    def readall(self):
        if self.verbose:
            print("\tPOPULATING all_requested with ALL MAIL")
        self.all_requested = []
        for ids in self.allIds():
            self.all_requested.append(self.getEmail(ids))
        return self.all_requested

    def readOnly(self, folder):
        return self.imap.select(folder, readonly=True)

    def writeEnable(self, folder):
        return self.imap.select(folder, readonly=False)

    def rawRead(self):
        list = self.readIds()
        latest_id = list[-1]
        r, d = self.imap.fetch(latest_id, "(RFC822)")
        raw_email = d[0][1]
        return raw_email

    def mailbody(self, ids):
        if ids.is_multipart():
            for payload in ids.get_payload():
                # if payload.is_multipart(): ...
                body = (
                    payload.get_payload()
                        .split(ids['from'])[0]
                        .split('\r\n\r\n2015')[0]
                )
                return body
        else:
            body = (
                ids.get_payload()
                    .split(ids['from'])[0]
                    .split('\r\n\r\n2015')[0]
            )
            return body

    def __clean(self, strattrb):
        return strattrb.replace("\n", ',').replace("\r", ',')

    def stripRequestedMail(self):
        unreademails = []
        for ids in self.all_requested:
            email_from = str(self.__clean(ids['from'])).split("<")
            name, email = email_from[0], email_from[1][:-1]
            date = self.__clean(ids['date']).split(",")[1].split('-')[0]
            subject = self.__clean(ids['Subject'])
            body = self.__clean(self.mailbody(ids))
            unreademails.append({'Name': name, 'Email': email, 'Date': date, 'Subject': subject, 'Body': body})
        return unreademails

    def setVerbose(self, b):
        self.verbose = b
