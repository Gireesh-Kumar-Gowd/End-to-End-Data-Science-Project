import os
import sys
from src.DataScienceProject.exception import CustomException
from src.DataScienceProject.logger import logging
import pandas as pd
from dotenv import load_dotenv

import pymysql

import pickle
import numpy as np

load_dotenv()

host=os.getenv("host")
user=os.getenv("user")
password=os.getenv("password")
db=os.getenv('db')



def read_sql_data():
    logging.info("Reading SQL database started")
    mydb = None
    try:
        mydb = pymysql.connect(
            host=host,
            user=user,
            password=password,
            db=db
        )
        logging.info("Connection established to %s/%s", host, db)
        cursor = mydb.cursor()
        cursor.execute('Select * from students')
        data = cursor.fetchall()
        columns = [column[0] for column in cursor.description]
        df = pd.DataFrame(data, columns=columns)
        print(df.head())

        return df

    except Exception as ex:
        raise CustomException(ex)
    finally:
        if mydb is not None:
            mydb.close()

def save_object(file_path, obj):
    try:
        dir_path = os.path.dirname(file_path)

        os.makedirs(dir_path, exist_ok=True)

        with open(file_path, "wb") as file_obj:
            pickle.dump(obj, file_obj)

    except Exception as e:
        raise CustomException(e, sys)