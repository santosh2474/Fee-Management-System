# Fee-Management-System
**Short Description:**   A user-friendly **Fees Management System** built with Python and Tkinter, designed to manage student registrations, track fee payments, generate receipts, and provide insightful reports. Ideal for schools and educational institutions to streamline administrative tasks and ensure efficient financial tracking.

README - Fees Management System
Introduction
This software is a Fees Management System that allows users to perform the following operations:
- Manage student registration and store their details.
- Record and verify fee payments.
- Generate receipts and reports.
- Provide access to registered students' details and handle various payment operations.
Prerequisites
- Python 3.x must be installed.
- Required libraries:
 - `tkinter`
 - `Pillow`
 - `openpyxl`
 - `pandas`
Install the dependencies using:
pip install pillow openpyxl pandas
How to Use the Software
1. Running the Application
✓ Open a terminal or command prompt.
✓ Navigate to the directory containing the project files.
✓ Run the main script:
 python main.py
2. Login and User Authentication
- On the login screen, enter User ID and Password.
 - Sample credentials:
 - User: `admin`, Password: `password`
- Click Login to access the dashboard.
3. Modules and Features
✓ Registration Module (`sreg.py`):
 - Add student details, including photos and contact information.
 - Store data in the `student_registration.xlsx` file.
 - Use the Upload Photo button to attach a photo to the student profile.
✓ Fee Management Module (`fms.py`):
 - Record fee payments by students.
 - Keep track of due and total fees.
 - Generate receipts with a unique receipt number and option to print them.
 - Payments are stored in `student_fee_status.xlsx`.
✓ Receipt Verification (`verify.py`):
 - Enter the receipt number to display its details and ensure validity.
✓ View Student Details (`students_details.py`):
 - Search and filter student data based on name, year, or student ID.
 - Print student information with attached photos.
4. Generating Reports
- HTML Payment Reports: Available from the Fee Management Module by selecting a date range.
- Daily Payment Summary: View total paid fees for a specific day.
5. Folder Structure
- `Excel_Sheets/`: Contains all Excel files for logs and data.
- `receipts/`: Stores receipt images.
- `student_photos/`: Stores photos for registered students.
- `logo_folder/`: Contains the logo used on receipts and screens.
6. Common Issues
- Logo not found: Ensure the logo is placed in the `logo_folder` directory.
- Excel files missing: The system creates required Excel files on the first run if they do not exist.
7. Contact Information
If you encounter issues, reach out to the developer:
- Developer: Er. Santosh Thakur
- Contact No.: +977-9804743283
- Email: santoshthakur@engineer.com
- Website: www.santoshthakur.online
This README should guide you through the setup and usage of the Fees Management System effectively. Enjoy using
the software!

SCREENSHOT:

![image](https://github.com/user-attachments/assets/9b6088f6-320f-4314-b4d5-c765a0301157)
![image](https://github.com/user-attachments/assets/7ce71a63-53b0-4831-b767-4d51a093d89b)
![image](https://github.com/user-attachments/assets/d6bac966-5905-486b-b85d-90a725f63283)
![image](https://github.com/user-attachments/assets/28d941d9-0f19-408a-8872-9ff9903ef27f)
![image](https://github.com/user-attachments/assets/575cae98-27cd-4b42-9792-7a21792a5670)
![image](https://github.com/user-attachments/assets/36c027c4-9ae9-4d9f-a1c8-a1a3375e8cf3)
![image](https://github.com/user-attachments/assets/ce22c7bc-e148-4c91-b341-2aa1f38a6f24)
![image](https://github.com/user-attachments/assets/7b2c682e-0a1c-461b-9add-e7b1ba607721)
![image](https://github.com/user-attachments/assets/5b22878a-a0f0-42e5-b59b-ce8cddabc7f5)
![image](https://github.com/user-attachments/assets/95fef838-94d6-472a-b8e3-babd50a89992)





