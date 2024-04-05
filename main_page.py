import tkinter as tk
from tkinter import Menu, ttk
from tkinter import messagebox
import mysql.connector
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from StudentTrackerGUI import *
from Data_Extration import DataExtractor

def plot_minmax_scores(tests, lowest_scores, highest_scores, average_scores, frame):
    """
    Plot a clustered column chart with lowest, highest, and average scores for each test.

    Parameters:
        tests (list): Names of the tests.
        lowest_scores (list): Lowest scores for each test.
        highest_scores (list): Highest scores for each test.
        average_scores (list): Average scores for each test.
        frame (tk.Frame): The Tkinter frame to embed the plot.
    """
    # Check if the arrays have the same length
    print(tests, lowest_scores, highest_scores, average_scores)
    if len(tests) != len(average_scores):
        print("Error: Length of tests and average_scores arrays must be the same.")
        return

    # Plot clustered column chart
    plt.figure(figsize=(10, 6))
    index = np.arange(len(tests))
    bar_width = 0.25

    plt.bar(index, lowest_scores, bar_width, label='Lowest')
    plt.bar(index + bar_width, highest_scores, bar_width, label='Highest')
    plt.bar(index + 2 * bar_width, average_scores, bar_width, label='Average')

    plt.xlabel('Test')
    plt.ylabel('Score')
    plt.title('Test Scores: Lowest, Highest, Average')
    plt.xticks(index + bar_width, tests)
    plt.legend()
    plt.grid(True)
    plt.tight_layout()

    # Embed the plot in the frame
    canvas = FigureCanvasTkAgg(plt.gcf(), master=frame)
    canvas.draw()
    canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

def plot_three_line_graphs(tests, percentages_1, percentages_2, frame):
    if None in (tests, percentages_1, percentages_2):
        print("Invalid data for Matplotlib plot. Check your data sources.")
        return
    fig, ax = plt.subplots(figsize=(6, 4), tight_layout=True)

    ax.plot(tests, percentages_1, marker='o', linestyle='-', color='blue', label='Student')
    ax.plot(tests, percentages_2, marker='x', linestyle='--', color='red', label='Average')

    # Add a third line at a constant value of 70
    ax.axhline(y=70, color='green', linestyle='-.', label='MEG')

    ax.set_xlabel('Tests')
    ax.set_ylabel('Percentage Achieved')
    ax.set_title('Test Score Graph')
    ax.legend()
    ax.grid(True)

    canvas = FigureCanvasTkAgg(fig, master=frame)
    canvas.draw()
    canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)


def display_score_comparison(tests, current_scores, average_scores, frame):
    if None in (tests, current_scores, average_scores):
        print("Invalid data for Matplotlib plot. Check your data sources.")
        return
    # Calculate the differences between current scores and average scores
    differences = [current - average for current, average in zip(current_scores, average_scores)]
    # Count the number of scores in each section
    above_target = sum(diff > 0 for diff in differences)
    below_target = sum(diff < 0 for diff in differences)
    on_target = sum(diff == 0 for diff in differences)

    # Create a table to display the score comparison
    comparison_table = ttk.Treeview(frame, columns=("Category", "Number"), show="headings", height=4)

    # Define column headings
    comparison_table.heading("Category", text="Category")
    comparison_table.heading("Number", text="Number")
    comparison_table.column("Category", width=150)
    comparison_table.column("Number", width=150)

    # Insert data into the table
    comparison_table.insert("", "end", values=("Above Target", above_target))
    comparison_table.insert("", "end", values=("Below Target", below_target))
    comparison_table.insert("", "end", values=("On Target", on_target))

    # Pack the table into the frame
    comparison_table.pack(side=tk.TOP)

    # Example: Plotting the differences
    fig, ax = plt.subplots(figsize=(6, 4), tight_layout=True)
    ax.bar(tests, differences, color=['green' if diff == 0 else 'red' if diff < 0 else 'blue' for diff in differences])
    ax.set_xlabel('Tests')
    ax.set_ylabel('Score Difference')
    ax.set_title('Score Differences')
    ax.grid(True)

    # Embed the plot in the frame
    canvas = FigureCanvasTkAgg(fig, master=frame)
    canvas.draw()
    canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)


def create_student_table(top_frame, data_extractor):
    # Create a table for student scores
    student_table = ttk.Treeview(top_frame, columns=("Test Name", "Score", "Average Score", "Difference", "Grade"), show="headings", height=10)

    # Define column headings
    for col in ("Test Name", "Score", "Average Score", "Difference", "Grade"):
        student_table.heading(col, text=col)
        student_table.column(col, width=150)

    # Fetch data for table + add loop to add multiple rows
    all_test_ids = data_extractor.get_all_test_ids()

    if all_test_ids is not None:
        for test_id in all_test_ids:
            test_name = data_extractor.get_test_name(test_id)
            test_score = data_extractor.get_test_score(test_id)
            test_avg_score = data_extractor.calc_average_score_for_test(test_id)
            test_difference = data_extractor.calc_score_difference(int(test_id), test_score)

            # Calculate the grade based on specified boundaries
            if test_score is not None:
                grade = "F"
                if test_score >= 90:
                    grade = "A*"
                elif test_score >= 80:
                    grade = "A"
                elif test_score >= 70:
                    grade = "B"
                elif test_score >= 60:
                    grade = "C"
                elif test_score >= 50:
                    grade = "D"
                elif test_score >= 40:
                    grade = "E"
            else:
                grade = "N/A"

            # Insert the data into the table
            student_table.insert("", "end", values=(test_name, test_score, test_avg_score, test_difference, grade))
    else:
        print("Error: Unable to fetch test IDs.")

    # Pack the student table into Top frame
    student_table.pack(side=tk.LEFT)


