import time
from random import seed
from random import randint
from webscrapping import WebScrapping


ws = WebScrapping()

# Scrapping a list of URL categories
url = "https://business.edmontonchamber.com/list"
catFileName = 'categories_url'
compFileName = 'companies_url'

"""
categoryList = ws.scrapCategories(url)

# Save URL categories in a CSV file
categoryHeader = ['Category Name', 'Category URL']
categoryList.insert(0, categoryHeader)
ws.createCSV(catFileName, categoryList)

# read url categories file for further scrapping
categoriesUrl = ws.getValueFromCsv(catFileName, 'Category URL')

# scraping a list of URL companies
companies = ws.scrapCompaniesUrl(categoriesUrl)

# Save URL companies in a CSV file
companyHeader = ['Company Name', 'Company URL']
companies.insert(0, companyHeader)
ws.createCSV(compFileName, companies)

"""
# starting scraping of companies data
print('LOG: START SCRAPPING COMPANIES ============================')

# read url companies file for further scrapping
companiesUrl = ws.getValueFromCsv(compFileName, 'Company URL')

companyList = list()
header = ['URL', 'Name', 'Category', 'Address', 'City', 'Region', 'Postal Code',
          'Google Maps', 'Phone', 'Site', 'Fax', 'Contact Name',
          'Contact Title', 'Contact Phone', 'Email']
companyList.append(header)

# is possible to define the range of data to colect. In case you need to restart for any problem.
start = 90
stop = 100
#stop = len(companiesUrl)
countComp = start
for companyUrl in companiesUrl[start:stop]:
    sec = randint(1, 10)
    print(f"LOG: wait {int(sec)} sec.")
    time.sleep(sec)
    print(f"LOG: {str(countComp)} from {str(stop)} -> {companyUrl}")
    countComp += 1
    try:
        # scrapping data companies
        companyData = ws.scrapCompanyData(companyUrl)
        email = 'null'
        if companyData[9] != 'null':
            emails = ws.scrapEmail(companyData[9])
            if emails:
                email = emails[0]
        companyData.append(email)

        companyList.append(companyData)
    except Exception as e:
        print('LOG: FATAL ERROR AT COMPANY DATA COLECTION')
        print('ERROR: ', e)
        break  # Stop data scrapping

# Create companies data CSV file
ws.createCSV(f"companies_data_{str(start)}-{str(countComp)}", companyList)
