import pandas as pd
import os, glob


class Parse():
    """Parse class"""
    def __init__(self):
        self.data = None
        self.read_path = '/Users/garrettlesher/Downloads'
        self.extension = 'csv'

    def parse_csv(self):
        """parses most recent csv files in downloads folder"""
        print('running parse_csv')
        os.chdir(self.read_path)
        result = glob.glob(f'*.{self.extension}')

        for file in result:
            df = pd.read_csv(file)
            self.data = df.T.to_dict('dict')
        return self.data

    # *Dont need this function if running through another class *
    def run(self):
        """runs Parse class"""
        self.parse_csv()
        

# Parse().run()