# Name: Rohit Vasudev

import sys  # Importing the sys function

# This function includes everything related to making a booking, which includes booking an apartment unit, purchasing supplementary and so on.


def make_booking(guests, apartments, supplementary_items, booking_order_history):

    # Enter guest information and added a check to enter only names which carry characters with the help of .isalpha()
    while True:
        guest_name = input(
            "\nEnter the name of the main guest [e.g. Alyssa]:\n").strip()
        if guest_name.isalpha():
            break
        print("Error: enter a valid name with alphabetic characters")

# Enter the number of guests, ensuring that the input will only be an integer
    number_of_guests = int(input("How many people will stay?:\n"))

    while True:
        apartment_id = input("Enter apartment unit ID to book:\n")
        if apartment_id in apartments:
            # dictionary lookup to look up the rate of the apartment unit
            unit_rate = apartments[apartment_id]["rate"]
            print(f"[AUTO] The selected apartment unit rate is ${unit_rate}")
            break
        print("Error: enter a valid apartment unit ID")

# Enter the unit rate, check-in, check-out date, date is handled as a string
    unit_rate = float(
        input("Enter this unit rate per night in AUD (e.g. 100.5):\n"))
    checkin_date = input(
        "When is the guest expected to check in (d/m/yyyy):\n")
    checkout_date = input(
        "When is the guest expected to check out (d/m/yyyy):\n")

# Enter the duration of your stay, added a check to ensure that the guest stays between 1 to 7 nights
    while True:
        length_of_stay = int(input("How long will they stay?:\n"))
        if 1 <= length_of_stay <= 7:
            break
        print("Error: length of stay must be between 1 to 7 nights")

    booking_date = input("Enter the current date (d/m/yyyy):\n")

    # Initializing an empty list to keep track of supplementary orders ordered by the guests at the hotel.
    supplementary_items_ordered = []
    supplementary_items_sub_total = 0.0

    result = bed_capacity_check(
        apartments,
        apartment_id,
        number_of_guests,
        supplementary_items,
        supplementary_items_ordered,
        supplementary_items_sub_total,
        unit_rate,
        length_of_stay
    )

    if result is None:
        print("Returning to main menu...\n")
        return
    else:
        print("Apartment booking confirmed.\n")

    # ======== Supplementary Items =========
    first_item = True

    while True:
        if first_item:
            prompt = "Do you want to order a supplementary item? (y/n):\n"
            first_item = False
        else:
            prompt = "Do you want to order another supplementary item? (y/n):\n"

        # validation of y or n input
        while True:
            choice = input(prompt).lower()
            if choice in ("y", "n"):
                break
            print("Error: please enter y or n")

        if choice == "y":
            while True:
                item_id = input("Enter the supplementary item ID:\n")
                if item_id in supplementary_items:
                    item_price = supplementary_items[item_id]
                    print(f"[AUTO] The selected item price is ${item_price}")
                    break
                print("Error: enter a valid supplementary item ID")

            item_price = float(
                input("Enter the price for this supplementary item:\n"))

            while True:
                item_quantity = int(
                    input("Enter the quantity of the supplementary item:\n"))
                if item_quantity >= 1:
                    break
                print("Error: enter a valid quantity for the supplementary item")

            # Calculation of the cost of the supplementary items
            item_cost = item_price * item_quantity

            print(f"The cost for the supplementary item will be ${item_cost}")

            while True:
                confirmation = input(
                    "Confirm this supplementary item? (y/n):\n").lower()
                if confirmation in ("y", "n"):
                    break
                print("Error: please enter y or n")

            if confirmation == "y":
                supplementary_items_sub_total += item_cost
                supplementary_items_ordered.append(
                    (item_id, item_quantity, item_price, item_cost))
                total_cost_so_far = unit_rate * length_of_stay + supplementary_items_sub_total
                print(f"Item saved. Total cost so far: ${total_cost_so_far}\n")
            else:
                print("Item cancelled")

        elif choice == "n":
            break
        else:
            print("Please enter y or n")

    # ---------Cost calculation-----------
    total_cost_before_discount = unit_rate * \
        length_of_stay + supplementary_items_sub_total
    total_cost = total_cost_before_discount

    # Reward points calculation
    # dictionary look up to return reward points of a guest by using the key guest_name
    current_reward_points = guests.get(guest_name, 0)
    if current_reward_points >= 100:
        print(
            f"[AUTO] {guest_name} currently has {current_reward_points} points")
        while True:
            entry = input(
                "Do you want to use your reward points to add a discount to your booking? (y/n): ").lower()
            if entry in ("y", "n"):
                break
            print("Error: please enter y or n")

        if entry == "y":
            # calculating absolute value of the reward points as 100 reward points = 10$ discount
            max_reward_chunks = current_reward_points // 100
            while True:
                try:
                    reward_chunks = int(input(
                        f"How many 100 reward points chunks do you want to use? (0-{max_reward_chunks}) chunks where each 100 reward chunks = $10: "))
                except ValueError:
                    print("Error: please enter an integer")
                    continue
                # The reward chunks must be between 0 or equal to the max available chunks
                if 0 <= reward_chunks <= max_reward_chunks:
                    break
                print(
                    f"Error: enter a number between 0 and {max_reward_chunks}")

            discount = 10 * reward_chunks
            total_cost = total_cost - discount
            if total_cost < 0:
                total_cost = 0.0

            current_reward_points = current_reward_points - 100 * reward_chunks
            print(f"Discount applied: ${discount}")
            print(f"New total cost: ${total_cost}")

    reward_points = round(total_cost)

    guests[guest_name] = current_reward_points + reward_points

    booking_receipt(guest_name, number_of_guests, apartment_id, unit_rate,
                    checkin_date, checkout_date, length_of_stay, booking_date, total_cost, reward_points, supplementary_items_ordered, supplementary_items_sub_total)

    # Saving orders into booking history of the guest
    if guest_name not in booking_order_history:
        # Makes a list for a new guest to record the booking order history
        booking_order_history[guest_name] = []

        booking_order_history[guest_name].append({
            "apartment": apartment_id,
            "supplementary": [(item_id, qty) for (item_id, qty, _price, _cost) in supplementary_items_ordered],
            "total_cost": total_cost,
            "rewards": reward_points
        })

