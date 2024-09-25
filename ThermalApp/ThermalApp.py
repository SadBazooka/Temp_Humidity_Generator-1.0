import customtkinter as ctk
from tkinter import filedialog, messagebox
from tkcalendar import DateEntry  # Import tkcalendar for date picker
import pandas as pd
import numpy as np
from datetime import datetime

# Function to generate random data based on user input
def generate_data(start_date, end_date, temp_range, hum_range):
    date_range = pd.date_range(start=start_date, end=end_date, freq='D').to_pydatetime()[::-1]
    
    timestamps = []
    for date in date_range:
        timestamps.append(datetime(date.year, date.month, date.day, 21, 0))  # 9:00 PM
        timestamps.append(datetime(date.year, date.month, date.day, 7, 0))   # 7:00 AM
    
    temperatures = np.round(np.random.uniform(temp_range[0], temp_range[1], len(timestamps)), 1)
    humidities = np.round(np.random.uniform(hum_range[0], hum_range[1], len(timestamps)), 1)
    
    data = {
        "Time": [dt.strftime('%m/%d/%Y %H:%M') for dt in timestamps],
        "Temperature_Fahrenheit": temperatures,
        "Relative_Humidity_Percent": humidities
    }
    
    df = pd.DataFrame(data)
    return df

# Function to create the correct filename format
def generate_file_name(file_type, start_date, end_date):
    start_str = start_date.strftime('%Y%m%d') + "0700"  # Start date + 0700
    end_str = end_date.strftime('%Y%m%d') + "2100"      # End date + 2100
    file_name = f"Chemist Shop {file_type} Thermo-hygrometer_Export Data_{start_str}_{end_str}.csv"
    return file_name

# Function to save the CSV file
def save_file(dataframe, file_type, start_date, end_date):
    file_name = generate_file_name(file_type, start_date, end_date)
    
    file_path = filedialog.asksaveasfilename(defaultextension=".csv", initialfile=file_name, filetypes=[("CSV Files", "*.csv")])
    if file_path:
        dataframe.to_csv(file_path, index=False)
        messagebox.showinfo("Success", f"File saved as {file_path}")

# Function to autofill temperature and humidity values based on fridge/freezer preset
def apply_preset():
    if file_type_var.get() == "Fridge":
        temp_min_entry.delete(0, ctk.END)
        temp_min_entry.insert(0, "37")
        temp_max_entry.delete(0, ctk.END)
        temp_max_entry.insert(0, "45")
        hum_min_entry.delete(0, ctk.END)
        hum_min_entry.insert(0, "80")
        hum_max_entry.delete(0, ctk.END)
        hum_max_entry.insert(0, "95")
    elif file_type_var.get() == "Freezer":
        temp_min_entry.delete(0, ctk.END)
        temp_min_entry.insert(0, "-12")
        temp_max_entry.delete(0, ctk.END)
        temp_max_entry.insert(0, "13")
        hum_min_entry.delete(0, ctk.END)
        hum_min_entry.insert(0, "85")
        hum_max_entry.delete(0, ctk.END)
        hum_max_entry.insert(0, "95")

def generate_csv():
    try:
        temp_min = float(temp_min_entry.get())
        temp_max = float(temp_max_entry.get())
        hum_min = float(hum_min_entry.get())
        hum_max = float(hum_max_entry.get())
        start_date = start_date_entry.get_date()  # Get date from DateEntry
        end_date = end_date_entry.get_date()  # Get date from DateEntry
        file_type = file_type_var.get()

        data = generate_data(start_date, end_date, (temp_min, temp_max), (hum_min, hum_max))
        save_file(data, file_type, start_date, end_date)
    except Exception as e:
        messagebox.showerror("Error", str(e))

# Setup the CustomTkinter window
ctk.set_appearance_mode("dark")  # Use dark mode for a modern look
ctk.set_default_color_theme("blue")  # Set the color theme (you can choose others too)

root = ctk.CTk()  # Create a CustomTkinter window
root.title("Modern Thermo-Hygrometer Data Generator")
root.geometry("400x600")  # Set a larger window size to fit all elements

# Disable maximize button
root.resizable(False, False)  # Disable window resizing and maximizing, only allow minimizing and closing

# Create modern-styled widgets
ctk.CTkLabel(root, text="Temperature Range (Fahrenheit)", font=("Arial", 16)).pack(pady=10)
temp_min_entry = ctk.CTkEntry(root, placeholder_text="Min Temp")
temp_min_entry.pack(pady=5)
temp_max_entry = ctk.CTkEntry(root, placeholder_text="Max Temp")
temp_max_entry.pack(pady=5)

ctk.CTkLabel(root, text="Humidity Range (%)", font=("Arial", 16)).pack(pady=10)
hum_min_entry = ctk.CTkEntry(root, placeholder_text="Min Humidity")
hum_min_entry.pack(pady=5)
hum_max_entry = ctk.CTkEntry(root, placeholder_text="Max Humidity")
hum_max_entry.pack(pady=5)

# Add Preset Button for Fridge/Freezer settings
preset_button = ctk.CTkButton(root, text="Apply Preset", command=apply_preset)
preset_button.pack(pady=10)

ctk.CTkLabel(root, text="Start Date (MM/DD/YYYY)", font=("Arial", 16)).pack(pady=10)
start_date_entry = DateEntry(root, date_pattern="mm/dd/yyyy")  # Add calendar date picker
start_date_entry.pack(pady=5)

ctk.CTkLabel(root, text="End Date (MM/DD/YYYY)", font=("Arial", 16)).pack(pady=10)
end_date_entry = DateEntry(root, date_pattern="mm/dd/yyyy")  # Add calendar date picker
end_date_entry.pack(pady=5)

# Radio buttons for file type (Fridge/Freezer)
file_type_var = ctk.StringVar(value="Fridge")
ctk.CTkRadioButton(root, text="Fridge", variable=file_type_var, value="Fridge").pack(pady=5)
ctk.CTkRadioButton(root, text="Freezer", variable=file_type_var, value="Freezer").pack(pady=5)

# Generate button with custom styling
generate_button = ctk.CTkButton(root, text="Generate CSV", command=generate_csv)
generate_button.pack(pady=20)

root.mainloop()
