import pandas as pd
from tkinter import *
from tkinter import ttk, messagebox, filedialog
import os
import webbrowser
from datetime import datetime

EXCEL_PATH = r"Excel_Sheets\student_fee_status.xlsx"

def fetch_data_by_date():
    """Fetch and display fee data between two dates and calculate the total sum."""
    global filtered_data
    from_date = entry_from_date.get()
    to_date = entry_to_date.get()

    try:
        df = pd.read_excel(EXCEL_PATH, engine='openpyxl')

        if 'Pay Fee' not in df.columns:
            messagebox.showerror("Error", "The 'Pay Fee' column is missing in the Excel file.")
            return

        df['Date'] = pd.to_datetime(df['Payment Date and Time'], errors='coerce').dt.date
        from_date = pd.to_datetime(from_date).date()
        to_date = pd.to_datetime(to_date).date()

        filtered_data = df[(df['Date'] >= from_date) & (df['Date'] <= to_date)]

        if filtered_data.empty:
            messagebox.showinfo("No Data", f"No records found between {from_date} and {to_date}.")
            return

        # Clear previous data
        for item in tree.get_children():
            tree.delete(item)

        # Insert new data into TreeView
        for _, row in filtered_data.iterrows():
            tree.insert("", "end", values=list(row[:-1]))

        # Update the total paid fee label
        total_paid_fee = filtered_data['Pay Fee'].sum()
        label_total.config(text=f"Total Paid Fee: {total_paid_fee}")

    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")

def open_payment_fee():
    try:
        root.destroy()
        os.system("python Additional_Files/fms.py")
    except Exception as e:
        messagebox.showerror("Error", str(e))

def print_data():
    """Generate an HTML report and open it in the browser."""
    global filtered_data

    if 'filtered_data' not in globals() or filtered_data.empty:
        messagebox.showinfo("No Data", "No data to print. Please fetch data first.")
        return

    try:
        folder_path = "Daily_Payments"
        os.makedirs(folder_path, exist_ok=True)

        from_date = entry_from_date.get().replace("-", "_")
        to_date = entry_to_date.get().replace("-", "_")
        file_name = f"{from_date}_{to_date}.html"
        file_path = os.path.join(folder_path, file_name)

        html_content = f"""
        <html>
        <head>
            <title>Fee Data Report</title>
            <style>
                table {{ border-collapse: collapse; width: 100%; }}
                th, td {{ border: 1px solid black; padding: 8px; text-align: center; }}
                th {{ background-color: #f2f2f2; }}
            </style>
        </head>
        <body>
            <h2>Fee Data Report: {entry_from_date.get()} to {entry_to_date.get()}</h2>
            <table>
                <tr>
                    <th>Student ID</th>
                    <th>Student Name</th>
                    <th>Payment To Semester</th>
                    <th>Paid Fee</th>
                    <th>Due Fee</th>
                    <th>Total Fee</th>
                    <th>Payment Done By</th>
                </tr>"""

        for _, row in filtered_data.iterrows():
            html_content += f"""
            <tr>
                <td>{row['Student ID']}</td>
                <td>{row['Student Name']}</td>
                <td>{row['Payment To Semester']}</td>
                <td>{row['Pay Fee']}</td>
                <td>{row['Due Fee']}</td>
                <td>{row['Total Fee']}</td>
                <td>{row['Payment Done By']}</td>
            </tr>"""

        html_content += """
            </table>
        </body>
        </html>"""

        with open(file_path, "w", encoding="utf-8") as file:
            file.write(html_content)

        webbrowser.open(f"file://{os.path.abspath(file_path)}")

    except Exception as e:
        messagebox.showerror("Error", f"Failed to generate HTML report: {e}")

root = Tk()
root.title("Pay Fee Status Viewer")
root.state('zoomed')

style = ttk.Style(root)
style.theme_use('clam')

# Custom style for TreeView font size
style.configure("Treeview", font=("Arial", 14))  # Adjust the font size here
style.configure("Treeview.Heading", font=("Arial", 12, "bold"))  # Heading font size

frame = Frame(root, padx=20, pady=20)
frame.pack(expand=True, fill=BOTH)

Label(frame, text="From Date (YYYY-MM-DD):", font=("Arial", 16)).grid(row=0, column=0, padx=10, pady=10, sticky=W)
entry_from_date = Entry(frame, font=("Arial", 16), width=20)
entry_from_date.grid(row=0, column=1, padx=(10, 0), pady=10, sticky=W)

Label(frame, text="To Date (YYYY-MM-DD):", font=("Arial", 16)).grid(row=0, column=2, padx=10, pady=10, sticky=W)
entry_to_date = Entry(frame, font=("Arial", 16), width=20)
entry_to_date.grid(row=0, column=3, padx=(10, 0), pady=10, sticky=W)

btn_fetch = Button(frame, text="Fetch Data", font=("Arial", 16), command=fetch_data_by_date)
btn_fetch.grid(row=0, column=4, padx=(20, 0), pady=10, sticky=W)

tree_frame = Frame(frame)
tree_frame.grid(row=1, column=0, columnspan=6, padx=10, pady=10, sticky='nsew')

tree_scroll_y = Scrollbar(tree_frame, orient=VERTICAL)
tree_scroll_x = Scrollbar(tree_frame, orient=HORIZONTAL)

tree = ttk.Treeview(tree_frame, columns=("ID", "Name", "Payment To Semester", "Pay Fee", "Due Fee", "Total Fee", "Payment Done By"),
                    show='headings', yscrollcommand=tree_scroll_y.set, xscrollcommand=tree_scroll_x.set)

tree_scroll_y.config(command=tree.yview)
tree_scroll_x.config(command=tree.xview)

tree_scroll_y.pack(side=RIGHT, fill=Y)
tree_scroll_x.pack(side=BOTTOM, fill=X)
tree.pack(expand=True, fill=BOTH)

for col in tree["columns"]:
    tree.heading(col, text=col)
    tree.column(col, anchor=CENTER, width=150)

btn_back = Button(frame, text="Go Back To Payment Dashboard", font=("Arial", 16), command=open_payment_fee)
btn_back.grid(row=2, column=5, padx=(20, 0), pady=10, sticky=W)

label_total = Label(frame, text="Total Paid Fee: 0", font=("Arial", 16))
label_total.grid(row=2, column=0, columnspan=4, padx=10, pady=10, sticky=W)

btn_print = Button(frame, text="Print Data", font=("Arial", 16), command=print_data)
btn_print.grid(row=2, column=4, padx=10, pady=10, sticky=E)

frame.grid_rowconfigure(1, weight=1)
frame.grid_columnconfigure(1, weight=1)

def on_closing():
    if messagebox.askokcancel("Quit", "Do you want to quit?"):
        root.destroy()

root.protocol("WM_DELETE_WINDOW", on_closing)
root.mainloop()
