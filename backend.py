import mysql.connector
from datetime import date

class DatabaseManager:
    def __init__(self):
        self.db_config = {
            "host": "mysql.railway.internal",
            "port": 3306,
            "user": "root",
            "password": "EseXahnZSfRpzysBNjzRPStescYkJBW",
            "database": "railway"
        }

    def get_connection(self):
        return mysql.connector.connect(**self.db_config)

    def execute_query(self, query, params=None, fetch=False):
        conn = self.get_connection()
        cursor = conn.cursor()

        cursor.execute(query, params or ())

        if fetch:
            result = cursor.fetchall()
        else:
            conn.commit()
            result = cursor.lastrowid

        cursor.close()
        conn.close()
        return result

    def get_all_hotels(self):
        return self.execute_query("SELECT * FROM HOTEL", fetch=True)

    def get_all_rooms(self):
        return self.execute_query("SELECT * FROM ROOM", fetch=True)

    def get_all_bookings(self):
        return self.execute_query("SELECT * FROM BOOKING", fetch=True)

    def add_customer(self, name):
        return self.execute_query(
            "INSERT INTO CUSTOMER (Customer_Name) VALUES (%s)", (name,)
        )
