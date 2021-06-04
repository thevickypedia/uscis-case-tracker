from json import load
from os import environ, listdir
from random import choice
from sys import exit

from bs4 import BeautifulSoup
from requests import Session

from lib.emailer import Emailer, Session as Boto_Session
from lib.logger import logger


class USCIS:
    """USCIS. A parent class for case tracker."""

    def __init__(self, receipt_number: str):
        """__init__

        :param receipt_number: Receipt Number for which the information is needed.
        """

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

        sns_client = Boto_Session(aws_access_key_id=access_key, aws_secret_access_key=secret_key)
        self.sns = sns_client.client('sns', region_name='us-west-2')

    def get_case_status(self):
        """
        Creates a session to the USCIS origin and fetches details from the response.
        """
        with Session() as session:
            session.headers = self.headers
            response = session.get(url=self.url, headers=session.headers)
            session.close()

        if response.status_code != 200:
            exit('Failed to make a call to origin!')

        # to use lxml (instead of html.parser) run "pip install lxml" before hand
        scrapped = BeautifulSoup(response.text, "html.parser")
        soup = scrapped.find_all('div', {'class': 'rows text-center'})[0]

        title = soup.find('h1').text
        description = soup.find('p').text

        if title.strip() != 'Case Was Received':
            logger.info(f'New Update::{title}')
            logger.info(f'Description::{description}')
            self.notify(message=f"{title}\n\n{description}")
            Emailer(sender=f"USCIS Case Tracker <{sender}>", recipients=[recipient],
                    title=title, text=description,
                    access_key=access_key, secret_key=secret_key)
        else:
            logger.info(f"Last Update::{title} on {','.join(description.split(',')[0:2]).strip('On ')}")

    def notify(self, message):
        """
        Notification is triggered when the case status, is other than 'Case Was Received'
        Notifies using AWS SNS and AWS SES
        """
        sns_response = self.sns.publish(PhoneNumber=phone_number, Message=message)
        if sns_response.get('ResponseMetadata').get('HTTPStatusCode') == 200:
            logger.info('SNS notification has been sent.')
        else:
            logger.error(f'Unable to send SNS notification.\n{sns_response}')


if __name__ == '__main__':
    if environ.get('DOCKER'):
        if 'params.json' not in listdir('lib'):
            exit('Using a Dockerfile requires a json file (params.json) with credentials stored as key value pairs.')
        logger.info('Running within a Docker container.')
        json_file = load(open('lib/params.json'))
        receipt = json_file.get('RECEIPT')
        phone_number = json_file.get('PHONE')
        access_key = json_file.get('ACCESS_KEY')
        secret_key = json_file.get('SECRET_KEY')
        sender = json_file.get('SENDER')
        recipient = json_file.get('RECIPIENT')
    else:
        receipt = environ.get('RECEIPT')
        phone_number = environ.get('PHONE')
        access_key = environ.get('ACCESS_KEY')
        secret_key = environ.get('SECRET_KEY')
        sender = environ.get('SENDER')
        recipient = environ.get('RECIPIENT')

    env_vars = [receipt, phone_number, access_key, secret_key]

    if any(env_var is None for env_var in env_vars):
        exit("Check your environment variables. It should be set as:\n"
             "'RECEIPT=<USCIS_case_ID>'\n'PHONE=<phone_number>'\n"
             "'ACCESS_KEY=<aws_access_key>'\n'SECRET_KEY=<aws_secret_key>'")

    USCIS(receipt_number=receipt).get_case_status()
