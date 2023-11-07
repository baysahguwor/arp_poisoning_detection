import tkinter as tk
from tkinter import ttk
from datetime import datetime
import sqlite3
import pandas as pd
from logs import view_logs
from config import config_gui_set
import subprocess  
import platform 

DATABASE_NAME = 'arp_aware_db.sqlite'

# Function to run main.py in the background and hide the window
def run_main_py_background():
    if platform.system() == "Windows":
        startupinfo = subprocess.STARTUPINFO()
        startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
        subprocess.Popen(["python", "main.py"], startupinfo=startupinfo)
    else:
        # On non-Windows systems, you can try the following
        subprocess.Popen(["python", "main.py"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


def fetch_current_date_logs():
    today = datetime.now().strftime('%Y-%m-%d')

    # Connect to the database
    conn = sqlite3.connect(DATABASE_NAME)
    c = conn.cursor()

    # Fetch attack logs for the current date in descending order
    c.execute('SELECT * FROM attack_logs WHERE date = ? ORDER BY time DESC', (today,))
    logs = c.fetchall()

    # Create a formatted string to display the logs
    log_str = "Warning!!\t\tDate\t\tTime\t\tAttacker MAC\t\t\tRouter MAC\n"
    for log in logs:
        log_str += f"{'Under Attack !!' if log[1] else 'No'}\t\t{log[0]}\t\t{log[1]}\t\t{log[2]}\t\t\t{log[3]}\n"

    # Update the log display
    log_display.config(state=tk.NORMAL)
    log_display.delete('1.0', tk.END)
    log_display.insert(tk.END, log_str)
    log_display.config(state=tk.DISABLED)

    # Close the database connection
    conn.close()

    # Schedule the next fetch after 5000 milliseconds (5 seconds)
    root.after(5000, fetch_current_date_logs)


# Initialize the main application window
root = tk.Tk()
root.title('Live Monitoring')

# Set the window size (widthxheight)
root.geometry('1100x600')

# Create and place the widgets
title_label = ttk.Label(root, text='Live Monitoring', font=("Arial", 18))
title_label.grid(row=0, column=0, padx=10, pady=10, columnspan=4)

log_display = tk.Text(root, height=30, width=100, font=("Arial", 12), spacing3=20)
log_display.grid(row=1, column=0, padx=10, pady=5, columnspan=4)
log_display.config(state=tk.DISABLED)  # Set to read-only

# Function to handle "View Email Settings" button click
def view_email_settings():
    # Add the logic for handling the "View Email Settings" button click here
    pass

# Function to handle "Change Email Settings" button click
def change_email_settings():
    # Add the logic for handling the "Change Email Settings" button click here
    pass

# Create and place the buttons on the top right
view_button = tk.Button(root, text="Configurations", command=config_gui_set)
view_button.grid(row=1, column=5, padx=10, pady=60, sticky=tk.NE)

change_button = tk.Button(root, text="View Logs", command=view_logs)
change_button.grid(row=1, column=5, padx=10, pady=100, sticky=tk.NE)

# Start the initial fetch and schedule periodic updates
fetch_current_date_logs()

# Automatically start main.py when live_monitor.py is executed
run_main_py_background()



# Start the main event loop
root.mainloop()
