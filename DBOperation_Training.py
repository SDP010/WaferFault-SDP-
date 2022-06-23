import csv
import shutil
import mysql.connector as connection
from Logger import Applogger
import os
from os import  listdir

class DBOperation:
    """
            This class shall be use for handling all the SQL operation
    """

    def __init__(self):
        self.path = 'Training_Database/'
        self.good_file_path = 'Training_raw_files_validated/Good_Raw/'
        self.bad_file_path = 'Training_raw_files_validated/Bad_Raw/'
        self.logger = Applogger()



    def db_connector(self,db_name):
        """
            Method Name : db_connector
            Description : This method creates the database with the given name and
                          if Database already exists then opens the connection to the DB.
            Output : database connection
            On Failure : Raise exception
        """
        file = open('Logs/Training_Logs/training_log.txt', 'a+')
        try:
            conn = connection.connect(host='localhost', user='root', passwd='Subhra@1234')
            cursor = conn.cursor()

            try:
                cursor.execute(f'create database {db_name}')
                cursor.execute(f'use {db_name}')
            except:
                cursor.execute(f'use {db_name}')

            self.logger.log(file, 'Connection established successfully !!')
            file.close()

        except Exception as e:
            raise e
        return conn



    def create_table(self, db_name, col_names):
        """
           Method Name : create_table
           Description : This method creates a table in the given database which will be used for
                         inserting the good raw training data.
           Output : None
           On Failure : Raise exception

        """

        try:
            file = open('Logs/Training_Logs/training_log.txt', 'a+')
            conn = self.db_connector(db_name=db_name)
            cursor = conn.cursor()
            cursor.execute(f'use {db_name}')
            cursor.execute('drop table if exists Good_Raw_Data')
            for key in col_names:
                type = col_names[key]
                key1 = key.replace(' - ','_')
                try:
                    cursor.execute(f'create table Good_Raw_Data ({key1} {type}(20))')
                except:
                    cursor.execute(f'alter table Good_Raw_Data add ({key1} {type}(20))')
                    self.logger.log(file, 'alter table Good_Raw_Dataa!!')
            conn.commit()
            conn.close()
            file.close()

        except Exception as e :
            raise e




    def insert_good_data_into_table(self, db_name):
        """
            Method Name : insert_good_data_into_table
            Description : This method inserts the good raw training data from the folder
                          inside the given database.
            Output : None
            On Failure : Raise Exception

        """
        # file_1 = open('Logs/Training_Logs/training_log.txt', 'a+')
        conn = self.db_connector(db_name= db_name)
        cursor = conn.cursor()
        good_file_path = self.good_file_path
        bad_file_path = self.bad_file_path
        onlyfiles = [file for file in listdir(good_file_path)]
        try :
            for file in onlyfiles :
                try:
                    with open(good_file_path + file) as f :
                        next(f)
                        reader = csv.reader(f, delimiter='\n')
                        for line in enumerate(reader):
                            for l in line[1]:
                                try:
                                    cursor.execute(f'insert into Good_Raw_Data values ({l})')
                                    conn.commit()
                                except Exception as e :
                                    raise e
                    # self.logger.log(file_1, f'{file} loaded to database sucessfully!!')
                    # file_1.close()

                except Exception as e:
                    raise e

        except Exception as e:
            conn.close()
            raise e


    def export_data_from_table_into_final_csv(self, db_name):
        """
            Method Name : export_data_from_table_into_final_csv
            Description : This method exports the good data into a csv file.
            Output : None
            On Failure : Raise exception

        """
        file = open('Logs/Training_Logs/training_log.txt', 'a+')
        self.file_fromdb = 'Training_file_fromdb/'
        self.file_name = 'Training_Input_file.csv'
        # if os.path.isdir(self.file_fromdb):
        #     shutil.rmtree(self.file_fromdb)    # pore final run er time e checking krte hobe
        try:
            conn = self.db_connector(db_name=db_name)
            cursor = conn.cursor()
            cursor.execute('use TrainingDB')
            cursor.execute('select * from Good_Raw_Data')
            result = cursor.fetchall()
            headers = [i[0] for i in cursor.description]   # get the headers of the csv file
            # making the csv output directory
            if not os.path.isdir(self.file_fromdb):
                os.makedirs(self.file_fromdb)

            # open csv file for writting
            csv_file = csv.writer(open(self.file_fromdb + self.file_name, 'w', newline=''), delimiter=',')
            csv_file.writerow(headers)
            csv_file.writerows(result)
            self.logger.log(file,'Data Successfully Exported')
            conn.close()
            file.close()

        except Exception as e:
            raise e


