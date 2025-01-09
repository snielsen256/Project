# SuppliCore - Nutrition and Supplement Database Manager

## Features
* A database containing tables for supplements and medical conditions
* The ability to easily add, change, and delete items from this database
* Generates a report for a patient
* Optionally autofill patient data from database

## Using the Program
1. Download supplicore.exe and db_setup.sql, the latter contains the structure needed to set up the database. MySQL Workbench can help with this if you want this database on your PC.
3. Wherever you choose to set up the database, you edit the connection on the "Settings" page, however you must set up the database login information before the program can be run for the first time. Create a file called "config.json" and fill it with the code below. 
```
{
 "user": "***",
 "password": "***",
 "host": "***",
 "port": ***,
 "database": "supplicore_db",
 "raise_on_warnings": true
}
```
4. Replace the *** with relevant information. Take note that numbers values aren't in quotation marks. If you are running the database on the same computer as the program, user is "root", host is "localhost" and the port is likely 3306. The password is defined by you when you set up the database.

## Files
* app.py - The main file
* db_interface.py - Holds all the functions for interfacing with the database
* GUI.py - Everything to do with the user interface
* README.md

## Notes
* To recompile the exe file, run "python -m pyinstaller --onefile --name Supplicore --distpath . app.py"

## Reference
* MySQL Connector, the Python/MySQL interface: https://dev.mysql.com/doc/connector-python/en/
       * Guidelines: https://dev.mysql.com/doc/connector-python/en/connector-python-coding.html 
       * W3 resource: https://www.w3schools.com/python/python_mysql_getstarted.asp 
* Medical calculations
       * Holliday-Segar: https://www.msdmanuals.com/professional/multimedia/table/holliday-segar-formula-for-maintenance-fluid-requirements-by-weight 
       * WHO REE: http://www.nafwa.org/who_equation.html 
* Saving as PDF
       * https://stackoverflow.com/questions/66269130/how-to-use-python-to-save-dict-as-a-table-in-pdf-with-cell-coloring 
       * https://prog.world/create-pdf-document-in-python-using-ptext/
* GUI
       * https://www.pythontutorial.net/tkinter/
* Creating executable file
       * https://python.land/deployment/pyinstaller


## To Do
* Add calendar select to database interface to avoid date format issues
* Add medical condition to autofill
* Add ability to export as PDF
* Add ability to import and edit reports that have been saved as a file
* Revise supplement and condition database interface
* Add ability to edit associations between supplements and conditions
* Add more scroll bars, and link them (and existing ones) to the mouse wheel.
* Add icon and logo on home page
* Fix calculation labels becoming worse when patient details are fetched