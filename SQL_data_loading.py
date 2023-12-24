import pymysql
from datetime import datetime
import re



def load_data(items_list, connection):
    """
    Main function to load data from a CSV file into the Propstore_details database.
    It processes each row in the CSV, parses various fields, and inserts them into the database.
    :return: None
    """

    def parse_movie_name_and_year(movie_item):
        """
        Parses a string containing a movie's name and its release year.

        :param movie_item: A string in the format "Movie Name (Release Year)".
        :return: A tuple containing the movie's name and release year. Returns (None, None) if parsing fails or the format is incorrect.
        """

        try:
            match = re.search(r"\(\d", movie_item)
            if match:
                movies_name_position = match.start()
                full_movie_name = movie_item[:movies_name_position].strip()
                if full_movie_name.lower().endswith(", the"):
                    movies_name = full_movie_name.rsplit(',', 1)[0].strip()
                else:
                    movies_name = full_movie_name

                release_year = movie_item[movies_name_position + 1:movies_name_position + 5]

                return movies_name, release_year
            else:
                return movie_item, None
        except Exception as error:
            print(f"Error in parsing movie name and year: {error}")
            return None, None

    def parse_price(price_str):
        """
        Parse a price string and extract the currency and value.

        :param price_str: A string representing the price (e.g., "$1,000").
        :return: A tuple containing the numerical value of the price and its currency symbol. Returns (None, None) if parsing fails.
        """

        try:
            currency = price_str[0]
            value = price_str[1:].replace(",", "")
            return float(value), currency
        except Exception as error:
            print(f"Error in parsing price: {error}")
            return None, None

    def parse_date(date_str):
        """
        Parse a date string into a Python date object.

        :param date_str: A string representing the date (e.g., "Sold on 01 Jan, 2020").
        :return: A datetime.date object representing the date. Returns None if parsing fails.
        """

        try:
            date_str = date_str.replace("Sold on ", "")
            date_ref = datetime.strptime(date_str, "%d %b, %Y").date()
            return date_ref
        except Exception as error:
            print(f"error in parsing date: {error}")
            return None

    def create_or_get_id(cursor, table, column, value):
        """
        Retrieve or create an ID for a given value in a specified table and column.

        :param cursor: The database cursor for executing queries.
        :param table: The name of the table in the database.
        :param column: The name of the column in the table.
        :param value: The value to search or insert in the table.
        :return: The ID of the existing or newly inserted value.
        """

        cursor.execute(f"SELECT {table}_id FROM {table} WHERE {column} = %s", (value,))
        result = cursor.fetchone()
        if result:
            return result[f"{table}_id"]

        # If not, insert the new record and return the new ID
        cursor.execute(f"INSERT INTO {table} ({column}) VALUES (%s)", (value,))
        return cursor.lastrowid

    def create_or_get_status_id(cursor, status, sold_date):
        """
        Retrieve or create a status ID for a given status and sold date.

        :param cursor: The database cursor for executing queries.
        :param status: The status of the item.
        :param sold_date: The date when the item was sold.
        :return: The ID of the existing or newly inserted status.
        """

        cursor.execute("SELECT status_id FROM status WHERE status = %s AND sold_date = %s", (status, sold_date))
        result = cursor.fetchone()
        if result:
            return result['status_id']

        cursor.execute("INSERT INTO status (status, sold_date) VALUES (%s, %s)", (status, sold_date))
        return cursor.lastrowid

    def create_or_get_movies_id(cursor, movies_name, release_year):
        """
        Retrieve or create a status ID for a given status and sold date.

        :param cursor: The database cursor for executing queries.
        :param status: The status of the item.
        :param sold_date: The date when the item was sold.
        :return: The ID of the existing or newly inserted status.
        """
        try:
            cursor.execute("SELECT movies_id FROM movies WHERE movies_name = %s", (movies_name,))
            result = cursor.fetchone()
            if result:
                return result['movies_id']

            cursor.execute("INSERT INTO movies (movies_name, release_year) VALUES (%s, %s)",
                           (movies_name, release_year))
            return cursor.lastrowid
        except pymysql.err.IntegrityError as e:
            print(f"Integrity error: {e}")

    with connection.cursor() as cursor:
        for item in items_list:
            price, currencies = parse_price(item[4]) if item[4] else (None, None)
            movies_name, release_year, = parse_movie_name_and_year(item[2]) if item[2] else (
                None, None)
            sold_date = parse_date(item[5]) if item[5] else None

            categories = item[1]
            card_title = item[3]
            status = item[0]

            categories_id = create_or_get_id(cursor, 'categories', 'categories', categories)
            movies_id = create_or_get_movies_id(cursor, movies_name, release_year)
            currencies_id = create_or_get_id(cursor, 'currencies', 'currencies', currencies)
            status_id = create_or_get_status_id(cursor, status, sold_date)

            if categories_id and movies_id and status_id and currencies_id:
                cursor.execute(
                    "INSERT INTO items (description,categories_id,status_id,movies_id,price,currencies_id) VALUES ("
                    "%s,%s,%s,%s,%s,%s)",
                    (card_title, categories_id, status_id, movies_id, price, currencies_id))
            connection.commit()
