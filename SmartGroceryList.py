"""
Author: Shayne Frost
Assignment: Module 08 Final Project Submission
Date Revised: 10/13/2024

This program is a GUI grocery list that allows the user to create delete save or edit a list
that tracks the items, quantity, and product type and displays a total cost for all the items
in the list. this program saves lists in to a json file to be loaded and used again in the future
or to be shared.
"""



import tkinter as tk
from tkinter import simpledialog
from tkinter import ttk
from tkinter import messagebox
import json
import os


class GroceryListApp:
    def __init__(self, master):
        self.master = master  # Main application window
        master.title("Smart Grocery List")

        # Initialize list data
        self.lists = {}  # Stores grocery lists as {list_name: [items]}
        self.current_list = None  # Holds the name of the currently selected list

        # Create frames for layout
        self.list_frame = tk.Frame(master)
        self.list_frame.pack(side=tk.LEFT, padx=10, pady=10)

        self.item_frame = tk.Frame(master)
        self.item_frame.pack(side=tk.LEFT, padx=10, pady=10)

        # Button to open the list manager
        self.open_list_manager_button = tk.Button(master, text="Manage Lists", command=self.open_list_manager)
        self.open_list_manager_button.pack()

        # Item management section
        self.item_label = tk.Label(self.item_frame, text="Items:")
        self.item_label.pack()

        self.item_listbox = tk.Listbox(self.item_frame, width=30, height=10)
        self.item_listbox.pack()

        self.add_item_button = tk.Button(self.item_frame, text="Add Item", command=self.add_item)
        self.add_item_button.pack()

        self.edit_item_button = tk.Button(self.item_frame, text="Edit Item", command=self.edit_item)
        self.edit_item_button.pack()

        self.remove_item_button = tk.Button(self.item_frame, text="Remove Item", command=self.remove_item)
        self.remove_item_button.pack()

        # Item details input section
        self.item_details_frame = tk.Frame(self.item_frame)
        self.item_details_frame.pack()

        self.product_label = tk.Label(self.item_details_frame, text="Product:")
        self.product_label.grid(row=0, column=0)

        self.product_entry = tk.Entry(self.item_details_frame)  # Entry for product name
        self.product_entry.grid(row=0, column=1)

        self.quantity_label = tk.Label(self.item_details_frame, text="Quantity:")
        self.quantity_label.grid(row=1, column=0)

        self.quantity_entry = tk.Entry(self.item_details_frame)  # Entry for product quantity
        self.quantity_entry.grid(row=1, column=1)

        self.price_label = tk.Label(self.item_details_frame, text="Price:")
        self.price_label.grid(row=2, column=0)

        self.price_entry = tk.Entry(self.item_details_frame)  # Entry for product price
        self.price_entry.grid(row=2, column=1)

        self.type_label = tk.Label(self.item_details_frame, text="Type:")
        self.type_label.grid(row=3, column=0)

        self.type_combobox = ttk.Combobox(self.item_details_frame, 
            values=["Fruit", "Vegetable", "Dairy", "Meat", "Bakery", "Other"])  # Dropdown for product type
        self.type_combobox.grid(row=3, column=1)

        # Total information section
        self.total_frame = tk.Frame(self.item_frame)
        self.total_frame.pack()

        self.total_items_label = tk.Label(self.total_frame, text="Total Items: 0")  # Displays total items
        self.total_items_label.pack(side=tk.LEFT)

        self.total_cost_label = tk.Label(self.total_frame, text="Total Cost: $0.00")  # Displays total cost
        self.total_cost_label.pack(side=tk.LEFT)

        # Event binding for selecting items
        self.item_listbox.bind("<<ListboxSelect>>", self.select_item)

    def open_list_manager(self):
        """Opens the List Manager window."""
        list_manager_window = tk.Toplevel(self.master)  # Creates a new top-level window
        ListManager(list_manager_window, self)  # Passes the new window and current app instance

    # Item management functions
    def add_item(self):
        """Adds an item to the current grocery list."""
        if self.current_list:
            product = self.product_entry.get()  # Gets product name from entry
            quantity = self.quantity_entry.get()  # Gets product quantity from entry
            price = self.price_entry.get()  # Gets product price from entry
            type_ = self.type_combobox.get()  # Gets product type from combobox

            if product and quantity and price:
                try:
                    quantity = int(quantity)  # Converts quantity to integer
                    price = float(price)  # Converts price to float
                    self.lists[self.current_list].append(
                        {"product": product, "quantity": quantity, "price": price, "type": type_}
                    )  # Adds item to the current list
                    self.update_item_listbox()  # Updates the item list display
                    self.clear_item_details()  # Clears input fields
                    self.update_total_info()  # Updates total items and cost
                except ValueError:
                    messagebox.showerror("Error", "Invalid quantity or price!")  # Error handling
            else:
                messagebox.showerror("Error", "Please fill in all item details!")  # Error handling
        else:
            messagebox.showerror("Error", "No list selected!")  # Error handling

    def edit_item(self):
        """Opens a dialog to edit the selected item."""
        selected_item_index = self.item_listbox.curselection()
        if selected_item_index:
            selected_item_index = selected_item_index[0]  # Gets the selected item index
            item = self.lists[self.current_list][selected_item_index]  # Gets the selected item

            # Opens a new window for editing
            edit_window = tk.Toplevel(self.master)
            edit_window.title("Edit Item")

            # Add labels and entries for editing item details
            product_label = tk.Label(edit_window, text="Product:")
            product_label.grid(row=0, column=0)
            product_entry = tk.Entry(edit_window)
            product_entry.insert(0, item["product"])
            product_entry.grid(row=0, column=1)

            quantity_label = tk.Label(edit_window, text="Quantity:")
            quantity_label.grid(row=1, column=0)
            quantity_entry = tk.Entry(edit_window)
            quantity_entry.insert(0, str(item["quantity"]))
            quantity_entry.grid(row=1, column=1)

            price_label = tk.Label(edit_window, text="Price:")
            price_label.grid(row=2, column=0)
            price_entry = tk.Entry(edit_window)
            price_entry.insert(0, str(item["price"]))
            price_entry.grid(row=2, column=1)

            type_label = tk.Label(edit_window, text="Type:")
            type_label.grid(row=3, column=0)
            type_combobox = ttk.Combobox(edit_window, values=["Fruit", "Vegetable", "Dairy", "Meat", "Bakery", "Other"])
            type_combobox.current(type_combobox['values'].index(item["type"]))
            type_combobox.grid(row=3, column=1)

            # Save button
            def save_changes():
                """Saves changes made to the item."""
                new_product = product_entry.get()
                new_quantity = quantity_entry.get()
                new_price = price_entry.get()
                new_type = type_combobox.get()

                if new_product and new_quantity and new_price:
                    try:
                        new_quantity = int(new_quantity)
                        new_price = float(new_price)
                        self.lists[self.current_list][selected_item_index] = {
                            "product": new_product,
                            "quantity": new_quantity,
                            "price": new_price,
                            "type": new_type
                        }  # Updates the item
                        self.update_item_listbox()  # Refreshes the item list display
                        self.clear_item_details()  # Clears input fields
                        self.update_total_info()  # Updates total items and cost
                        edit_window.destroy()  # Closes the edit window
                    except ValueError:
                        messagebox.showerror("Error", "Invalid quantity or price!")  # Error handling
                else:
                    messagebox.showerror("Error", "Please fill in all item details!")  # Error handling

            save_button = tk.Button(edit_window, text="Save Changes", command=save_changes)
            save_button.grid(row=4, column=0, columnspan=2)

    def remove_item(self):
        """Removes the selected item from the current grocery list."""
        selected_item_index = self.item_listbox.curselection()
        if selected_item_index:
            selected_item_index = selected_item_index[0]
            if messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this item?"):
                del self.lists[self.current_list][selected_item_index]  # Deletes the item
                self.update_item_listbox()  # Refreshes the item list display
                self.clear_item_details()  # Clears input fields
                self.update_total_info()  # Updates total items and cost

    def select_item(self, event):
        """Selects an item from the list and populates the input fields with its details."""
        selected_item_index = self.item_listbox.curselection()
        if selected_item_index:
            selected_item_index = selected_item_index[0]
            item = self.lists[self.current_list][selected_item_index]  # Gets the selected item
            # Populates input fields with item details
            self.product_entry.delete(0, tk.END)
            self.product_entry.insert(0, item["product"])
            self.quantity_entry.delete(0, tk.END)
            self.quantity_entry.insert(0, str(item["quantity"]))
            self.price_entry.delete(0, tk.END)
            self.price_entry.insert(0, str(item["price"]))
            self.type_combobox.current(self.type_combobox['values'].index(item["type"]))

    def update_item_listbox(self):
        """Updates the item list box to display current items."""
        self.item_listbox.delete(0, tk.END)  # Clears the list box
        if self.current_list:
            for item in self.lists[self.current_list]:
                # Displays each item with its product type
                self.item_listbox.insert(
                    tk.END, 
                    f"{item['product']} ({item['quantity']} x ${item['price']:.2f}, Type: {item['type']})"
                )

    def clear_item_details(self):
        """Clears all input fields for item details."""
        self.product_entry.delete(0, tk.END)
        self.quantity_entry.delete(0, tk.END)
        self.price_entry.delete(0, tk.END)
        self.type_combobox.current(0)  # Resets to the first option

    def update_total_info(self):
        """Calculates and updates total items and total cost for the current list."""
        if self.current_list:
            total_items = sum(item["quantity"] for item in self.lists[self.current_list])  # Total quantity
            total_cost = sum(item["quantity"] * item["price"] for item in self.lists[self.current_list])  # Total cost
            # Updates labels with the calculated totals
            self.total_items_label.config(text=f"Total Items: {total_items}")
            self.total_cost_label.config(text=f"Total Cost: ${total_cost:.2f}")
        else:
            self.total_items_label.config(text="Total Items: 0")  # Default if no list
            self.total_cost_label.config(text="Total Cost: $0.00")  # Default if no list


