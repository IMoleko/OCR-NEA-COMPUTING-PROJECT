import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector
from StudentTrackerGUI import *
from User_data_3 import *
from Test_data_v3 import *
from Student_score_data import *
from change_pass_file import *
from delete_account_file import *
from main_page import *
from data_collect_v2 import *

#############################################################
# Name: Ivan Moleko
# Purpose: To make the login UI for the user
#############################################################
def return_start(wx):
    wx.destroy()
    start_page()

def display_table_gui(cursor, parent_frame, table_name, column_widths=None):
    try:
        # Create a frame to hold the treeview widget
        table_frame = tk.Frame(parent_frame)
        table_frame.pack(pady=10, padx=10)

        # Execute a SQL query to select all data from the specified table
        cursor.execute(f"SELECT * FROM {table_name}")
        table_data = cursor.fetchall()

        # Create a treeview widget to display the data
        tree = ttk.Treeview(table_frame)
        tree["columns"] = [desc[0] for desc in cursor.description]

        # Define column headings
        for col in tree["columns"]:
            tree.heading(col, text=col)

        # Set column widths if provided
        if column_widths:
            for i, width in enumerate(column_widths):
                tree.column(tree["columns"][i], width=width)

        # Insert data into the treeview
        for i, row in enumerate(table_data, start=1):
            tree.insert("", "end", text=str(i), values=row)

        # Pack the treeview widget
        tree.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

    except mysql.connector.Error as err:
        print(f"Error: {err}")

def change_password_function():
    window = tk.Tk()
    window.title("Change Password")
    change_password(window)
    mainloop()

def delete_records_function():
    window = tk.Tk()
    window.title("Delete Records")
    delete_records(window)

    mainloop()

def update_frames(connection, user_id, title_frame, top_frame, bottom_frame):
    # Clear existing frames
    for widget in title_frame.winfo_children():
        widget.destroy()
    for widget in top_frame.winfo_children():
        widget.destroy()
    for widget in bottom_frame.winfo_children():
        widget.destroy()

    # Call the main_class function to update the frames with new data
    main_class(connection, user_id, title_frame, top_frame, bottom_frame)
def display_table_gui_func():
    window = tk.Tk()
    window.title("Data Tables")

    # Create an instance of the Data class
    table_data = Data()

    # Display the "Users" table
    table_data.display_table_gui(parent_frame=window, table_name="Users")

    # Display the "Tests" table
    table_data.display_table_gui(parent_frame=window, table_name="Tests")

    # Start the Tkinter event loop
    window.mainloop()

def main_class(connection, user_id, title_frame, top_frame, bottom_frame, window):
    # Create DataExtractor obj
    with DataExtractor(connection,user_id) as data_extractor:
        def show_button_pressed(show_entry):
            try:
                # Your database-related code here
                # Ensure the connection is established within this function
                db_connection = mysql.connector.connect(
                    user='thapelomoleko',
                    password='Thapeloivan2006*',
                    host='db4free.net',
                    database='tracker'
                )

                # Get the content of the entry widget
                user_id = show_entry.get()
                idcheck = Data()


                if idcheck.checkUserIdExists(user_id):
                    main_teach(window, user_id)
                else:
                    messagebox.showerror("Error", "Invalid User ID")

            except mysql.connector.Error as e:
                messagebox.showerror("Database Error", f"An error occurred: {e}")

            finally:
                # Close the connection to release resources
                if 'connection' in locals():
                    db_connection.close()

        # Table button

        table_btn = tk.Button(title_frame, text="Data Tables", command=lambda: display_table_gui_func())
        table_btn.grid(row=1, column=0, pady=5, padx=5)

        # Display student name
        user_name = data_extractor.get_user_name()
        title_label = tk.Label(title_frame, text=f"Student Name: {user_name}", font=("Helvetica", 16))
        title_label.grid(row=1, column=3, pady=5, padx=5)

        # Show id
        show_label = tk.Label(title_frame, text="Show ID", font=("Helvetica", 12))
        show_entry = tk.Entry(title_frame)
        show_btn = tk.Button(title_frame, text="Show", command=lambda: show_button_pressed(show_entry))
        show_label.grid(row=0, column=1, pady=5, padx=5)
        show_entry.grid(row=1, column=1, pady=5, padx=5)
        show_btn.grid(row=1, column=2, pady=5, padx=5)



        # Create a table for grade boundaries
        create_grade_boundaries_table(top_frame)

        # Fetch student scores
        create_student_table(top_frame, data_extractor)

        # Fetch test data
        test_ids = data_extractor.get_all_test_ids()

        if test_ids is not None:
            tests = []
            percentages_1 = []
            percentages_2 = []

            for test_id in test_ids:
                test_name = data_extractor.get_test_name(test_id)
                test_score = data_extractor.get_test_score(test_id)
                avg_score = data_extractor.calc_average_score_for_test(test_id)

                if None not in (test_name, test_score, avg_score):
                    tests.append(test_name)
                    percentages_1.append(data_extractor.calc_percentage(test_id, test_score))
                    percentages_2.append(avg_score)

            # Plot line graph
            graph_frame = tk.Frame(bottom_frame)
            graph_frame.pack(side=tk.RIGHT)
            plot_three_line_graphs(tests, percentages_1, percentages_2, graph_frame)

            # Display score comparison
            current_scores = []
            target_scores = []
            for test_id in test_ids:
                test_score = data_extractor.get_test_score(test_id)
                avg_score = data_extractor.calc_average_score_for_test(test_id)
                if None not in (test_score, avg_score):
                    current_scores.append(test_score)
                    target_scores.append(avg_score)

            comparison_frame = tk.Frame(bottom_frame)
            comparison_frame.pack(side=tk.RIGHT)
            display_score_comparison(tests, current_scores, target_scores, comparison_frame)

            # Plot clustered column chart
            plot_frame = tk.Frame(bottom_frame)
            plot_frame.pack(side=tk.RIGHT)
            plot_minmax_scores(tests, current_scores, target_scores, test_ids, plot_frame)

        else:
            print("Error: Unable to fetch test IDs.")

        # Close the database connection
        connection.close()

