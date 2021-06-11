from email.message import EmailMessage
from os import environ
from smtplib import SMTP, SMTP_SSL, SMTPAuthenticationError, SMTPException
from ssl import create_default_context

# conditional imports to avoid module errors while running as a docker container
if environ.get('DOCKER'):
    # noinspection PyUnresolvedReferences
    from lib.logger import logger
else:
    from src.lib.logger import logger


class Emailer:
    """Initiates Emailer object.

    Takes gmail email id, password, recipient, title and text as parameters, to send notification using TLS by default.

    >>> Emailer()

    Args:
        sender: Email address of the sender alias username.
        password: Password of the sender email address.
        recipient: Recipient email address.
        title: The title of the email.
        text: The text version of the email body.

    """

    def __init__(self, sender: str, password: str, recipient: str, title: str, text: str,
                 tls: bool = False, ssl: bool = False):
        self.message = EmailMessage()
        self.message.set_content(text)
        self.message['Subject'] = title
        self.message['From'] = f"USCIS Case Tracker <{sender}>"
        self.message['To'] = recipient
        self.sender = sender
        self.password = password
        if tls or (not tls and not ssl):
            self.using_tls()
        else:
            self.using_ssl()

    def using_tls(self):
        """To send an email using Transport Layer Security - TLS."""
        try:
            server = SMTP(host='smtp.gmail.com', port=587)
            server.starttls(context=create_default_context())
            server.ehlo()
            server.login(self.sender, self.password)
            self.message.set_content(self.message.get_content() + '\nEmail was sent through a secure tunnel using TLS')
            server.send_message(msg=self.message)
            server.quit()
            server.close()
            logger.info('Email notification has been sent.')
        except (SMTPException, SMTPAuthenticationError) as error:
            if 'Username and Password not accepted' in str(error):
                logger.error(error)
                exit(1)
            else:
                logger.error('Login Failed. Please check the GMAIL_USER and GMAIL_PASS in params.json.')
                logger.critical('Logon to https://myaccount.google.com/lesssecureapps and turn ON less secure apps.')

    def using_ssl(self):
        """To send an email using Secure Sockets Layer - SSL."""
        try:
            server = SMTP_SSL(host='smtp.gmail.com', port=465, context=create_default_context())
            server.login(self.sender, self.password)
            self.message.set_content(self.message.get_content() + '\nEmail was sent through a secure tunnel using SSL')
            server.send_message(msg=self.message)
            server.quit()
            server.close()
            logger.info('Email notification has been sent.')
        except (SMTPException, SMTPAuthenticationError) as error:
            if 'Username and Password not accepted' in str(error):
                logger.error(error)
                exit(1)
            else:
                logger.error('Login Failed. Please check the GMAIL_USER and GMAIL_PASS in params.json.')
                logger.critical('Logon to https://myaccount.google.com/lesssecureapps and turn ON less secure apps.')
