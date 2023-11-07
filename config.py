import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from database import get_email_settings, save_email_settings, initialize_database

def config_gui_set():

    # Initialize the database and create tables
    initialize_database()

    def view_email_settings():
        smtp_server, smtp_port, smtp_username, smtp_password = get_email_settings()
        message = f"SMTP Server: {smtp_server}\nSMTP Port: {smtp_port}\nSMTP Username: {smtp_username}\nSMTP Password: ********"
        email_settings_text.config(state="normal")
        email_settings_text.delete("1.0", tk.END)
        email_settings_text.insert("1.0", message)
        email_settings_text.config(state="disabled")

    def save_email_settings_gui():
        smtp_server = smtp_server_entry.get()
        smtp_port = smtp_port_entry.get()
        smtp_username = smtp_username_entry.get()
        smtp_password = smtp_password_entry.get()

        save_email_settings(smtp_server, smtp_port, smtp_username, smtp_password)
        messagebox.showinfo("Email Settings", "Email settings updated successfully.")

    # Initialize the main application window
    root = tk.Tk()
    root.title("Email Settings Menu")
    root.geometry("600x400")  # Set the window size here

    # Increase font size for all text
    style = ttk.Style()
    style.configure('.', font=('Arial', 18))

    # Create a Notebook (tabbed interface)
    notebook = ttk.Notebook(root)

    # Tab 1: View Email Settings
    tab1 = ttk.Frame(notebook)
    notebook.add(tab1, text='View Email Settings')

    email_settings_text = tk.Text(tab1, width=50, height=10, font=('Arial', 18), state="disabled")
    email_settings_text.pack(padx=20, pady=20)

    view_button = tk.Button(tab1, text="View Email Settings", command=view_email_settings, font=('Arial', 18))
    view_button.pack(pady=10)

    # Tab 2: Change Email Settings
    tab2 = ttk.Frame(notebook)
    notebook.add(tab2, text='Change Email Settings')

    smtp_server_label = tk.Label(tab2, text="SMTP Server:", font=('Arial', 18))
    smtp_server_label.grid(row=0, column=0)
    smtp_server_entry = tk.Entry(tab2, font=('Arial', 18))
    smtp_server_entry.grid(row=0, column=1)

    smtp_port_label = tk.Label(tab2, text="SMTP Port:", font=('Arial', 18))
    smtp_port_label.grid(row=1, column=0)
    smtp_port_entry = tk.Entry(tab2, font=('Arial', 18))
    smtp_port_entry.grid(row=1, column=1)

    smtp_username_label = tk.Label(tab2, text="SMTP Username:", font=('Arial', 18))
    smtp_username_label.grid(row=2, column=0)
    smtp_username_entry = tk.Entry(tab2, font=('Arial', 18))
    smtp_username_entry.grid(row=2, column=1)

    smtp_password_label = tk.Label(tab2, text="SMTP Password:", font=('Arial', 18))
    smtp_password_label.grid(row=3, column=0)
    smtp_password_entry = tk.Entry(tab2, show="*", font=('Arial', 18))
    smtp_password_entry.grid(row=3, column=1)

    save_button = tk.Button(tab2, text="Save", command=save_email_settings_gui, font=('Arial', 18))
    save_button.grid(row=4, column=0, columnspan=2, pady=10)

    notebook.pack(expand=True, fill='both')

    # Start the main event loop
    root.mainloop()
