# app.py
from flask import Flask, request, jsonify, render_template # Added render_template
from flask_cors import CORS 
from backend import DatabaseManager 

app = Flask(__name__)
CORS(app)

# Initialize your DatabaseManager
db_manager = DatabaseManager()

# --- UPDATED HOME ROUTE ---
@app.route('/')
def home():
    """Serves the main website HTML file."""
    return render_template('index.html')

@app.route('/login', methods=['POST'])
def login():
    """
    Handles user login authentication.
    Expected JSON: {"username": "...", "password": "..."}
    """
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    # For now, using hardcoded credentials as per your Tkinter app's logic
    if username == "admin" and password == "admin":
        return jsonify({"success": True, "message": "Login successful"}), 200
    else:
        return jsonify({"success": False, "message": "Invalid credentials"}), 401

@app.route('/hotels', methods=['GET'])
def get_hotels():
    """Fetches and returns all hotel data."""
    try:
        hotels = db_manager.get_all_hotels()
        # Convert tuples to list of dictionaries for better JSON representation
        hotel_list = [
            {"id": h[0], "name": h[1], "address": h[2], "star_rating": h[3], "contact": h[4], "email": h[5], "website": h[6], "description": h[7], "amenities": h[8]}
            for h in hotels
        ]
        return jsonify(hotel_list), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/hotels/add', methods=['POST'])
def add_hotel():
    """Adds a new hotel."""
    data = request.get_json()
    try:
        hotel_id = db_manager.add_hotel(
            data['name'], data['address'], data['star_rating'],
            data['contact_number'], data.get('email'), data.get('website'),
            data.get('description'), data.get('amenities')
        )
        return jsonify({"success": True, "hotel_id": hotel_id, "message": "Hotel added successfully"}), 201
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@app.route('/hotels/remove/<int:hotel_id>', methods=['DELETE'])
def remove_hotel(hotel_id):
    """Removes a hotel by ID."""
    try:
        db_manager.remove_hotel(hotel_id)
        return jsonify({"success": True, "message": f"Hotel {hotel_id} removed successfully"}), 200
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@app.route('/hotels/<int:hotel_id>/rooms', methods=['GET'])
def get_rooms_by_hotel(hotel_id):
    """Fetches and returns rooms for a specific hotel ID."""
    try:
        rooms = db_manager.get_rooms_by_hotel_id(hotel_id)
        room_list = [
            {"id": r[0], "number": r[1], "floor": r[2]} 
            for r in rooms
        ]
        return jsonify(room_list), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/rooms', methods=['GET'])
def get_all_rooms():
    """Fetches and returns all room data."""
    try:
        rooms = db_manager.get_all_rooms()
        room_list = [
            {"id": r[0], "number": r[1], "floor": r[2], "hotel_name": r[3]}
            for r in rooms
        ]
        return jsonify(room_list), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/rooms/add', methods=['POST'])
def add_room():
    """Adds a new room."""
    data = request.get_json()
    try:
        room_id = db_manager.add_room(
            data['hotel_id'], data['room_number'], data['floor']
        )
        return jsonify({"success": True, "room_id": room_id, "message": "Room added successfully"}), 201
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@app.route('/bookings', methods=['GET'])
def get_bookings():
    """Fetches and returns all booking data."""
    try:
        bookings = db_manager.get_all_bookings()
        booking_list = [
            {
                "id": b[0], "customer_name": b[1], "check_in": str(b[2]),
                "check_out": str(b[3]), "room_numbers": b[4], "hotel_name": b[5]
            }
            for b in bookings
        ]
        return jsonify(booking_list), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/booking/create', methods=['POST'])
def create_booking():
    """Creates a new booking."""
    data = request.get_json()
    customer_name = data.get('customer_name')
    check_in_date = data.get('check_in_date')
    check_out_date = data.get('check_out_date')
    room_ids = data.get('room_ids')
    payment_method = data.get('payment_method')

    if not all([customer_name, check_in_date, check_out_date, room_ids, payment_method]):
        return jsonify({"error": "Missing required fields"}), 400

    try:
        customer_id = db_manager.add_customer(customer_name)
        booking_id = db_manager.add_booking(customer_id, check_in_date, check_out_date)
        db_manager.assign_rooms_to_booking(booking_id, room_ids)
        db_manager.add_payment(booking_id, payment_method)
        return jsonify({"success": True, "booking_id": booking_id, "message": "Booking created successfully"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/payments', methods=['GET'])
def get_payments():
    """Fetches and returns all payment data."""
    try:
        payments = db_manager.get_all_payments()
        payment_list = [
            {"payment_id": p[0], "booking_id": p[1], "customer_name": p[2], "payment_method": p[3], "booking_date": str(p[4])}
            for p in payments
        ]
        return jsonify(payment_list), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':

    import os
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
