from selenium import webdriver
from time import sleep

# my files
from parse import Parse
from scrape import RedfinScraper

# replace with city from settings
city = 'Louisburg'
city_code = str(10915)
state = 'KS'
city_url = f'city/{city_code}/{state}/{city}/'

# replace with zipcode from settings
zipcode = '04981'
zip_code_url = f'zipcode/{zipcode}/'

# replace with filters from settings
filters = 'property-type=house,max-price=300k' 
filters_url = f'filter/{filters}'

# complete_url = f'https://www.redfin.com/{zip_code_url}{filters_url}'
complete_url = f'https://www.redfin.com/{city_url}{filters_url}'


class RedfinBot():
    def __init__(self):
        self.url = complete_url
        self.driver = webdriver.Chrome()
        self.parsed_urls = []

    def webdriver(self):
        """Opens chrome webpage, downloads csv file"""
        # needs work to operate headless with ability to download files
        # op = webdriver.ChromeOptions() # chrome options
        # op.add_argument('headless') # add headles option
        # self.driver = webdriver.Chrome(options=op) # open chrome driver headless
        self.driver.get(self.url)
        sleep(2)
        self.driver.find_element_by_xpath("//a[@id=\"download-and-save\"]")\
            .click()
        sleep(5)

    def parse_csv_data(self):
        """Parses csv file downloaded in 'webdriver' function above"""
        self.parsed_data = Parse.parse_csv(Parse())
        for key in self.parsed_data:
            parsed_url = self.parsed_data[key]['URL (SEE http://www.redfin.com/buy-a-home/comparative-market-analysis FOR INFO ON PRICING)']
            self.parsed_urls.append(parsed_url)

    def scrape(self):
        """scrapes all webpages from list of parsed csv file urls"""
        self.scraped_data = RedfinScraper().run(self.parsed_urls)

    def combine(self):
        """combines parsed and scraped data into one dictionary"""
        final_copy = self.parsed_data.copy()
        scraped = self.scraped_data.copy()
        
        # adds values of each dictionary in 'scraped' to end of each respective \
        # 'final copy' dictionary based on key values
        for key, value in enumerate(scraped): 
            final_copy[key]['DESCRIPTION'] = value['DESCRIPTION']
            final_copy[key]['ANNUAL TAXES'] = value['ANNUAL TAXES']
            final_copy[key]['HOMEOWNERS INSURANCE'] = value['HOMEOWNERS INSURANCE']
            final_copy[key]['HOA'] = value['HOA']
            final_copy[key]['IMAGE NAME'] = value['IMAGE NAME']

        print(final_copy)
        

    def run(self):
        """runs RedfinBot"""
        self.webdriver()
        self.parse_csv_data()
        self.scrape()
        self.combine()


RedfinBot().run()