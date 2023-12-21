import pymysql
import main_file

def split_SQL_movies_table(connection):
    """

    :param connection:
    :return:
    """

    extract_movie_name = """
    SELECT 
    SELECT SUBSTRING(movies_name, 1, LOCATE("(", movies_name)-2) as movie_name, 
    SUBSTRING(movies_name, LOCATE("(", movies_name)+1,4) as year
    from movies
    ORDER by movies_id ASC;
    """

    with connection.cursor() as cursor:
        cursor.execute(f"USE propstore_details;")
        cursor.execute(extract_movie_name)
        rows = cursor.fetchall()
        print(rows)

        movies_dict = {row[0]: row[1] for row in rows}
        print(movies_dict)



config = main_file.load_config(main_file.config_filename)

connection = pymysql.connect(host=config["SQL_host"], user=config["SQL_user"], password=config["SQL_password"],
                             database=config['database_name'],
                             cursorclass=pymysql.cursors.DictCursor)

split_SQL_movies_table(connection)

