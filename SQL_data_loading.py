import pymysql
import csv
from pathlib import Path
from datetime import datetime

connection = pymysql.connect(host='localhost', user='root', password='root', database="Propstore_details5",
                             cursorclass=pymysql.cursors.DictCursor)


def insert_query(query, data):
    try:
        with connection.cursor() as cursor:
            cursor.execute(query, data)
            connection.commit()
            return cursor.lastrowid
    except Exception as error:
        print(f"SQL error: {error}")
        return None


def parse_price(price_str):
    try:
        currency = price_str[0]
        value = price_str[1:].replace(",", "")
        return float(value), currency
    except Exception as error:
        print(f"Error in parsing price: {error}")
        return None, None


def parse_date(date_str):
    try:
        date_str = date_str.replace("Sold on ", "")
        date_ref = datetime.strptime(date_str, "%d %b, %Y").date()
        return date_ref
    except Exception as error:
        print(f"error in parsing date: {error}")
        return None


path = Path("./Propstore_data.csv")

with open(path, "r") as file:
    reader = csv.DictReader(file)
    for count, row in enumerate(reader,start=1):
        status = row["button"]
        categories = row["category"]
        movie_name = row["movie_name"]
        card_title = row["card_title"]
        price, currencies = parse_price(row["price"]) if row["price"] else (None, None)
        sold_date = parse_date(row["sold_date"]) if row["sold_date"].strip() else None

        categories_id = insert_query("INSERT IGNORE INTO categories (categories) VALUES (%s)", (categories,))
        movies_id = insert_query("INSERT IGNORE INTO movies (movies_name) VALUES (%s)", (movie_name,))
        status_id = insert_query("INSERT IGNORE INTO status (status, sold_date) VALUES (%s, %s)",
                                 (status, sold_date))
        currencies_id = insert_query("INSERT IGNORE into currencies (currencies) VALUES (%s)", (currencies,))
        if categories_id and movies_id and status_id and currencies_id:
            insert_query(
                "INSERT INTO items (description,categories_id,status_id,movies_id,price,currencies_id) VALUES (%s,%s,%s,%s,%s,%s)",
                (card_title, categories_id, status_id, movies_id, price, currencies_id))

            connection.commit()
