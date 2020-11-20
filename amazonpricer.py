import locale
import sqlite3
import sys
import unicodedata

import click
import pandas as pd
import requests
from bs4 import BeautifulSoup
from tabulate import tabulate

locale.setlocale(locale.LC_NUMERIC, '')

headers = {
  'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Mobile Safari/537.36'
}
default_db_file = 'db.sqlite3'


class Config(object):
    def __init__(self):
        self.db_connection = None
        pass

pass_config = click.make_pass_decorator(Config, ensure=True)

def check_if_database_exist(db_cursor):
    db_cursor.execute(""" SELECT count(name) FROM sqlite_master WHERE type='table' AND name='products' """)
    #if the count is 1, then table exists
    if db_cursor.fetchone()[0]==1: 
        return 0
    else :
        print('Table does not exist.')
        #sys.exit.
        return None

def printLocale():
    loc = locale.getlocale()
    print(loc)

#title = soup.find(id="title", class_="a-size-small").get_text()
def create_table(db_cursor):
    print('creating new tables')
    sql_create_projects_table = """ CREATE TABLE IF NOT EXISTS products (
                                        product_id text PRIMARY KEY,
                                        price_wanted real NOT NULL,
                                        prices_last_seen real
                                    ); """
    try:
        db_cursor.execute(sql_create_projects_table)
    except Exception as e:
        print(e)

def getProductPrice(productid: str = None):
    if productid == None:
        print('Cant get price. No productID provided. IDs are like: B0748KLR39')
        price = None
    else:
        try:
            url = 'https://www.amazon.de/gp/product/'+productid.upper()+'/'
            page = requests.get(url, headers=headers)
            soup = BeautifulSoup(page.content, features="lxml")
            price = getPrice(soup)
        except:
            print('cant get price for: ' + productid )
            price = None
    return price

def getPrice(soupPage: BeautifulSoup) -> float:
    def StripPrice(priceRaw: str = '0.00€') -> float:
        priceRaw = unicodedata.normalize("NFKD", priceRaw)
        priceRaw = "".join(priceRaw.split())
        priceRaw = priceRaw.strip()
        price = float(locale.atof(priceRaw[:-1]))
        return price
    priceRaw = soupPage.find(id="priceblock_ourprice").get_text()
    price = StripPrice(priceRaw)
    return price

def create_connection(db_file=default_db_file):
    """ create a database connection to a SQLite database """
    db_connection = None
    try:
        db_connection = sqlite3.connect(db_file)
        db_cursor = db_connection.cursor()
        #print(sqlite3.version)
        if check_if_database_exist(db_cursor) != 0:
            create_table(db_cursor)
        return db_connection
    except Exception as e:
        print(e)

def create_db_cursor(db_file=default_db_file):
    """ returns a ready to use cursor """
    db_connection = create_connection(db_file)
    db_cursor = db_connection.cursor()
    return db_cursor

@click.group()
@pass_config
def main(config):
    #add_product(db_cursor, args.product_id, args.price, getProductPrice(args.product_id))
    #add_product(db_cursor, 'B0748KLR39', 19.00, getProductPrice('B0748KLR39'))
    #list_products(db_connection)
    config.db_connection=create_connection()

@main.command()
def huhu():
    print('huhu bam')
    
@main.command()
@pass_config
@click.option('-a', '--add', 'product_id', help='add a productid to the database', type=str)
@click.option('-p', '--price', 'price_wanted', type=float)
def add(config, product_id, price_wanted):
    def add_product(db_connection, product_id, price_wanted, prices_last_seen = None):
        sql_add_product = "INSERT INTO products (product_id, price_wanted, prices_last_seen) VALUES (?, ?, ?)"
        try:
            db_cursor = create_db_cursor(db_connection)
            db_cursor.execute(sql_add_product, (product_id, price_wanted, prices_last_seen))
            config.db_connection.commit()

        except Exception as e:
            print(e)

    add_product(config.db_connection, product_id, price_wanted)
    print('product added.')
    ls(config)

@main.command()
@pass_config
def ls(config):
    print('listing products: ')
    sql_list_products = """ SELECT * FROM products; """
    try:
        df = pd.read_sql_query(sql_list_products, config.db_connection)
        df['buy?'] = df['prices_last_seen'] < df['price_wanted']
        df = df.replace(True, 'x')
        df = df.replace(False, '')
        print(tabulate(df, headers='keys', tablefmt='psql',stralign='center'))
    except Exception as e:
        print('list_products crashed')
        print(e)


if __name__ == "__main__":
    main()
