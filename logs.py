import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from tkcalendar import DateEntry
from datetime import datetime
import sqlite3
import pandas as pd

DATABASE_NAME = 'arp_aware_db.sqlite'

def view_logs():
    def display_logs():
        start_date = start_date_entry.get_date().strftime('%Y-%m-%d')
        end_date = end_date_entry.get_date().strftime('%Y-%m-%d')

        # Connect to the database
        conn = sqlite3.connect(DATABASE_NAME)
        c = conn.cursor()

        # Fetch attack logs within the specified date range
        c.execute('SELECT * FROM attack_logs WHERE date BETWEEN ? AND ?', (start_date, end_date))
        logs = c.fetchall()

        # Display the logs
        log_display.delete('1.0', tk.END)
        for log in logs:
            log_display.insert(tk.END, f"Date: {log[0]}, Time: {log[1]}, Attacker MAC: {log[2]}, Router MAC: {log[3]}\n")

        # Close the database connection
        conn.close()

    def delete_logs():
        start_date = start_date_entry.get_date().strftime('%Y-%m-%d')
        end_date = end_date_entry.get_date().strftime('%Y-%m-%d')

        # Connect to the database
        conn = sqlite3.connect(DATABASE_NAME)
        c = conn.cursor()

        # Delete attack logs within the specified date range
        c.execute('DELETE FROM attack_logs WHERE date BETWEEN ? AND ?', (start_date, end_date))
        conn.commit()

        # Close the database connection
        conn.close()

        messagebox.showinfo("Deletion Successful", "Logs deleted successfully.")

    def export_to_excel():
        logs_text = log_display.get('1.0', tk.END)
        logs_list = logs_text.strip().split('\n')
        data = [log.split(', ') for log in logs_list]

        # Create a DataFrame from the data
        df = pd.DataFrame(data, columns=['Date', 'Time', 'Attacker MAC', 'Router MAC'])

        # Export to Excel
        file_path = filedialog.asksaveasfilename(defaultextension=".xlsx",
                                                filetypes=[("Excel files", "*.xlsx")])
        if file_path:
            df.to_excel(file_path, index=False)
            messagebox.showinfo("Export Successful", "Logs exported to Excel successfully.")

    # Initialize the main application window
    root = tk.Tk()
    root.title('Attack Log Viewer')

    # Set the window size (widthxheight)
    root.geometry('900x600')

    # Create and place the widgets
    ttk.Label(root, text='Start Date:').grid(row=0, column=0, padx=10, pady=5)
    start_date_entry = DateEntry(root, width=12, background='darkblue', foreground='white', date_pattern='yyyy-mm-dd')
    start_date_entry.grid(row=0, column=1, padx=10, pady=5)

    ttk.Label(root, text='End Date:').grid(row=1, column=0, padx=10, pady=5)
    end_date_entry = DateEntry(root, width=12, background='darkblue', foreground='white', date_pattern='yyyy-mm-dd')
    end_date_entry.grid(row=1, column=1, padx=10, pady=5)

    view_button = ttk.Button(root, text='View Logs', command=display_logs)
    view_button.grid(row=2, column=0, padx=10, pady=10)

    delete_button = ttk.Button(root, text='Delete Logs', command=delete_logs)
    delete_button.grid(row=2, column=1, padx=10, pady=10)

    export_button = ttk.Button(root, text='Export to Excel', command=export_to_excel)
    export_button.grid(row=2, column=2, padx=10, pady=10)

    log_display = tk.Text(root, height=40, width=100)
    log_display.grid(row=3, column=0, columnspan=3, padx=10, pady=5)

    # Start the main event loop
    root.mainloop()