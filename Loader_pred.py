import pandas as pd
from Logger import Applogger

class Data_loader_Pred:
    """
        This class should be used for loadig the data from the source
    """

    def __init__(self):
        self.prediction_file = 'Prediction_file_fromdb/Input_file.csv'
        self.logger = Applogger()


    def get_data(self):
        try:
            file = open('Logs/Prediction_Logs/prediction_log.txt', 'a+')
            data = pd.read_csv(self.prediction_file)
            self.logger.log(file, 'data loaded into pandas dataframe')
            return data
        except Exception as e:
            raise e