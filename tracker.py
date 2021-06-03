from os import environ
from random import choice
from sys import exit

from boto3 import client
from bs4 import BeautifulSoup
from requests import Session


class USCIS:
    def __init__(self, receipt_number: str = None):
        if not receipt_number:
            exit('No receipt number was given to make a request call to USCIS.')

        self.url = f'https://egov.uscis.gov/casestatus/mycasestatus.do?appReceiptNum={receipt_number}'
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
        self.headers = {
            'User-Agent': choice(header_list)
        }

    def get_case_status(self):
        with Session() as session:
            session.headers = self.headers
            response = session.get(url=self.url, headers=session.headers)
            session.close()

        if response.status_code != 200:
            exit('Failed to make a call to uscis!')

        # to use lxml (instead of html.parser) run "pip install lxml" before hand
        scrapped = BeautifulSoup(response.text, "html.parser")
        soup = scrapped.find_all('div', {'class': 'rows text-center'})[0]

        title = soup.find('h1').text
        description = soup.find('p').text
        if title.strip() != 'Case Was Received':
            sns.publish(PhoneNumber=phone_number,
                        Message=f"{title}\n{description}")
        else:
            print(f"Last Update::{title} on {','.join(description.split(',')[0:2]).strip('On ')}")


if __name__ == '__main__':
    receipt = environ.get('RECEIPT')
    phone_number = environ.get('PHONE')
    access_key = environ.get('ACCESS_KEY')
    secret_key = environ.get('SECRET_KEY')
    sender = environ.get('SENDER')
    recipient = environ.get('RECIPIENT')
    sns = client('sns')

    env_vars = [receipt, phone_number]

    if any(env_var is None for env_var in env_vars):
        exit("Check your environment variables. It should be set as:\n"
             "'RECEIPT=<USCIS_case_ID>'\n'PHONE=<phone_number>'")
    USCIS(receipt_number=receipt).get_case_status()
