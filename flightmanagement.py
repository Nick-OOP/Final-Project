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
            cursor.execute("INSERT INTO passengers (name, seat_number, class_type) VALUES (?, ?, ?)",
                           (passenger_name, seat_number, 'Economy'))
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

# GUI Functions
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

def add_flight_gui():
    def add():
        flight_name = entry_name.get()
        available_seats = int(entry_seats.get())
        cursor.execute("INSERT INTO flights (flight_name, available_seats, status) VALUES (?, ?, ?)",
                       (flight_name, available_seats, 'Scheduled'))
        conn.commit()
        messagebox.showinfo("Success", "Flight added successfully!")
        add_flight_window.destroy()

    add_flight_window = tk.Toplevel(window)
    add_flight_window.geometry("300x200")
    add_flight_window.title("Add Flight")

    label_name = tk.Label(add_flight_window, text="Flight Name:")
    label_name.pack(pady=5)
    entry_name = tk.Entry(add_flight_window)
    entry_name.pack(pady=5)

    label_seats = tk.Label(add_flight_window, text="Available Seats:")
    label_seats.pack(pady=5)
    entry_seats = tk.Entry(add_flight_window)
    entry_seats.pack(pady=5)

    button_add = tk.Button(add_flight_window, text="Add Flight", command=add)
    button_add.pack(pady=10)

# Create Buttons
flight_system = FlightManagement()

button_view_seats = tk.Button(window, text="View Flight Schedules", font=("Helvetica", 12), command=view_seats)
button_view_seats.pack(pady=10)

button_book_seat = tk.Button(window, text="Book Seat", font=("Helvetica", 12), command=book_seat_gui)
button_book_seat.pack(pady=10)

button_change_seat = tk.Button(window, text="Change Seat", font=("Helvetica", 12), command=change_seat_gui)
button_change_seat.pack(pady=10)

button_add_flight = tk.Button(window, text="Add Flight", font=("Helvetica", 12), command=add_flight_gui)
button_add_flight.pack(pady=10)

# Start the Tkinter event loop
window.mainloop()
