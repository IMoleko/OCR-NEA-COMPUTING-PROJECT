from tkinter import *
from tkinter import ttk

#############################################################
# Name: Ivan Moleko
# Purpose: To make the login UI for the user
#############################################################

def teacher_Controls():  # admin menu screen
    win_admin = Tk()
    win_admin.title("Accounts")
    win_admin.geometry("262x210")
    win_admin.resizable(0,0)

    note_teach = ttk.Notebook(win_admin)
    note_teach.pack(expand=1, fill=BOTH)

    tab_new = Frame(note_teach)
    note_teach.add(tab_new, text="New Account")

    tab_reset = Frame(note_teach)
    note_teach.add(tab_reset, text="Reset Password")

    tab_delete = Frame(note_teach)
    note_teach.add(tab_delete, text="Delete Account")
    # --------------------------tab Create-------------------------------------#
    lbl_newuser = Label(tab_new, text="Enter New Username: ")
    lbl_newuser.pack() #grid(row=0, column=0, pady=10, padx=10)


    ent_newuser = Entry(tab_new)
    ent_newuser.pack() #grid(row=0, column=1, pady=10, padx=10)

    lbl_newpass = Label(tab_new, text="Enter New Password: ")
    lbl_newpass.pack() #(row=1, column=0, pady=10, padx=10)

    ent_newpass = Entry(tab_new)
    ent_newpass.pack() #(row=1, column=1, pady=10, padx=10)
    # ------------------------tab reset --------------------------------------#
    lbl_resetuser = Label(tab_reset, text="Enter Username: ")
    lbl_resetuser.pack() #(row=0, column=0, pady=10, padx=10)

    ent_resetuser = Entry(tab_reset)
    ent_resetuser.pack() #(row=0, column=1, pady=10, padx=10)

    lbl_newpass = Label(tab_reset, text="New Password: ")
    lbl_newpass.pack() #(row=1, column=0, pady=10, padx=10)

    txt_newpass = Entry(tab_reset)
    txt_newpass.pack() #(row=1, column=1, pady=10, padx=10)

    lbl_verifypass = Label(tab_reset, text="Verify Password: ")
    lbl_verifypass.pack() #(row=2, column=0, pady=10, padx=10)

    ent_verifypass =Entry(tab_reset)
    ent_verifypass.pack() #(row=2, column=1, pady=10, padx=10)
    # -------------------------tab delete -----------------------------------#
    lbl_usernew = Label(tab_delete, text="Enter Username: ")
    lbl_usernew.pack() #(row=0, column=0, pady=10, padx=10)

    txt_usernew = Entry(tab_delete)
    txt_usernew.pack() #(row=0, column=1, pady=10, padx=10)

    lbl_dateadded = Label(tab_delete, text="Enter Date Added: ")
    lbl_dateadded.pack()  # (row=0, column=0, pady=10, padx=10)

    txt_dateadded = Entry(tab_delete)
    txt_dateadded.pack()

    lbl_delete = Label(tab_delete, text="Reason For Deletion: ")
    lbl_delete.pack() #(row=1, column=0, pady=10, padx=10)

    ent_delete = Entry(tab_delete)
    ent_delete.pack() #(row=1, column=1, pady=10, padx=10)

    mainloop()

if __name__ == "__main__":
    teacher_Controls()
