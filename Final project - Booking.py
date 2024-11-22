import tkinter as tk
import sqlite3 as sql
from tkinter import messagebox

conn = sql.connect('temp.db')
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS flights (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    flight_number TEXT NOT NULL,
    destination TEXT NOT NULL,
    departure_time TEXT NOT NULL,
    seats_available INTEGER NOT NULL
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS tickets (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    flight_id INTEGER NOT NULL,
    passenger_name TEXT NOT NULL,
    FOREIGN KEY (flight_id) REFERENCES flights (id)
)
""")

conn.commit()

window = tk.Tk()
window.geometry("800x600")
window.configure(bg="#f0f0f0")
window.title("Flight Booking System")

label = tk.Label(window, text="Flight Booking System", font=("Helvetica", 20, "bold"), fg="#333", bg="#f0f0f0")
label.pack(pady=20)

def enter_flights():
    def save_flight():
        flight_num = flight_number_entry.get()
        dest = destination_entry.get()
        date = date_entry.get()
        time = time_entry.get()
        seats = seats_entry.get()

        if flight_num and dest and date and time and seats.isdigit():
            departure_time = f"{date} {time}"

            cursor.execute(
                "INSERT INTO flights (flight_number, destination, departure_time, seats_available) VALUES (?, ?, ?, ?)",
                (flight_num, dest, departure_time, int(seats))
            )
            conn.commit()
            messagebox.showinfo("Success", "Flight added!")
            entry_window.destroy()
        else:
            messagebox.showerror("Error", "Please fill all fields correctly!")

    entry_window = tk.Toplevel(window)
    entry_window.title("Enter Flight Details")
    entry_window.geometry("400x350")

    tk.Label(entry_window, text="Flight Number:").pack(pady=5)
    flight_number_entry = tk.Entry(entry_window)
    flight_number_entry.pack(pady=5)

    tk.Label(entry_window, text="Destination:").pack(pady=5)
    destination_entry = tk.Entry(entry_window)
    destination_entry.pack(pady=5)

    tk.Label(entry_window, text="Departure date (YYYY-MM-DD):").pack(pady=5)
    date_entry = tk.Entry(entry_window)
    date_entry.pack(pady=5)

    tk.Label(entry_window, text="Departure time (HH:MM):").pack(pady=5)
    time_entry = tk.Entry(entry_window)
    time_entry.pack(pady=5)

    tk.Label(entry_window, text="Seats Available:").pack(pady=5)
    seats_entry = tk.Entry(entry_window)
    seats_entry.pack(pady=5)

    tk.Button(entry_window, text="Save Flight", command=save_flight).pack(pady=10)

def view_flights():
    flights_window = tk.Toplevel(window)
    flights_window.title("Available Flights")
    flights_window.geometry("600x400")
    flights_window.configure(bg="#f0f0f0")

    tk.Label(flights_window, text="Available Flights", font=("Helvetica", 16, "bold"), bg="#f0f0f0").pack(pady=10)

    cursor.execute("SELECT * FROM flights")
    flights = cursor.fetchall()

    if flights:
        frame = tk.Frame(flights_window, bg="#f0f0f0")
        frame.pack(pady=10)

        tk.Label(frame, text="ID", width=5, anchor="w", font=("Helvetica", 12, "bold")).grid(row=0, column=0, padx=5)
        tk.Label(frame, text="Flight Number", width=15, anchor="w", font=("Helvetica", 12, "bold")).grid(row=0, column=1, padx=5)
        tk.Label(frame, text="Destination", width=15, anchor="w", font=("Helvetica", 12, "bold")).grid(row=0, column=2, padx=5)
        tk.Label(frame, text="Departure", width=15, anchor="w", font=("Helvetica", 12, "bold")).grid(row=0, column=3, padx=5)
        tk.Label(frame, text="Seats", width=5, anchor="w", font=("Helvetica", 12, "bold")).grid(row=0, column=4, padx=5)

        for i, flight in enumerate(flights, start=1):
            tk.Label(frame, text=flight[0], width=5, anchor="w", font=("Helvetica", 12)).grid(row=i, column=0, padx=5)
            tk.Label(frame, text=flight[1], width=15, anchor="w", font=("Helvetica", 12)).grid(row=i, column=1, padx=5)
            tk.Label(frame, text=flight[2], width=15, anchor="w", font=("Helvetica", 12)).grid(row=i, column=2, padx=5)
            tk.Label(frame, text=flight[3], width=15, anchor="w", font=("Helvetica", 12)).grid(row=i, column=3, padx=5)
            tk.Label(frame, text=flight[4], width=5, anchor="w", font=("Helvetica", 12)).grid(row=i, column=4, padx=5)
    else:
        tk.Label(flights_window, text="No flights available.", font=("Helvetica", 12), bg="#f0f0f0").pack(pady=10)

def view_tickets():
    tickets_window = tk.Toplevel(window)
    tickets_window.title("Purchased Tickets")
    tickets_window.geometry("600x400")
    tickets_window.configure(bg="#f0f0f0")

    tk.Label(tickets_window, text="Purchased Tickets", font=("Helvetica", 16, "bold"), bg="#f0f0f0").pack(pady=10)

    cursor.execute("""
    SELECT t.id, t.passenger_name, f.flight_number, f.destination
    FROM tickets t
    JOIN flights f ON t.flight_id = f.id
    """)
    tickets = cursor.fetchall()

    if tickets:
        frame = tk.Frame(tickets_window, bg="#f0f0f0")
        frame.pack(pady=10)

        tk.Label(frame, text="ID", width=5, anchor="w", font=("Helvetica", 12, "bold")).grid(row=0, column=0, padx=5)
        tk.Label(frame, text="Passenger", width=20, anchor="w", font=("Helvetica", 12, "bold")).grid(row=0, column=1, padx=5)
        tk.Label(frame, text="Flight Number", width=15, anchor="w", font=("Helvetica", 12, "bold")).grid(row=0, column=2, padx=5)
        tk.Label(frame, text="Destination", width=15, anchor="w", font=("Helvetica", 12, "bold")).grid(row=0, column=3, padx=5)

        for i, ticket in enumerate(tickets, start=1):
            tk.Label(frame, text=ticket[0], width=5, anchor="w", font=("Helvetica", 12)).grid(row=i, column=0, padx=5)
            tk.Label(frame, text=ticket[1], width=20, anchor="w", font=("Helvetica", 12)).grid(row=i, column=1, padx=5)
            tk.Label(frame, text=ticket[2], width=15, anchor="w", font=("Helvetica", 12)).grid(row=i, column=2, padx=5)
            tk.Label(frame, text=ticket[3], width=15, anchor="w", font=("Helvetica", 12)).grid(row=i, column=3, padx=5)
    else:
        tk.Label(tickets_window, text="No tickets purchased.", font=("Helvetica", 12), bg="#f0f0f0").pack(pady=10)

def purchase_ticket():
    def book_ticket():
        flight_id = flight_id_entry.get()
        passenger_name = passenger_name_entry.get()

        cursor.execute("SELECT seats_available FROM flights WHERE id = ?", (flight_id,))
        flight = cursor.fetchone()

        if flight and passenger_name:
            if flight[0] > 0:
                cursor.execute("INSERT INTO tickets (flight_id, passenger_name) VALUES (?, ?)",
                               (flight_id, passenger_name))
                cursor.execute("UPDATE flights SET seats_available = seats_available - 1 WHERE id = ?",
                               (flight_id,))
                conn.commit()
                messagebox.showinfo("Success", "Ticket booked!")
                purchase_window.destroy()
            else:
                messagebox.showerror("Error", "No seats available.")
        else:
            messagebox.showerror("Error", "Invalid flight ID or missing name.")

    purchase_window = tk.Toplevel(window)
    purchase_window.title("Purchase Ticket")
    purchase_window.geometry("400x300")
    purchase_window.configure(bg="#f0f0f0")

    tk.Label(purchase_window, text="Flight ID:").pack(pady=5)
    flight_id_entry = tk.Entry(purchase_window)
    flight_id_entry.pack(pady=5)

    tk.Label(purchase_window, text="Passenger Name:").pack(pady=5)
    passenger_name_entry = tk.Entry(purchase_window)
    passenger_name_entry.pack(pady=5)

    tk.Button(purchase_window, text="Book Ticket", command=book_ticket).pack(pady=10)

B1 = tk.Button(window, text="Enter Flights", command=enter_flights)
B1.place(x=100, y=100)

B2 = tk.Button(window, text="View Available Flights", command=view_flights)
B2.place(x=100, y=150)

B3 = tk.Button(window, text="Purchase Ticket", command=purchase_ticket)
B3.place(x=100, y=200)

B4 = tk.Button(window, text="View Tickets", command=view_tickets)
B4.place(x=100, y=250)

window.mainloop()
