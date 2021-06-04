from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from boto3 import Session

from lib.logger import logger


class Emailer:
    def __init__(self, sender: str, recipients: list, title: str, text: str, access_key: str, secret_key: str):
        """Returns a new Emailer object.
        >>> Emailer() #doctest: +ELLIPSIS
        <emailer.Emailer object at 0x...>

        :param access_key: Access Key to access AWS clients
        :param secret_key: Secret Key to access AWS clients
        """
        boto3_ses_client = Session(
            aws_access_key_id=access_key,
            aws_secret_access_key=secret_key
        ).client('ses', region_name='us-west-2')
        response = self.send_mail(boto3_ses_client, sender, recipients, title, text)
        if response.get('ResponseMetadata').get('HTTPStatusCode') == 200:
            logger.info('Email notification has been sent')
        else:
            logger.error(f'Unable to send email notification.\n{response}')

    @staticmethod
    def create_multipart_message(sender: str, recipients: list, title: str, text: str) -> MIMEMultipart:
        """
        Creates a MIME multipart message object.
        Uses only the Python `email` standard library.
        Emails, both sender and recipients, can be just the email string or
        have the format 'The Name <the_email@host.com>'.

        :param sender: The sender.
        :param recipients: List of recipients. Needs to be a list, even if only one recipient.
        :param title: The title of the email.
        :param text: The text version of the email body (optional).
        :return: A `MIMEMultipart` to be used to send the email.
        """
        multipart_content_subtype = 'alternative' if text else 'mixed'
        msg = MIMEMultipart(multipart_content_subtype)
        msg['Subject'] = title
        msg['From'] = sender
        msg['To'] = ', '.join(recipients)
        if text:
            part = MIMEText(text, 'plain')
            msg.attach(part)
        return msg

    def send_mail(self, boto3, sender: str, recipients: list, title: str, text: str) -> dict:
        """
        Sends email using the ses_client
        """
        msg = self.create_multipart_message(sender, recipients, title, text)
        ses_client = boto3
        return ses_client.send_raw_email(
            Source=sender,
            Destinations=recipients,
            RawMessage={'Data': msg.as_string()}
        )
