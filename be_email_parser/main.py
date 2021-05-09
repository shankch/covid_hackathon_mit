# -*- coding: utf-8 -*-
"""
Created on Sat Apr  4 22:31:57 2020

@author: TEJAS
"""

# N95,Ventilator, Respirator .......

from filter_keywords import FilterKeywords
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from outlook import Outlook
import pandas as pd
import config
import time


def main():
    # opens up mailbox
    mailbox = Outlook(username='covidconnect2020@outlook.com', password='mithack10')
    mailbox.setVerbose(True)
    mailbox.inbox()

    # put stuff in firebase
    # Use a service account
    cred = credentials.Certificate('credentials.json')
    firebase_admin.initialize_app(cred)
    db = firestore.client()

    while True:
        new_mail_df = get_new_mail(mailbox, db)
        autoReply(mailbox, new_mail_df)
        time.sleep(5)


def autoReply(mailbox, new_mail_df):
    if new_mail_df is not None:
        for index, row in new_mail_df.iterrows():
            mailbox.send_email([row["Email"]], "Donation Request Received", config.generateMessage(row['Name'], row['Supplies']))


# gets new mail and adds it to database
def get_new_mail(mailbox, db):
    # mailbox.readall()
    mailbox.unread()
    requested_mail = mailbox.stripRequestedMail()
    df = pd.DataFrame.from_dict(requested_mail)

    if len(df) > 0:
        filter_key = FilterKeywords(df)
        filter_key.process()

        for index, row in filter_key.df.iterrows():
            data = {u'Name': row['Name'], u'Email': row['Email'], u'Date': row['Date'], u'Subject': row['Subject'],
                    u'Body': row['Body'], u'relInfo': row['relInfo'], u'Status': row['Status'],
                    u'Keywords': row['Keywords'], u'Supplies': row['Supplies']}
            db.collection(u'Expected Masks').add(data)
        return filter_key.df


if __name__ == "__main__":
    main()
