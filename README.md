# SuppliCore - Nutrition and Supplement Database Manager

## Features
* A database containing tables for supplements and medical conditions
* The ability to easily add, change, and delete items from this database
* Generates a report for a patient
* Optionally autofill patient data from database

## Using the Program
* The runnable program is the .exe file. If you want to use the program, this is the only file that is absolutely necessary to download.
* If you choose to use a database, download db_setup.sql as well. It contains the structure needed to set up the database. MySQL Workbench can help with this if you want this database on your PC.
* Wherever you choose to set up the database, you can connect to it on the "Settings" page of Supplicore.

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