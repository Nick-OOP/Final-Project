import tkinter as tk
import sqlite3 as sql

conn = sql.connect('flight_data.db')
cursor = conn.cursor()
window = tk.Tk()
window.geometry("1600x900")
window.configure(bg="White")

window.title("Flight booking system")

label = tk.Label(window, text="Flight Booking System", font=("Helvetica", 16), fg="Grey", bg="White")
label.pack(pady=25)

def view_clicked():

B1=tk.Button(window, text="View available flights", font=("Helvetica", 12, "underline"), fg="Blue", command=view_clicked)
B1.place(x=100, y= 60)

window.mainloop()
