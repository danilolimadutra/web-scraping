import time
from random import seed
from random import randint
from webscrapping import WebScrapping
from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
import ssl
from urllib import parse

import re


ws = WebScrapping()

"""
urlList = ['http://www.westcanadian.com']

for url in urlList:
    emails = ws.scrap_email(url)
    print(emails)
"""

companyData = ws.scrap_company_data(
    'https://business.edmontonchamber.com/list/member/madsen-avenue-28020')
email = 'null'
if companyData[9] != 'null':
    emails = ws.scrap_email(companyData[9])
    if emails:
        email = emails[0]
companyData.append(email)
print(companyData)
