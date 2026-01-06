import sqlite3
import pandas as pd
from sqlite3 import Connection, Cursor
from pandas import DataFrame
import numpy as np


class Metro():
    def __init__(self, country: str, name: str, state: str, population: int, lat: float, lng: float):
        self.country: str = country
        self.name: str = name
        self.state: str = state
        self.population: int = population
        self.lat: float = lat
        self.lng: float = lng


# Function to write a data frame into a SQL table of an existing SQL database
def df_to_sql(df: DataFrame, cur: Cursor, table_name: str, db_name: str, conn: Connection):
    res = cur.execute("SELECT name FROM sqlite_master")
    if res.fetchone() is None:
        cur.execute(f"CREATE TABLE {table_name}(country, metro, state, population, lat, lng)")
    else:
        print('Table already exists.')
        cur.execute(f"DELETE FROM {table_name}")
    
    for index, row in df.iterrows():
        metro_str: str = str(row['Metro Area'])
        
        metro_index: int = metro_str.rfind("'")
        if metro_str.rfind("'") != -1:
            metro_str = metro_str[:metro_index] + "'" + metro_str[metro_index:] 
            
        pop_str: str = np.char.replace(row['Population'], ',', '')
        cur.execute(f"INSERT INTO {table_name} VALUES ('{str(row['Country'])}', '{metro_str}', '{str(row['State'])}', {int(pop_str)}, {float(row['lat'])}, {float(row['lng'])})")
    
    conn.commit()


#connect to the sqlite database
def connect() -> Connection:
    db_name: str = 'na_metros.db'
    conn: Connection = sqlite3.connect(db_name)
    return conn


# Create a SQL database from metros.csv
def create_database(conn: Connection):
    df: DataFrame = pd.read_csv('data/csv/na_metros.csv')

    db_name: str = 'na_metros.db'
    table_name: str = 'na_metros'

    cur: Cursor = conn.cursor()

    df_to_sql(df, cur, table_name, db_name, conn) 



def find_metro(metro_name: str, conn: Connection, debug: bool = False) -> Metro:
    table_name: str = 'na_metros'
    cur: Cursor = conn.cursor()
    cur = cur.execute(f"SELECT * FROM {table_name} WHERE metro LIKE '%{metro_name}%'")
    res: tuple = cur.fetchone()

    if res:
        metro: Metro = Metro(res[0], res[1], res[2], res[3], res[4], res[5])
        if debug:
            print(f"Found metro area: {metro.name, metro.state}")
        return metro
    else:
        if debug:
            print(f"No metro area found containing '{metro_name}'")
        return None