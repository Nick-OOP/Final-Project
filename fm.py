class SeatingManagement:
    def __init__(self, capacity):
        self.bookings = []  
        self.capacity = capacity 
        self.preferences = {}  

    def allocate_seat(self, booking):
        if len(self.bookings) < self.capacity:
            self.bookings.append(booking)
            print(f"Seat allocated to {booking.passenger_id}.")
            return True
        else:
            print("No available seats. Overbooking management required.")
            return False

    def manage_overbookings(self):
        if len(self.bookings) > self.capacity:
            removed_booking = self.bookings.pop()
            print(f"Booking for {removed_booking.passenger_id} removed due to overbooking.")
            return removed_booking
        else:
            print("No overbookings to manage.")
            return None

    def update_preferences(self, booking):
        self.preferences[booking.passenger_id] = booking.preferences
        print(f"Preferences updated for {booking.passenger_id}.")


class ClassManagement:
    def __init__(self):
        self.service_classes = {} 

    def add_service_class(self, class_info):
        self.service_classes[class_info['type']] = class_info
        print(f"Service class {class_info['type']} added.")

    def get_pricing(self, class_type):
        price = self.service_classes.get(class_type, {}).get('price')
        print(f"Price for {class_type}: {price}.")
        return price

    def list_offerings(self, class_type):
        offerings = self.service_classes.get(class_type, {}).get('offerings', [])
        print(f"Offerings for {class_type}: {offerings}.")
        return offerings


class LuggageHandling:
    def __init__(self):
        self.luggage_list = {} 

    def check_in_luggage(self, luggage_item):
        self.luggage_list[luggage_item.id] = luggage_item
        print(f"Luggage {luggage_item.id} checked in.")

    def track_luggage(self, luggage_id):
        luggage = self.luggage_list.get(luggage_id)
        if luggage:
            print(f"Luggage {luggage_id} found: {luggage}.")
        else:
            print(f"Luggage {luggage_id} not found.")
        return luggage

    def deliver_luggage(self, luggage_item):
        if luggage_item.id in self.luggage_list:
            del self.luggage_list[luggage_item.id]
            print(f"Luggage {luggage_item.id} delivered.")
        else:
            print(f"Luggage {luggage_item.id} not found in the system.")


class TravelScheduling:
    def __init__(self):
        self.flights = {} 

    def update_flight_status(self, flight_id, status):
        if flight_id in self.flights:
            self.flights[flight_id]['status'] = status
            print(f"Flight {flight_id} status updated to {status}.")
        else:
            print(f"Flight {flight_id} not found.")

    def get_flight_schedule(self):
        print("Current flight schedule:")
        for flight_id, details in self.flights.items():
            print(f"{flight_id}: {details}")
        return self.flights

    def notify_passengers(self, flight_id):
        if flight_id in self.flights:
            print(f"Notification sent to passengers of flight {flight_id}.")
        else:
            print(f"Flight {flight_id} not found.")


while 1:
    print("----------- FLIGHT --- MANAGEMENT --- SYSTEM ------------")
    print("1. Boook seat") #how many seats? Are there any seats remaining how much.
    print("2. Change seat ") #urgent $pay. or stay in normal
    print("3. Check seat number.")
    print("4. Select class ")
    print("5. Change class ")
    print("6. Check class ")
    print("7. Track luggage")
    print("8. ")
