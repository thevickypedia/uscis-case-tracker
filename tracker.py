from os import environ
from random import choice

from bs4 import BeautifulSoup
from requests import Session


class USCIS:
    def __init__(self, receipt_number):
        self.url = f'https://egov.uscis.gov/casestatus/mycasestatus.do?appReceiptNum={receipt_number}'
        header_list = ['Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) '
                       'AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.1.2 Safari/605.1.15',

                       'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) '
                       'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36',

                       'Mozilla/5.0 (iPhone; CPU iPhone OS 12_2 like Mac OS X) '
                       'AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148',

                       'Mozilla/5.0 (Windows NT 6.2; Win64; x64) '
                       'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',

                       'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                       'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
                       ]
        self.headers = {
            'User-Agent': choice(header_list)
        }

    def get_case_status(self):
        with Session() as session:
            session.headers = self.headers
            response = session.get(url=self.url, headers=session.headers)
            if response.status_code != 200:
                return 'Failed to make a call to uscis!'

            # to use lxml (instead of html.parser) run pip install lxml before hand
            scrapped = BeautifulSoup(response.text, "html.parser")
            soup = scrapped.find_all('div', {'class': 'rows text-center'})[0]

            title = soup.find('h1').text
            description = soup.find('p').text
            if title.strip() != 'Case Was Received':
                print(f'New Update::{title}')
                print(f'Description::{description}')
            else:
                print('No change in Case Status')


if __name__ == '__main__':
    USCIS(environ.get('RECEIPT')).get_case_status()
