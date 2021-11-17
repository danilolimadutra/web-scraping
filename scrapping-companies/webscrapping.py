from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
import ssl
import csv
import time
import os
from random import seed
from random import randint
from urllib import parse


class WebScrapping:

    def __init__(self):
        self.dataPath = 'data'

    # 1. Capturar todos os links de macro categorias

    # parse URL to avoid unicode codec problem

    def urlParse(self, link):
        scheme, netloc, path, query, fragment = parse.urlsplit(link)
        path = parse.quote(path)
        url = parse.urlunsplit((scheme, netloc, path, query, fragment))
        return url

    # scrap email from home and contact page

    def requestPageToSoup(self, url):
        # Ignore SSL certificate errors
        self.ctx = ssl.create_default_context()
        self.ctx.check_hostname = False
        self.ctx.verify_mode = ssl.CERT_NONE

        try:
            url = self.urlParse(url)
            req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            html = urlopen(req, context=self.ctx).read()
            soup = BeautifulSoup(html, "html.parser")
        except Exception as e:
            print('LOG: ERROR REQUESTING URL')
            print('ERROR: ', e)
            soup = False

        return soup

    def scrapEmail(self, url):
        print('LOG: scrapping email from: ', url)

        soup = self.requestPageToSoup(url)

        emails = list()
        if soup:
            tags = soup('a')
            contactPages = list()
            contactLink = False
            if tags:
                for tag in tags:
                    link = tag.get('href')
                    if link:
                        if 'mailto' in link:
                            email = link[7:]
                            if email not in emails:
                                emails.append(email)
                        if 'contact' in link:
                            if 'http' in link:
                                contactLink = link
                            else:
                                if url[len(url)-1:] == '/' and link[:1] == '/':
                                    contactLink = url + link[1:]
                                else:
                                    contactLink = url + link

                        if contactLink and contactLink not in contactPages:
                            contactPages.append(contactLink)

            if not emails and contactPages:
                for url in contactPages:
                    print('LOG: scrapping email from contact page: ', url)
                    sec = randint(1, 10)
                    time.sleep(sec)

                    soup = self.requestPageToSoup(url)
                    if soup:
                        tags = soup('a')
                        if tags:
                            for tag in tags:
                                link = tag.get('href')
                                if link:
                                    if 'mailto' in link:
                                        email = link[7:]
                                        if email not in emails:
                                            emails.append(email)
            return emails

    def scrapCategories(self, url):
        soup = self.requestPageToSoup(url)

        tags = soup('a')

        lstCategory = []
        for tag in tags:
            url = tag.get('href')
            if url is not None:
                if 'list/ql' in url:
                    lstCategory.append([tag.contents[0], url])
        print('LOG: ending category scrapping')
        return lstCategory

    # 2. capturar todos os links das empresas

    def scrapCompaniesUrl(self, lstCategory):
        count = 0
        lstCompany = []
        print('LOG: starting company URL scraping ====================')
        for url in lstCategory:
            sec = randint(1, 10)
            print(f"LOG: waiting {int(sec)} seg.")
            time.sleep(sec)
            count += 1
            total = len(lstCategory)
            print(
                f"LOG: scrapping companies URL from category: {str(count)} de {str(total)}")
            print('URL:', url)
            soup = self.requestPageToSoup(url)

            tags = soup('a')

            lstTemp = list()
            lstUrl = list()
            for tag in tags:
                url = tag.get('href')
                if url is not None:
                    if 'list/member' in url and url not in lstUrl:
                        lstUrl.append(url)
                        lstTemp.append([tag.get('alt'), url])

            print('LOG: total companies URL from category:', len(lstTemp))
            lstCompany += lstTemp

        print('LOG: total companies:', len(lstCompany))
        return lstCompany

    def scrapCompanyData(self, url):
        soup = self.requestPageToSoup(url)

        company = list()
        company.append(url)

        try:
            name = soup.find('span', class_="fl-heading-text")
            company.append(name.contents[0])
        except:
            company.append('null')

        try:
            category = soup.find('span', class_="gz-cat")
            company.append(category.contents[0])
        except:
            company.append('null')

        try:
            street = soup.find('span', class_="gz-street-address")
            company.append(street.contents[0])
        except:
            company.append('null')

        try:
            city = soup.find('span', class_="gz-address-city")
            company.append(city.contents[0])
        except:
            company.append('null')

        try:
            region = soup.find('span', itemprop="addressRegion")
            company.append(region.contents[0])
        except:
            company.append('null')

        try:
            postalCode = soup.find('span', itemprop="postalCode")
            company.append(postalCode.contents[0])
        except:
            company.append('null')

        try:
            googleMaps = soup.find('a', class_='card-link')
            company.append(googleMaps.get('href'))
        except:
            company.append('null')

        try:
            telephone = soup.find('span', itemprop="telephone")
            company.append(telephone.contents[0])
        except:
            company.append('null')

        try:
            site = soup.findAll('a', itemprop='url')
            company.append(site[1].get('href'))
        except:
            company.append('null')

        try:
            fax = soup.find('span', itemprop="faxNumber")
            company.append(fax.contents[0])
        except:
            company.append('null')

        try:
            repName = soup.find('div', class_='gz-member-repname')
            company.append(repName.contents[0])
        except:
            company.append('null')

        try:
            repTitle = soup.find('div', class_='gz-member-reptitle')
            company.append(repTitle.contents[0])
        except:
            company.append('null')

        try:
            repPhone = soup.find('span', class_='gz-rep-phone-num')
            company.append(repPhone.contents[0])
        except:
            company.append('null')

        return company

    def createCSV(self, fileName, data):
        filePath = os.path.join(self.dataPath, f"{fileName}.csv")
        myFile = open(filePath, 'w', newline='')
        with myFile:
            writer = csv.writer(myFile, delimiter=';')
            writer.writerows(data)
        myFile.close
        print(f'LOG: ending create of {fileName}.csv')

    def readCSV(self, fileName):
        filePath = os.path.join(self.dataPath, f"{fileName}.csv")
        with open(filePath, newline='') as myFile:
            reader = csv.reader(myFile, delimiter=';')
            lst = list()
            for row in reader:
                lst.append(row)
        myFile.close()
        return lst

    def getValueFromCsv(self, fileName, columnName):
        # read url companies file for further scrapping
        csvData = self.readCSV(fileName)

        index = 0
        header = csvData[0]
        valueIndex = -1
        for value in header:  # ignore the header
            if value == columnName:
                valueIndex = index
                print(f"{index} => {value}")
            index += 1

        lst = list()
        if valueIndex >= 0:
            for value in csvData[1:]:
                lst.append(value[valueIndex])

        return lst
