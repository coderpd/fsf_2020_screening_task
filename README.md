# Python-Screening-Task-2--FOSSEE
a desktop application that will take inputs for four different categories (modules).

GUI have a spreadsheet, Load Inputs, Validate and Submit buttons, message box to display warning messages if the user gives a bad value.

A spreadsheet of different modules is opened in different tabs of the same window.

Based on the selected module corresponding header row is displayed in spreadsheet GUI. Details of header rows, with sample input values for each module, are given in resources.

For example You can develop UI with four tabs, one for each module, which has respective header rows. (Checkout QTableWidget, QStakedWidget, QTabWidget of PyQt5 for GUI design)

“Load Inputs” button shall prompt for selecting CSV/xlxs file, which populate the spreadsheet. Also, Users can fill data manually in each row.

The clicking of the “Validate” button validates the data and a suitable error message for bad values are displayed in the message box.

Required validators are:

All cells other than headers only take numerical inputs.

Headers are not editable.

ID column is unique, i.e., ID number is not to be repeated

Once the user submits the data by clicking on the “Submit” button, it creates a new text file for each row. This text file is a dictionary with header value as key and cell value as value.

Text files are saved in the folder location input by the user.

Text files are saved as Modulename_ID. For example, if the user submits fin plate inputs, the first row will be saved as FinPlate_1 automatically, i.e., the user does not have to specify the file name for each row.

An easy to use, user-friendly and clean looking GUI application would help the user to quickly adapt to the application.

Also created an installer (Windows or Ubuntu) for your application.
