import tkinter as tk
from tkinter import ttk, messagebox, Label
import pandas as pd
from PIL import Image, ImageTk  # For displaying images
import tkinter.font as font  # To set custom fonts
import os
import webbrowser

# File paths
FILE_PATH = r"Excel_Sheets\student_registration.xlsx"
PHOTO_DIR = r"student_photos"  # Directory containing photos

def print_data():
    selected_items = tree.get_children()
    if not selected_items:
        messagebox.showwarning("No Data", "No data to print. Please fetch data first.")
        return

    # Start building the HTML content
    html_content = """
    <html>
    <head>
        <title>Student Registration Details</title>
        <style>
            body {font-family: Arial, sans-serif; margin: 20px;}
            table {width: 100%; border-collapse: collapse;}
            th, td {padding: 8px; text-align: left; border-bottom: 1px solid #ddd;}
            th {background-color: #f2f2f2; font-weight: bold;}
            img {max-width: 120px; height: auto; border-radius: 5px;}
            .photo-cell {text-align: center;}
        </style>
    </head>
    <body>
        <h2>Student Registration Details</h2>
        <table>
            <thead>
                <tr>
                    <th>Student ID</th>
                    <th>Name</th>
                    <th>Father's Name</th>
                    <th>Course</th>
                    <th>Semester</th>
                    <th>Total Fees</th>
                    <th>Student Contact No.</th>
                    <th>Guardian Contact No.</th>
                    <th>Address</th>
                    <th>Registration Date (AD)</th>
                    <th>Date of Birth (BS)</th>
                    <th>Photo</th>
                </tr>
            </thead>
            <tbody>
    """

    for item in selected_items:
        student_id = tree.item(item)["values"][0]
        name = tree.item(item)["values"][1]
        father_name = tree.item(item)["values"][2]
        course = tree.item(item)["values"][3]
        semester = tree.item(item)["values"][4]
        total_fees = tree.item(item)["values"][5]
        student_contact = tree.item(item)["values"][6]
        guardian_contact = tree.item(item)["values"][7]
        address = tree.item(item)["values"][8]
        registration_date = tree.item(item)["values"][9]
        dob = tree.item(item)["values"][10]  # Date of Birth added here

        photo_filename = f"{name.replace(' ', '_')}_{student_id}.jpg"
        photo_path = f"{PHOTO_DIR}/{photo_filename}"

        if os.path.exists(photo_path):
            photo_html = f'<img src="{photo_path}" alt="Photo">'
        else:
            photo_html = "<span>No photo available</span>"

        html_content += f"""
        <tr>
            <td>{student_id}</td>
            <td>{name}</td>
            <td>{father_name}</td>
            <td>{course}</td>
            <td>{semester}</td>
            <td>{total_fees}</td>
            <td>{student_contact}</td>
            <td>{guardian_contact}</td>
            <td>{address}</td>
            <td>{registration_date}</td>
            <td>{dob}</td>
            <td class="photo-cell">{photo_html}</td>
        </tr>
        """

    html_content += """
            </tbody>
        </table>
    </body>
    </html>
    """

    html_file = "student_registration_details.html"
    with open(html_file, "w") as file:
        file.write(html_content)

    webbrowser.open(f"file://{os.path.abspath(html_file)}")

def open_payment_fee():
    try:
        root.destroy()
        os.system("python Additional_Files/fms.py")
    except Exception as e:
        messagebox.showerror("Error", str(e))

def load_data():
    try:
        df = pd.read_excel(FILE_PATH, parse_dates=["Registration Date"])
        df['Year'] = df['Registration Date'].dt.year
        df['Registration Date'] = df['Registration Date'].dt.date
        return df
    except Exception as e:
        messagebox.showerror("Error", f"Unable to load the Excel file:\n{e}")
        return None

def filter_data():
    year = year_var.get().strip()
    student_name = name_var.get().strip()
    student_id = student_id_var.get().strip()  # Get Student ID from the new entry

    if not year and not student_name and not student_id:  # Check for all fields
        messagebox.showwarning("Input Error", "Please enter a year, student name, or student ID.")
        return

    # Initialize filtered DataFrame with the original DataFrame
    filtered_df = df

    # Filter by year if provided
    if year:
        filtered_df = filtered_df[filtered_df['Year'].astype(str) == year]
    
    # Filter by student name if provided
    if student_name:
        filtered_df = filtered_df[filtered_df['Name'].str.contains(student_name, case=False, na=False)]
    
    # Filter by student ID if provided
    if student_id:
        filtered_df = filtered_df[filtered_df['Student ID'].astype(str) == student_id]

    # Clear the Treeview and photo label
    for row in tree.get_children():
        tree.delete(row)
    photo_label.config(image='')

    if not filtered_df.empty:
        for _, row in filtered_df.iterrows():
            tree.insert("", "end", values=[ 
                row['Student ID'], row['Name'], row["Father's Name"], row['Course'], row['Semester'],
                row['Total Fees'], row['Student Contact No.'], row['Guardian Contact No.'],
                row['Address'], row['Registration Date'], row['Date of Birth']  # Added DOB here
            ])
    else:
        messagebox.showinfo("No Data", "No student data found for the selected year, name, or Student ID.")

