import requests, urllib.request, time, re
from bs4 import BeautifulSoup

# my files
from headers import headers


class RedfinScraper():
    """Scrapes websites for property data"""
    def __init__(self):
        self.results = []
        self.headers = headers

    def fetch(self, url):
        """fetch url"""
        response = requests.get(url, headers=self.headers)
        print(response.status_code)
        return response

    def parse(self, response):
        """parse given html responses for data"""
        content = BeautifulSoup(response, 'html.parser')
        desc = content.select_one('div.remarks > p.text-base > span').text

        find_taxes = content.find_all(text=re.compile('^Full Tax Amount: $|^Tax Annual Amount: $'))
        taxes = [tax.parent for tax in find_taxes]
        if taxes:
            tax_amt = taxes[0].find('span').text
        else:
            tax_amt = 0

        find_hi = content.find_all(text=re.compile("^Homeowners' Insurance$"))
        h_i = [hi.parent.parent.parent.parent for hi in find_hi]
        if h_i:
            hi_amt = h_i[0].find('span', {'class': 'Row--content text-right'}).text
        else:
            hi_amt = 0

        find_hoa = content.find_all(text=re.compile('^Association Fee: $'))
        hoa = [hoa.parent for hoa in find_hoa]
        find_hoa_freq = content.find_all(text=re.compile('^Association Fee Frequency: $'))
        hoa_freq = [hoa_freq.parent for hoa_freq in find_hoa_freq]

        cleaned_hoa_amt = 0
        if hoa:
            if hoa_freq:
                hoa_freq_timeframe = hoa_freq[0].find('span').text
            else:
                hoa_freq_timeframe = ''

            if hoa_freq_timeframe == 'Monthly':
                hoa_amt = hoa[0].find('span').text
                if ',' in hoa_amt:
                    hoa_amt = hoa_amt.replace(',', '')
                cleaned_hoa_amt = int(hoa_amt.strip('$'))
            elif hoa_freq_timeframe == 'Annually' or hoa_freq_timeframe == 'Annual':
                hoa_amt = hoa[0].find('span').text
                if ',' in hoa_amt:
                    hoa_amt = hoa_amt.replace(',', '')
                cleaned_hoa_amt = int(hoa_amt.strip('$')) / 12
            else:
                cleaned_hoa_amt = 0
            
        prop_image = content.select_one('img.img-card').get('src')
        image_name = '_'.join(prop_image.split('/')[5:])

        # saves image to downloads folder
        urllib.request.urlretrieve(prop_image, image_name)

        self.results.append({
            'DESCRIPTION': desc,
            'ANNUAL TAXES': tax_amt,
            'HOMEOWNERS INSURANCE': hi_amt,
            'HOA': str(cleaned_hoa_amt),
            'IMAGE NAME': image_name,
        })
    
    def run(self, url_list):
        """run Redfin Scraper"""
        for url in url_list:
            res = self.fetch(url)
            self.parse(res.text)
            time.sleep(2)

        return self.results


# if __name__ == '__main__':
#     scraper = RedfinScraper()
#     scraper.run()