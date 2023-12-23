import pymysql
import pymysql.err
import SQL_data_loading
from pathlib import Path
import logging
from main_file import load_config
import main_file

logging.basicConfig(filename=main_file.log_filename,
                    format='%(asctime)s-%(levelname)s-FILE:%(filename)s-FUNC:%(funcName)s-LINE:%(lineno)d-%(message)s',
                    level=logging.INFO)


def create_database(config, connection):
    """
    Creates a database and necessary tables based on the provided configuration.

    :param config: A dictionary containing configuration data such as the database name.
                   Expected keys include 'database_name'.
    :param connection: A pymysql connection object used to execute database operations.
    :return: None. The function creates a database and tables, and handles exceptions internally.
    """
    config = load_config(main_file.config_filename)


    with connection.cursor() as cursor:
        try:
            cursor.execute(f"CREATE DATABASE {config['database_name']};")
        except (pymysql.err.ProgrammingError, pymysql.err.InternalError) as error:
            logging.warning(f"Database already exists or error occurred: {error}")
            print(f"Database already exists so inserting new data into database")
        try:
            cursor.execute(f"USE {config['database_name']};")
            cursor.execute("""
                    CREATE TABLE IF NOT EXISTS categories(
                        categories_id INT AUTO_INCREMENT PRIMARY KEY,
                        categories VARCHAR(255) UNIQUE
                    )
                """)
            cursor.execute("""
                    CREATE TABLE IF NOT EXISTS movies (
                        movies_id INT AUTO_INCREMENT PRIMARY KEY,
                        movies_name VARCHAR(255) UNIQUE, 
                        release_year VARCHAR(255),
                        API_title VARCHAR (255),
                        API_year VARCHAR(255),
                        API_rated VARCHAR(255),
                        API_runtime VARCHAR(255),
                        API_genre VARCHAR(255),
                        API_directors VARCHAR(255),
                        API_country VARCHAR(255),
                        API_awards VARCHAR(255),
                        API_rating_imdb VARCHAR(255),
                        API_rating_metascore VARCHAR(255),
                        API_boxoffice VARCHAR(255)
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
            connection.commit()

        except Exception as error:
            logging.error(f"Error in creating tables: {error}")
        finally:
            logging.info("Finished creating database")
            print("Finished creating database")