# This function is used to add a new apartment or update the existing information of an apartment unit


def add_update_info(apartments):
    apartment_info = input("Enter apartment_id, rate and capacity: ").split()

    # the apartment info must be 3 arguments long if the number of arguments is not equal to 3 it raises an error message
    if len(apartment_info) != 3:
        print("Error: Please enter 3 values (id rate capacity).")
        return

    apartment_id = apartment_info[0]
    rate = apartment_info[1]
    capacity = apartment_info[2]

    # If the apartment unit name does not start with a "U" and does not follow naming conventions then it raises an error message. This is achieved with the help of the startswith() function
    if not apartment_id.startswith("U"):
        print("Error: Apartment ID must start with a 'U'")
        return

    # A try and except block is used if the information entered is of the wrong type [5]
    try:
        rate = float(rate)
        capacity = int(capacity)
    except ValueError:
        print("Error: the rate must be a number and capacity must be an integer")
        return

    # if the information of the apartment name or ID follows the naming conventions and has the correct amount of arguments then the information is added to the apartments dictionary with the help of the apartment_id key. Information of an apartment unit such as the unit rate and capacity can also be altered by acessing an existing key in the dictionary
    apartments[apartment_id] = {"rate": rate, "capacity": capacity}
    print(f"Apartment {apartment_id} has been added/updated successfully!")

# This function helps add or update supplementary items to the supplementsary_items dictionary. It can also alter the information about a supplementary item in the dictionary


def add_update_supplementary_items(supplementary_items):

    while True:
        seq = input(
            "Enter supplementary items id and prices (e.g. 'car_park 6.2, towel 7.5'): ")
        try:
            # Initializing an empty list to store the updated supplementary items which is later updated to the supplementary item dictionary
            supplementary_items_updates = {}
            # using a loop to split the input with commas
            # .split() function is used here to split the input with white spaces and commas 
            for x in seq.split(","):
                parts = x.strip().split()
                if len(parts) != 2:  # Adding a check where the length of the supplementary item information must be equal to 2, raises an error if != 2
                    raise ValueError
                id, item_price = parts
                price = float(item_price)
                if price <= 0:
                    raise ValueError
                supplementary_items_updates[id] = price
        except ValueError:
            print("Error: please use 'id, price' with positive numbers.")
            continue

        # .update() function is used for supplementary_item dictionary which is updated with values from the supplementary_items_updates dictionary 
        supplementary_items.update(supplementary_items_updates)
        print("Supplementary Items updated")
        break


# This function helps display the existing guests with the hotel, and also shows their reward points respectively


