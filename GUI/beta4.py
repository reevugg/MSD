import tkinter as tk
from tkinter import ttk
import serial
import time

# Function to send numeric data to Arduino
def send_numeric_data(data):
    if data.isdigit():
        arduino.write(data.encode())
        current_data_label.config(text=f"Sends: {data}")

# Function to handle main button click and send data periodically
def button_click_handler(button_value):
    if not button_locked[button_value]:
        custom_value = custom_data.get(button_value, "")
        if custom_value:
            data_list = custom_value.split(',')
            for data in data_list:
                send_numeric_data(data)
                time.sleep(2)  # Pause for 2 seconds between data sends
        button_locked[button_value] = True

# Function to handle return button click and enable the main button
def return_button_click_handler(button_value):
    custom_return_value = custom_return_data.get(button_value, "")
    if custom_return_value:
        send_numeric_data(custom_return_value)
        button_locked[button_value] = False

# Function to update the data table
def update_data_table():
    for i in range(1, 6):
        custom_value = custom_data.get(i, "")
        custom_return_value = custom_return_data.get(i, "")

        data_table.item(f"item{i}_main", values=(f"Button {i}", custom_value))
        data_table.item(f"item{i}_return", values=(f"Return {i}", custom_return_value))

# Create a serial connection to the Arduino
try:
    arduino = serial.Serial('COM3', 9600)  # Change 'COM3' to your Arduino's serial port
except serial.SerialException as e:
    print(f"Error: {e}")
    arduino = None

# Create the GUI window
root = tk.Tk()
root.title("Arduino GUI")

# Dictionary to store custom data assignments for main buttons
custom_data = {}

# Dictionary to store custom data assignments for return buttons
custom_return_data = {}

# Create dictionaries to store button and return button widgets
button_states = {}
return_states = {}

# Create a dictionary to track button lock state for both main buttons and return buttons
button_locked = {i: False for i in range(1, 6)}

# Create main buttons and bind them to the click handlers
for i in range(1, 6):
    main_button = tk.Button(root, text=f"Button {i}", command=lambda i=i: button_click_handler(i))
    return_button = tk.Button(root, text=f"Return {i}", command=lambda i=i: return_button_click_handler(i), state=tk.DISABLED)

    main_button.pack()
    return_button.pack()

    button_states[i] = main_button
    return_states[i] = return_button

# Create a label for custom data assignment
custom_data_label = tk.Label(root, text="Custom Data Assignment:")
custom_data_label.pack()

# Entry widget for button selection
button_selector_label = tk.Label(root, text="Select Button:")
button_selector_label.pack()

button_selector = tk.Entry(root)
button_selector.pack()

# Entry widget for custom data entry
custom_data_entry_label = tk.Label(root, text="Enter Numeric Data (comma-separated):")
custom_data_entry_label.pack()

custom_data_entry = tk.Entry(root)
custom_data_entry.pack()

# Button to set custom data for main buttons
def set_custom_data():
    button_value = int(button_selector.get())
    custom_data_value = custom_data_entry.get()
    
    custom_data[button_value] = custom_data_value
    update_data_table()  # Update the data table after setting custom data

set_custom_data_button = tk.Button(root, text="Set Custom Data", command=set_custom_data)
set_custom_data_button.pack()

# Entry widget for custom data entry for return buttons
custom_return_data_entry_label = tk.Label(root, text="Enter Numeric Data (Return):")
custom_return_data_entry_label.pack()

custom_return_data_entry = tk.Entry(root)
custom_return_data_entry.pack()

# Button to set custom data for return buttons
def set_custom_return_data():
    button_value = int(button_selector.get())
    custom_return_data_value = custom_return_data_entry.get()
    
    custom_return_data[button_value] = custom_return_data_value
    return_states[button_value].config(state=tk.NORMAL)  # Enable the corresponding return button
    update_data_table()  # Update the data table after setting custom return data

set_custom_return_data_button = tk.Button(root, text="Set Custom Data (Return)", command=set_custom_return_data)
set_custom_return_data_button.pack()

# Label to display the currently sent data
current_data_label = tk.Label(root, text="")
current_data_label.pack()

# Create a data table
data_table = ttk.Treeview(root, columns=("Item", "Custom Data"), show="headings")
data_table.heading("Item", text="Item")
data_table.heading("Custom Data", text="Custom Data")
data_table.pack()

# Add data to the data table for main buttons and return buttons
for i in range(1, 6):
    custom_value = custom_data.get(i, "")
    custom_return_value = custom_return_data.get(i, "")

    data_table.insert("", "end", iid=f"item{i}_main", values=(f"Button {i}", custom_value))
    data_table.insert("", "end", iid=f"item{i}_return", values=(f"Return {i}", custom_return_value))

# Start the GUI main loop
root.mainloop()

# Close the serial connection when the GUI is closed
if arduino:
    arduino.close()
