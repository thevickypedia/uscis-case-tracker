from os import environ

from bs4 import BeautifulSoup
from requests import Session

url = f'https://egov.uscis.gov/casestatus/mycasestatus.do?appReceiptNum={environ.get("RECEIPT")}'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/58.0.3029.110 Safari/537.3'
}
with Session() as session:
    session.headers = headers
    response = session.get(url=url, headers=headers)

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