def display_existing_guests(guests):
    print(" ")
    print("========================================")
    print("        Guests & Reward Points          ")
    print("========================================")
    # If the guests dictionary iniialized is empty ir returns False and then displays a message
    if not guests:
        print("No guests found")
        return

    for name, points in guests.items():
        print(name, ":", points, "reward points")
    print("========================================")
    print(" ")

# This function displays the apartment units that are available at the hotel or the apartment units that are initialized


def display_apartment_units(apartments):
    print(" ")
    print("========================================")
    print("            Apartment Units             ")
    print("========================================")

    print("Apartment_ID      Rate      Capacity")
    print("========================================")
    print(" ")

    if not apartments:
        print("No apartments found")
        return
    # A for loop is used to loop over the dictionary and retrieve values in the dictionary with the help of the .items() function, which is used to print the rate and capacity of an apartment unit at the hotel.
    # .items() function is used to access the values inside a dictionary 
    for apartment_id, info in apartments.items():
        rate = info.get("rate")
        capacity = info.get("capacity")
        print("  ", apartment_id, "      ", "$", rate, "        ", capacity)
    print("========================================")

# This function displays all the available supplementary items to add on to the guest's booking


def display_supplementary_items(supplementary_items):
    print(" ")
    print("========================================")
    print("          Supplementary Items           ")
    print("========================================")
    print(" ")

    # if the supplementary item does not exist in the supplementary_items dictionary it raises a message that the item was not found
    if not supplementary_items:
        print("No supplementary items found")
        return
    for supplementary_id, price in supplementary_items.items():
        print("         ", supplementary_id, ":", "$", price)
    print("========================================")


def bed_capacity_check(apartments, apartment_id, number_of_guests, supplementary_items, supplementary_items_ordered, supplementary_items_sub_total, unit_rate, length_of_stay):

    # dictionary look up to find the default capacity which was inisitalized to the apartment
    capacity = apartments[apartment_id]["capacity"]
    apartment_capacity = capacity  # temporary capacity
    extra_bed_purchased = 0
    extra_bed_cost = supplementary_items.get("extra_bed", 50.0)

    if number_of_guests > apartment_capacity:
        print("Warning: please consider ordering an extra bed")

        while number_of_guests > apartment_capacity and extra_bed_purchased < 2:
            entry = input(
                f"Add an extra bed?(y/n). You can add upto {2 - extra_bed_purchased} bed(s): ").lower()
            if entry not in ("y", "n"):
                print("Error: please enter y or n")
                continue
            if entry == "n":
                break

            beds_left = 2 - extra_bed_purchased
            
            try:
                quantity = int(
                    input(f"How many extra beds (extra beds available - {beds_left})?: "))
            except ValueError:
                print("Error: please enter an integer")
                continue

            if not (1 <= quantity <= beds_left):
                print(f"Error: enter a number between 1 and {beds_left}")
                continue

            item_id = "extra_bed"
            item_price = extra_bed_cost
            item_cost = item_price * quantity

            print(f"[AUTO] Extra bed price: ${item_price}")
            print(f"Cost for {quantity} extra bed(s): ${item_cost}")

            confirmation = input(
                "Confirm extra bed(s) purchase? (y/n): ").lower()
            if confirmation == "y":
                apartment_capacity += 2 * quantity
                extra_bed_purchased += quantity
                supplementary_items_sub_total += item_cost
                supplementary_items_ordered.append(
                    (item_id, quantity, item_price, item_cost))
                total_cost_so_far = unit_rate * length_of_stay + supplementary_items_sub_total
                print(
                    f"Extra bed(s) added. New apartment capacity: {apartment_capacity}")
                print(f"Total cost accumulated so far: ${total_cost_so_far}")
            else:
                print("Extra bed(s) cancelled")

    if number_of_guests > apartment_capacity:
        print("Sorry, this booking cannot proceed: the number of guests exceed the capacity of the apartment despite having extra beds")
        return None

    return supplementary_items_sub_total  # return the updated subtotal

# This function displays the order history of the guest along with any order history of supplementary items


def display_guest_order_history(booking_order_history):

    guest_name = input("Enter guest name: ")

    if guest_name not in booking_order_history:
        print(f"No booking and order history available for {guest_name}.")
        return

    print(f"This is the booking and order history for {guest_name}")
    print("List     Total Cost  Earned Rewards")

    count = 1
    for order in booking_order_history[guest_name]:
        items_text = f"1 x {order['apartment']}"

        for item, quantity in order["supplementary"]:
            items_text += f", {quantity} X {item}"

        print(
            f"Order {count}: {items_text}\t{order['total_cost']}\t{order['rewards']}")
        count += 1


