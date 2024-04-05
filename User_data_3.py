import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
import mysql.connector
from Validate import IsValid
from data_collect_v2 import Data

def save_input(accept_var, name_entry, titles, dob_entry, email_entry, phone_entry, choose_status):
    try:
        # Perform data insertion using userdata object
        accepted = accept_var.get()

        if accepted != "Accepted":
            messagebox.showwarning(title="Error", message="You have not accepted the terms")
            return

        name = name_entry.get()
        title = titles.get()
        email = email_entry.get()
        dob = dob_entry.get()
        phone_no = phone_entry.get()
        status = choose_status.get()

        # Validation
        if not (name and title and email and dob and phone_no and status):
            messagebox.showwarning(title="Error", message="All data is required.")
            return

        validate = IsValid()

        if not validate.Length(name, 35, 4):
            messagebox.showwarning(title="Error", message="Invalid Name length")
            return

        if not validate.name_check(name,None):
            messagebox.showwarning(title="Error", message="Invalid Name")
            return

        if not validate.Number(phone_no):
            messagebox.showwarning(title="Error", message="Invalid Phone Number")
            return

        if not validate.Email(email):
            messagebox.showwarning(title="Error", message="Invalid Email")
            return

        if status not in ("Student", "Teacher"):
            messagebox.showwarning(title="Error", message="Invalid Status")
            return

        if titles.get() not in ("Mr", "Mrs", "Sir", "Dr", "Ms", "Miss"):
            messagebox.showwarning(title="Error", message="Invalid Title")
            return

        # if validate.name_check(name):
        #     messagebox.showwarning(title="Error", message="Invalid Name")
        #     return

        # Verifying at least a 10 years difference
        if not validate.validate_date_of_birth(dob, min_age_days=3650):
            messagebox.showwarning(title="Error", message="Invalid date of birth. Age must be at least 10 years ")
            return

        # Inserting Data
        userdata = Data()
        userdata.insertUserData(
            givenName=name, givenTitle=title, givenEmail=email, givenDob=dob,
            givenStatus=status, givenNum=phone_no
        )

        messagebox.showinfo("Success", "Data has been successfully entered into the database.")

    except mysql.connector.Error as e:
        # Handle any MySQL connection errors
        messagebox.showerror("Database Error", f"An error occurred: {e}")


def main_user_data(window):
    frame = tk.Frame(window)
    frame.pack(side=tk.TOP)

    user_info_frame = tk.LabelFrame(frame, text="User Information")
    user_info_frame.grid(row=0, column=0, padx=10, pady=10)
    name_label = tk.Label(user_info_frame, text="Name")
    name_label.grid(row=0, column=0, pady=5, padx=5)
    title_label = tk.Label(user_info_frame, text="Title")
    title_label.grid(row=0, column=1, pady=5, padx=5)

    name_entry = tk.Entry(user_info_frame, width=20)
    name_entry.grid(row=1, column=0, pady=5, padx=5)

    var1 = tk.StringVar()
    titles = ttk.Combobox(user_info_frame, textvariable=var1, width=15)
    titles['values'] = ("Mr", "Mrs", "Sir", "Dr", "Ms", "Miss")
    titles.grid(row=1, column=1, pady=5, padx=5 )
    titles.current(0)

    dob_label = tk.Label(user_info_frame, text="Date of Birth")
    dob_entry = DateEntry(user_info_frame, background='darkblue', foreground='white', borderwidth=2, width=12, date_pattern='yyyy/mm/dd')
    dob_label.grid(row=0, column=2, pady=5, padx=5)
    dob_entry.grid(row=1, column=2, pady=5, padx=5)

    email_label = tk.Label(user_info_frame, text="Email")
    email_entry = tk.Entry(user_info_frame, width=20)
    email_label.grid(row=2, column=0, pady=5, padx=5)
    email_entry.grid(row=3, column=0, pady=5, padx=5)

    phone_label = tk.Label(user_info_frame, text="Phone No")
    phone_entry = tk.Entry(user_info_frame, width=20)
    phone_label.grid(row=2, column=1, pady=5, padx=5)
    phone_entry.grid(row=3, column=1, pady=5, padx=5)

    status_label = tk.Label(user_info_frame, text="Teacher/Student")
    var2 = tk.StringVar()
    choose_status = ttk.Combobox(user_info_frame, textvariable=var2, width=15)
    choose_status['values'] = ("Student", "Teacher")
    status_label.grid(row=2, column=2, pady=5, padx=5)
    choose_status.grid(row=3, column=2, pady=5, padx=5)
    choose_status.current(0)

    # Define accept_var here
    accept_var = tk.StringVar(value="Not Accepted")

    for widget in user_info_frame.winfo_children():
        widget.grid_configure(padx=5, pady=5)

    terms_frame = tk.LabelFrame(frame, text="Terms&Conditions")
    terms_frame.grid(row=1, column=0, sticky="news", padx=20, pady=10)

    terms_check = tk.Checkbutton(terms_frame, text="Agree to have data stored and used",
                                  variable=accept_var, onvalue="Accepted", offvalue="Not Accepted")
    terms_check.grid(row=0, column=0, pady=5, padx=5)

    # Button
    button = tk.Button(frame, text="Enter data", command=lambda: save_input(accept_var, name_entry, titles, dob_entry, email_entry, phone_entry, choose_status))
    button.grid(row=2, column=0, sticky="news", padx=20, pady=10)

if __name__ == "__main__":
    window = tk.Tk()
    window.title("Student Entry Form")  # Set window size to 22cm x 37cm
    main_user_data(window)
    window.mainloop()


























