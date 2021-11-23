# Web Scraping of Edmonton Chamber Web Site

This is a web scraping project focused on scrap companies data from Edmonton Chamber directory web site: [https://business.edmontonchamber.com/list](https://business.edmontonchamber.com/list)

It was a freelancer work for a client in UpWork. The main system contains the following steps for scrap the data.

1. Scrap all categories URL from Edmonton Chamber directory web site.
2. Save categories URL on CSV file.
3. Scrap all company URL existing on categories URL
4. Save companies URL on CSV file.
5. Scrap company information from company page on Edmonton Chamber Site.
6. Scrap company email from each company web site. Because it is not avaliable on Edmonton Chamber site.

## Code

The code contain:

- webscraping.py: generic class that contains some common methods for general web scraping purposes.
- scrapedmontchamber.py: specific class that contains specific mathods for web scraping Edmonton web site.
- main.py: main file that contain the code to execute the web scraping and save the CSV files.
- /data: a sugested directory to save the CSV files
  - categories_url_example.csv: example file that contain categories URL scraped
  - companies_url_example.csv: example file that contain companies URL scraped
  - companies_data_example.csv: example file that contain company data scraped

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.
