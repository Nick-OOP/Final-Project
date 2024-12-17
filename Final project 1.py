import tkinter as tk
import sqlite3 as sql
from tkinter import messagebox
from datetime import datetime

conn = sql.connect('Data file.db')
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS flights (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    flight_number TEXT NOT NULL,
    destination TEXT NOT NULL,
    departure TEXT NOT NULL,
    seats_available INTEGER NOT NULL
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS tickets (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    flight_id INTEGER NOT NULL,
    passenger_name TEXT NOT NULL,
    seat_class TEXT NOT NULL,
    seat_number TEXT NOT NULL,
    luggage TEXT NOT NULL,
    price REAL NOT NULL,
    FOREIGN KEY (flight_id) REFERENCES flights (id)
)
""")

conn.commit()


class Luggage:
    def __init__(self):
        self.class_configs = {
            'e': {
                'free_carry_on_limit': 10,
                'free_luggage_count': 1,
                'free_luggage_weight': 23,
                'overweight_fee': 50,
                'extra_luggage_fee': 100
            },
            'p_e': {
                'free_carry_on_limit': 10,
                'free_luggage_count': 2,
                'free_luggage_weight': 23,
                'overweight_fee': 55,
                'extra_luggage_fee': 100
            },
            'b': {
                'free_carry_on_limit': 10,
                'free_luggage_count': 3,
                'free_luggage_weight': 32,
                'overweight_fee': 55,
                'extra_luggage_fee': 250
            },
            'fc': {
                'free_carry_on_limit': 10,
                'free_luggage_count': 3,
                'free_luggage_weight': 32,
                'overweight_fee': 75,
                'extra_luggage_fee': 250
            }
        }

    def add_luggage(self):
        while True:
            print("-" * 36)
            travel_class = input("Enter your class preference (e/p_e/b/fc): ").lower()

            if travel_class not in self.class_configs:
                print("Invalid option. Please choose e, p_e, b, or fc.")
                continue

            config = self.class_configs[travel_class]
            print("*" * 36)
            print(f"1 carry-on free = {config['free_carry_on_limit']}Kg limit")
            print(f"{config['free_luggage_count']} luggage(s) free = {config['free_luggage_weight']}Kg limit")
            print("*" * 15 + " Fine " + "*" * 15)
            print(f"${config['overweight_fee']} for overweight luggage")
            print(f"${config['extra_luggage_fee']} for extra luggage")
            print("*" * 36)

            check_in = int(input("Enter the number of luggages: "))
            luggage_cost = 0

            if check_in > config['free_luggage_count']:
                luggage_cost += (check_in - config['free_luggage_count']) * config[
                    'extra_luggage_fee']

            for i in range(check_in):
                weight = float(input(f"Enter the weight of bag {i + 1} (kg): "))
                if weight <= config['free_carry_on_limit']:
                    print(f"Carry-On (S): {weight} kg")
                elif weight <= config['free_luggage_weight']:
                    print(f"Luggage (M): {weight} kg")
                else:
                    overweight_fee = (weight - config['free_luggage_weight']) * config['overweight_fee']
                    luggage_cost += overweight_fee
                    print(f"Overweight luggage (L): {weight} kg, Overweight Fee: ${overweight_fee:.2f}")

            print(f"Total extra luggage cost: ${luggage_cost:.2f}")

            u_continue = input("Do you want to add more luggage details? (Y/N): ").lower()
            if u_continue != 'y':
                print('Your bags will be safe with us!')
                break


class ClassType:
    def __init__(self):
        self.classes = {
            "Economy": 100,
            "Premium Economy": 300,
            "Business": 500,
            "First Class": 1000
        }

    def get_class_price(self, seat_class):
        return self.classes.get(seat_class, 0)

class Discount:
    def __init__(self, base_price):
        self.base_price = base_price

    def apply_discounts(self, age):
        price = self.holiday_discount()
        price = self.elderly_discount(age, price)
        return price

    def holiday_discount(self):
        current_date = datetime.now()
        if current_date.month == 12 and current_date.day == 25:
            return self.base_price * 0.85
        elif current_date.month == 11 and current_date.day == 28:
            return self.base_price * 0.90
        elif current_date.month == 10 and current_date.day == 31:
            return self.base_price * 0.90
        return self.base_price

    def elderly_discount(self, age, price):
        if age >= 70:
            return price * 0.95
        return price

window = tk.Tk()
window.geometry("800x600")
window.configure(bg="#f0f0f0")
window.title("Flight Booking System")

label = tk.Label(window, text="Flight Booking System", font=("Helvetica", 20, "bold"), fg="#333", bg="#f0f0f0")
label.pack(pady=20)

class_type = ClassType()

def enter_flights():
    def save_flight():
        flight_num = flight_number_entry.get()
        dest = destination_entry.get()
        date = date_entry.get()
        time = time_entry.get()
        seats = seats_entry.get()

        if flight_num and dest and date and time and seats.isdigit():
            departure = f"{date} {time}"

            cursor.execute(
                "INSERT INTO flights (flight_number, destination, departure, seats_available) VALUES (?, ?, ?, ?)",
                (flight_num, dest, departure, int(seats))
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

    tk.Label(entry_window, text="Departure date (MM/DD/YYYY):").pack(pady=5)
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
    tickets_window.geometry("1000x1000")
    tickets_window.configure(bg="#f0f0f0")

    tk.Label(tickets_window, text="Purchased Tickets", font=("Helvetica", 16, "bold"), bg="#f0f0f0").pack(pady=10)

    cursor.execute("""
    SELECT t.id, t.passenger_name, f.flight_number, f.destination, f.departure, t.seat_number
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
        tk.Label(frame, text="Destination", width=20, anchor="w", font=("Helvetica", 12, "bold")).grid(row=0, column=3, padx=5)
        tk.Label(frame, text="Departure", width=15, anchor="w", font=("Helvetica", 12, "bold")).grid(row=0, column=4, padx=5)
        tk.Label(frame, text="Seat Number", width=15, anchor="w", font=("Helvetica", 12, "bold")).grid(row=0, column=5, padx=5)
        for i, ticket in enumerate(tickets, start=1):
            tk.Label(frame, text=ticket[0], width=5, anchor="w", font=("Helvetica", 12)).grid(row=i, column=0, padx=5)
            tk.Label(frame, text=ticket[1], width=20, anchor="w", font=("Helvetica", 12)).grid(row=i, column=1, padx=5)
            tk.Label(frame, text=ticket[2], width=15, anchor="w", font=("Helvetica", 12)).grid(row=i, column=2, padx=5)
            tk.Label(frame, text=ticket[3], width=15, anchor="w", font=("Helvetica", 12)).grid(row=i, column=3, padx=5)
            tk.Label(frame, text=ticket[4], width=15, anchor="w", font=("Helvetica", 12)).grid(row=i, column=4, padx=5)
            tk.Label(frame, text=ticket[5], width=15, anchor="w", font=("Helvetica", 12)).grid(row=i, column=5, padx=5)

    else:
        tk.Label(tickets_window, text="No tickets purchased.", font=("Helvetica", 12), bg="#f0f0f0").pack(pady=10)


class seat():
    def __init__(self):
        self.seats = {
            "Economy": [f"E-{i}" for i in range(1, 11)],
            "Premium Economy": [f"PE-{i}" for i in range(1, 11)],
            "Business": [f"B-{i}" for i in range(1, 11)],
            "First Class": [f"F-{i}" for i in range(1, 11)]
        }

    def assign_seat(self, seat_class):
        if seat_class in self.seats and self.seats[seat_class]:
            return self.seats[seat_class].pop(0)
        else:
            return None


def purchase_ticket():
    current_price = tk.DoubleVar(value=0.0)

    def book_ticket():
        seating = seat()
        flight_id = flight_id_entry.get()
        passenger_name = passenger_name_entry.get()
        seat_class = class_var.get()
        seat_number = seating.assign_seat(seat_class)
        age = int(age_entry.get()) if age_entry.get().isdigit() else 0

        cursor.execute("SELECT seats_available FROM flights WHERE id = ?", (flight_id,))
        flight = cursor.fetchone()

        if flight and passenger_name and seat_class and seat_number:
            if flight[0] > 0:
                base_price = class_type.get_class_price(seat_class)
                final_price = Discount(base_price).apply_discounts(age)

                current_price.set(final_price)

                cursor.execute(
                    "INSERT INTO tickets (flight_id, passenger_name, seat_class, seat_number, price) VALUES (?, ?, ?, ?, ?)",
                    (flight_id, passenger_name, seat_class, seat_number, final_price)
                )
                cursor.execute("UPDATE flights SET seats_available = seats_available - 1 WHERE id = ?",
                               (flight_id,))
                conn.commit()
                messagebox.showinfo("Success", f"Ticket booked! Seat: {seat_number}, Final price: ${final_price:.2f}")
                purchase_window.destroy()
            else:
                messagebox.showerror("Error", "No seats available.")
        else:
            messagebox.showerror("Error", "Invalid flight ID or missing details.")
        luggage = Luggage()
        luggage.add_luggage()

    purchase_window = tk.Toplevel(window)
    purchase_window.title("Purchase Ticket")
    purchase_window.geometry("500x600")
    purchase_window.configure(bg="#f0f0f0")

    tk.Label(purchase_window, text="Flight ID:").pack(pady=5)
    flight_id_entry = tk.Entry(purchase_window)
    flight_id_entry.pack(pady=5)

    tk.Label(purchase_window, text="Passenger Name:").pack(pady=5)
    passenger_name_entry = tk.Entry(purchase_window)
    passenger_name_entry.pack(pady=5)

    tk.Label(purchase_window, text="Seat Class:").pack(pady=5)
    class_var = tk.StringVar(value="Economy")
    class_dropdown = tk.OptionMenu(purchase_window, class_var, *class_type.classes.keys())
    class_dropdown.pack(pady=5)

    tk.Label(purchase_window, text="Age:").pack(pady=5)
    age_entry = tk.Entry(purchase_window)
    age_entry.pack(pady=5)

    tk.Button(purchase_window, text="Book Ticket", command=book_ticket).pack(pady=10)

    price_var = tk.StringVar()
    price_var.set(f"Total Ticket Price: ${current_price.get():.2f}")

    label = tk.Label(purchase_window, textvariable=price_var, font=("Arial", 16))
    label.pack(pady=20)


    def update_price():
        selected_class = class_var.get()
        base_price = class_type.get_class_price(selected_class)
        current_price.set(base_price)
        price_var.set(f"Total Ticket Price: ${base_price:.2f}")

    update_button = tk.Button(purchase_window, text="Calculate price", command=update_price)
    update_button.pack(pady=10)



def remove_ticket():
    def delete_ticket():
        ticket_id = ticket_id_entry.get()

        if ticket_id.isdigit():
            ticket_id = int(ticket_id)

            cursor.execute("SELECT flight_id FROM tickets WHERE id = ?", (ticket_id,))
            ticket = cursor.fetchone()

            if ticket:
                flight_id = ticket[0]

                cursor.execute("DELETE FROM tickets WHERE id = ?", (ticket_id,))
                cursor.execute("UPDATE flights SET seats_available = seats_available + 1 WHERE id = ?", (flight_id,))
                conn.commit()
                messagebox.showinfo("Success", "Ticket removed successfully!")
                remove_ticket_window.destroy()
            else:
                messagebox.showerror("Error", "Ticket ID not found!")
        else:
            messagebox.showerror("Error", "Please enter a valid ticket ID!")

    remove_ticket_window = tk.Toplevel(window)
    remove_ticket_window.title("Remove Ticket")
    remove_ticket_window.geometry("400x200")
    remove_ticket_window.configure(bg="#f0f0f0")

    tk.Label(remove_ticket_window, text="Ticket ID:").pack(pady=5)
    ticket_id_entry = tk.Entry(remove_ticket_window)
    ticket_id_entry.pack(pady=5)

    tk.Button(remove_ticket_window, text="Delete Ticket", command=delete_ticket).pack(pady=10)


def remove_flight():
    def delete_flight():
        flight_id = flight_id_entry.get()

        if flight_id.isdigit():
            flight_id = int(flight_id)

            cursor.execute("SELECT * FROM flights WHERE id = ?", (flight_id,))
            flight = cursor.fetchone()

            if flight:
                cursor.execute("SELECT * FROM tickets WHERE flight_id = ?", (flight_id,))
                tickets = cursor.fetchall()

                if tickets:
                    cursor.execute("DELETE FROM tickets WHERE flight_id = ?", (flight_id,))
                    messagebox.showinfo("Info", "Associated tickets have been deleted.")

                cursor.execute("DELETE FROM flights WHERE id = ?", (flight_id,))
                conn.commit()
                messagebox.showinfo("Success", "Flight removed successfully!")
                remove_flight_window.destroy()
            else:
                messagebox.showerror("Error", "Flight ID not found!")
        else:
            messagebox.showerror("Error", "Please enter a valid flight ID!")

    remove_flight_window = tk.Toplevel(window)
    remove_flight_window.title("Remove Flight")
    remove_flight_window.geometry("400x200")
    remove_flight_window.configure(bg="#f0f0f0")

    tk.Label(remove_flight_window, text="Flight ID:").pack(pady=5)
    flight_id_entry = tk.Entry(remove_flight_window)
    flight_id_entry.pack(pady=5)

    tk.Button(remove_flight_window, text="Delete Flight", command=delete_flight).pack(pady=10)


B1 = tk.Button(window, text="Enter Flights", command=enter_flights)
B1.place(x=100, y=100)
B2 = tk.Button(window, text="Remove Flight", command=remove_flight)
B2.place(x=100, y=150)
B3 = tk.Button(window, text="View Available Flights", command=view_flights)
B3.place(x=100, y=200)

B4 = tk.Button(window, text="Purchase Ticket", command=purchase_ticket)
B4.place(x=100, y=250)
B5 = tk.Button(window, text="Remove Ticket", command=remove_ticket)
B5.place(x=100, y=300)
B6 = tk.Button(window, text="View Tickets", command=view_tickets)
B6.place(x=100, y=350)

window.mainloop()