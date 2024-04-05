import tkinter as tk
from tkinter import messagebox
from Validate import IsValid
from tkcalendar import DateEntry
from data_collect_v2 import Data
from tkinter import scrolledtext


def enter_data(accept_var, test_name_entry, test_description_entry, test_date_entry, test_time_entry,
               test_score_spinbox):
    accepted = accept_var.get()
    if accepted == "Accepted":
        # Test info
        name = test_name_entry.get()
        description = test_description_entry.get("1.0", "end-1c")
        date = test_date_entry.get()
        time = int(test_time_entry.get()) # Convert to integer
        score = int(test_score_spinbox.get())
        if name and description and date and time and score:
            validate = IsValid()  # Instantiate the IsValid class

            if validate.Length(name, 35, 4):  # Call the Length method on the instance
                pass
            else:
                tk.messagebox.showwarning(title="Error", message="Test Name invalid Length")

            if validate.Length(description, 100, 4):  # Call the Length method on the instance
                pass
            else:
                tk.messagebox.showwarning(title="Error", message="Test Description invalid Length")

            if validate.Length(str(time), 5, 4):  # Call the Length method on the instance
                pass
            else:
                tk.messagebox.showwarning(title="Error", message="Time invalid Length")

            if validate.name_check(name, pattern=r'^[a-zA-Z0-9]+$'):  # Call the name_check method on the instance
                pass
            else:
                tk.messagebox.showwarning(title="Error", message="Name invalid")

            if time > 0:
                pass
            else:
                tk.messagebox.showwarning(title="Error", message="Time invalid ")

            if score > 0:
                pass
            else:
                tk.messagebox.showwarning(title="Error", message="Score invalid ")

            if validate.validate_date_of_birth(date, 2):  # Call the validate_date_of_birth method on the instance
                pass
            else:
                tk.messagebox.showwarning(title="Error", message="Date invalid ")

            testdata = Data()
            testdata.insertTestData(
                givenName=name, givenDesc=description, givenDate=date, givenScore=score, givenTime=time
            )
            tk.messagebox.showinfo("Success", "Data has been successfully inserted.")
        else:
            tk.messagebox.showwarning(title="Error", message="All data is required")
    else:
        tk.messagebox.showwarning(title="Error", message="You have not accepted the terms")


def main_test_data(window):
    frame = tk.Frame(window)
    frame.pack(side=tk.BOTTOM)

    # Saving Test Info
    test_frame = tk.LabelFrame(frame, text="Test Details")
    test_frame.grid(row=0, column=0, padx=20, pady=10)

    test_name_label = tk.Label(test_frame, text="Test Name")
    test_name_label.grid(row=0, column=0, pady=5, padx=5)
    test_description_label = tk.Label(test_frame, text="Test Description")
    test_description_label.grid(row=0, column=1, pady=5, padx=5)

    test_name_entry = tk.Entry(test_frame, width=20)
    test_description_entry = scrolledtext.ScrolledText(test_frame, wrap=tk.WORD, width=20, height=3,
                                                       font=("Calibri", 10))
    test_name_entry.grid(row=1, column=0, pady=5, padx=5)
    test_description_entry.grid(row=1, column=1)

    test_date_label = tk.Label(test_frame, text="Test Date")
    test_date_entry = DateEntry(test_frame, width=12, background='darkblue', foreground='white', borderwidth=2,
                                date_pattern='yyyy/mm/dd')
    test_date_label.grid(row=0, column=2, pady=5, padx=5)
    test_date_entry.grid(row=1, column=2, pady=5, padx=5)

    test_time_label = tk.Label(test_frame, text="Allotted Time (min)")
    test_time_entry = tk.Entry(test_frame, width=20)
    test_time_label.grid(row=2, column=0, pady=5, padx=5)  # Corrected column index
    test_time_entry.grid(row=3, column=0, pady=5, padx=5)  # Corrected column index

    test_mscore_label = tk.Label(test_frame, text="Max Score")
    test_mscore_spinbox = tk.Spinbox(test_frame, from_=0, to="infinity", width=15)
    test_mscore_label.grid(row=2, column=2, pady=5, padx=5)  # Corrected column index
    test_mscore_spinbox.grid(row=3, column=2, pady=5, padx=5)  # Corrected column index

    for widget in test_frame.winfo_children():
        widget.grid_configure(padx=10, pady=5)

    # Accept terms
    terms_frame = tk.LabelFrame(frame, text="Verification")
    terms_frame.grid(row=2, column=0, sticky="news", padx=20, pady=10)

    accept_var = tk.StringVar(value="Not Accepted")
    terms_check = tk.Checkbutton(terms_frame, text="All data has been inputted corrected ",
                                 variable=accept_var, onvalue="Accepted", offvalue="Not Accepted")
    terms_check.grid(row=0, column=0, pady=5, padx=5)

    # Button
    button = tk.Button(frame, text="Enter data", command=lambda: enter_data(accept_var, test_name_entry,
                                                                            test_description_entry, test_date_entry,
                                                                            test_time_entry, test_mscore_spinbox))
    button.grid(row=3, column=0, sticky="news", padx=20, pady=10)

    window.mainloop()


if __name__ == "__main__":
    window = tk.Tk()
    window.title("Test Data Form")
    main_test_data(window)
