import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import os

# Create the main window
root = tk.Tk()
root.title("Receipt Viewer")
root.state('zoomed')  # Start in fullscreen mode
root.configure(bg="#e0f7fa")  # Light blue background

# Function to resize the image based on window size
def resize_image(img, target_width, target_height):
    return img.resize((target_width, target_height), Image.Resampling.LANCZOS)

# Function to crop the top half of the image
def crop_top_half(img):
    # Get the original width and height of the image
    width, height = img.size
    # Crop the top half of the image (0, 0, width, height // 2)
    return img.crop((0, 0, width, height // 2))

# Function to display the receipt image based on user input
def display_receipt():
    receipt_no = receipt_input.get()  # Get the receipt number from the input field
    receipts_folder = "receipts"

    # Search for files matching the pattern "*_<receipt_no>.png"
    matching_files = [f for f in os.listdir(receipts_folder) if f.endswith(f"_{receipt_no}.png")]

    if matching_files:
        try:
            # Use the first matching file (if more exist)
            receipt_path = os.path.join(receipts_folder, matching_files[0])
            
            # Open the image
            receipt_image = Image.open(receipt_path)
            
            # Crop the image to show only the top half
            receipt_image = crop_top_half(receipt_image)
            
            # Get the current size of the window
            window_width = root.winfo_width()
            window_height = root.winfo_height()
            
            # Set the size to a percentage of the window's size
            target_width = int(window_width * 0.5)  # 50% of window width
            target_height = int(window_height * 0.6)  # 60% of window height
            
            # Resize the cropped image
            receipt_image = resize_image(receipt_image, target_width, target_height)
            
            # Display the image
            img = ImageTk.PhotoImage(receipt_image)
            receipt_display.config(image=img, text="")  # Clear the text if an image is found
            receipt_display.image = img  # Keep a reference to avoid garbage collection
            status_label.config(text=f"Displaying Receipt: {receipt_no}", fg="green")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load receipt image: {e}")
    else:
        # Display a red highlighted "Receipt Not Found" message
        receipt_display.config(image="", text="!!!!RECEIPT NOT FOUND!!!!", font=("Arial", 30, "bold"), bg="red", fg="white")
        status_label.config(text="Receipt not found. Please check the receipt number.", fg="red")

# Create input field for receipt number
title_label = tk.Label(root, text="Receipt Viewer", font=("Arial", 24, "bold"), bg="#e0f7fa", fg="#00796b")
title_label.pack(pady=20)

receipt_label = tk.Label(root, text="Enter Receipt No:", font=("Arial", 16), bg="#e0f7fa", fg="#004d40")
receipt_label.pack(pady=10)

receipt_input = tk.Entry(root, font=("Arial", 14), width=20, bd=2, relief="solid")
receipt_input.pack(pady=5)

# Function to open sreg.py
def open_registration():
    try:
        # Close the current main window (main.py)
        root.destroy()
        os.system("python Additional_Files/sreg.py")
    except Exception as e:
        messagebox.showerror("Error", str(e))

# Function to open fms.py
def open_payment_fee():
    try:
        # Close the current main window (main.py)
        root.destroy()
        os.system("python Additional_Files/fms.py")
    except Exception as e:
        messagebox.showerror("Error", str(e))

# Create button to fetch and display receipt
fetch_button = tk.Button(root, text="Fetch Receipt", font=("Arial", 14, "bold"), bg="#00796b", fg="white", width=15, height=1, command=display_receipt, bd=0, relief="flat")
fetch_button.pack(pady=15)

# Frame to hold the Registration and Payment Fee buttons
button_frame = tk.Frame(root, bg="#e0f7fa")
button_frame.pack(pady=10)

# New buttons for Registration and Payment Fee in a single line
registration_button = tk.Button(button_frame, text="Registration", font=("Arial", 14, "bold"), bg="#00796b", fg="white", width=15, command=open_registration)
registration_button.grid(row=0, column=0, padx=10)  # Add some horizontal padding

payment_fee_button = tk.Button(button_frame, text="Payment Fee", font=("Arial", 14, "bold"), bg="#00796b", fg="white", width=15, command=open_payment_fee)
payment_fee_button.grid(row=0, column=1, padx=10)  # Add some horizontal padding

# Label to show the image of the receipt or error message
receipt_display = tk.Label(root, bg="#e0f7fa")
receipt_display.pack(pady=10)

# Status label to show messages
status_label = tk.Label(root, text="", font=("Arial", 12), bg="#e0f7fa", fg="red")
status_label.pack(pady=20)

# Function to handle Exit
def on_closing():
    if messagebox.askokcancel("Quit", "Do you want to quit?"):
        root.destroy()

root.protocol("WM_DELETE_WINDOW", on_closing) 
# Run the main loop
root.mainloop()
