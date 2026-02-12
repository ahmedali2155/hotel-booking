-- 1. Create the Database
CREATE DATABASE IF NOT EXISTS hotel_booking_db;
USE hotel_booking_db;

-- 2. Create HOTEL Table
CREATE TABLE HOTEL (
    Hotel_ID INT PRIMARY KEY AUTO_INCREMENT,
    Hotel_Name VARCHAR(255) NOT NULL,
    Address TEXT,
    Star_Rating INT,
    Contact_Number VARCHAR(20),
    Email VARCHAR(100),
    Website VARCHAR(100),
    Description TEXT,
    Amenities TEXT
);

-- 3. Create ROOM Table with Hotel_ID as Foreign Key
CREATE TABLE ROOM (
    Room_ID INT PRIMARY KEY AUTO_INCREMENT,
    Room_Number VARCHAR(10) NOT NULL,
    Floor INT NOT NULL,
    Hotel_ID INT,
    FOREIGN KEY (Hotel_ID) REFERENCES HOTEL(Hotel_ID) ON DELETE CASCADE
);

-- 4. Create CUSTOMER Table
CREATE TABLE CUSTOMER (
    Customer_ID INT PRIMARY KEY AUTO_INCREMENT,
    Customer_Name VARCHAR(100) NOT NULL
);

-- 5. Create BOOKING Table
CREATE TABLE BOOKING (
    Booking_ID INT PRIMARY KEY AUTO_INCREMENT,
    Customer_ID INT NOT NULL,
    Booking_Date DATE NOT NULL,
    Check_in DATE NOT NULL,
    Check_out DATE NOT NULL,
    FOREIGN KEY (Customer_ID) REFERENCES CUSTOMER(Customer_ID) ON DELETE CASCADE
);

-- 6. Create PAYMENT Table
CREATE TABLE PAYMENT (
    Payment_ID INT PRIMARY KEY AUTO_INCREMENT,
    Booking_ID INT UNIQUE NOT NULL,
    Payment_Method VARCHAR(50) NOT NULL,
    FOREIGN KEY (Booking_ID) REFERENCES BOOKING(Booking_ID) ON DELETE CASCADE
);

-- 7. Create BOOKING_ROOM Table
CREATE TABLE BOOKING_ROOM (
    Booking_ID INT NOT NULL,
    Room_ID INT NOT NULL,
    PRIMARY KEY (Booking_ID, Room_ID),
    FOREIGN KEY (Booking_ID) REFERENCES BOOKING(Booking_ID) ON DELETE CASCADE,
    FOREIGN KEY (Room_ID) REFERENCES ROOM(Room_ID) ON DELETE CASCADE
);

