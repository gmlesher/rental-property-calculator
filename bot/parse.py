import pandas as pd
import os, glob


class Parse():
    """Parse class"""
    def __init__(self):
        self.data = None
        self.read_path = '/Users/garrettlesher/Downloads/'
        self.extension = '*.csv'

    def parse_csv(self):
        """parses most recent csv files in downloads folder"""
        print('Parsing downloaded csv file...')
        files = glob.glob(self.read_path + self.extension)
        latest_file = max(files, key=os.path.getctime)
        df  = pd.read_csv(latest_file)
        self.data = df.T.to_dict('dict')
        try:
            os.remove(latest_file) # removes the file
        except OSError:
            pass

    def run(self):
        """runs Parse class"""
        self.parse_csv()
        return self.data