from urllib.request import urlopen
from bs4 import BeautifulSoup
import ssl
import csv
import time

# generate random floating point values
from random import seed
from random import randint

# 1. Capturar todos os links de macro categorias


def scrapCategories(url):
    print('LOG: iniciando coleta de categorias: ', url)
    html = urlopen(url, context=ctx).read()
    soup = BeautifulSoup(html, "html.parser")

    # TODO melhorar essa consulta com um complemento do atributo de classe
    tags = soup('a')

    lstCategory = []
    for tag in tags:
        url = tag.get('href')
        if url is not None:
            if 'list/ql' in url:
                lstCategory.append([tag.contents[0], url])
    print('LOG: finalizado coleta de categorias')
    return lstCategory

# 2. capturar todos os links das empresas

# TODO criar uma requisição a parte para urlopen e beautifulSoap


def scrapCompaniesUrl(lstCategory):
    count = 0
    lstCompany = []
    for category in lstCategory:
        sec = randint(1, 10)
        print('LOG: Empresas ===========================================')
        print(f"LOG: espera {int(sec)} seg.")
        time.sleep(sec)
        count += 1
        total = len(lstCategory)
        print(
            f"LOG: coletando empresas categoria: {str(count)} de {str(total)}")
        print('URL:', category)
        html = urlopen(category, context=ctx).read()
        soup = BeautifulSoup(html, "html.parser")

        # TODO melhorar essa consulta com um complemento do atributo de classe
        tags = soup('a')

        lstTemp = list()
        lstUrl = list()
        for tag in tags:
            url = tag.get('href')
            if url is not None:
                if 'list/member' in url and url not in lstUrl:
                    lstUrl.append(url)
                    lstTemp.append([tag.get('alt'), url])

        print('LOG: total de empresas:', len(lstTemp))
        lstCompany += lstTemp

    print('LOG: total final:', len(lstCompany))
    return lstCompany


def scrapCompanyData(url):
    html = urlopen(url, context=ctx).read()
    soup = BeautifulSoup(html, "html.parser")

    company = list()
    company.append(url)

    name = soup.find('span', class_="fl-heading-text")
    company.append(name.contents[0])
    category = soup.find('span', class_="gz-cat")
    company.append(category.contents[0])

    try:
        street = soup.find('span', class_="gz-street-address")
        company.append(street.contents[0])
    except:
        company.append('null')
        print('LOG: street null')

    try:
        city = soup.find('span', class_="gz-address-city")
        company.append(city.contents[0])
    except:
        company.append('null')
        print('LOG: city null')

    try:
        region = soup.find('span', itemprop="addressRegion")
        company.append(region.contents[0])
    except:
        company.append('null')
        print('LOG: region null')

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

    fax = soup.find('span', itemprop="faxNumber")
    if fax is not None:
        company.append(fax.contents[0])
    else:
        company.append('null')

    repName = soup.find('div', class_='gz-member-repname')
    if repName is not None:
        company.append(repName.contents[0])
    else:
        company.append('null')

    repTitle = soup.find('div', class_='gz-member-reptitle')
    if repTitle is not None:
        company.append(repTitle.contents[0])
    else:
        company.append('null')

    repPhone = soup.find('span', class_='gz-rep-phone-num')
    if repPhone is not None:
        company.append(repPhone.contents[0])
    else:
        company.append('null')

    return company


def createCSV(fileName, data):
    print(f'LOG: iniciando criação de {fileName}.csv')
    myFile = open(f"{fileName}.csv", 'w', newline='')
    with myFile:
        writer = csv.writer(myFile, delimiter=';')
        writer.writerows(data)
    myFile.close
    print(f'LOG: concluindo criação de {fileName}.csv')


def readCSV(fileName):
    with open(f"{fileName}.csv", newline='') as myFile:
        reader = csv.reader(myFile, delimiter=';')
        lst = list()
        for row in reader:
            lst.append(row)
    myFile.close()
    return lst


# Ignore SSL certificate errors
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE


url = "https://business.edmontonchamber.com/list"

"""
# bloco de criação da lista de categorias
categoryList = scrapCategories(url)
categoryHeader = ['Category Name', 'Category URL']

categoryList.insert(0, categoryHeader)

createCSV('categories', categoryList)


csvCategory = readCSV('categories')

categoriesUrl = list()
for category in csvCategory[1:]:  # ignorando o cabeçalho
    categoriesUrl.append(category[1])  # coletando apenas urls

companies = scrapCompaniesUrl(categoriesUrl)

companyHeader = ['Company Name', 'Company URL']
companies.insert(0, companyHeader)
createCSV('companies_url', companies)
"""

csvCompany = readCSV('companies_url')

companiesUrl = list()
for company in csvCompany[1:]:  # ignorando o cabeçalho
    companiesUrl.append(company[1])  # coletando apenas urls

companyList = list()
header = ['URL', 'Name', 'Category', 'Address', 'City', 'Region', 'Postal Code',
          'Google Maps', 'Phone', 'Site', 'Fax', 'Contact Name',
          'Contact Title', 'Contact Phone']
companyList.append(header)

# 3. coletar os dados das empresas
print('LOG: COMPANIES ============================')
start = 1828
stop = 1857
countComp = start
# for companyUrl in ['https://business.edmontonchamber.com/list/member/get-social-yeg-28713', 'https://business.edmontoamber.com/list/member/get-social-yeg-28713']:
for companyUrl in companiesUrl[start:stop]:
    sec = randint(1, 10)
    print(f"LOG: espera {int(sec)} seg.")
    time.sleep(sec)
    countComp += 1
    print(f"{str(countComp)} -> {companyUrl}")
    try:
        companyData = scrapCompanyData(companyUrl)
        companyList.append(companyData)
    except Exception as e:
        print('LOG: ERRO FATAL - COLETA DADOS EMPRESA')
        print('ERROR: ', e)
        break


createCSV(f"companies_data_{str(start)}-{str(countComp)}", companyList)
