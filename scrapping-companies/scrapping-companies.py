from scrapedmontchamber import ScrapEdmontChamber


sec = ScrapEdmontChamber()

"""
category_list = sec.scrap_categories()

sec.save_category_file(category_list)

categories_url = sec.get_value_from_csv(sec.cat_file_name, 'Category URL')

companies_url = sec.scrap_companies_url(categories_url)

sec.save_company_file(companies_url)
"""

# read url companies file for further scrapping
companies_url = sec.get_value_from_csv(sec.comp_file_name, 'Company URL')

start = 425
#stop = 4
company_list = sec.scrap_company_and_email(companies_url, start)

#file_name = f"companies_data_{str(start)}-{str(start+len(company_list))}"
#sec.save_company_data_file(company_list, file_name)
