# Web Scraping of Edmonton Chamber Web Site

A web scraping project focused on scrap companies data from the Edmonton Chamber directory website: [https://business.edmontonchamber.com/list](https://business.edmontonchamber.com/list)

It was a freelancer working for a client. The main system contains the following steps for scraping the data.

1. Scrap all category URLs from the Edmonton Chamber directory website.
2. Save categories URL on CSV file.
3. Scrap all company URLs existing on categories URLs.
4. Save company URLs on CSV file.
5. Scrap company information from the company page on the Edmonton Chamber Site.
6. Scrap company email from each company website. Because it is not available on the Edmonton Chamber site.

## Code

The code contains:

- webscraping.py: a generic class that contains some common methods for general web scraping purposes.
- scrapedmontchamber.py: a specific class that contains specific methods for web scraping Edmonton website.
- main.py: main file that contains the code to execute the web scraping and save the CSV files.
- /data: a suggested directory to save the CSV files:
  - categories_url_example.csv: example file that contains categories URL scraped.
  - companies_url_example.csv: example file that contains companies URL scraped.
  - companies_data_example.csv: example file that contains company data scraped.

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.
