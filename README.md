# Debugger's Hut Serviced Apartments 🏨

This is a **Python-based hotel booking system** that allows users to manage guests, apartment units, and supplementary items for a serviced apartment business.  
It is a **menu-driven console application** built using only Python’s standard library (`sys`).

---

## Features

- Make and manage bookings:
  - Collects guest details with input validation
  - Choose apartment units with rates and capacities
  - Add supplementary items (e.g., car park, breakfast, extra bed)
  - Calculates total cost and generates a detailed booking receipt
  - Redeem reward points (100 points = $10 discount)

- Manage data:
  - Add or update apartment unit information (ID, rate, capacity)
  - Add or update supplementary items with prices
  - Display all existing guests and their reward points
  - Display available apartment units and supplementary items

- Track guest history:
  - Stores booking and order history
  - Shows past stays and purchased supplementary items

---

## How to Run

1. Clone this repository:
   ```bash
   git clone https://github.com/YOUR-USERNAME/hotel-booking-system.git

2. Navigate into the folder:
   ```bash
   cd hotel-booking-system
   
3. Run the program:
   ```bash
   python ProgFunA1_s4173731.py
   ```


## Example Menu:

Welcome to Debugger's Hut Serviced Apartments!
=============================================================
Please choose from the following options:
1) Make a booking
2) Add/update information of an apartment unit
3) Add/update information of a supplementary item
4) Display existing guests
5) Display existing apartment units
6) Display existing supplementary items
7) Display a guest booking and order history
0) Exit the program
=============================================================


## Future Improvements:

1. Save data to a database (SQLite/JSON)
2. Build a GUI version (Tkinter or PyQt)
3. Add PDF export for receipts
4. Expand the reward system with tiers
