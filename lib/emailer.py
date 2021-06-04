from email.message import EmailMessage
from smtplib import SMTP_SSL, SMTP, SMTPAuthenticationError, SMTPException
from ssl import create_default_context

from lib.logger import logger


class Emailer:
    def __init__(self, sender: str, password: str, recipient: str, title: str, text: str,
                 tls: bool = False, ssl: bool = False):
        """Returns a new Emailer object.
        >>> Emailer()
        <emailer.Emailer object at 0x...>
        Uses TLS by default, unless specified to use SSL connection.

        :param sender: The sender.
        :param password: Aunthenticate sender.
        :param recipient: Recipient email address.
        :param title: The title of the email.
        :param text: The text version of the email body.
        """
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
        """
        Sends email using TLS (Transport Layer Security)

        :return: None
        """
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
            logger.error('Login Failed. Please check the GMAIL_USER and GMAIL_PASS in params.json.')
            logger.critical('Logon to https://myaccount.google.com/lesssecureapps and turn ON less secure apps.')
            logger.error(error)

    def using_ssl(self):
        """
        Sends email using SSL (Secure Sockets Layer)

        :return: None
        """
        try:
            server = SMTP_SSL(host='smtp.gmail.com', port=465, context=create_default_context())
            server.login(self.sender, self.password)
            self.message.set_content(self.message.get_content() + '\nEmail was sent through a secure tunnel using SSL')
            server.send_message(msg=self.message)
            server.quit()
            server.close()
            logger.info('Email notification has been sent.')
        except (SMTPException, SMTPAuthenticationError) as error:
            logger.error('Login Failed. Please check the GMAIL_USER and GMAIL_PASS in params.json.')
            logger.critical('Logon to https://myaccount.google.com/lesssecureapps and turn ON less secure apps.')
            logger.error(error)
