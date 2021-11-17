import time
from random import seed
from random import randint
from webscrapping import WebScrapping


ws = WebScrapping()

# Scrapping a list of URL categories
url = "https://business.edmontonchamber.com/list"
cat_file_name = 'categories_url'
comp_file_name = 'companies_url'

category_list = ws.scrap_categories(url)

# Save URL categories in a CSV file
category_header = ['Category Name', 'Category URL']
category_list.insert(0, category_header)
ws.create_csv(cat_file_name, category_list)

# read url categories file for further scrapping
categories_url = ws.get_value_from_csv(cat_file_name, 'Category URL')

# scraping a list of URL companies
companies = ws.scrap_companies_url(categories_url)

# Save URL companies in a CSV file
company_header = ['Company Name', 'Company URL']
companies.insert(0, company_header)
ws.create_csv(comp_file_name, companies)

# starting scraping of companies data
print('LOG: START SCRAPPING COMPANIES ============================')

# read url companies file for further scrapping
companies_url = ws.get_value_from_csv(comp_file_name, 'Company URL')

company_list = list()
header = ['URL', 'Name', 'Category', 'Address', 'City', 'Region', 'Postal Code',
          'Google Maps', 'Phone', 'Site', 'Fax', 'Contact Name',
          'Contact Title', 'Contact Phone', 'Email']
company_list.append(header)

# is possible to define the range of data to colect. In case you need to restart for any problem.
start = 0
stop = 5
#stop = len(companies_url)
count_comp = start
for company_url in companies_url[start:stop]:
    sec = randint(1, 10)
    print(f"LOG: wait {int(sec)} sec.")
    time.sleep(sec)
    print(f"LOG: {str(count_comp)} from {str(stop)} -> {company_url}")
    count_comp += 1
    try:
        # scrapping data companies
        company_data = ws.scrap_company_data(company_url)
        email = 'null'
        if company_data[9] != 'null':
            emails = ws.scrap_email(company_data[9])
            if emails:
                email = emails[0]
        company_data.append(email)

        company_list.append(company_data)
    except Exception as e:
        print('LOG: FATAL ERROR AT COMPANY DATA COLECTION')
        print('ERROR: ', e)
        break  # Stop data scrapping

# Create companies data CSV file
ws.create_csv(f"companies_data_{str(start)}-{str(count_comp)}", company_list)
