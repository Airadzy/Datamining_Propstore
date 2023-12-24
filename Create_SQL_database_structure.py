import pymysql
import pymysql.err
import logging
import main_file

logging.basicConfig(filename=main_file.log_filename,
                    format='%(asctime)s-%(levelname)s-FILE:%(filename)s-FUNC:%(funcName)s-LINE:%(lineno)d-%(message)s',
                    level=logging.INFO)


def get_connection_without_database(config):
    """
    Establishes and returns a SQL connection without a specified database
    :config: parameters from json file
    :return: Database connection
    """
    try:
        connection_without_database = pymysql.connect(host=config["SQL_host"], user=config["SQL_user"],
                                                  password=config["SQL_password"],
                                                  cursorclass=pymysql.cursors.DictCursor)
        return connection_without_database
    except pymysql.err.OperationalError as e:
        logging.error(f"Operational error in database connection: {e}")
    except pymysql.err.InternalError as e:
        logging.error(f"Internal error in database: {e}")
    except pymysql.err.DatabaseError as e:
        logging.error(f"Database error: {e}")


def get_connection_with_database(config):
    """
    Establishes and returns a connection to the relevant propstore database
    :config: parameters from json file
    :return: Database connection
    """
    try:
        connection = pymysql.connect(host=config["SQL_host"], user=config["SQL_user"], password=config["SQL_password"],
                                     database=config['database_name'],
                                     cursorclass=pymysql.cursors.DictCursor)
        return connection
    except pymysql.err.OperationalError as e:
        logging.error(f"Operational error in database connection: {e}")
    except pymysql.err.InternalError as e:
        logging.error(f"Internal error in database: {e}")
    except pymysql.err.DatabaseError as e:
        logging.error(f"Database error: {e}")


def create_database(config, connection):
    """
    Creates a database unless the relevant database already exists.

    :param config: A dictionary containing configuration data such as the database name.
                   Expected keys include 'database_name'.
    :param connection: A pymysql connection object used to execute database operations.
    :return: None. The function creates a database and tables, and handles exceptions internally.
    """

    with connection.cursor() as cursor:
        try:
            cursor.execute(f"CREATE DATABASE {config['database_name']};")
            logging.info(f"Created new database: {config['database_name']}")
            print(f"Created new SQL database: {config['database_name']}")
        except (pymysql.err.ProgrammingError, pymysql.err.InternalError) as error:
            logging.warning(f"SQL database already exists or error occurred: {error}")
            print(f"SQL database already exists so inserting new data into existing database instead")


def create_database_tables(config, connection):
    """
    Creates a database and necessary tables based on the provided configuration.

    :param config: A dictionary containing configuration data such as the database name.
                   Expected keys include 'database_name'.
    :param connection: A pymysql connection object used to execute database operations.
    :return: None. The function creates the relevant database tables, and handles exceptions internally.
    """
    with connection.cursor() as cursor:
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
            logging.info("Finished creating database")
            print("Finished creating database")
            connection.commit()

        except Exception as error:
            logging.error(f"Error in creating tables: {error}")