def on_row_select(event):
    selected_item = tree.selection()
    if not selected_item:
        return

    item = tree.item(selected_item)
    student_name = item['values'][1]
    student_id = item['values'][0]

    photo_filename = f"{student_name.replace(' ', '_')}_{student_id}.jpg"

    try:
        image_path = f"{PHOTO_DIR}/{photo_filename}"
        image = Image.open(image_path).resize((120, 120))
        photo = ImageTk.PhotoImage(image)
        photo_label.config(image=photo)
        photo_label.image = photo
    except Exception as e:
        messagebox.showerror("Error", f"Unable to load photo:\n{e}")

# Initialize the main window
root = tk.Tk()
root.title("Student Registration Details")
root.state('zoomed')

df = load_data()
if df is None:
    root.destroy()

custom_font = font.Font(family="Helvetica", size=12)
button_font = font.Font(family="Helvetica", size=14, weight="bold")
heading_font = font.Font(family="Helvetica", size=16, weight="bold")

year_var = tk.StringVar()
name_var = tk.StringVar()
student_id_var = tk.StringVar()  # New variable for Student ID

heading_label = tk.Label(root, text="Student Registration Details", font=heading_font)
heading_label.grid(row=0, column=0, columnspan=3, padx=10, pady=10, sticky="n", ipady=5)

input_frame = tk.Frame(root)
input_frame.grid(row=1, column=0, columnspan=3, padx=10, pady=10, sticky="w")

ttk.Label(input_frame, text="Registered Year:", font=custom_font).grid(row=0, column=0, padx=(5, 2), pady=5, sticky="w")
year_entry = ttk.Entry(input_frame, textvariable=year_var, font=custom_font)
year_entry.grid(row=0, column=1, padx=(2, 5), pady=5, sticky="w")

ttk.Label(input_frame, text="Name:", font=custom_font).grid(row=0, column=2, padx=(5, 2), pady=5, sticky="w")
name_entry = ttk.Entry(input_frame, textvariable=name_var, font=custom_font)
name_entry.grid(row=0, column=3, padx=(2, 5), pady=5, sticky="w")

# Add entry for Student ID
ttk.Label(input_frame, text="Student ID:", font=custom_font).grid(row=0, column=4, padx=(5, 2), pady=5, sticky="w")
student_id_entry = ttk.Entry(input_frame, textvariable=student_id_var, font=custom_font)
student_id_entry.grid(row=0, column=5, padx=(2, 5), pady=5, sticky="w")

button_frame = tk.Frame(root)
button_frame.grid(row=2, column=0, columnspan=3, padx=10, pady=10, sticky="w")

fetch_button = ttk.Button(button_frame, text="Fetch Data", command=filter_data, style="Custom.TButton")
fetch_button.grid(row=0, column=0, padx=(0, 10))

print_button = ttk.Button(button_frame, text="Print Data", command=print_data, style="Custom.TButton")
print_button.grid(row=0, column=1)

go_back_button = ttk.Button(button_frame, text="Go Back to Payment Dashboard", command=open_payment_fee, style="Custom.TButton")
go_back_button.grid(row=0, column=2, padx=(10, 0))

style = ttk.Style()
style.configure("Custom.TButton", font=button_font)

# Frame for the Treeview and scrollbars (Treeview placed in the bottom area)
tree_frame = tk.Frame(root)
tree_frame.grid(row=3, column=0, columnspan=3, padx=5, pady=5, sticky='nsew')

# Configure row and column to expand in the root window
root.grid_rowconfigure(3, weight=1)  # Ensure row 3 (where the tree is) expands
root.grid_columnconfigure(0, weight=1)  # Make the first column expand
root.grid_columnconfigure(1, weight=1)  # Make the second column expand
root.grid_columnconfigure(2, weight=1)  # Make the third column expand

# Define the Treeview widget
columns = [
    "Student ID", "Name", "Father's Name", "Course", "Semester", "Total Fees",
    "Student Contact No.", "Guardian Contact No.", "Address", "Registration Date (AD)", "Date of Birth (BS)"
]

tree = ttk.Treeview(tree_frame, columns=columns, show="headings", height=15)

for col in columns:
    tree.heading(col, text=col)
    if col == "Student ID":
        tree.column(col, width=100, anchor='center')
    elif col == "Semester":
        tree.column(col, width=100, anchor='center')
    elif col == "Total Fees":
        tree.column(col, width=100, anchor='center')
    elif col == "Date of Birth":
        tree.column(col, width=120, anchor='center')
    else:
        tree.column(col, width=150, anchor='center')

tree.grid(row=0, column=0, sticky="nsew")

# Configure the tree to expand
tree_frame.grid_rowconfigure(0, weight=1)
tree_frame.grid_columnconfigure(0, weight=1)

# Photo label for displaying student photos
photo_label = Label(root)
photo_label.grid(row=0, column=2, padx=100, pady=10, sticky="e")

# Bind row selection for photo preview
tree.bind("<ButtonRelease-1>", on_row_select)

root.mainloop()