class ListManager:
    def __init__(self, master, app):
        self.master = master  # List Manager window
        self.master.title("Manage Grocery Lists")
        self.app = app  # Reference to the main app

        self.list_label = tk.Label(master, text="Grocery Lists:")
        self.list_label.pack()

        self.list_listbox = tk.Listbox(master, width=30, height=10)  # Displays available grocery lists
        self.list_listbox.pack()

        self.new_list_button = tk.Button(master, text="New List", command=self.new_list)
        self.new_list_button.pack()

        self.delete_list_button = tk.Button(master, text="Delete List", command=self.delete_list)
        self.delete_list_button.pack()

        self.save_list_button = tk.Button(master, text="Save List", command=self.save_list)
        self.save_list_button.pack()

        self.load_list_button = tk.Button(master, text="Load List", command=self.load_list)
        self.load_list_button.pack()

        self.exit_button = tk.Button(master, text="Exit", command=self.exit_application)
        self.exit_button.pack()

        self.update_listbox()  # Populate the list box with existing lists

    def new_list(self):
        """Creates a new grocery list."""
        new_list_name = simpledialog.askstring("New List", "Enter list name:")
        if new_list_name and new_list_name not in self.app.lists:
            self.app.lists[new_list_name] = []  # Initializes an empty list for the new grocery list
            self.update_listbox()  # Refreshes the display
        else:
            messagebox.showerror("Error", "List name already exists or is empty!")  # Error handling

    def delete_list(self):
        """Deletes the selected grocery list."""
        selected_list = self.list_listbox.get(tk.ANCHOR)  # Gets the selected list
        if selected_list and messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete list '{selected_list}'?"):
            del self.app.lists[selected_list]  # Deletes the list
            self.update_listbox()  # Refreshes the display

    def save_list(self):
        """Saves the selected grocery list to a JSON file."""
        selected_list = self.list_listbox.get(tk.ANCHOR)  # Gets the selected list
        if selected_list:
            file_name = simpledialog.askstring("Save List", "Enter file name (without extension):")
            if file_name:
                with open(f"{file_name}.json", "w") as f:
                    json.dump({selected_list: self.app.lists[selected_list]}, f)  # Saves the list to a JSON file
                messagebox.showinfo("Save List", f"List '{selected_list}' saved successfully!")  # Confirmation
        else:
            messagebox.showerror("Error", "No list selected!")  # Error handling

    def load_list(self):
        """Loads a grocery list from a JSON file."""
        file_name = simpledialog.askstring("Load List", "Enter file name (without extension):")
        if file_name and os.path.exists(f"{file_name}.json"):
            with open(f"{file_name}.json", "r") as f:
                loaded_lists = json.load(f)  # Loads the list from the JSON file
                self.app.lists.update(loaded_lists)  # Updates the app's lists with loaded data
                self.app.current_list = list(loaded_lists.keys())[0]  # Sets the loaded list as current
                self.app.update_item_listbox()  # Updates item display
                self.app.update_total_info()  # Updates totals
                self.update_listbox()  # Refreshes the display
                messagebox.showinfo("Load List", f"List '{self.app.current_list}' loaded successfully!")  # Confirmation
        else:
            messagebox.showerror("Error", "File does not exist or invalid name!")  # Error handling

    def update_listbox(self):
        """Updates the list box to show existing grocery lists."""
        self.list_listbox.delete(0, tk.END)  # Clears the list box
        for list_name in self.app.lists.keys():
            self.list_listbox.insert(tk.END, list_name)  # Inserts each list name into the list box


if __name__ == "__main__":
    root = tk.Tk()
    app = GroceryListApp(root)  # Initializes the main app
    root.mainloop()  # Starts the Tkinter event loop
