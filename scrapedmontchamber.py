from webscraping import WebScraping
import os
import time
from random import randint
import datetime

# from webscraping import *


class ScrapEdmontChamber(WebScraping):
    """A Class for specific scraping methods for edmontchamber.com site."""

    def __init__(
        self,
        data_path="data",
        base_url="https://business.edmontonchamber.com/list",
        cat_file_name="categories_url",
        comp_file_name="companies_url",
        comp_data_file="companies_data",
    ):
        """
        Parameters:
            data_path (str): folder name for save CSV files.
            base_url (str): url off edmontchamber where the categories are displaied.
            cat_file_name (str): name of the category url CSV file without the .csv extension
            comp_file_name (str): name of the company url CSV file without the .csv extension
            cat_file_name (str): name of the company data CSV file without the .csv extension
        """
        WebScraping.__init__(self, data_path)
        self.base_url = base_url
        self.cat_file_name = cat_file_name
        self.comp_file_name = comp_file_name
        self.comp_data_file_name = comp_data_file

    def scrap_categories(self) -> list:
        """Method for scraping all the categories URL.

        Returns:
            list: list of category name and URL category
        """
        soup = self.request_page_to_soup(self.base_url)

        tags = soup("a")

        lst_category = []
        for tag in tags:
            url = tag.get("href")
            if url is not None:
                if "list/ql" in url:
                    lst_category.append([tag.contents[0], url])
        print("LOG: ending category scraping")
        return lst_category

    def save_category_file(self, category_list: list):
        """Method to save category list (company name, url) in a CSV file.

        Parameters:
            category_list (list): list of category name and URL category
        """
        category_header = ["Category Name", "Category URL"]
        category_list.insert(0, category_header)
        self.create_csv(self.cat_file_name, category_list)

    # 2. capturar todos os links das empresas

    def scrap_companies_url(self, lst_category: list) -> list:
        """Method to scrapy companies URL from category pages.

        Parameters:
            lst_category (list): a list of URL categories
        Returns:
            list: list of company name and URL category
        """
        lst_company = []
        print("LOG: starting company URL scraping ====================")
        for count, url in enumerate(lst_category):
            sec = randint(1, 10)
            print(f"LOG: waiting {int(sec)} seg.")
            time.sleep(sec)
            total = len(lst_category)
            print(
                f"LOG: scraping companies URL from category: {str(count)} de {str(total)}"
            )
            print("URL:", url)
            soup = self.request_page_to_soup(url)

            tags = soup("a")

            lst_temp = list()
            lst_url = list()
            for tag in tags:
                url = tag.get("href")
                if url is not None:
                    if "list/member" in url and url not in lst_url:
                        lst_url.append(url)
                        lst_temp.append([tag.get("alt"), url])

            print("LOG: total companies URL from category:", len(lst_temp))
            lst_company += lst_temp

        print("LOG: total companies:", len(lst_company))
        return lst_company

    def save_company_file(self, company_list: list):
        """Method to save company list (company name, url) in a CSV file.

        Parameters:
            category_list (list): list of category name and URL category
        """
        company_header = ["Company Name", "Company URL"]
        company_list.insert(0, company_header)
        self.create_csv(self.comp_file_name, company_list)

    def scrap_company_data(self, url: str) -> list:
        """Method for scrap data company from company URL.

        Parameters:
            url (str): Company page URL
        Returns:
            list: a list of all company data
        """
        soup = self.request_page_to_soup(url)

        content = soup.find("span", class_="fl-heading-text")
        name = content.contents[0] if content else "null"

        content = soup.find("span", class_="gz-cat")
        category = content.contents[0] if content else "null"

        content = soup.find("span", class_="gz-street-address")
        street = content.contents[0] if content else "null"

        content = soup.find("span", class_="gz-address-city")
        city = content.contents[0] if content else "null"

        content = soup.find("span", itemprop="addressRegion")
        region = content.contents[0] if content else "null"

        content = soup.find("span", itemprop="postalCode")
        postal_code = content.contents[0] if content else "null"

        content = soup.find("a", class_="card-link")
        google_maps = content.get("href") if content else "null"

        content = soup.find("span", itemprop="telephone")
        telephone = content.contents[0] if content else "null"

        content = soup.findAll("a", itemprop="url")
        site = content[1].get("href") if len(content) >= 2 else "null"

        content = soup.find("span", itemprop="faxNumber")
        fax = content.contents[0] if content else "null"

        content = soup.find("div", class_="gz-member-repname")
        rep_name = content.contents[0] if content else "null"

        content = soup.find("div", class_="gz-member-reptitle")
        rep_title = content.contents[0] if content else "null"

        content = soup.find("span", class_="gz-rep-phone-num")
        rep_phone = content.contents[0] if content else "null"

        company = [
            url,
            name,
            category,
            street,
            city,
            region,
            postal_code,
            google_maps,
            telephone,
            site,
            fax,
            rep_name,
            rep_title,
            rep_phone,
        ]

        return company

    def scrap_company_and_email(self, companies_url: list, start=0, stop=None) -> list:
        """Method for scrap company data from each edmont company site and each company email
        from company email and save data company and email direct to CSV file.

        Parameters:
            companies_url (list): list of companies URL
            start (int): start point of scraping from companies_url
            stop (int): stop point of scraping from companies_url, if None them end of list is defined.
        Returns:
            list: list o company data
        """
        print("LOG: START SCRAPING COMPANIES ============================")
        stop = len(companies_url) if stop is None else stop

        count_comp = start
        company_list = list()
        for company_url in companies_url[start:stop]:
            sec = randint(1, 10)
            print(f"LOG: wait {int(sec)} sec.")
            time.sleep(sec)
            print(f"LOG: {str(count_comp)} from {str(stop)} -> {company_url}")
            count_comp += 1
            try:
                # scraping data companies
                company_data = self.scrap_company_data(company_url)
                email = "null"
                if company_data[9] != "null":
                    emails = self.scrap_email(company_data[9])
                    if emails:
                        email = emails[0]
                company_data.append(email)

                company_list.append(company_data)
            except Exception as e:
                print("LOG: FATAL ERROR AT COMPANY DATA COLECTION")
                print("ERROR: ", e)
                break  # Stop data scraping

            if company_data:
                self.write_company_data(company_data, self.comp_data_file_name)

        return company_list

    def save_company_data_file(self, data: list, name: str):
        """Method for create csv company data file at once with all the data company.

        Parameters:
            data (list): list of companies data scraped from sites
            name (str): name of file without .CSV extension
        """
        header = [
            "URL",
            "Name",
            "Category",
            "Address",
            "City",
            "Region",
            "Postal Code",
            "Google Maps",
            "Phone",
            "Site",
            "Fax",
            "Contact Name",
            "Contact Title",
            "Contact Phone",
            "Email",
        ]
        data.insert(0, header)
        self.create_csv(name, data)

    def write_company_data(self, data: list, file_name: str):
        """A method to save data company on CSV file.

        Parameters:
            data (list): list of data company
            name (str): name of file without .CSV extension
        """
        file_path = os.path.join(self.data_path, f"{file_name}.csv")
        if os.path.exists(file_path):
            self.writer_row_csv(file_name, data)
        else:
            header = [
                "URL",
                "Name",
                "Category",
                "Address",
                "City",
                "Region",
                "Postal Code",
                "Google Maps",
                "Phone",
                "Site",
                "Fax",
                "Contact Name",
                "Contact Title",
                "Contact Phone",
                "Email",
            ]
            # TODO: melhorar esse método para só criar o arquivo com cabeçalho ou unir os dois em um
            self.create_csv(file_name, [header])
            self.writer_row_csv(file_name, data)

        exact_time = datetime.datetime.now()
        print("LOG: data company saved time: ", exact_time.strftime("%X"))
