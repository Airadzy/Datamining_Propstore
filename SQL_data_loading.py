import pymysql
import csv
from pathlib import Path
from datetime import datetime

connection = pymysql.connect(host='localhost', user='root', password='root', database="Propstore_details",
                             cursorclass=pymysql.cursors.DictCursor)


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


def create_or_get_id(cursor, table, column, value):
    cursor.execute(f"SELECT {table}_id FROM {table} WHERE {column} = %s", (value,))
    result = cursor.fetchone()
    if result:
        return result[f"{table}_id"]

    # If not, insert the new record and return the new ID
    cursor.execute(f"INSERT INTO {table} ({column}) VALUES (%s)", (value,))
    return cursor.lastrowid


def create_or_get_status_id(cursor, status, sold_date):
    # Check if the status record already exists and get its ID
    cursor.execute("SELECT status_id FROM status WHERE status = %s AND sold_date = %s", (status, sold_date))
    result = cursor.fetchone()
    if result:
        return result['status_id']

    # If not, insert the new record and return the new ID
    cursor.execute("INSERT INTO status (status, sold_date) VALUES (%s, %s)", (status, sold_date))
    return cursor.lastrowid


path = Path("./Propstore_data.csv")

with connection.cursor() as cursor:
    with open(path, "r") as file:
        reader = csv.DictReader(file)
        for row in reader:
            price, currencies = parse_price(row["price"]) if row["price"] else (None, None)
            sold_date = parse_date(row["sold_date"]) if row["sold_date"].strip() else None

            categories = row["category"]
            movie_name = row["movie_name"]
            card_title = row["card_title"]
            status = row["button"]

            categories_id = create_or_get_id(cursor, 'categories', 'categories', categories)
            movies_id = create_or_get_id(cursor, 'movies', 'movies_name', movie_name)
            currencies_id = create_or_get_id(cursor, 'currencies', 'currencies', currencies)
            status_id = create_or_get_status_id(cursor, status, sold_date)

            if categories_id and movies_id and status_id and currencies_id:
                cursor.execute(
                    "INSERT INTO items (description,categories_id,status_id,movies_id,price,currencies_id) VALUES (%s,%s,%s,%s,%s,%s)",
                    (card_title, categories_id, status_id, movies_id, price, currencies_id))

            connection.commit()
connection.close()