import customtkinter as ctk
import tkinter.messagebox as mb
from tkinter import ttk
import pandas as pd
from tkcalendar import Calendar
from hotel_management import *


class HotelApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Hotel Management System")
        self.geometry("1000x700")
        ctk.set_appearance_mode("System")
        ctk.set_default_color_theme("blue")
        self.hotel_manager = HotelManager()
        self.booking_manager = BookingManager(self.hotel_manager)
        self.heading_font = ctk.CTkFont(family="Times New Roman", size=24, weight="bold")
        self.label_font = ctk.CTkFont(family="Arial", size=12)
        self.entry_font = ctk.CTkFont(family="Arial", size=12)
        self.button_font = ctk.CTkFont(family="Arial", size=12, weight="bold")
        self.style = ttk.Style(self)
        self.style.configure("Treeview", font=("Arial", 12))
        self.create_widgets()
        self.setup_tables()
        self.refresh_tables()

    def create_widgets(self):
        main_frame = ctk.CTkFrame(self)
        main_frame.pack(fill="both", expand=True)
        self.tabview = ctk.CTkTabview(main_frame, width=980, height=660)
        self.tabview.pack(expand=True, fill="both")
        self.room_tab = self.tabview.add("Room Management")
        self.booking_tab = self.tabview.add("Booking Management")
        self.room_tab.grid_columnconfigure(0, weight=1)
        self.booking_tab.grid_columnconfigure(0, weight=1)
        room_heading = ctk.CTkLabel(self.room_tab, text="Manage Rooms",
                                    font=self.heading_font, anchor="center")
        room_heading.grid(row=0, column=0, pady=(20, 20))
        actions_frame = ctk.CTkFrame(self.room_tab)
        actions_frame.grid(row=1, column=0, pady=10, padx=10, sticky="ew")
        actions_frame.grid_columnconfigure(0, weight=1)
        actions_frame.grid_columnconfigure(1, weight=1)
        room_input_frame = ctk.CTkFrame(actions_frame)
        room_input_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        room_id_label = ctk.CTkLabel(room_input_frame, text="Room Number:", font=self.label_font)
        room_id_label.pack(pady=5)
        self.room_id_entry = ctk.CTkEntry(room_input_frame, width=200, placeholder_text="e.g. 101",
                                          font=self.entry_font)
        self.room_id_entry.pack(pady=5)
        room_type_label = ctk.CTkLabel(room_input_frame, text="Room Type:", font=self.label_font)
        room_type_label.pack(pady=5)
        self.room_type_option = ctk.CTkOptionMenu(room_input_frame, values=["Single", "Double", "Suite"],
                                                  font=self.entry_font)
        self.room_type_option.set("Single")
        self.room_type_option.pack(pady=5)
        self.add_room_btn = ctk.CTkButton(room_input_frame, text="Add Room", command=self.add_room,
                                          font=self.button_font)
        self.add_room_btn.pack(pady=10)
        delete_room_frame = ctk.CTkFrame(actions_frame)
        delete_room_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")
        delete_label = ctk.CTkLabel(delete_room_frame, text="Delete Room by ID:", font=self.label_font)
        delete_label.pack(pady=5)
        self.delete_room_id_entry = ctk.CTkEntry(delete_room_frame, width=200, placeholder_text="e.g. 101",
                                                 font=self.entry_font)
        self.delete_room_id_entry.pack(pady=5)
        self.delete_room_btn = ctk.CTkButton(delete_room_frame, text="Delete Room", command=self.delete_room,
                                             font=self.button_font)
        self.delete_room_btn.pack(pady=10)
        tables_frame = ctk.CTkFrame(self.room_tab)
        tables_frame.grid(row=2, column=0, pady=20)
        tables_frame.grid_columnconfigure(0, weight=1)
        tables_frame.grid_columnconfigure(1, weight=1)
        rooms_label = ctk.CTkLabel(tables_frame, text="Rooms in Hotel:",
                                   font=self.label_font, anchor="center")
        rooms_label.grid(row=0, column=0, pady=(5, 10), padx=10)
        self.rooms_tree = ttk.Treeview(tables_frame, show="headings", style="Treeview")
        self.rooms_tree.grid(row=1, column=0, padx=10, pady=10)
        guest_label = ctk.CTkLabel(tables_frame, text="Guest Bookings:",
                                   font=self.label_font, anchor="center")
        guest_label.grid(row=0, column=1, pady=(5, 10), padx=10)
        self.guest_tree = ttk.Treeview(tables_frame, show="headings", style="Treeview")
        self.guest_tree.grid(row=1, column=1, padx=10, pady=10)
        self.generate_history_btn = ctk.CTkButton(tables_frame, text="Generate Booking History",
                                                  command=self.generate_booking_history,
                                                  font=self.button_font)
        self.generate_history_btn.grid(row=2, column=0, columnspan=2, pady=(10, 0))
        self.booking_scroll_frame = ctk.CTkScrollableFrame(self.booking_tab, width=960, height=640)
        self.booking_scroll_frame.pack(expand=True, fill="both")
        self.booking_scroll_frame.grid_columnconfigure(0, weight=1)
        booking_heading = ctk.CTkLabel(self.booking_scroll_frame, text="Manage Bookings",
                                       font=self.heading_font, anchor="center")
        booking_heading.grid(row=0, column=0, pady=(20, 20), sticky="ew")
        booking_actions_frame = ctk.CTkFrame(self.booking_scroll_frame)
        booking_actions_frame.grid(row=1, column=0, pady=10, padx=10, sticky="ew")
        booking_actions_frame.grid_columnconfigure(0, weight=1)
        booking_actions_frame.grid_columnconfigure(1, weight=1)
        booking_input_frame = ctk.CTkFrame(booking_actions_frame)
        booking_input_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        booking_input_frame.grid_columnconfigure(0, weight=1)
        room_type_booking_label = ctk.CTkLabel(booking_input_frame, text="Room Type:", font=self.label_font)
        room_type_booking_label.pack(pady=5)
        self.booking_room_type_option = ctk.CTkOptionMenu(
            booking_input_frame,
            values=["Single", "Double", "Suite"],
            font=self.entry_font,
            command=self.update_room_id_options
        )
        self.booking_room_type_option.set("")
        self.booking_room_type_option.pack(pady=5)
        booking_room_id_label = ctk.CTkLabel(booking_input_frame, text="Available Rooms:", font=self.label_font)
        booking_room_id_label.pack(pady=5)
        self.booking_room_id_option = ctk.CTkOptionMenu(booking_input_frame, values=[], font=self.entry_font)
        self.booking_room_id_option.set("")
        self.booking_room_id_option.pack(pady=5)
        guest_name_label = ctk.CTkLabel(booking_input_frame, text="Guest Name:", font=self.label_font)
        guest_name_label.pack(pady=5)
        self.guest_name_entry = ctk.CTkEntry(booking_input_frame, width=200, placeholder_text="e.g. Suyash",
                                             font=self.entry_font)
        self.guest_name_entry.pack(pady=5)
        checkin_label = ctk.CTkLabel(booking_input_frame, text="Check-in Date:", font=self.label_font)
        checkin_label.pack(pady=5)
        self.checkin_btn = ctk.CTkButton(booking_input_frame, text="Select Check-in Date",
                                         command=lambda: self.open_calendar(self.checkin_entry),
                                         font=self.button_font)
        self.checkin_btn.pack(pady=5)
        self.checkin_entry = ctk.CTkEntry(booking_input_frame, width=200, font=self.entry_font,
                                          placeholder_text="e.g. YYYY-MM-DD")
        self.checkin_entry.pack(pady=5)
        checkout_label = ctk.CTkLabel(booking_input_frame, text="Check-out Date:", font=self.label_font)
        checkout_label.pack(pady=5)
        self.checkout_btn = ctk.CTkButton(booking_input_frame, text="Select Check-out Date",
                                          command=lambda: self.open_calendar(self.checkout_entry),
                                          font=self.button_font)
        self.checkout_btn.pack(pady=5)
        self.checkout_entry = ctk.CTkEntry(booking_input_frame, width=200, font=self.entry_font,
                                           placeholder_text="e.g. YYYY-MM-DD")
        self.checkout_entry.pack(pady=5)
        booking_buttons_frame = ctk.CTkFrame(booking_input_frame)
        booking_buttons_frame.pack(pady=10)
        self.make_booking_btn = ctk.CTkButton(booking_buttons_frame, text="Make Booking", command=self.make_booking,
                                              font=self.button_font)
        self.make_booking_btn.pack(side="left", padx=5)
        self.clear_fields_btn = ctk.CTkButton(booking_buttons_frame, text="Clear", command=self.clear_booking_fields,
                                              font=self.button_font)
        self.clear_fields_btn.pack(side="left", padx=5)
        modify_frame = ctk.CTkFrame(booking_actions_frame)
        modify_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")
        modify_frame.grid_columnconfigure(0, weight=1)
        modify_label = ctk.CTkLabel(modify_frame, text="Modify Booking", font=self.heading_font, anchor="center")
        modify_label.pack(pady=10)
        booking_id_label = ctk.CTkLabel(modify_frame, text="Booking ID:", font=self.label_font)
        booking_id_label.pack(pady=5)
        self.modify_booking_id_entry = ctk.CTkEntry(modify_frame, width=200, placeholder_text="e.g. B1",
                                                    font=self.entry_font)
        self.modify_booking_id_entry.pack(pady=5)
        new_guest_label = ctk.CTkLabel(modify_frame, text="New Guest Name:", font=self.label_font)
        new_guest_label.pack(pady=5)
        self.modify_guest_entry = ctk.CTkEntry(modify_frame, width=200, placeholder_text="e.g. Shrey",
                                               font=self.entry_font)
        self.modify_guest_entry.pack(pady=5)
        modify_checkin_label = ctk.CTkLabel(modify_frame, text="New Check-in Date:", font=self.label_font)
        modify_checkin_label.pack(pady=5)
        self.modify_checkin_btn = ctk.CTkButton(modify_frame, text="Select New Check-in Date",
                                                command=lambda: self.open_calendar(self.modify_checkin_entry),
                                                font=self.button_font)
        self.modify_checkin_btn.pack(pady=5)
        self.modify_checkin_entry = ctk.CTkEntry(modify_frame, width=200, font=self.entry_font,
                                                 placeholder_text="e.g. YYYY-MM-DD")
        self.modify_checkin_entry.pack(pady=5)
        modify_checkout_label = ctk.CTkLabel(modify_frame, text="New Check-out Date:", font=self.label_font)
        modify_checkout_label.pack(pady=5)
        self.modify_checkout_btn = ctk.CTkButton(modify_frame, text="Select New Check-out Date",
                                                 command=lambda: self.open_calendar(self.modify_checkout_entry),
                                                 font=self.button_font)
        self.modify_checkout_btn.pack(pady=5)
        self.modify_checkout_entry = ctk.CTkEntry(modify_frame, width=200, font=self.entry_font,
                                                  placeholder_text="e.g. YYYY-MM-DD")
        self.modify_checkout_entry.pack(pady=5)
        self.modify_booking_btn = ctk.CTkButton(modify_frame, text="Modify Booking", command=self.modify_booking,
                                                font=self.button_font)
        self.modify_booking_btn.pack(pady=10)
        cancel_frame = ctk.CTkFrame(self.booking_scroll_frame)
        cancel_frame.grid(row=2, column=0, pady=10, sticky="ew")
        cancel_frame.grid_columnconfigure(0, weight=1)
        cancel_label = ctk.CTkLabel(cancel_frame, text="Cancel Booking", font=self.heading_font, anchor="center")
        cancel_label.pack(pady=10)
        cancel_booking_id_label = ctk.CTkLabel(cancel_frame, text="Booking ID:", font=self.label_font)
        cancel_booking_id_label.pack(pady=5)
        self.cancel_booking_id_entry = ctk.CTkEntry(cancel_frame, width=200, placeholder_text="e.g. B1",
                                                    font=self.entry_font)
        self.cancel_booking_id_entry.pack(pady=5)
        self.cancel_booking_btn = ctk.CTkButton(cancel_frame, text="Cancel Booking", command=self.cancel_booking,
                                                font=self.button_font)
        self.cancel_booking_btn.pack(pady=10)

    def open_calendar(self, entry_field):
        cal_win = ctk.CTkToplevel(self)
        cal_win.title("Select Date")
        cal_win.grab_set()
        cal_win.lift()
        cal_win.focus_set()
        today = datetime.date.today()
        cal = Calendar(cal_win, selectmode='day', year=today.year, month=today.month, day=today.day,
                       mindate=today)
        cal.pack(pady=20)
        def set_date():
            selected_date = cal.selection_get()
            entry_field.delete(0, "end")
            entry_field.insert(0, selected_date.isoformat())
            cal_win.destroy()
        select_btn = ctk.CTkButton(cal_win, text="Select", command=set_date)
        select_btn.pack(pady=10)

    def update_room_id_options(self, selected_type):
        if not selected_type:
            self.booking_room_id_option.configure(values=[])
            self.booking_room_id_option.set("")
            return
        rooms = [r.room_id for r in self.hotel_manager.get_all_rooms() if r.type == selected_type and r.availability_status]
        if not rooms:
            mb.showerror("Error", "No room available")
            self.booking_room_id_option.configure(values=[])
            self.booking_room_id_option.set("")
        else:
            self.booking_room_id_option.configure(values=rooms)
            self.booking_room_id_option.set(rooms[0] if rooms else "")

    def clear_booking_fields(self):
        self.booking_room_type_option.set("")
        self.booking_room_id_option.configure(values=[])
        self.booking_room_id_option.set("")
        self.guest_name_entry.delete(0, "end")
        self.checkin_entry.delete(0, "end")
        self.checkout_entry.delete(0, "end")
        self.show_info("Entries cleared successfully")

    def setup_tables(self):
        room_columns = ["Room Number", "Type", "Price", "Available"]
        self.rooms_tree["columns"] = room_columns
        for col in room_columns:
            self.rooms_tree.heading(col, text=col)
            self.rooms_tree.column(col, width=120, anchor="center")
        booking_columns = ["Booking ID", "Room Number", "Room Type", "Guest Name", "Check-in", "Check-out"]
        self.guest_tree["columns"] = booking_columns
        for col in booking_columns:
            self.guest_tree.heading(col, text=col)
            self.guest_tree.column(col, width=120, anchor="center")

    def show_error(self, message, widget_to_clear=None):
        mb.showerror("Error", message)
        if widget_to_clear is not None:
            widget_to_clear.delete(0, "end")
            widget_to_clear.focus_set()

    def show_info(self, message):
        mb.showinfo("Success", message)

    def validate_room_id(self, room_id_str, widget):
        try:
            room_id = int(room_id_str)
            return room_id
        except ValueError:
            self.show_error("Room Number can only be an integer", widget)
            return None

    def validate_guest_name(self, guest_name, widget):
        if not guest_name.isalpha():
            self.show_error("Guest name can only be alphabetic characters", widget)
            return False
        return True

    def add_room(self):
        room_id_str = self.room_id_entry.get()
        room_type = self.room_type_option.get()
        if not room_id_str or not room_type:
            self.show_error("Missing room details.", self.room_id_entry if not room_id_str else None)
            return
        room_id = self.validate_room_id(room_id_str, self.room_id_entry)
        if room_id is None:
            return
        if str(room_id) in self.hotel_manager.rooms:
            self.show_error("Room already exists", self.room_id_entry)
            return
        if room_type == "Single":
            room = SingleRoom(str(room_id))
        elif room_type == "Double":
            room = DoubleRoom(str(room_id))
        else:
            room = Suite(str(room_id))
        try:
            self.hotel_manager.add_room(room)
            self.refresh_tables()
        except Exception as e:
            self.show_error(str(e), self.room_id_entry)

    def delete_room(self):
        room_id_str = self.delete_room_id_entry.get()
        if not room_id_str:
            self.show_error("Please provide a Room Number to delete.", self.delete_room_id_entry)
            return
        room_id = self.validate_room_id(room_id_str, self.delete_room_id_entry)
        if room_id is None:
            return
        for booking in self.booking_manager.bookings.values():
            if booking.room_id == str(room_id):
                self.show_error("Cannot delete a booked room")
                return
        if str(room_id) not in self.hotel_manager.rooms:
            self.show_error("Room does not exist", self.delete_room_id_entry)
            return
        try:
            self.hotel_manager.delete_room(str(room_id))
            self.refresh_tables()
        except Exception as e:
            self.show_error(str(e), self.delete_room_id_entry)

    def make_booking(self):
        room_id_str = self.booking_room_id_option.get()
        room_type = self.booking_room_type_option.get()
        guest_name = self.guest_name_entry.get()
        checkin = self.checkin_entry.get()
        checkout = self.checkout_entry.get()
        if not (room_id_str and room_type and guest_name and checkin and checkout):
            clear_widget = None
            if not room_id_str:
                clear_widget = None
            elif not guest_name:
                clear_widget = self.guest_name_entry
            elif not checkin:
                clear_widget = self.checkin_entry
            elif not checkout:
                clear_widget = self.checkout_entry
            self.show_error("Missing booking details.", clear_widget)
            return
        room_id = self.validate_room_id(room_id_str, None)
        if room_id is None:
            return
        if not self.validate_guest_name(guest_name, self.guest_name_entry):
            return
        try:
            checkin_date = datetime.date.fromisoformat(checkin)
            checkout_date = datetime.date.fromisoformat(checkout)
        except ValueError:
            self.show_error("Invalid date format. Please re-select or re-enter dates.", self.checkin_entry)
            return
        today = datetime.date.today()
        if checkin_date < today or checkout_date < today:
            self.show_error("Check-in and Check-out dates cannot be before today's date.", self.checkin_entry)
            return
        if checkout_date <= checkin_date:
            self.show_error("Check-out must be after check-in", self.checkout_entry)
            return
        try:
            booking_id = self.booking_manager.make_booking(str(room_id), room_type, guest_name, checkin_date, checkout_date)
            self.refresh_tables()
            self.booking_room_id_option.set("")
            self.guest_name_entry.delete(0, "end")
            self.checkin_entry.delete(0, "end")
            self.checkout_entry.delete(0, "end")
            self.show_info("Booking done successfully")
        except Exception as e:
            self.show_error(str(e), None)

    def modify_booking(self):
        booking_id = self.modify_booking_id_entry.get()
        new_guest_name = self.modify_guest_entry.get()
        new_checkin_str = self.modify_checkin_entry.get().strip()
        new_checkout_str = self.modify_checkout_entry.get().strip()
        if not booking_id:
            self.show_error("Missing modification details.", self.modify_booking_id_entry)
            return
        if booking_id not in self.booking_manager.bookings:
            self.show_error("Booking does not exist.", self.modify_booking_id_entry)
            return
        if new_guest_name and not self.validate_guest_name(new_guest_name, self.modify_guest_entry):
            return
        checkin_date = None
        checkout_date = None
        if new_checkin_str or new_checkout_str:
            if not new_checkin_str:
                self.show_error("New Check-in date is missing.", self.modify_checkin_entry)
                return
            if not new_checkout_str:
                self.show_error("New Check-out date is missing.", self.modify_checkout_entry)
                return
            try:
                checkin_date = datetime.date.fromisoformat(new_checkin_str)
                checkout_date = datetime.date.fromisoformat(new_checkout_str)
            except ValueError:
                self.show_error("Invalid date format. Please re-select or re-enter dates.", self.modify_checkin_entry)
                return
            today = datetime.date.today()
            if checkin_date < today or checkout_date < today:
                self.show_error("Check-in and Check-out dates cannot be before today's date.", self.modify_checkin_entry)
                return
            if checkout_date <= checkin_date:
                self.show_error("Check-out must be after check-in", self.modify_checkout_entry)
                return
        modify_kwargs = {}
        if new_guest_name:
            modify_kwargs['guest_name'] = new_guest_name
        if checkin_date and checkout_date:
            modify_kwargs['checkin_date'] = checkin_date
            modify_kwargs['checkout_date'] = checkout_date
        try:
            self.booking_manager.modify_booking(booking_id, **modify_kwargs)
            self.refresh_tables()
            self.modify_booking_id_entry.delete(0, "end")
            self.modify_guest_entry.delete(0, "end")
            self.modify_checkin_entry.delete(0, "end")
            self.modify_checkout_entry.delete(0, "end")
            self.show_info("Booking modified successfully")
        except Exception as e:
            self.show_error(str(e), self.modify_booking_id_entry)

    def cancel_booking(self):
        booking_id = self.cancel_booking_id_entry.get()
        if not booking_id:
            self.show_error("No booking ID provided.", self.cancel_booking_id_entry)
            return
        if booking_id not in self.booking_manager.bookings:
            self.show_error("Booking does not exist.", self.cancel_booking_id_entry)
            return
        try:
            # Before cancellation, retrieve the booking and log it
            booking = self.booking_manager.bookings[booking_id]
            self.booking_manager.log_booking_history(booking)
            self.booking_manager.cancel_booking(booking_id)
            self.refresh_tables()
            self.cancel_booking_id_entry.delete(0, "end")
            self.show_info("Booking cancelled successfully")
        except Exception as e:
            self.show_error(str(e), self.cancel_booking_id_entry)

    def refresh_tables(self):
        self.refresh_room_table()
        self.refresh_guest_booking_table()

    def refresh_room_table(self):
        self.rooms_tree.delete(*self.rooms_tree.get_children())
        rooms_data = []
        for r in self.hotel_manager.get_all_rooms():
            rooms_data.append([r.room_id, r.type, r.price, r.availability_status])
        df_rooms = pd.DataFrame(rooms_data, columns=["Room Number", "Type", "Price", "Available"])
        for idx, row in df_rooms.iterrows():
            self.rooms_tree.insert("", "end", values=list(row))

    def refresh_guest_booking_table(self):
        self.guest_tree.delete(*self.guest_tree.get_children())
        bookings_data = []
        for b in self.booking_manager.bookings.values():
            bookings_data.append([b.booking_id, b.room_id, b.room_type, b.guest_name, b.checkin_date, b.checkout_date])
        df_bookings = pd.DataFrame(bookings_data,
                                   columns=["Booking ID", "Room Number", "Room Type", "Guest Name", "Check-in",
                                            "Check-out"])
        for idx, row in df_bookings.iterrows():
            self.guest_tree.insert("", "end", values=list(row))

    def generate_booking_history(self):
        if not os.path.exists(self.booking_manager.BOOKING_HISTORY_FILE):
            mb.showerror("Error", "No booking history found.")
            return
        try:
            with open(self.booking_manager.BOOKING_HISTORY_FILE, "r", newline='', encoding='utf-8') as f:
                reader = csv.reader(f)
                data = list(reader)
        except Exception as e:
            mb.showerror("Error", f"Failed to read booking history: {e}")
            return
        if not data:
            mb.showerror("Error", "No booking history found.")
            return
        history_window = ctk.CTkToplevel(self)
        history_window.title("Booking History")
        columns = ["Booking ID", "Room Number", "Room Type", "Guest Name", "Check-in", "Check-out"]
        history_tree = ttk.Treeview(history_window, show="headings", columns=columns)
        for col in columns:
            history_tree.heading(col, text=col)
            history_tree.column(col, width=120, anchor="center")
        history_tree.pack(fill="both", expand=True)
        for row in data:
            if row:
                history_tree.insert("", "end", values=row)

if __name__ == "__main__":
    app = HotelApp()
    app.mainloop()
