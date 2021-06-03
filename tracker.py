from os import environ

from bs4 import BeautifulSoup
from requests import get

url = f'https://egov.uscis.gov/casestatus/mycasestatus.do?appReceiptNum={environ.get("RECEIPT")}'

response = get(url=url)

scrapped = BeautifulSoup(response.text, "html.parser")
soup = scrapped.find_all('div', {'class': 'rows text-center'})[0]
print(soup.find('h1').text)
print(soup.find('p').text)
