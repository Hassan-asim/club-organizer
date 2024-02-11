import tkinter as tk
from tkinter import messagebox

class SeniorClubOuting:
    def __init__(self, master):
        self.master = master
        self.master.title("Senior Citizens' Club Outing Organizer")

        self.label1 = tk.Label(master, text="Number of Senior Citizens:")
        self.label1.grid(row=0, column=0)
        self.entry1 = tk.Entry(master)
        self.entry1.grid(row=0, column=1)

        self.button1 = tk.Button(master, text="Calculate Cost", command=self.calculate_cost)
        self.button1.grid(row=1, columnspan=2)

        self.extra_passengers_button = None

        # Initialize variables for recording outing details
        self.num_senior_citizens = 0
        self.coach_cost = 0
        self.meal_cost = 0
        self.ticket_cost = 0
        self.total_cost = 0
        self.num_carers = 0
        self.per_head_cost = 0

    def calculate_cost(self):
        try:
            self.num_senior_citizens = int(self.entry1.get())
            if self.num_senior_citizens < 10 or self.num_senior_citizens > 36:
                messagebox.showerror("Error", "Number of senior citizens must be between 10 and 36.")
                return

            # Calculate total cost
            if 12 <= self.num_senior_citizens <= 16:
                self.coach_cost = 150
                self.meal_cost = 14.00
                self.ticket_cost = 21.00
            elif 17 <= self.num_senior_citizens <= 26:
                self.coach_cost = 190
                self.meal_cost = 13.50
                self.ticket_cost = 20.00
            else:
                self.coach_cost = 225
                self.meal_cost = 13.00
                self.ticket_cost = 19.00

            self.num_carers = 2 if self.num_senior_citizens <= 24 else 3
            self.total_cost = self.coach_cost + (self.meal_cost + self.ticket_cost) * self.num_senior_citizens
            self.per_head_cost = self.total_cost / self.num_senior_citizens

            messagebox.showinfo("Cost Details", f"Total Cost: ${self.total_cost:.2f}\nPer Head Cost: ${self.per_head_cost:.2f}")

            # Open window to record names and amounts paid
            self.record_window = tk.Toplevel(self.master)
            self.record_window.title("Record Outing Details")

            # Adjust window size based on content
            window_width = 800
            window_height = 100 + (self.num_senior_citizens + self.num_carers) * 30
            self.record_window.geometry(f"{window_width}x{window_height}")

            # Create fields to record names and amounts paid
            self.entries = []
            for i in range(self.num_senior_citizens):
                name_label = tk.Label(self.record_window, text=f"Name of Senior Citizen {i+1}:")
                name_label.grid(row=i, column=0)
                name_entry = tk.Entry(self.record_window)
                name_entry.grid(row=i, column=1)
                amount_label = tk.Label(self.record_window, text=f"Amount Paid by Senior Citizen {i+1}:")
                amount_label.grid(row=i, column=2)
                amount_entry = tk.Entry(self.record_window)
                amount_entry.grid(row=i, column=3)
                self.entries.append((name_entry, amount_entry))

            # Create field to record carer's name
            for i in range(self.num_carers):
                carer_label = tk.Label(self.record_window, text=f"Name of Carer {i+1}:")
                carer_label.grid(row=self.num_senior_citizens + i, column=0)
                carer_entry = tk.Entry(self.record_window)
                carer_entry.grid(row=self.num_senior_citizens + i, column=1)

            # Submit button
            submit_button = tk.Button(self.record_window, text="Submit", command=self.record_submit)
            submit_button.grid(row=self.num_senior_citizens + self.num_carers, columnspan=4)

            # Calculate Profit button
            calculate_profit_button = tk.Button(self.record_window, text="Calculate Profit", command=self.calculate_profit)
            calculate_profit_button.grid(row=self.num_senior_citizens + self.num_carers + 1, columnspan=4)

            # Add extra passengers button
            if self.num_senior_citizens < 36:
                available_seats = 36 - self.num_senior_citizens - self.num_carers
                if available_seats > 0:
                    self.extra_passengers_button = tk.Button(self.record_window, text="Add Extra Passengers", command=self.add_extra_passengers)
                    self.extra_passengers_button.grid(row=self.num_senior_citizens + self.num_carers + 2, columnspan=4)

        except ValueError:
            messagebox.showerror("Error", "Please enter a valid number of senior citizens.")

    def record_submit(self):
        try:
            # Validate amounts paid
            amounts_paid = []
            for name_entry, amount_entry in self.entries:
                name = name_entry.get()
                amount = amount_entry.get()  # Get text from entry widget
                if not amount:
                    messagebox.showerror("Error", "Please enter an amount for all senior citizens.")
                    return
                amount = float(amount)  # Convert text to float
                if amount < 0:
                    messagebox.showerror("Error", "Amount paid cannot be negative.")
                    return
                amounts_paid.append((name, amount))

            # Validate carer's name
            carer_names = []
            for i in range(self.num_carers):
                # Get carer entry widgets
                carer_entries = [widget for widget in self.record_window.grid_slaves() if isinstance(widget, tk.Entry) and widget.grid_info()["row"] == self.num_senior_citizens + i]
                if carer_entries:
                    carer_name = carer_entries[0].get()
                    if not carer_name:
                        messagebox.showerror("Error", f"Please enter name for Carer {i+1}.")
                        return
                    carer_names.append(carer_name)
                else:
                    messagebox.showerror("Error", f"Carer {i+1} entry widget not found.")
                    return

            # Calculate total amount collected
            total_collected = sum(amount for _, amount in amounts_paid)

            # Display list of people going on the trip
            outing_list = [f"{name}: ${amount:.2f}" for name, amount in amounts_paid]
            outing_list += [f"Carer {i+1}: {carer_names[i]}" for i in range(self.num_carers)]
            messagebox.showinfo("Outing List", "People going on the trip:\n" + "\n".join(outing_list))
            messagebox.showinfo("Success", f"Outing details recorded successfully.\nTotal amount collected: ${total_collected:.2f}")

        except ValueError:
            messagebox.showerror("Error", "Please enter valid amounts paid.")


    def calculate_profit(self):
        try:
            total_paid = sum(float(amount_entry.get()) for _, amount_entry in self.entries)  # Get text from entry widget
            if total_paid >= self.total_cost:
                messagebox.showinfo("Profit", f"The outing has made a profit of ${total_paid - self.total_cost:.2f}.")
            else:
                messagebox.showinfo("Break-even", "The outing has broken even.")
        except ValueError:
            messagebox.showerror("Error", "Please enter valid amounts paid.")


    def add_extra_passengers(self):
        extra_passenger_window = tk.Toplevel(self.record_window)
        extra_passenger_window.title("Add Extra Passengers")

        # Adjust window size based on content
        window_width = 800
        window_height = 100 + (36 - self.num_senior_citizens - self.num_carers) * 30
        extra_passenger_window.geometry(f"{window_width}x{window_height}")

        available_seats = 36 - self.num_senior_citizens - self.num_carers
        label = tk.Label(extra_passenger_window, text=f"Available Seats: {available_seats}")
        label.grid(row=0, columnspan=2)

        self.extra_entries = []
        for i in range(available_seats):
            name_label = tk.Label(extra_passenger_window, text=f"Name of Extra Passenger {i+1}:")
            name_label.grid(row=i+1, column=0)
            name_entry = tk.Entry(extra_passenger_window)
            name_entry.grid(row=i+1, column=1)
            amount_label = tk.Label(extra_passenger_window, text=f"Amount Paid by Extra Passenger {i+1}:")
            amount_label.grid(row=i+1, column=2)
            amount_entry = tk.Entry(extra_passenger_window)
            amount_entry.grid(row=i+1, column=3)
            self.extra_entries.append((name_entry, amount_entry))

        submit_button = tk.Button(extra_passenger_window, text="Submit", command=lambda: self.record_extra_passengers(extra_passenger_window))
        submit_button.grid(row=available_seats+1, columnspan=4)

    def record_extra_passengers(self, window):
        try:
            # Validate extra passengers
            extra_passengers = []
            for name_entry, amount_entry in self.extra_entries:
                name = name_entry.get()
                amount = float(amount_entry.get())
                if name and amount:
                    extra_passengers.append((name, amount))
                elif (name and not amount) or (amount and not name):
                    messagebox.showerror("Error", "Please enter both name and amount for extra passengers.")
                    return

            if len(extra_passengers) > 36 - self.num_senior_citizens - self.num_carers:
                messagebox.showerror("Error", "Number of extra passengers exceeds available seats.")
                return

            # Display updated total cost and per head cost
            updated_total_cost = self.total_cost + (self.meal_cost + self.ticket_cost) * len(extra_passengers)
            updated_per_head_cost = updated_total_cost / (self.num_senior_citizens + len(extra_passengers) + self.num_carers)
            messagebox.showinfo("Cost Details", f"Updated Total Cost: ${updated_total_cost:.2f}\nUpdated Per Head Cost: ${updated_per_head_cost:.2f}")

            # Display list of people going on the trip
            outing_list = [f"{name}: ${amount:.2f}" for name, amount in extra_passengers]
            outing_list += [f"Carer {i+1}: {self.record_window.children[f'!entry{i}'].get()}" for i in range(self.num_carers)]
            messagebox.showinfo("Outing List", f"People going on the trip:\n{', '.join(outing_list)}")

            window.destroy()

        except ValueError:
            messagebox.showerror("Error", "Please enter valid names and amounts for extra passengers.")

def main():
    root = tk.Tk()
    app = SeniorClubOuting(root)
    root.mainloop()

if __name__ == "__main__":
    main()
