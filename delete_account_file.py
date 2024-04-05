import tkinter as tk
from tkinter import messagebox, ttk
import mysql.connector
from Validate import IsValid
from data_collect_v2 import Data

def save_input(accept_var, id_entry, table_entry):
    try:
        # Perform data insertion using userdata object
        accepted = accept_var.get()

        if accepted != "Accepted":
            messagebox.showwarning(title="Error", message="You have not accepted the terms")
            return

        id = id_entry.get()
        table = table_entry.get()
        userdata = Data()
        # Validation
        if not (id and table ):
            messagebox.showwarning(title="Error", message="All data is required.")
            return

        if table not in ("Users", "Tests"):
            messagebox.showwarning(title="Error", message="Invalid Table")
            return

        if userdata.checkUserIdExists(id) or userdata.checkTestExists(id):
            pass
        else:
            messagebox.showwarning(title="Error", message="Invalid ID")
            return
        # Inserting Data
        userdata.deleteRecord(id, table)
        messagebox.showinfo("Success", "Data has been successfully deleted.")
    except mysql.connector.Error as e:
        # Handle any MySQL connection errors
        messagebox.showerror("Database Error", f"An error occurred: {e}")


def delete_records(window):
    frame = tk.Frame(window)
    frame.pack()

    delete_frame = tk.LabelFrame(frame, text="Delete Account/Tests")
    delete_frame.grid(row=0, column=0, padx=10, pady=10)

    id_label = tk.Label(delete_frame, text="Id")
    id_label.grid(row=0, column=0)
    table_label = tk.Label(delete_frame, text="Table")
    table_label.grid(row=0, column=1)

    id_entry = tk.Spinbox(delete_frame, from_=0, to=1000000000, increment=1)
    id_entry.grid(row=1, column=0)
    varTable = tk.StringVar()
    table_entry = ttk.Combobox(delete_frame, textvariable=varTable)
    table_entry['values'] = ("Users", "Tests")
    table_entry.grid(row=1, column=1)

    # Define accept_var here
    accept_var = tk.StringVar(value="Not Accepted")

    for widget in delete_frame.winfo_children():
        widget.grid_configure(padx=5, pady=5)

    terms_frame = tk.LabelFrame(frame, text="All data has been inputted correctly")
    terms_frame.grid(row=1, column=0, sticky="news", padx=20, pady=10)

    terms_check = tk.Checkbutton(terms_frame, text="Agree to have data stored and used",
                                  variable=accept_var, onvalue="Accepted", offvalue="Not Accepted")
    terms_check.grid(row=0, column=0)

    # Button
    button = tk.Button(frame, text="Delete data", command=lambda: save_input(accept_var, id_entry, table_entry))
    button.grid(row=2, column=0, sticky="news", padx=20, pady=10)

if __name__ =="__main__":
    window = tk.Tk()
    window.title("Account Settings")
    delete_records(window)
    window.mainloop()
