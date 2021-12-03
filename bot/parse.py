# 3rd party imports
import pandas as pd
import os

# My file imports
from calculator.models import UserSettings

class Parse():
    """Parses csv files"""
    def __init__(self,  user):
        self.user = user
        self.data = None
        self.read_path = '/Users/garrettlesher/Downloads/'
        self.extension = '.csv'

    def parse_csv(self):
        """parses most recent csv files in downloads folder"""
        print('Parsing downloaded csv file...')
        csv_files = []
        for file in os.listdir(self.read_path):
            if file.endswith(self.extension):
                csv_files.append(os.path.join(self.read_path, file))
        latest_file = max(csv_files, key=os.path.getctime)

        usr_settings = UserSettings.objects.get(user=self.user)
        current_json = getattr(usr_settings, 'addr_blacklist')

        df  = pd.read_csv(latest_file) # creates dataframe of latest csv file
        df_addrs = df["ADDRESS"] + " " + df["CITY"] + "," + " " + \
            df["STATE OR PROVINCE"] + " " + df["ZIP OR POSTAL CODE"].astype(str)

        drop_list = [] #list of addresses that need to be dropped from dataframe
        for parsed_addr in df['ADDRESS']:
            for concat_addr in df_addrs:
                if parsed_addr in concat_addr and \
                    concat_addr in current_json[self.user.username]['addresses']:
                    drop_idx = df.index[df["ADDRESS"] == parsed_addr].item()
                    drop_list.append(drop_idx)
                    print(f'Blacklisted address found: {concat_addr}')

        if drop_list:
            df.drop(drop_list, inplace=True) 
            print("Blacklisted addresses skipped...")
        self.data = df.T.to_dict('dict')
        
        try:
            os.remove(latest_file) # removes the file from downloads
        except OSError:
            print("Error removing latest downloaded csv file")

    def run(self):
        """runs Parse class"""
        self.parse_csv()
        return self.data
