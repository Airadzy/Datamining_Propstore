import pymysql
import pymysql.err
import SQL_data_loading
from pathlib import Path
import logging
import main_file
from main_file import load_config

logging.basicConfig(filename=main_file.log_filename,
                    format='%(asctime)s-%(levelname)s-FILE:%(filename)s-FUNC:%(funcName)s-LINE:%(lineno)d-%(message)s',
                    level=logging.INFO)

connection_without_database = pymysql.connect(host='localhost', user='root', password='root',
                                              cursorclass=pymysql.cursors.DictCursor)


def create_database():
    with connection_without_database.cursor() as cursor:
        try:
            cursor.execute("CREATE DATABASE propstore_details;")
        except (pymysql.err.ProgrammingError, pymysql.err.InternalError) as error:
            print(f"Database already exists so inserting new data into database")
        try:
            cursor.execute("USE propstore_details;")
            cursor.execute("""
                    CREATE TABLE IF NOT EXISTS categories(
                        categories_id INT AUTO_INCREMENT PRIMARY KEY,
                        categories VARCHAR(255) UNIQUE
                    )
                """)
            cursor.execute("""
                    CREATE TABLE IF NOT EXISTS movies (
                        movies_id INT AUTO_INCREMENT PRIMARY KEY,
                        movies_name VARCHAR(255) UNIQUE 
                    )
                """)
            cursor.execute("""
                    CREATE TABLE IF NOT EXISTS status (
                        status_id INT AUTO_INCREMENT PRIMARY KEY,
                        status VARCHAR(255) ,
                        sold_date DATE
                    )
                """)
            cursor.execute("""
                    CREATE TABLE IF NOT EXISTS currencies (
                        currencies_id INT AUTO_INCREMENT PRIMARY KEY,
                        currencies VARCHAR(255) UNIQUE
                    )
                """)
            cursor.execute("""
                    CREATE TABLE IF NOT EXISTS items (
                        items_id INT AUTO_INCREMENT PRIMARY KEY,
                        description VARCHAR(255),
                        categories_id INT,
                        status_id INT,
                        movies_id INT,
                        price VARCHAR(255),
                        currencies_id INT,
                        FOREIGN KEY (categories_id) REFERENCES categories (categories_id),
                        FOREIGN KEY (status_id) REFERENCES status (status_id),
                        FOREIGN KEY (movies_id) REFERENCES movies (movies_id),
                        FOREIGN KEY (currencies_id) REFERENCES currencies (currencies_id)
                    )
                """)
            connection_without_database.commit()

        finally:
            print("Finished creating database")


def main():
    create_database()
    try:
        connection = SQL_data_loading.get_connection()
    except Exception as error:
        logging.error(f"Couldnt get connection: {error}")
        print(f"Couldnt get connection: {error}")
    path = Path("./Propstore_data.csv")
    if path:
        SQL_data_loading.load_data(path, connection)
        print("finished loading items into database")
    else:
        print(f"Need to create propstore csv file first")


if __name__ == "__main__":
    main()
