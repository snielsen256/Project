# SuppliCore - Nutrition and Supplement Database Manager

## Features
* A database containing tables for supplements and medical conditions
* The ability to easily add, change, and delete items from this database
* Generates a report for a patient

## Notes
* Medical condition data includes nutrition requirements
* supplement information contains nutritional content
 

## Files
* main.py
* db_interface.py - holds all the functions for interfacing with the database
* README.md

## Reference
* MySQL Connector, the Python/MySQL interface: https://dev.mysql.com/doc/connector-python/en/
       * Guidelines: https://dev.mysql.com/doc/connector-python/en/connector-python-coding.html 
       * W3 resource: https://www.w3schools.com/python/python_mysql_getstarted.asp 
* Medical calculations
       * Holliday-Segar: https://www.msdmanuals.com/professional/multimedia/table/holliday-segar-formula-for-maintenance-fluid-requirements-by-weight 
       * WHO REE: http://www.nafwa.org/who_equation.html 