import mysql.connector
from datetime import date

class DatabaseManager:
    """
    Manages all interactions with the MySQL hotel booking database.
    Uses a context manager pattern to ensure connections are properly closed.
    """
    def __init__(self, host="127.0.0.1", port=3306, user="root", password="your_password", database="hotel_booking_db"):
        self.db_config = {
            "host": host,
            "port": port,
            "user": user,
            "password": password,
            "database": database
        }
        # Use your actual password here. It's 'root' based on your provided backend.py
        self.db_config["password"] = "root" 

    def __enter__(self):
        """Establishes a database connection when entering the 'with' block."""
        self.connection = mysql.connector.connect(**self.db_config)
        return self.connection

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Closes the database connection when exiting the 'with' block."""
        if self.connection:
            self.connection.close()

    def _execute_query(self, query, params=None, fetch_one=False, commit=False):
        """
        Internal helper method to execute a query, handle cursor,
        and manage fetching data or committing changes.
        """
        try:
            with self as db: # Use the context manager to get a connection
                cursor = db.cursor()
                cursor.execute(query, params)
                if commit:
                    db.commit()
                if fetch_one:
                    return cursor.fetchone()
                else:
                    return cursor.fetchall()
        except mysql.connector.Error as err:
            print(f"Database Error: {err}")
            raise # Re-raise the exception to be handled by the caller

    def get_all_hotels(self):
        """Fetches all hotels from the HOTEL table, including all columns."""
        query = "SELECT Hotel_ID, Hotel_Name, Address, Star_Rating, Contact_Number, Email, Website, Description, Amenities FROM HOTEL"
        return self._execute_query(query)

    def add_hotel(self, name, address, star_rating, contact_number, email=None, website=None, description=None, amenities=None):
        """Inserts a new hotel into the HOTEL table and returns its ID."""
        query = """
        INSERT INTO HOTEL (Hotel_Name, Address, Star_Rating, Contact_Number, Email, Website, Description, Amenities)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """
        params = (name, address, star_rating, contact_number, email, website, description, amenities)
        with self as db:
            cursor = db.cursor()
            cursor.execute(query, params)
            db.commit()
            return cursor.lastrowid

    def remove_hotel(self, hotel_id):
        """Deletes a hotel by its ID."""
        query = "DELETE FROM HOTEL WHERE Hotel_ID = %s"
        # Using _execute_query with commit=True as it's a modifying operation
        self._execute_query(query, (hotel_id,), commit=True)

    def get_rooms_by_hotel_id(self, hotel_id):
        """Fetches all rooms for a specific hotel ID."""
        query = """
        SELECT Room_ID, Room_Number, Floor
        FROM ROOM
        WHERE Hotel_ID = %s
        """
        return self._execute_query(query, (hotel_id,))

    def get_all_rooms(self):
        """Fetches all rooms along with their associated hotel names."""
        query = """
        SELECT R.Room_ID, R.Room_Number, R.Floor, H.Hotel_Name
        FROM ROOM R
        JOIN HOTEL H ON R.Hotel_ID = H.Hotel_ID
        """
        return self._execute_query(query)

    def add_room(self, hotel_id, room_number, floor):
        """Inserts a new room into the ROOM table and returns its ID."""
        query = "INSERT INTO ROOM (Hotel_ID, Room_Number, Floor) VALUES (%s, %s, %s)"
        with self as db:
            cursor = db.cursor()
            cursor.execute(query, (hotel_id, room_number, floor))
            db.commit()
            return cursor.lastrowid

    def add_customer(self, customer_name):
        """Inserts a new customer into the CUSTOMER table and returns their ID."""
        query = "INSERT INTO CUSTOMER (Customer_Name) VALUES (%s)"
        with self as db:
            cursor = db.cursor()
            cursor.execute(query, (customer_name,))
            db.commit()
            return cursor.lastrowid

    def add_booking(self, customer_id, check_in_date, check_out_date):
        """Inserts a new booking and returns the booking ID."""
        booking_date = date.today().isoformat()
        query = """
        INSERT INTO BOOKING (Customer_ID, Booking_Date, Check_in, Check_out)
        VALUES (%s, %s, %s, %s)
        """
        with self as db:
            cursor = db.cursor()
            cursor.execute(query, (customer_id, booking_date, check_in_date, check_out_date))
            db.commit()
            return cursor.lastrowid

    def assign_rooms_to_booking(self, booking_id, room_ids):
        """Assigns multiple rooms to a specific booking."""
        query = "INSERT INTO BOOKING_ROOM (Booking_ID, Room_ID) VALUES (%s, %s)"
        with self as db:
            cursor = db.cursor()
            for room_id in room_ids:
                cursor.execute(query, (booking_id, room_id))
            db.commit()

    def add_payment(self, booking_id, payment_method):
        """Adds a payment record for a given booking."""
        query = "INSERT INTO PAYMENT (Booking_ID, Payment_Method) VALUES (%s, %s)"
        self._execute_query(query, (booking_id, payment_method), commit=True)

    def get_all_bookings(self):
        """Fetches all bookings with associated customer, room numbers, and hotel names."""
        query = """
        SELECT B.Booking_ID, C.Customer_Name, B.Check_in, B.Check_out, GROUP_CONCAT(R.Room_Number SEPARATOR ', '), H.Hotel_Name
        FROM BOOKING B
        JOIN CUSTOMER C ON B.Customer_ID = C.Customer_ID
        JOIN BOOKING_ROOM BR ON B.Booking_ID = BR.Booking_ID
        JOIN ROOM R ON BR.Room_ID = R.Room_ID
        JOIN HOTEL H ON R.Hotel_ID = H.Hotel_ID
        GROUP BY B.Booking_ID, C.Customer_Name, B.Check_in, B.Check_out, H.Hotel_Name
        ORDER BY B.Booking_ID DESC
        """
        return self._execute_query(query)

    def get_all_payments(self):
        """Fetches all payment records with associated booking and customer names."""
        query = """
        SELECT P.Payment_ID, P.Booking_ID, C.Customer_Name, P.Payment_Method, B.Booking_Date
        FROM PAYMENT P
        JOIN BOOKING B ON P.Booking_ID = B.Booking_ID
        JOIN CUSTOMER C ON B.Customer_ID = C.Customer_ID
        ORDER BY P.Payment_ID DESC
        """
        return self._execute_query(query)

# Example usage (for testing backend directly, not part of the app)
if __name__ == "__main__":
    db_manager = DatabaseManager()

    try:
        print("--- All Hotels ---")
        hotels = db_manager.get_all_hotels()
        for hotel in hotels:
            print(hotel)

        print("\n--- All Rooms ---")
        rooms = db_manager.get_all_rooms()
        for room in rooms:
            print(room)

        print("\n--- Creating a new booking... ---")
        customer_id = db_manager.add_customer("Refactored Test Customer")
        booking_id = db_manager.add_booking(customer_id, "2025-07-01", "2025-07-05")
        db_manager.assign_rooms_to_booking(booking_id, [1, 2]) # Assuming Room_IDs 1 and 2 exist
        db_manager.add_payment(booking_id, "Refactored Card")
        print(f"Booking {booking_id} created successfully for customer ID {customer_id}!")

        print("\n--- All Bookings (including new one) ---")
        bookings = db_manager.get_all_bookings()
        for booking in bookings:
            print(booking)

        print("\n--- Adding a new hotel ---")
        new_hotel_id = db_manager.add_hotel("Test Hotel", "Test Address", 3, "123-456-7890", "test@test.com", "www.test.com", "A test hotel.", "Wifi, Parking")
        print(f"New hotel added with ID: {new_hotel_id}")

        print("\n--- Adding a new room to Test Hotel ---")
        new_room_id = db_manager.add_room(new_hotel_id, "999", 9)
        print(f"New room added with ID: {new_room_id}")

        print("\n--- Rooms for Test Hotel ---")
        test_hotel_rooms = db_manager.get_rooms_by_hotel_id(new_hotel_id)
        for room in test_hotel_rooms:
            print(room)

        print("\n--- All Payments ---")
        payments = db_manager.get_all_payments()
        for payment in payments:
            print(payment)
            
        print("\n--- Removing Test Hotel ---")
        db_manager.remove_hotel(new_hotel_id)
        print(f"Hotel {new_hotel_id} removed.")


    except Exception as e:
        print(f"An error occurred during backend testing: {e}")