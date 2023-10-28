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
    * create_new_database() 
    * start_database(username, user_password, host_address, db_name)
    * close_database(cnx)
    * create_new_report()
    * edit_reports(report)
    * view_reports(report)
    * create_new_patient()
    * edit_patients(patient)
    * create_new_nutrient()
    * edit_nutrients(nutrient)
    * create_new_supplement()
    * edit_supplements(supplement)
    * create_new_medication()
    * edit_medications(medication)
    * create_new_ref_chart()
    * edit_ref_charts(ref_chart)

* README.md

## Reference
* MySQL Connector, the Python/MySQL interface: https://dev.mysql.com/doc/connector-python/en/
       * Guidelines: https://dev.mysql.com/doc/connector-python/en/connector-python-coding.html 
       * W3 resource: https://www.w3schools.com/python/python_mysql_getstarted.asp 