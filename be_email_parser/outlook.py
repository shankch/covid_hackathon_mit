import Mail
import config


class Outlook(Mail.Mail):
    def __init__(self, username, password):
        super().__init__(username, password, config.OUTLOOK_SMTP_SERVER, config.OUTLOOK_SMTP_PORT, config.OUTLOOK_IMAP_SERVER, config.OUTLOOK_IMAP_PORT)

    # Functions specific to outlook inboxes