-- 8. Insert HOTEL Data
INSERT INTO HOTEL (Hotel_Name, Address, Star_Rating, Contact_Number, Email, Website, Description, Amenities)
VALUES
('The Grand Hyatt', '123 Main St, New York, NY, USA', 5, '+1-212-555-1234', 'info@grandhyatt.com', 'www.grandhyatt.com', 'Luxury 5-star hotel in the heart of the city.', 'Free Wi-Fi, Swimming Pool, Spa, Gym, Restaurant'),
('Mountain View Inn', '456 Hill Rd, Denver, CO, USA', 4, '+1-303-555-4567', 'contact@mountainview.com', 'www.mountainview.com', 'Scenic mountain resort with modern amenities.', 'Free Wi-Fi, Hiking Trails, Fireplace, Breakfast'),
('Seaside Escape', '789 Ocean Blvd, Miami, FL, USA', 5, '+1-305-555-7890', 'stay@seasideescape.com', 'www.seasideescape.com', 'Beachfront resort with stunning views and luxury suites.', 'Beach Access, Pool Bar, Free Wi-Fi, Yoga'),
('City Central Hotel', '321 Downtown Ave, Chicago, IL, USA', 3, '+1-312-555-3210', 'book@citycentral.com', 'www.citycentral.com', 'Affordable hotel in downtown with easy transport access.', 'Business Center, Wi-Fi, Parking'),
('Lakeview Lodge', '147 Lakeshore Dr, Minneapolis, MN, USA', 4, '+1-612-555-1470', 'reservations@lakeviewlodge.com', 'www.lakeviewlodge.com', 'Quiet lodge overlooking the lake.', 'Kayaking, Free Wi-Fi, Fireplace, Restaurant'),
('Urban Suites', '159 City Park Rd, Austin, TX, USA', 4, '+1-512-555-1590', 'info@urbansuites.com', 'www.urbansuites.com', 'Modern hotel with suite-style rooms and a rooftop pool.', 'Rooftop Pool, Gym, Free Wi-Fi, Parking'),
('Historic Inn', '753 Heritage St, Boston, MA, USA', 3, '+1-617-555-7530', 'contact@historicinn.com', 'www.historicinn.com', 'Charming historic inn in the heart of the old town.', 'Antique Decor, Free Breakfast, Wi-Fi'),
('Desert Oasis', '852 Mirage Way, Phoenix, AZ, USA', 4, '+1-480-555-8520', 'hello@desertoasis.com', 'www.desertoasis.com', 'Relaxing oasis with spa and desert excursions.', 'Spa, Pool, Desert Tours, Free Wi-Fi'),
('Island Retreat', '963 Palm Tree Ln, Honolulu, HI, USA', 5, '+1-808-555-9630', 'escape@islandretreat.com', 'www.islandretreat.com', 'Private island resort with luxury villas.', 'Private Beach, Infinity Pool, Yoga, Wi-Fi'),
('Countryside Hotel', '369 Country Rd, Nashville, TN, USA', 3, '+1-615-555-3690', 'stay@countrysidehotel.com', 'www.countrysidehotel.com', 'Peaceful rural retreat with outdoor activities.', 'Horseback Riding, Free Wi-Fi, Garden');

-- 9. Insert ROOM Data (Assign 2 rooms per hotel)
INSERT INTO ROOM (Room_Number, Floor, Hotel_ID) VALUES
('101A', 1, 1), ('102A', 1, 1),
('201B', 2, 2), ('202B', 2, 2),
('301C', 3, 3), ('302C', 3, 3),
('401D', 4, 4), ('402D', 4, 4),
('501E', 5, 5), ('502E', 5, 5);

-- 10. Insert CUSTOMER Data
INSERT INTO CUSTOMER (Customer_Name) VALUES
('Alice Johnson'), ('Bob Smith'), ('Clara Oswald'), ('David Tennant'), ('Eve Polastri'),
('Frank Castle'), ('Grace Hopper'), ('Hank Pym'), ('Ivy League'), ('Jack Reacher');

-- 11. Insert BOOKING Data
INSERT INTO BOOKING (Customer_ID, Booking_Date, Check_in, Check_out) VALUES
(1, '2025-06-01', '2025-06-10', '2025-06-12'),
(2, '2025-06-02', '2025-06-11', '2025-06-14'),
(3, '2025-06-03', '2025-06-12', '2025-06-13'),
(4, '2025-06-04', '2025-06-13', '2025-06-15'),
(5, '2025-06-05', '2025-06-14', '2025-06-16'),
(6, '2025-06-06', '2025-06-15', '2025-06-18'),
(7, '2025-06-07', '2025-06-16', '2025-06-17'),
(8, '2025-06-08', '2025-06-17', '2025-06-19'),
(9, '2025-06-09', '2025-06-18', '2025-06-20'),
(10,'2025-06-10', '2025-06-19', '2025-06-21');

-- 12. Insert PAYMENT Data
INSERT INTO PAYMENT (Booking_ID, Payment_Method) VALUES
(1, 'Credit Card'), (2, 'Cash'), (3, 'Debit Card'), (4, 'Credit Card'), (5, 'UPI'),
(6, 'Net Banking'), (7, 'Credit Card'), (8, 'Cash'), (9, 'Debit Card'), (10, 'UPI');

-- 13. Insert BOOKING_ROOM Data
INSERT INTO BOOKING_ROOM (Booking_ID, Room_ID) VALUES
(1, 1), (1, 2),
(2, 3),
(3, 4), (3, 5),
(4, 6),
(5, 7),
(6, 8),
(7, 9),
(8, 10);
USE hotel_booking_db;
SELECT Hotel_Name, Image_URL FROM HOTEL;
