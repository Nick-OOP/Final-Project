import tkinter as tk
from tkinter import messagebox
import sqlite3 as sql

# Database connection
conn = sql.connect('flight_data.db')
cursor = conn.cursor()

# Create necessary tables if they don't exist
cursor.execute('''
    CREATE TABLE IF NOT EXISTS flights (
        flight_id INTEGER PRIMARY KEY,
        flight_name TEXT,
        available_seats INTEGER,
        status TEXT
    )
''')
cursor.execute('''
    CREATE TABLE IF NOT EXISTS passengers (
        passenger_id INTEGER PRIMARY KEY,
        name TEXT,
        seat_number INTEGER,
        class_type TEXT,
        luggage_id INTEGER
    )
''')
cursor.execute('''
    CREATE TABLE IF NOT EXISTS luggage (
        luggage_id INTEGER PRIMARY KEY,
        owner_id INTEGER,
        weight REAL
    )
''')
conn.commit()

# Tkinter window setup
window = tk.Tk()
window.geometry("1600x900")
window.configure(bg="White")
window.title("Flight Booking System")

label = tk.Label(window, text="Flight Management System", font=("Helvetica", 16), fg="Grey", bg="White")
label.pack(pady=25)

class FlightManagement:
    def __init__(self):
        self.seating_capacity = 100  # For simplicity, 100 seats per flight
        self.passenger_count = 0

    def book_seat(self, passenger_name):
        if self.passenger_count < self.seating_capacity:
            self.passenger_count += 1
            seat_number = self.passenger_count
            # Insert into the database
            cursor.execute("INSERT INTO passengers (name, seat_number, class_type) VALUES (?, ?, ?)",
                           (passenger_name, seat_number, 'Economy'))  # Default class
            conn.commit()
            messagebox.showinfo("Success", f"Seat booked successfully! Seat number: {seat_number}")
        else:
            messagebox.showwarning("Warning", "No available seats.")

    def change_seat(self, old_seat_number, new_seat_number):
        cursor.execute("SELECT * FROM passengers WHERE seat_number = ?", (old_seat_number,))
        passenger = cursor.fetchone()
        if passenger:
            cursor.execute("UPDATE passengers SET seat_number = ? WHERE seat_number = ?",
                           (new_seat_number, old_seat_number))
            conn.commit()
            messagebox.showinfo("Success", f"Seat changed to: {new_seat_number}")
        else:
            messagebox.showwarning("Warning", "Old seat number not found.")

    def check_seat(self, passenger_name):
        cursor.execute("SELECT seat_number FROM passengers WHERE name = ?", (passenger_name,))
        seat = cursor.fetchone()
        if seat:
            messagebox.showinfo("Seat Number", f"Your seat number is: {seat[0]}")
        else:
            messagebox.showwarning("Warning", "Passenger not found.")

    def select_class(self, seat_number, class_type):
        cursor.execute("UPDATE passengers SET class_type = ? WHERE seat_number = ?",
                       (class_type, seat_number))
        conn.commit()
        messagebox.showinfo("Class Selection", f"Class for seat number {seat_number} set to {class_type}.")

    def change_class(self, seat_number, new_class_type):
        cursor.execute("UPDATE passengers SET class_type = ? WHERE seat_number = ?",
                       (new_class_type, seat_number))
        conn.commit()
        messagebox.showinfo("Class Change", f"Class for seat number {seat_number} changed to {new_class_type}.")

    def track_luggage(self, luggage_id):
        cursor.execute("SELECT * FROM luggage WHERE luggage_id = ?", (luggage_id,))
        luggage = cursor.fetchone()
        if luggage:
            messagebox.showinfo("Luggage Tracking", f"Luggage found: Weight - {luggage[2]} kg")
        else:
            messagebox.showwarning("Luggage not found", "No luggage found with this ID.")

    def cancel_flight(self, flight_id):
        cursor.execute("UPDATE flights SET status = ? WHERE flight_id = ?", ('Cancelled', flight_id))
        conn.commit()
        messagebox.showinfo("Flight Cancellation", f"Flight {flight_id} cancelled successfully.")

    def view_flights(self):
        cursor.execute("SELECT * FROM flights")
        flights = cursor.fetchall()
        flights_info = "\n".join([f"Flight {flight[1]} (ID: {flight[0]}) - Status: {flight[3]}, Available Seats: {flight[2]}" for flight in flights])
        messagebox.showinfo("Flight Schedule", flights_info if flights else "No flights available.")

# Instance of the Flight Management system
flight_system = FlightManagement()

# Button actions for the GUI
def view_seats():
    flight_system.view_flights()

def book_seat_gui():
    def book():
        name = entry_name.get()
        if name:
            flight_system.book_seat(name)
            booking_window.destroy()

    booking_window = tk.Toplevel(window)
    booking_window.geometry("300x200")
    booking_window.title("Book a Seat")

    label_name = tk.Label(booking_window, text="Enter your name:")
    label_name.pack(pady=10)
    entry_name = tk.Entry(booking_window)
    entry_name.pack(pady=10)

    button_book = tk.Button(booking_window, text="Book Seat", command=book)
    button_book.pack(pady=10)

def change_seat_gui():
    def change():
        old_seat = int(entry_old_seat.get())
        new_seat = int(entry_new_seat.get())
        flight_system.change_seat(old_seat, new_seat)
        change_window.destroy()

    change_window = tk.Toplevel(window)
    change_window.geometry("300x200")
    change_window.title("Change Seat")

    label_old_seat = tk.Label(change_window, text="Enter old seat number:")
    label_old_seat.pack(pady=10)
    entry_old_seat = tk.Entry(change_window)
    entry_old_seat.pack(pady=10)

    label_new_seat = tk.Label(change_window, text="Enter new seat number:")
    label_new_seat.pack(pady=10)
    entry_new_seat = tk.Entry(change_window)
    entry_new_seat.pack(pady=10)

    button_change = tk.Button(change_window, text="Change Seat", command=change)
    button_change.pack(pady=10)

def track_luggage_gui():
    def track():
        luggage_id = int(entry_luggage_id.get())
        flight_system.track_luggage(luggage_id)
        luggage_window.destroy()

    luggage_window = tk.Toplevel(window)
    luggage_window.geometry("300x200")
    luggage_window.title("Track Luggage")

    label_luggage_id = tk.Label(luggage_window, text="Enter luggage ID:")
    label_luggage_id.pack(pady=10)
    entry_luggage_id = tk.Entry(luggage_window)
    entry_luggage_id.pack(pady=10)

    button_track = tk.Button(luggage_window, text="Track Luggage", command=track)
    button_track.pack(pady=10)

# Creating the GUI buttons
button_view_seats = tk.Button(window, text="View Flight Schedules", font=("Helvetica", 12), command=view_seats)
button_view_seats.pack(pady=10)

button_book_seat = tk.Button(window, text="Book Seat", font=("Helvetica", 12), command=book_seat_gui)
button_book_seat.pack(pady=10)

button_change_seat = tk.Button(window, text="Change Seat", font=("Helvetica", 12), command=change_seat_gui)
button_change_seat.pack(pady=10)

button_track_luggage = tk.Button(window, text="Track Luggage", font=("Helvetica", 12), command=track_luggage_gui)
button_track_luggage.pack(pady=10)

# Start the Tkinter event loop
window.mainloop()
