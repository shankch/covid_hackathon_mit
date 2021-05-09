# for outlook.com
OUTLOOK_IMAP_SERVER = "imap-mail.outlook.com"
OUTLOOK_IMAP_PORT = 993
OUTLOOK_SMTP_SERVER = "smtp.office365.com"
OUTLOOK_SMTP_PORT = 587

# FILTER
FILTER_KEYWORD_DICTIONARY = {'n95', 'mask', 'masks' 'donate', 'sell', 'offer', 'ventilator', 'face', 'shield', 'face-shield', 'face shield', 'facemask', 'respirator', 'gown', 'glove', 'sanitizer'}


# EMAIL FORMAT
def generateMessage(name, supplies):
    msg = "Hi %s,\nThank you for your donation. This auto-reply program has generated a report based on your email.\nSupplies:\n\t%s" % (name, supplies)