# This is the main function of the program
def main():

    # Initializing the guests, apartments and supplementary items of the hotel booking system with the help of dictionaries.
    guests = {
        "Alyssa": 20,
        "Luigi": 32
    }

    apartments = {
        "U12swan": {"rate": 95.0, "capacity": 2},
        "U209duck": {"rate": 106.7, "capacity": 2},
        "U49goose": {"rate": 145.2, "capacity": 2},
    }

    # Initialized a dictionary of supplementary items
    supplementary_items = {
        "car_park": 25.0,
        "breakfast": 21.0,
        "toothpaste": 5.0,
        "extra_bed": 50.0
    }

    # Initializing an empty dictionary for tracking the order history of guests who make bookings at the hotel
    booking_order_history = {}

    # if a valid menu number option is entered it executes one of the following functions linked with the menu number. Functions include the different options to make a booking, add/update supplementary items, apartments, and so on

    # Using a menu driven program
    while True:
        menu()
        choice = menu_choice()

        if choice == "1":
            make_booking(guests, apartments, supplementary_items,
                         booking_order_history)
        elif choice == "2":
            add_update_info(apartments)
        elif choice == "3":
            add_update_supplementary_items(supplementary_items)
        elif choice == "4":
            display_existing_guests(guests)
        elif choice == "5":
            display_apartment_units(apartments)
        elif choice == "6":
            display_supplementary_items(supplementary_items)
        elif choice == "7":
            display_guest_order_history(booking_order_history)
        elif choice == "0":
            print("\nGood bye!")
            break


# Prints the menu booking system


def menu():

    print("\nWelcome to Debugger's Hut Serviced Apartments!"
          "\n"
          "\n============================================================="
          "\nPlease choose from the following options:"
          "\n1) Make a booking"
          "\n2) Add/update information of an apartment unit"
          "\n3) Add/update information of a supplementary item"
          "\n4) Display existing guests"
          "\n5) Display existing apartment units"
          "\n6) Display existing supplementary items"
          "\n7) Display a guest booking and order history"
          "\n0) Exit the program"
          "\n=============================================================")

# This function adds a check to only enter the numbers within the set of menu choices, it raises an error if an invalid number is entered which does not belong to the set


def menu_choice():
    num_choices = {"1", "2", "3", "4", "5", "6", "7", "0"}
    # A while loop is used here to allow the user to enter an entry multiple times and then finally breaks once the correct ntry is entered
    while True:
        choice = input("\nEnter a number to choose an option: ")
        if choice in num_choices:
            return choice
        print("Error: please enter a valid menu number")


# This function prints the booking receipt of the guests who stay at the hotel
def booking_receipt(guest_name, number_of_guests, apartment_name, unit_rate, checkin_date, checkout_date, length_of_stay, booking_date, total_cost, reward_points, supplementary_items_ordered, supplementary_items_sub_total):

    print("\n"
          "\n======================================================================="
          "\n\t  Debuggers Hut Serviced Apartments - Booking Receipt"
          "\n======================================================================="
          f"\nGuest Name:           {guest_name}"
          f"\nNumber of guests:     {number_of_guests}"
          f"\nApartment name:       {apartment_name}"
          f"\nApartment rate:       {unit_rate}(AUD)"
          f"\nCheck-in date:        {checkin_date}"
          f"\nCheck-out date:       {checkout_date}"
          f"\nLength of stay:       {length_of_stay} (nights)"
          f"\nBooking date:         {booking_date}"
          "\n-----------------------------------------------------------------------")

    # If there are any supplementary items purchased during the booking of an apartment unit at the hotel, it checks if the supplementary_items_ordered list is empty or not. If supplementary_items_ordered is True and is not empty then it prints another part of the booking receipt which includes the information about the supplementary items purchased while booking an apartment unit
    if supplementary_items_ordered:
        print("\nSupplementary items")
        for item_id, item_quantity, item_price, item_cost in supplementary_items_ordered:
            print(f"\nItem id:               {item_id}"
                  f"\nQuantity:              {item_quantity}"
                  f"\nPrice:                 ${item_price}"
                  f"\nCost:                  ${item_cost}"
                  f"\nSub-total:             ${supplementary_items_sub_total}"
                  "\n-----------------------------------------------------------------------")

    print(f"\nTotal cost: {total_cost} (AUD)"
          f"\nEarned rewards: {reward_points} (points)"
          "\n"
          "\nThank you for your booking! We hope you will have an enjoyable stay."

          "\n======================================================================="
          "\n")


if __name__ == "__main__":
    main()

