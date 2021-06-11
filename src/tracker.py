from json import load
from os import environ, listdir
from random import choice
from sys import exit

from bs4 import BeautifulSoup
from requests import Session

# conditional imports to avoid module errors while running as a docker container
if environ.get('DOCKER'):
    from lib.emailer import SMTP, Emailer, SMTPException
    from lib.logger import logger
else:
    from src.lib.emailer import SMTP, Emailer, SMTPException
    from src.lib.logger import logger


class USCIS:
    """USCIS. A parent class for USCIS case tracker.

        >>> USCIS

    Args:
         receipt_number: Receipt Number for which the information is needed.

    """

    def __init__(self, receipt_number: str):
        header_list = [
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) '
            'AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.1.2 Safari/605.1.15',

            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) '
            'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36',

            'Mozilla/5.0 (iPhone; CPU iPhone OS 14_6 like Mac OS X) '
            'AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148',

            'Mozilla/5.0 (Windows NT 8.0; Win64; x64) '
            'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.109 Safari/537.36',

            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
            'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.61 Safari/537.36'
        ]

        self.url = f'https://egov.uscis.gov/casestatus/mycasestatus.do?appReceiptNum={receipt_number}'
        self.headers = {'User-Agent': choice(header_list)}

    def get_case_status(self):
        """To create a session to the USCIS origin using requests module and fetch details from the response."""
        with Session() as session:
            session.headers = self.headers
            response = session.get(url=self.url, headers=session.headers)
            session.close()

        if (status_code := response.status_code) != 200:
            exit(f'Failed to make a call to origin!\nHTTP Response Code: {status_code}')

        # to use lxml (instead of html.parser) run "pip install lxml" before hand
        scrapped = BeautifulSoup(response.text, "html.parser")
        soup = scrapped.find_all('div', {'class': 'rows text-center'})[0]

        subject = soup.find('h1').text
        body = soup.find('p').text

        if subject.strip() != 'Case Was Received' and subject and body:
            logger.info(f'New Update::{subject}')
            logger.info(f'Description::{body}')
            Emailer(sender=email_sender, password=email_password,
                    recipient=email_recipient, title=subject, text=body + '\n\n' + self.url)
            self.notify(subject=subject)
        elif subject and body:
            logger.info(f"Last Update::{subject} on {','.join(body.split(',')[0:2]).strip('On ')}")
        else:
            logger.fatal(f'No information was retrieved from {self.url}')

    def notify(self, subject: str):
        """Notification is triggered when the case status, is other than 'Case Was Received'.

        Notifies via text message through SMS gateway of destination number.

        Args:
            subject: Receives the title as argument `subject` and send an SMS notification.

        """
        try:
            to = f"{phone_number}@tmomail.net"
            message = (f"From: {email_sender}\n" + f"To: {to}\n" + f"Subject: {subject}\n" + "\n\n" + self.url)
            server = SMTP("smtp.gmail.com", 587)
            server.starttls()
            server.login(user=email_sender, password=email_password)
            server.sendmail(email_sender, to, message)
            server.quit()
            server.close()
            logger.info('SMS notification has been sent.')
        except SMTPException as error:
            if 'Username and Password not accepted' in str(error):
                logger.error(error)
                exit(1)
            else:
                logger.error('Failed to send SMS. Please check the GMAIL_USER and GMAIL_PASS in params.json.')
                logger.critical('Logon to https://myaccount.google.com/lesssecureapps and turn ON less secure apps.')
                exit(error)


if __name__ == '__main__':
    if 'params.json' not in listdir():
        exit('Script requires a json file (params.json) with credentials stored as key value pairs.')
    if not open('params.json').read():
        exit('Your "params.json" should appear as following:\n'
             '{\n'
             '\t"RECEIPT": "<your_receipt_number>",\n'
             '\t"PHONE": "<phone_number>",\n'
             '\t"GMAIL_USER": "<sender_email_address>",\n'
             '\t"GMAIL_PASS": "<sender_id_password>",\n'
             '\t"RECIPIENT": "<recipient_email_address>"\n'
             '}')
    json_file = load(open('params.json'))
    receipt = json_file.get('RECEIPT')
    phone_number = json_file.get('PHONE')
    email_sender = json_file.get('GMAIL_USER')
    email_password = json_file.get('GMAIL_PASS')
    email_recipient = json_file.get('RECIPIENT')

    env_vars = [receipt, phone_number, email_sender, email_password, email_recipient]

    if any(env_var is None for env_var in env_vars):
        exit("Your 'params.json' should appear as following:\n"
             "{\n"
             "\tRECEIPT: <your_receipt_number>,\n"
             "\tPHONE: <phone_number>,\n"
             "\tGMAIL_USER: <sender_email_address>,\n"
             "\tGMAIL_PASS: <sender_id_password>,\n"
             "\tRECIPIENT: <recipient_email_address>\n"
             "}")

    USCIS(receipt_number=receipt).get_case_status()
