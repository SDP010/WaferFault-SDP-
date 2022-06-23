import pandas as pd
from Logger import Applogger

class Data_loader:
    """
        This class should be used for loadig the data from the source
    """

    def __init__(self):
        self.training_file = 'Training_file_fromdb/Training_Input_file.csv'
        self.logger = Applogger()


    def get_data(self):
        try:
            file = open('Logs/Training_Logs/training_log.txt', 'a+')
            df = pd.read_csv(self.training_file)
            self.logger.log(file, 'Data loaded sucessfully!!')
            return df
        except Exception as e:
            raise e
