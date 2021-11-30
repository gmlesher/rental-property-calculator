from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from time import sleep
import json

# my files
from .parse import Parse
from .scrape import RedfinScraper, ZillowScraper
from .search import CreateSearchUrl
from .models import BotRentalReport


class RedfinBot():
    def __init__(self, user):
        self.user = user
        self.url = CreateSearchUrl.get_complete_url(CreateSearchUrl(self.user))
        self.parsed_urls = []
        self.all_data = None

    def webdriver(self):
        """Opens chrome webpage, downloads csv file"""
        # allows chrome to download csv file in headless mode
        chrome_options = Options()
        chrome_options.add_experimental_option("prefs", {
        "download.default_directory": "/Users/garrettlesher/Downloads/",
        "download.prompt_for_download": False,
        })
        chrome_options.add_argument("--headless")
        self.driver = webdriver.Chrome(chrome_options=chrome_options)
        self.driver.command_executor._commands["send_command"] = ("POST", '/session/$sessionId/chromium/send_command')
        params = {'cmd': 'Page.setDownloadBehavior', 'params': {'behavior': 'allow', 'downloadPath': "/Users/garrettlesher/Downloads/"}}
        self.driver.execute("send_command", params)

        print("Opening webpage with search URL...")
        self.driver.get(self.url)
        sleep(2)
        self.driver.find_element_by_xpath("//a[@id=\"download-and-save\"]")\
            .click()
        print("Downloading csv file...")
        sleep(5)

    def parse_csv_data(self):
        """Parses csv file downloaded in 'webdriver' function above"""
        self.parsed_data = Parse.run(Parse(self.user))
        current_urls = []
        # check current redfin urls. avoid scraping urls already in reports
        objs = BotRentalReport.objects.filter(owner=self.user).values()
        for obj in objs:
            current_urls.append(obj['redfin_listing_url'])
        # only scrape urls for reports not already added
        for key in self.parsed_data:
            parsed_url = self.parsed_data[key]['URL (SEE https://www.redfin.com/buy-a-home/comparative-market-analysis FOR INFO ON PRICING)']
            if not parsed_url in current_urls:
                self.parsed_urls.append(parsed_url)

    def scrape(self):
        """scrapes all webpages from list of parsed csv file urls"""
        print("Scraping Redfin URLs...")
        self.scraped_data = RedfinScraper().run(self.parsed_urls)

    def combine(self):
        """combines parsed and scraped data into one dictionary"""
        final_copy = self.parsed_data.copy()
        scraped = self.scraped_data.copy()
        keep_list = []
        # get final copy items that need to be created that aren't duplicates
        for i in list(final_copy):
            for url in self.parsed_urls:
                if url == final_copy[i]['URL (SEE https://www.redfin.com/buy-a-home/comparative-market-analysis FOR INFO ON PRICING)']:
                    keep_list.append(i)
            # delete duplicates
            if i not in keep_list:
                del final_copy[i]

        for i, v in enumerate(list(final_copy.keys())):
            final_copy[i] = final_copy.pop(v, None)

        # adds values of each dictionary in 'scraped' to end of each respective \
        # 'final copy' dictionary based on key values
        for key, value in enumerate(scraped): 
            final_copy[key]['DESCRIPTION'] = value['DESCRIPTION']
            final_copy[key]['ANNUAL TAXES'] = value['ANNUAL TAXES']
            final_copy[key]['HOMEOWNERS INSURANCE'] = value['HOMEOWNERS INSURANCE']
            final_copy[key]['HOA'] = value['HOA']
            final_copy[key]['IMAGE NAME'] = value['IMAGE NAME']

            street = '-'.join(i for i in final_copy[key]['ADDRESS'].split(' '))
            city = f"-{final_copy[key]['CITY']}"
            state = f"-{final_copy[key]['STATE OR PROVINCE']}"
            zip = f"-{final_copy[key]['ZIP OR POSTAL CODE']}"
            addr = street.lower() + city.lower().replace(' ', '-') +  state.lower() + zip.lower()
            zest_url = f'https://www.zillow.com/rental-manager/price-my-rental/results/{addr}/'
            final_copy[key]['ZESTIMATE URL'] = zest_url
            final_copy[key]['ZESTIMATE'] = ZillowScraper().run(zest_url)
        
        self.all_data = final_copy

    def run(self):
        """runs RedfinBot"""
        print(f'Running bot for {self.user.username}')
        print(f'Search URL: {self.url}')
        self.webdriver()
        self.parse_csv_data()
        if self.parsed_urls:
            self.scrape()
            print("Scraping Zillow URLs...")
            self.combine()
            return self.all_data
        else: 
            print("No new properties to report on")
            return
