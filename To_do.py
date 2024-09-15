import tkinter as tk
from tkinter import ttk
from datetime import datetime
import os
import json

# File path for saving and loading table data
data_file = r'enter_file_path'

# Initialize the main application window
root = tk.Tk()
root.title("Your Schedule")
root.geometry("320x700")
root.configure(bg='grey')

# Create frames
main_frame = tk.Frame(root, bg="grey")
add_frame = tk.Frame(root, bg="grey")
remove_frame = tk.Frame(root, bg="grey")

#aligning frames DONOT REMOVE WILL GIVE BLANK CONSOLE
root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(0, weight=1)

for frame in (main_frame, add_frame, remove_frame):
    frame.grid(row=0, column=0, sticky="nsew")

def show_frame(frame):
    frame.tkraise()

def click_add():
    show_frame(add_frame)

def click_remove():
    show_frame(remove_frame)

def greetings():
    current_hour = datetime.now().hour
    if current_hour < 12:
        greeting.config(text="Good Morning sir", bg="grey")
    elif 12 <= current_hour < 18:
        greeting.config(text="Good Afternoon sir", bg="grey")
    else:
        greeting.config(text="Good Evening sir", bg="grey")

# Main frame content
greeting = tk.Label(main_frame, text="")
greeting.place(x=110, y=15)

today = tk.Label(main_frame, text="Your tasks for today are", bg="grey")
today.place(x=95, y=100)

add = tk.Button(
    main_frame,
    text="Add task",
    width=10,
    height=2,
    fg="white",
    bg="black",
    command=click_add
)
add.place(x=20, y=45)
def remove_row_from_table(sno):
    # Find all rows in the table
    rows = table.get_children()

    for row in rows:
        # Get the values of the current row
        row_values = table.item(row, 'values')

        # Check if the 'Sno' matches
        if row_values[0] == sno:
            table.delete(row)  # Remove the row from the table
            break  # Exit loop after removing the matching row

    save_table_data()  # Save the updated table data to file

remove = tk.Button(
    main_frame,
    text="Mark as done",
    width=10,
    height=2,
    fg="white",
    bg="black",
    command=click_remove
)
remove.place(x=220, y=45)
remove_label = tk.Label(remove_frame, text="Enter Sno to remove", bg='grey')
remove_label.pack(pady=10)

sno_remove_entry = tk.Entry(remove_frame)
sno_remove_entry.pack(pady=5)

remove_button = tk.Button(remove_frame, text="Remove Task", command=lambda: remove_row_from_table(sno_remove_entry.get()))
remove_button.pack(pady=10)

# Table section
table = ttk.Treeview(main_frame, columns=('Sno', 'Task', 'Time left'), show='headings')
table.heading('Sno', text='Sno')
table.heading('Task', text='Task')
table.heading('Time left', text='Time left')

table.column('Sno', width=50)
table.column('Task', width=150)
table.column('Time left', width=100)
table.place(x=10, y=150, width=300, height=300)

# Add task frame content
add_label = tk.Label(add_frame, text="Please enter the task", bg='grey')
add_label.pack(pady=10)

sno_entry = tk.Entry(add_frame)
sno_entry.place(x=10, y=30, width=50)

task_entry = tk.Entry(add_frame)
task_entry.place(x=70, y=30, width=150)

time_left_entry = tk.Entry(add_frame)
time_left_entry.place(x=230, y=30, width=80)

def add_row_to_table():
    sno = sno_entry.get()
    task = task_entry.get()
    time_left = time_left_entry.get()

    if sno and task and time_left:
        table.insert('', 'end', values=(sno, task, time_left))
        sno_entry.delete(0, tk.END)
        task_entry.delete(0, tk.END)
        time_left_entry.delete(0, tk.END)
        save_table_data()
    else:
        print("Please fill out all fields.")

submit_button = tk.Button(add_frame, text="Add to Table", command=add_row_to_table)
submit_button.place(x=10, y=60)

# Remove frame content
remove_label = tk.Label(remove_frame, text="Remove tasks from table", bg='green')
remove_label.pack(pady=10)

def save_table_data():
    rows = table.get_children()
    data = []
    for row in rows:
        values = table.item(row, 'values')
        data.append(values)
    with open(data_file, 'w') as f:
        json.dump(data, f)

def load_table_data():
    if os.path.exists(data_file):
        with open(data_file, 'r') as f:
            try:
                data = json.load(f)
                for row in data:
                    table.insert('', 'end', values=row)
            except json.JSONDecodeError:
                print("Error decoding JSON. The file may be corrupted.")

# Load data when the application starts
load_table_data()

# Initialize the application
show_frame(main_frame)
greetings()
root.mainloop()
