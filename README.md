# USCIS Case Tracker
USCIS Case Tracker and notifier using:
- `requests` - Get details from [USCIS](https://egov.uscis.gov/)
- `BeautifulSoup` - Extract tag values from html response
- `SMTP` - Send email and SMS notification using Simple Mail Transfer Protocol [(choose between TLS or SSL)](lib/emailer.py)