def create_grade_boundaries_table(bottom_frame):
    # Create a table for grade boundaries
    grade_boundaries_columns = ("Grade", "Boundary")
    grade_boundaries_table = ttk.Treeview(bottom_frame, columns=grade_boundaries_columns, show="headings", height=7)

    # Define column headings
    for col in grade_boundaries_columns:
        grade_boundaries_table.heading(col, text=col)
        grade_boundaries_table.column(col, width=150)

    # Insert grade boundaries data
    grade_boundaries_data = [
        ("A*", 90),
        ("A", 80),
        ("B", 70),
        ("C", 60),
        ("D", 50),
        ("E", 40),
        ("F", 30)
    ]

    for boundary in grade_boundaries_data:
        grade_boundaries_table.insert("", "end", values=boundary)

    # Pack table into Bottom frame left
    grade_boundaries_table.pack(side=tk.RIGHT)


def create_comparison_frame(tests, current_scores, average_scores, frame):
    # Calculate the differences between current scores and average scores
    differences = [current - average for current, average in zip(current_scores, average_scores)]
    # Count the number of scores in each section
    above_target = sum(diff > 0 for diff in differences)
    below_target = sum(diff < 0 for diff in differences)
    on_target = sum(diff == 0 for diff in differences)

    # Create a table to display the score comparison
    comparison_table = ttk.Treeview(frame, columns=("Category", "Number"), show="headings", height=4)

    # Define column headings
    comparison_table.heading("Category", text="Category")
    comparison_table.heading("Number", text="Number")
    comparison_table.column("Category", width=150)
    comparison_table.column("Number", width=150)

    # Insert data into the table
    comparison_table.insert("", "end", values=("Above Target", above_target))
    comparison_table.insert("", "end", values=("Below Target", below_target))
    comparison_table.insert("", "end", values=("On Target", on_target))

    # Pack the table into the frame
    comparison_table.pack(side=tk.TOP)

    # Example: Plotting the differences
    fig, ax = plt.subplots(figsize=(6, 4), tight_layout=True)
    ax.bar(tests, differences, color=['green' if diff == 0 else 'red' if diff < 0 else 'blue' for diff in differences])
    ax.set_xlabel('Tests')
    ax.set_ylabel('Score Difference')
    ax.set_title('Score Differences')
    ax.grid(True)

    # Embed the plot in the frame
    canvas = FigureCanvasTkAgg(fig, master=frame)
    canvas.draw()
    canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)


def create_avg_score_table(bottom_frame, data_extractor):
    # Create a table to display average scores
    avg_score_table = ttk.Treeview(bottom_frame, columns=("Test Name", "Average Score"), show="headings", height=10)

    # Define column headings
    avg_score_table.heading("Test Name", text="Test Name")
    avg_score_table.heading("Average Score", text="Average Score")
    avg_score_table.column("Test Name", width=150)
    avg_score_table.column("Average Score", width=150)

    # Fetch data for the average score table + add loop to add multiple rows
    all_test_ids = data_extractor.get_all_test_ids()

    if all_test_ids is not None:
        for test_id in all_test_ids:
            test_name = data_extractor.get_test_name(test_id)
            test_avg_score = data_extractor.calc_average_score_for_test(test_id)

            # Insert the data into the table
            avg_score_table.insert("", "end", values=(test_name, test_avg_score))
    else:
        print("Error: Unable to fetch test IDs.")

    # Pack the average score table into Bottom frame
    avg_score_table.pack(side=tk.LEFT)

def create_window(email, wx):
    # Database connection
    db_connection = mysql.connector.connect(
        user='thapelomoleko',
        password='Thapeloivan2006*',
        host='db4free.net',
        database='tracker'
    )

    wx.destroy()
    # Get user ID from email
    cursor = db_connection.cursor(dictionary=True)
    query = '''SELECT user_id FROM Users WHERE email = %s;'''
    cursor.execute(query, (email,))
    user_id_result = cursor.fetchone()
    user_id = user_id_result['user_id'] if user_id_result else None
    cursor.close()

    given_user_id = user_id

    # Create DataExtractor obj
    with DataExtractor(db_connection, given_user_id) as data_extractor:
        # Tk Creation
        window = tk.Tk()
        window.title("Student Information")
        window.geometry("1800x950")  # Geometry for window
        window.resizable(True, True)  # Allow window resizing

        # Create a menubar
        menubar = Menu(window)
        window.config(menu=menubar)
        # Create a menu under the menubar
        student_menu = Menu(menubar)
        # Add a menu item to the student_menu
        student_menu.add_command(label='Log Out', command=lambda: return_start(window))  # Sign out to main login page
        menubar.add_cascade(label="Settings", menu=student_menu)

        # Create frames
        top_frame = tk.Frame(window)
        bottom_frame = tk.Frame(window)
        top_frame.pack(side=tk.TOP)
        bottom_frame.pack(side=tk.BOTTOM)

        # Display student name
        user_name = data_extractor.get_user_name()
        title_label = tk.Label(top_frame, text=f"Student Name: {user_name}", font=("Helvetica", 16))
        title_label.pack()

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
        db_connection.close()

        window.mainloop()

if __name__ == "__main__":
    create_window("Gilchrisk@gmail.com", tk.Tk())
