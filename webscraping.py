from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
import ssl
import csv
import time
import os
from random import seed
from random import randint
from urllib import parse
import datetime


class WebScraping:
    """A class to agregate all common methods of webscraping for every site."""

    def __init__(self, data_path="data"):
        """
        Parameters:
            data_path (str): The data path where will be stored csv files
        """
        self.data_path = data_path

    def url_parse(self, link: str) -> str:
        """A method to parse URL to avoid Unicode problems.

        Parameters:
            link (str): The URL link of the page to scrap

        Returns:
            str: The url string parsed
        """
        scheme, netloc, path, query, fragment = parse.urlsplit(link)
        path = parse.quote(path)
        url = parse.urlunsplit((scheme, netloc, path, query, fragment))
        return url

    def request_page_to_soup(self, url: str) -> BeautifulSoup:
        """Method to make a request and return the BeautifulSoup html content

        Parameters:
            url (str): The request url

        Returns:
            BeautifulSoup: A data structure representing a parsed HTML or XML document.
        """
        # Ignore SSL certificate errors
        self.ctx = ssl.create_default_context()
        self.ctx.check_hostname = False
        self.ctx.verify_mode = ssl.CERT_NONE

        try:
            url = self.url_parse(url)
            req = Request(
                url,
                headers={
                    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36",
                    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                },
            )
            html = urlopen(req, context=self.ctx).read()
            soup = BeautifulSoup(html, "html.parser")
        except Exception as e:
            print("LOG: ERROR REQUESTING URL")
            print("ERROR: ", e)
            soup = False

        return soup

    def scrap_email(self, url: str) -> list:
        """A method for email scraping at URL site. First, it will look up
        at the current URL, if no one email was found out, it will look up
        for contact pages and try to find out recursively at contact pages.

        Parameters:
            url (str): the url of research

        Returns:
            list: a list of emails string
        """

        print("LOG: scraping email from: ", url)

        soup = self.request_page_to_soup(url)

        emails = list()
        if soup:
            tags = soup("a")
            contact_pages = list()
            contact_link = False

            for tag in tags:
                link = tag.get("href")
                if link:
                    if "mailto" in link:
                        email = link[7:]
                        if email not in emails:
                            emails.append(email)
                    if "contact" in link:
                        if "http" in link:
                            contact_link = link
                        else:
                            if url[len(url) - 1 :] == "/" and link[:1] == "/":
                                contact_link = url + link[1:]
                            else:
                                contact_link = url + link

                    if contact_link and contact_link not in contact_pages:
                        contact_pages.append(contact_link)

            if not emails and contact_pages:
                for url in contact_pages:
                    print("LOG: scraping email from contact page: ", url)
                    sec = randint(1, 10)
                    time.sleep(sec)

                    soup = self.request_page_to_soup(url)
                    if soup:
                        tags = soup("a")

                        for tag in tags:
                            link = tag.get("href")
                            if link:
                                if "mailto" in link:
                                    email = link[7:]
                                    if email not in emails:
                                        emails.append(email)
            return emails

    def create_csv(self, file_name: str, data: list):
        """Method for create CSV files from lists os lists. Stores each item
        of the list in a single line separeted by ;

        Parameters:
            file_name (str): the name for the file
            data (list): the list of itens to be stored
        """
        file_path = os.path.join(self.data_path, f"{file_name}.csv")

        with open(file_path, "w", newline="") as my_file:
            writer = csv.writer(my_file, delimiter=";")
            writer.writerows(data)

        print(f"LOG: ending create of {file_name}.csv")

    def writer_row_csv(self, file_name: str, data: list):
        """Write a new line in a pre-existing CSV file.

        Parameters:
            file_name (str): the name for the file
            data (list): the list to be stored
        """
        file_path = os.path.join(self.data_path, f"{file_name}.csv")

        with open(file_path, "w", newline="") as my_file:
            writer = csv.writer(my_file, delimiter=";")
            writer.writerows(data)

        print(f"LOG: ending write data on {file_name}.csv")

    def read_csv(self, file_name: str) -> list:
        """Read the CSV content delimited by ';' and store in a list.

        Parameters:
            file_name (str): the file name without extension file

        Returns:
            list: the CSV content
        """
        file_path = os.path.join(self.data_path, f"{file_name}.csv")
        with open(file_path, newline="") as my_file:
            reader = csv.reader(my_file, delimiter=";")
            lst = list()
            for row in reader:
                lst.append(row)

        return lst

    def get_value_from_csv(self, file_name: str, column_name: str) -> list:
        """Search by a especific column name and return all the column data.

        Parameters:
            file_name (str): the file name without extension file.
            column_name (str): the column to be found in the file.

        Returns:
            list: a list containing all the column data.
        """
        # read url companies file for further scraping
        csv_data = self.read_csv(file_name)

        header = csv_data[0]
        value_index = -1
        for index, value in enumerate(header):  # ignore the header
            if value == column_name:
                value_index = index
                print(f"{index} => {value}")
            index += 1

        lst = list()
        if value_index >= 0:
            for value in csv_data[1:]:
                lst.append(value[value_index])

        return lst
