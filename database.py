import MySQLdb.converters
import mysql.connector
from mysql.connector import Error
import sys

def connect_db():
    try:
        connection = mysql.connector.connect(host='10.90.1.111',
                                            database='barcodes',
                                            user='stefan',
                                            password='Start2020!'
                                            )
        if connection.is_connected():
            db_Info = connection.get_server_info()
            print("Connected to MySQL Server version ", db_Info, file=sys.stdout)
            cursor = connection.cursor(buffered=True)
            cursor.execute("select database();")
            record = cursor.fetchone()
            print("You're connected to database: ", record, file=sys.stdout)
    except Error as e:
        print("Error while connecting to MySQL", e, file=sys.stdout)
    if 'connection' in locals():
        return connection, cursor


def deprecated():
    try:
        connection = mysql.connector.connect(host='10.90.1.110',
                                            database='LETS',
                                            user='stefan',
                                            password='Start2020!')
        if connection.is_connected():
            db_Info = connection.get_server_info()
            print("Connected to MySQL Server version ", db_Info, file=sys.stdout)
            cursor = connection.cursor(buffered=True)
            cursor.execute("select database();")
            record = cursor.fetchone()
            print("You're connected to database: ", record, file=sys.stdout)


            
            cursor.execute("SELECT * FROM barcodes")
            record = cursor.fetchall()
            print(len(record), file=sys.stdout)
            print(record, file=sys.stdout)
            print(type(record), file=sys.stdout)

            for i in range(len(record)+1, len(record)+4):
                key = 'ABCDEFGHI{}'.format(i)
                cursor.execute("INSERT INTO barcodes(barcode) VALUES ('{}');".format(key))

            # cursor.execute("")
            connection.commit()
            cursor.execute("SELECT * FROM barcodes")
            record = cursor.fetchall()
            print(record, file=sys.stdout)


    except Error as e:
        print("Error while connecting to MySQL", e, file=sys.stdout)
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection is closed", file=sys.stdout)