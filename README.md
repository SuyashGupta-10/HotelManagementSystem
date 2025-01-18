Project details-

This  project contains 5 files, one file with the back-end classes and functions (hotel_management.py), another with the front-end GUI (gui.py), 3 CSV files- one for the currently available rooms, another for booking history and another for current bookings that have been made.

The code can run on any operating system which has all the libraries (tkinter, customtkinter, pandas and tkcalendar) installed through the terminal.

  
  Run the gui.py file to run the project.
  
To install pandas-
    Open the terminal and give "pip install pandas" as the input in the
    terminal. The downloading process should start automatically.
    
To install customtkinter-
    Open the terminal and give "pip install customtkinter" as the input in
    the terminal. The downloading process should start automatically.
    
To install tkcalendar-
    Open the terminal and give "pip install tkcalendar" as the input in the
    terminal. The downloading process should start automatically.

Features-

This hotel management application allows you to do a variety of tasks related to managing hotel rooms and bookings through an interactive graphical interface. Some of the specific features include:

1. You can add new rooms to the hotel’s inventory and specify whether they are Single, Double, or Suite rooms. Each type of room has its own fixed price. Once added, rooms are stored in a CSV file, so that even if you close the program, the data is saved and will be there when you reopen it. If a room is no longer needed, you can delete it. The interface shows the manager all the rooms and their status—whether they are currently available or booked—so they always know which rooms they can still offer to guests.

2. For guests, you can create new bookings. When making a booking, you select the type of room first, and then the program shows you which specific rooms of that type are currently available. This makes it simpler for the guest as they don’t  have to guess which room is free.

3. When choosing check-in and check-out dates, you can either type them manually or use a calendar widget that pops up. This calendar ensures that you cannot pick any date that has already passed, so you don’t accidentally schedule a date of the past.

4. After making a booking, it gets saved and added to a table that shows all current bookings along with the guest’s name and their stay dates in the hotel manager’s window. The guest can also later modify the booking (for example, if the guest’s name is misspelled or they wish to change their check-in or check-out dates) or even cancel it entirely if their plans change. Canceling a booking makes the room available again automatically.

5. Check-in and Check-out:
  
   This feature is useful for keeping track of the room status as guests come and go. After a check-out, that room immediately becomes available for new guests.
Every new booking made is added to a history log. This means you have a record of all the bookings that ever happened, even after they’ve ended. You can also create a CSV report for bookings that fall between two specific dates. This report includes details like the room number, guest name, and the exact check-in and check-out dates. It’s handy for generating summaries and analyzing how busy the hotel was during a certain period.

6. All the information about rooms and bookings is stored in CSV files. This means that if you close the application and open it again later, all your data will still be there. Also, whenever bookings are created or canceled, the corresponding room’s availability is updated immediately, so you never have outdated information on which rooms are free.

7. The program does some checks to help the user avoid mistakes:
   
    1. Check-in and check-out dates cannot be before the current day’s date.
  
    2. If you try to book a room that’s unavailable, it will show an error message.
  
    3. If required fields are missing (like the room number or guest name), it lets you know.

  8. The interface has placeholders in the text fields (like “e.g. YYYY-MM-DD”) which guide you on how to enter the data.




Modules and classes-

1. Room, SingleRoom, DoubleRoom, Suite:
    These classes define a room, along with its type, price, and current
    availability. The specialized classes (SingleRoom, DoubleRoom, Suite) are
    just convenient ways to automatically set the price and type when you
    create a room, so you don’t have to remember the price of each kind.
   
2. Booking:
    This class stores all the details of a reservation made by a guest—like
    which room they booked, when they arrive and leave, and the guest’s
    name. It helps keep everything about a single booking in one place.

3. HotelManager:
    This class handles all the room-related actions. It reads and writes the
    room information to a CSV file, lets the manager add or remove rooms,
    updates availability when a booking is made or canceled, and provides
    methods for checking which rooms are available.
   
4. BookingManager:
    This class is all about bookings. It can create new bookings, save them,
    change them if the user made a mistake, or cancel them if the guest
    changes their mind. It also keeps a record of each booking in a history file
    and updates the room’s availability whenever a booking status changes.
5. GUI (HotelApp):
    This is the main user interface class built with customtkinter. It ties together
    everything you can do—adding rooms, making bookings, etc.—into a visual
    package that anyone can use by clicking buttons and selecting options
    from drop-down menus. It organizes the interface into tabs and frames,
    each responsible for different parts of the application (like “Room
    Management” and “Booking Management”), and it refreshes the tables
    whenever something changes, so the user always sees up-to-date
    information.
   
Libraries- 

1. csv:

   This library helps us easily work with CSV files, which are just simple text files that store tables of data. We use it to save and load information about rooms and bookings, so that the data stays there even after the program closes.
   
3. datetime:

   This library deals with dates and times. We use it to make sure the user can’t pick a check-in date from the past, and to compare check-in and check-out dates to prevent mistakes like checking out before checking in.
   
3. customtkinter and tkinter:
   
    These libraries let us create the graphical user interface for our program.
    They contain the tools we use to make windows, buttons, text fields, and
    tables that you see and interact with. customtkinter makes things look a bit
    nicer than the standard tkinter look.
   
4. tkcalendar:
   
    This library gives us a neat calendar widget inside the GUI, so users can
    pick a date by clicking on a calendar instead of typing it in. This helps
    prevent typing errors and makes choosing dates easier.
   
5. pandas:
   
    Pandas is a library that helps us handle data in a table-like format. It is
    similar to using Excel with spreadsheets right inside Python. We use it to
    sort our room and booking information into tables, which we then display in
    our GUI.




  
    
