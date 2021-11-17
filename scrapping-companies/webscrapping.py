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
        self.data_path = 'data'

    # 1. Capturar todos os links de macro categorias

    # parse URL to avoid unicode codec problem

    def url_parse(self, link):
        scheme, netloc, path, query, fragment = parse.urlsplit(link)
        path = parse.quote(path)
        url = parse.urlunsplit((scheme, netloc, path, query, fragment))
        return url

    # scrap email from home and contact page

    def request_page_to_soup(self, url):
        # Ignore SSL certificate errors
        self.ctx = ssl.create_default_context()
        self.ctx.check_hostname = False
        self.ctx.verify_mode = ssl.CERT_NONE

        try:
            url = self.url_parse(url)
            req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            html = urlopen(req, context=self.ctx).read()
            soup = BeautifulSoup(html, "html.parser")
        except Exception as e:
            print('LOG: ERROR REQUESTING URL')
            print('ERROR: ', e)
            soup = False

        return soup

    def scrap_email(self, url):
        print('LOG: scrapping email from: ', url)

        soup = self.request_page_to_soup(url)

        emails = list()
        if soup:
            tags = soup('a')
            contact_pages = list()
            contact_link = False
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
                                contact_link = link
                            else:
                                if url[len(url)-1:] == '/' and link[:1] == '/':
                                    contact_link = url + link[1:]
                                else:
                                    contact_link = url + link

                        if contact_link and contact_link not in contact_pages:
                            contact_pages.append(contact_link)

            if not emails and contact_pages:
                for url in contact_pages:
                    print('LOG: scrapping email from contact page: ', url)
                    sec = randint(1, 10)
                    time.sleep(sec)

                    soup = self.request_page_to_soup(url)
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

    def scrap_categories(self, url):
        soup = self.request_page_to_soup(url)

        tags = soup('a')

        lst_category = []
        for tag in tags:
            url = tag.get('href')
            if url is not None:
                if 'list/ql' in url:
                    lst_category.append([tag.contents[0], url])
        print('LOG: ending category scrapping')
        return lst_category

    # 2. capturar todos os links das empresas

    def scrap_companies_url(self, lst_category):
        count = 0
        lst_company = []
        print('LOG: starting company URL scraping ====================')
        for url in lst_category:
            sec = randint(1, 10)
            print(f"LOG: waiting {int(sec)} seg.")
            time.sleep(sec)
            count += 1
            total = len(lst_category)
            print(
                f"LOG: scrapping companies URL from category: {str(count)} de {str(total)}")
            print('URL:', url)
            soup = self.request_page_to_soup(url)

            tags = soup('a')

            lst_temp = list()
            lst_url = list()
            for tag in tags:
                url = tag.get('href')
                if url is not None:
                    if 'list/member' in url and url not in lst_url:
                        lst_url.append(url)
                        lst_temp.append([tag.get('alt'), url])

            print('LOG: total companies URL from category:', len(lst_temp))
            lst_company += lst_temp

        print('LOG: total companies:', len(lst_company))
        return lst_company

    def scrap_company_data(self, url):
        soup = self.request_page_to_soup(url)

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
            postal_code = soup.find('span', itemprop="postalCode")
            company.append(postal_code.contents[0])
        except:
            company.append('null')

        try:
            google_maps = soup.find('a', class_='card-link')
            company.append(google_maps.get('href'))
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
            rep_name = soup.find('div', class_='gz-member-repname')
            company.append(rep_name.contents[0])
        except:
            company.append('null')

        try:
            rep_title = soup.find('div', class_='gz-member-reptitle')
            company.append(rep_title.contents[0])
        except:
            company.append('null')

        try:
            rep_phone = soup.find('span', class_='gz-rep-phone-num')
            company.append(rep_phone.contents[0])
        except:
            company.append('null')

        return company

    def create_csv(self, file_name, data):
        file_path = os.path.join(self.data_path, f"{file_name}.csv")
        my_file = open(file_path, 'w', newline='')
        with my_file:
            writer = csv.writer(my_file, delimiter=';')
            writer.writerows(data)
        my_file.close
        print(f'LOG: ending create of {file_name}.csv')

    def read_csv(self, file_name):
        file_path = os.path.join(self.data_path, f"{file_name}.csv")
        with open(file_path, newline='') as my_file:
            reader = csv.reader(my_file, delimiter=';')
            lst = list()
            for row in reader:
                lst.append(row)
        my_file.close()
        return lst

    def get_value_from_csv(self, file_name, column_name):
        # read url companies file for further scrapping
        csv_data = self.read_csv(file_name)

        index = 0
        header = csv_data[0]
        value_index = -1
        for value in header:  # ignore the header
            if value == column_name:
                value_index = index
                print(f"{index} => {value}")
            index += 1

        lst = list()
        if value_index >= 0:
            for value in csv_data[1:]:
                lst.append(value[value_index])

        return lst
