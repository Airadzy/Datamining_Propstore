import pymysql
import pymysql.err
from SQL_tables_script import load_data

connection = pymysql.connect(host='localhost', user='root', password='root', cursorclass=pymysql.cursors.DictCursor)


def create_database():
    with connection.cursor() as cursor:
        try:
            cursor.execute("CREATE DATABASE propstore_details;")
        except (pymysql.err.ProgrammingError, pymysql.err.InternalError) as error:
            print(f"Database already exists: {error}")
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
            connection.commit()

        finally:
            connection.close()


def main():
    create_database()
    load_data()


if "__name__" == "__main__":
    main()
