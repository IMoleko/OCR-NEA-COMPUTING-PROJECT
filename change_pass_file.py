import tkinter as tk
from tkinter import messagebox
import mysql.connector
from Validate import IsValid
from data_collect_v2 import Data

def save_input(accept_var, student_id_entry, new_pass_entry, check_pass_entry):
    try:
        # Perform data insertion using userdata object
        accepted = accept_var.get()

        if accepted != "Accepted":
            messagebox.showwarning(title="Error", message="You have not accepted the terms")
            return

        userdata = Data()
        id = student_id_entry.get()
        new_pass = new_pass_entry.get()
        check_pass = check_pass_entry.get()

        # Validation
        if not (id and new_pass and check_pass):
            messagebox.showwarning(title="Error", message="All data is required.")
            return

        if userdata.checkUserIdExists(id):
            pass
        else:
            messagebox.showwarning(title="Error", message="Invalid ID")
            return

        validate = IsValid()

        if not validate.Length(id, 10, 4):
            messagebox.showwarning(title="Error", message="Invalid Last Name length")
            return

        if new_pass != check_pass:
            messagebox.showwarning(title="Error", message="Passwords do not match")
            return

        if not validate.Length(new_pass, 35, 4):
            messagebox.showwarning(title="Error", message="Invalid Password length")
            return
        # Inserting Data
        userdata.changePassword(id, new_pass)
        messagebox.showinfo("Success", "Data has been successfully entered into the database.")

    except mysql.connector.Error as e:
        # Handle any MySQL connection errors
        messagebox.showerror("Database Error", f"An error occurred: {e}")

def change_password(window):
    frame = tk.Frame(window)
    frame.pack()

    change_pass_frame = tk.LabelFrame(frame, text="Change Password")
    change_pass_frame.grid(row=0, column=0, padx=10, pady=10)

    student_id_label = tk.Label(change_pass_frame, text="Student Id")
    student_id_label.grid(row=0, column=0)
    new_pass_label = tk.Label(change_pass_frame, text="New password")
    new_pass_label.grid(row=0, column=1)

    student_id_entry = tk.Spinbox(change_pass_frame, from_=0, to="infinity")
    student_id_entry.grid(row=1, column=0)
    new_pass_entry = tk.Entry(change_pass_frame, show="*")
    new_pass_entry.grid(row=1, column=1)

    check_pass_label = tk.Label(change_pass_frame, text="Re-enter password")
    check_pass_entry = tk.Entry(change_pass_frame, show="*")
    check_pass_label.grid(row=0, column=2)
    check_pass_entry.grid(row=1, column=2)

    # Define accept_var here
    accept_var = tk.StringVar(value="Not Accepted")

    for widget in change_pass_frame.winfo_children():
        widget.grid_configure(padx=5, pady=5)

    terms_frame = tk.LabelFrame(frame, text="All data has been inputted correctly")
    terms_frame.grid(row=1, column=0, sticky="news", padx=20, pady=10)

    terms_check = tk.Checkbutton(terms_frame, text="Agree to have data stored and used",
                                  variable=accept_var, onvalue="Accepted", offvalue="Not Accepted")
    terms_check.grid(row=0, column=0)

    # Button
    button = tk.Button(frame, text="Enter data", command=lambda: save_input(accept_var, student_id_entry,
                                                                            new_pass_entry,check_pass_entry))
    button.grid(row=2, column=0, sticky="news", padx=20, pady=10)



if __name__ == "__main__":
    window = tk.Tk()
    window.title("Change Password")
    change_password(window)
    window.mainloop()
