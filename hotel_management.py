import csv
import datetime
import os


class Room:
    def __init__(self, room_id, room_type, price, availability_status=True):
        self.room_id = room_id
        self.type = room_type
        self.price = price
        self.availability_status = availability_status

    def to_csv_row(self):
        return [
            self.room_id,
            self.type,
            str(self.price),
            '1' if self.availability_status else '0'
        ]

    @staticmethod
    def from_csv_row(row):
        room_id = row[0]
        room_type = row[1]
        price = float(row[2])
        availability_status = (row[3] == '1')
        if room_type == "Single":
            return SingleRoom(room_id, availability_status=availability_status)
        elif room_type == "Double":
            return DoubleRoom(room_id, availability_status=availability_status)
        elif room_type == "Suite":
            return Suite(room_id, availability_status=availability_status)


class SingleRoom(Room):
    price = 2000

    def __init__(self, room_id, availability_status=True):
        super().__init__(room_id, "Single", SingleRoom.price, availability_status)


class DoubleRoom(Room):
    price = 5000

    def __init__(self, room_id, availability_status=True):
        super().__init__(room_id, "Double", DoubleRoom.price, availability_status)


class Suite(Room):
    price = 8000

    def __init__(self, room_id, availability_status=True):
        super().__init__(room_id, "Suite", Suite.price, availability_status)


class Booking:
    def __init__(self, booking_id, room_id, room_type, guest_name, checkin_date, checkout_date):
        self.booking_id = booking_id
        self.room_id = room_id
        self.room_type = room_type
        self.guest_name = guest_name
        self.checkin_date = checkin_date
        self.checkout_date = checkout_date

    def to_csv_row(self):
        return [
            self.booking_id,
            self.room_id,
            self.room_type,
            self.guest_name,
            self.checkin_date.isoformat(),
            self.checkout_date.isoformat()
        ]

    @staticmethod
    def from_csv_row(row):
        booking_id = row[0]
        room_id = row[1]
        room_type = row[2]
        guest_name = row[3]
        checkin_date = datetime.date.fromisoformat(row[4])
        checkout_date = datetime.date.fromisoformat(row[5])
        return Booking(booking_id, room_id, room_type, guest_name, checkin_date, checkout_date)


class HotelManager:
    ROOMS_FILE = "rooms.csv"

    def __init__(self):
        self.rooms = self.load_rooms()

    def load_rooms(self):
        rooms = {}
        if os.path.exists(HotelManager.ROOMS_FILE):
            try:
                with open(HotelManager.ROOMS_FILE, "r", newline='', encoding='utf-8') as f:
                    reader = csv.reader(f)
                    for row in reader:
                        if row:
                            room = Room.from_csv_row(row)
                            rooms[room.room_id] = room
            except Exception as e:
                print("Error reading rooms file:", e)
        return rooms

    def save_rooms(self):
        try:
            with open(HotelManager.ROOMS_FILE, "w", newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                for room in self.rooms.values():
                    writer.writerow(room.to_csv_row())
        except Exception as e:
            print("Error writing rooms file:", e)

    def add_room(self, room):
        self.rooms[room.room_id] = room
        self.save_rooms()

    def update_room(self, room_id, **kwargs):
        if room_id in self.rooms:
            room = self.rooms[room_id]
            if "availability_status" in kwargs:
                room.availability_status = kwargs["availability_status"]
            self.save_rooms()

    def delete_room(self, room_id):
        if room_id in self.rooms:
            del self.rooms[room_id]
            self.save_rooms()

    def check_availability(self, room_id):
        return self.rooms.get(room_id, None) and self.rooms[room_id].availability_status

    def get_all_rooms(self):
        return self.rooms.values()


class BookingManager:
    BOOKINGS_FILE = "bookings.csv"
    BOOKING_HISTORY_FILE = "booking_history.csv"

    def __init__(self, hotel_manager):
        self.hotel_manager = hotel_manager
        self.bookings = self.load_bookings()

    def load_bookings(self):
        bookings = {}
        if os.path.exists(self.BOOKINGS_FILE):
            try:
                with open(self.BOOKINGS_FILE, "r", newline='', encoding='utf-8') as f:
                    reader = csv.reader(f)
                    for row in reader:
                        if row:
                            booking = Booking.from_csv_row(row)
                            bookings[booking.booking_id] = booking
            except Exception as e:
                print("Error reading bookings file:", e)
        return bookings

    def save_bookings(self):
        try:
            with open(self.BOOKINGS_FILE, "w", newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                for booking in self.bookings.values():
                    writer.writerow(booking.to_csv_row())
        except Exception as e:
            print("Error writing bookings file:", e)

    def log_booking_history(self, booking):
        try:
            append_mode = 'a' if os.path.exists(self.BOOKING_HISTORY_FILE) else 'w'
            with open(self.BOOKING_HISTORY_FILE, append_mode, newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(booking.to_csv_row())
        except Exception as e:
            print("Error logging booking history:", e)

    def make_booking(self, room_id, room_type, guest_name, checkin_date, checkout_date):
        if not self.hotel_manager.check_availability(room_id):
            raise Exception("Room not available or does not exist.")

        booking_id = "B" + str(len(self.bookings) + 1)
        booking = Booking(booking_id, room_id, room_type, guest_name, checkin_date, checkout_date)
        self.bookings[booking_id] = booking

        self.hotel_manager.update_room(room_id, availability_status=False)
        self.save_bookings()
        self.log_booking_history(booking)
        return booking_id

    def modify_booking(self, booking_id, **kwargs):
        if booking_id in self.bookings:
            booking = self.bookings[booking_id]
            if "guest_name" in kwargs:
                booking.guest_name = kwargs["guest_name"]
            if "checkin_date" in kwargs:
                booking.checkin_date = kwargs["checkin_date"]
            if "checkout_date" in kwargs:
                booking.checkout_date = kwargs["checkout_date"]
            self.save_bookings()
        else:
            raise Exception("Booking not found")

    def cancel_booking(self, booking_id):
        if booking_id in self.bookings:
            booking = self.bookings[booking_id]
            self.hotel_manager.update_room(booking.room_id, availability_status=True)
            del self.bookings[booking_id]
            self.save_bookings()
        else:
            raise Exception("Booking not found")

    def check_in(self, booking_id):
        if booking_id in self.bookings:
            print(f"Check-in complete for Booking ID: {booking_id}")
        else:
            raise Exception("Booking not found")

    def check_out(self, booking_id):
        if booking_id in self.bookings:
            print(f"Check-out complete for Booking ID: {booking_id}")
            booking = self.bookings[booking_id]
            self.hotel_manager.update_room(booking.room_id, availability_status=True)
            del self.bookings[booking_id]
            self.save_bookings()
        else:
            raise Exception("Booking not found")

    def generate_booking_report(self, start_date, end_date, report_file="booking_report.csv"):
        filtered_bookings = [b for b in self.bookings.values()
                             if b.checkin_date >= start_date and b.checkout_date <= end_date]
        try:
            with open(report_file, "w", newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(["Booking ID", "Room Number", "Room Type", "Guest Name", "Check-in", "Check-out"])
                for b in filtered_bookings:
                    writer.writerow([
                        b.booking_id,
                        b.room_id,
                        b.room_type,
                        b.guest_name,
                        b.checkin_date.isoformat(),
                        b.checkout_date.isoformat()
                    ])
            return report_file
        except Exception as e:
            print("Error writing report:", e)
            return None


def str_to_date(date_str):
    return datetime.datetime.strptime(date_str, "%Y-%m-%d").date()
