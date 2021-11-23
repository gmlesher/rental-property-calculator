import pandas as pd
import os


class Parse():
    """Parse class"""
    def __init__(self):
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