def main_teach(x,user_id):
    db_connection = mysql.connector.connect(
        user='thapelomoleko',
        password='Thapeloivan2006*',
        host='db4free.net',
        database='tracker'
    )

    x.destroy()  # destroys any window passed into this function

    given_user_id = user_id # Replace with the actual user_id

    win_tmain = tk.Tk()
    win_tmain.title("StudentTracker")
    win_tmain.geometry("1800x950")
    win_tmain.resizable(10, 10)

    # create a menubar
    menubar = tk.Menu(win_tmain)
    win_tmain.config(menu=menubar)

    # create a menu
    teach_menu = tk.Menu(menubar)

    # add a menu item to the menu
    teach_menu.add_command(label="Account Settings",command=lambda: change_password_function()) # change pass
    teach_menu.add_command(label="Delete Records", command=lambda: delete_records_function()) # delete records
    teach_menu.add_command(label='Log Out', command=lambda: return_start(win_tmain))  # Sign out to main

    # add the File menu to the menubar
    menubar.add_cascade(label="Settings", menu=teach_menu)

    # -----------------------------------------------------------------------------------------------------#
    note_tmain = ttk.Notebook(win_tmain)
    note_tmain.pack(expand=1, fill=tk.BOTH)

    tab_main = tk.Frame()
    note_tmain.add(tab_main, text="Class Data")

    tab_input_data = tk.Frame()
    note_tmain.add(tab_input_data, text="Input Data")

    # tab_show_data = tk.Frame()
    # note_tmain.add(tab_show_data, text="Show Data")
    # #
    # tab_accounts = tk.Frame()
    # note_tmain.add(tab_accounts, text="Account settings")
    # -------------------------------------Tab1-------------------------------------------#
    # Create frames for tab1
    title_frame_1 = tk.Frame(tab_main)
    top_frame_1 = tk.Frame(tab_main)
    bottom_frame_1 = tk.Frame(tab_main)
    title_frame_1.pack(side=tk.TOP)
    top_frame_1.pack(side=tk.TOP)
    bottom_frame_1.pack(side=tk.BOTTOM)

    main_class(db_connection, given_user_id, title_frame_1, top_frame_1, bottom_frame_1, win_tmain)

    # -------------------------------------Tab2-------------------------------------------#
    # Create frames for tab2
    main_frame_2_top = tk.Frame(tab_input_data)
    main_frame_2_top.pack()

    # main_frame_2_bot = tk.Frame(tab_input_data)
    # main_frame_2_bot.pack(side=tk.BOTTOM)

    main_user_data(main_frame_2_top)
    main_student_data(main_frame_2_top)
    main_test_data(main_frame_2_top)

    # display_table_gui(db_connection.cursor(),main_frame_2_bot,"Users")
    # display_table_gui(db_connection.cursor(), main_frame_2_bot, "Users")

    # -----------------------------------Tab3---------------------------------#
    # tabe
    # tables = Data()
    # tables.display_table_gui(parent_frame=tab_show_data, table_name="Users")
    # print("table function success")
    # tables.display_table_gui(parent_frame=tab_show_data, table_name="Tests")
    # win_tmain.update()
    #
    # #
    # # --------------------------------Tab4----------------------------#
    # # Create frames for tab4
    # main_frame_4 = tk.Frame(tab_accounts)
    # main_frame_4.pack()
    #
    # change_password(main_frame_4)
    # delete_records(main_frame_4)

    # Close the database connection
    db_connection.close()
    win_tmain.mainloop()


if __name__ == "__main__":
    window = tk.Tk()
    main_teach(window,1)

