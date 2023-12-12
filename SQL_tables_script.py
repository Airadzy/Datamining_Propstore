import pymysql

connection = pymysql.connect(host='localhost', user='root', password='root', cursorclass=pymysql.cursors.DictCursor)

try:
    with connection.cursor() as cursor:
        cu
