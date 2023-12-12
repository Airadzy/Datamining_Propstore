import pymysql

connection = pymysql.connect(host='localhost', user='root', password='root', cursorclass=pymysql.cursors.DictCursor)

with connection.cursor() as cursor:
    try:
        cursor.execute("CREATE DATABASE Propstore_details;")
        cursor.execute("USE Propstore_details;")
    except Exception as error:
        print(f"ERROR: {error}")
    try:
        cursor.execute("""
                CREATE TABLE IF NOT EXISTS categories(
                    categories_id INT AUTO_INCREMENT PRIMARY KEY,
                    categories VARCHAR(255) UNIQUE NOT NULL
                )
            """)
        cursor.execute("""
                CREATE TABLE IF NOT EXISTS movies (
                    movies_id INT AUTO_INCREMENT PRIMARY KEY,
                    movies_name VARCHAR(255) UNIQUE NOT NULL
                )
            """)
        cursor.execute("""
                CREATE TABLE IF NOT EXISTS status (
                    status_id INT AUTO_INCREMENT PRIMARY KEY,
                    status VARCHAR(255) NOT NULL,
                    sold_date DATE
                )
            """)
        cursor.execute("""
                CREATE TABLE IF NOT EXISTS currencies (
                    currencies_id INT AUTO_INCREMENT PRIMARY KEY,
                    currencies VARCHAR(255) UNIQUE NOT NULL
                )
            """)
        cursor.execute("""
                CREATE TABLE IF NOT EXISTS items (
                    items_id INT AUTO_INCREMENT PRIMARY KEY,
                    description VARCHAR(255),
                    categories_id INT,
                    status_id INT,
                    movies_id INT,
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
