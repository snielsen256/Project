"""
db_interface.py
Holds all the functions for interfacing with the database
"""

import mysql.connector
from mysql.connector import errorcode
import json
import pandas as pd
import warnings

# General ----------------------------
def raw_sql(cnx, query:str):
    """
    Runs MySQL code
    * Parameters:
           * cnx - the connection to the database
           * query:str - the MySQL code
    * Returns: 
           * DataFrame - the result of the query
    """
    query_result = pd.read_sql(query, cnx)
    return query_result

# Database management -----------------------------
def create_new_database(config):
    """
    Creates a new database
    * Parameters:
           * config: dict
    * Returns: none
    """
    # Make sure that MySQL is installed
    pass

    # define database
    cnx = mysql.connector.connect(**config)
    cursor1 = cnx.cursor()
    cursor1.execute(
        f"""
        -- MySQL Workbench Forward Engineering

        SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
        SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
        SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

        -- -----------------------------------------------------
        -- Schema {config['database']}
        -- -----------------------------------------------------

        -- -----------------------------------------------------
        -- Schema {config['database']}
        -- -----------------------------------------------------
        CREATE SCHEMA IF NOT EXISTS `{config['database']}` DEFAULT CHARACTER SET utf8 ;
        USE `{config['database']}` ;

        -- -----------------------------------------------------
        -- Table `{config['database']}`.`Medical_conditions`
        -- -----------------------------------------------------
        CREATE TABLE IF NOT EXISTS `{config['database']}`.`Medical_conditions` (
        `Medical_conditions_id` VARCHAR(45) NOT NULL,
        `name` VARCHAR(45) NOT NULL,
        PRIMARY KEY (`Medical_conditions_id`))
        ENGINE = InnoDB;


        -- -----------------------------------------------------
        -- Table `{config['database']}`.`Supplements`
        -- -----------------------------------------------------
        CREATE TABLE IF NOT EXISTS `{config['database']}`.`Supplements` (
        `Supplements_id` INT NOT NULL AUTO_INCREMENT,
        `name` VARCHAR(45) NOT NULL,
        `kcal` FLOAT NOT NULL,
        `displacement` FLOAT NULL,
        `notes` VARCHAR(300) NULL,
        PRIMARY KEY (`Supplements_id`))
        ENGINE = InnoDB;


        -- -----------------------------------------------------
        -- Table `{config['database']}`.`Nutrients`
        -- -----------------------------------------------------
        CREATE TABLE IF NOT EXISTS `{config['database']}`.`Nutrients` (
        `Nutrients_id` INT NOT NULL,
        `name` VARCHAR(45) NOT NULL,
        `units` ENUM("g", "mg") NOT NULL,
        `goals_chart` JSON NULL,
        PRIMARY KEY (`Nutrients_id`))
        ENGINE = InnoDB;


        -- -----------------------------------------------------
        -- Table `{config['database']}`.`Patients`
        -- -----------------------------------------------------
        CREATE TABLE IF NOT EXISTS `{config['database']}`.`Patients` (
        `MRN` INT NOT NULL,
        `f_name` VARCHAR(45) NOT NULL,
        `m_name` VARCHAR(45) NULL,
        `l_name` VARCHAR(45) NOT NULL,
        `DOB` DATE NOT NULL,
        `age` FLOAT NOT NULL,
        `age_unit` ENUM("years", "months", "weeks", "days") NOT NULL,
        `weight_kg` FLOAT NOT NULL,
        `Medical_conditions_id` VARCHAR(45) NOT NULL,
        PRIMARY KEY (`MRN`),
        INDEX `fk_Patients_Medical_conditions1_idx` (`Medical_conditions_id` ASC) VISIBLE,
        CONSTRAINT `fk_Patients_Medical_conditions1`
            FOREIGN KEY (`Medical_conditions_id`)
            REFERENCES `{config['database']}`.`Medical_conditions` (`Medical_conditions_id`)
            ON DELETE NO ACTION
            ON UPDATE NO ACTION)
        ENGINE = InnoDB;


        -- -----------------------------------------------------
        -- Table `{config['database']}`.`Supplements_has_Nutrients`
        -- -----------------------------------------------------
        CREATE TABLE IF NOT EXISTS `{config['database']}`.`Supplements_has_Nutrients` (
        `Supplements_id` INT NOT NULL,
        `Nutrients_id` INT NOT NULL,
        PRIMARY KEY (`Supplements_id`, `Nutrients_id`),
        INDEX `fk_Supplements_has_Nutrients_Nutrients1_idx` (`Nutrients_id` ASC) VISIBLE,
        INDEX `fk_Supplements_has_Nutrients_Supplements_idx` (`Supplements_id` ASC) VISIBLE,
        CONSTRAINT `fk_Supplements_has_Nutrients_Supplements`
            FOREIGN KEY (`Supplements_id`)
            REFERENCES `{config['database']}`.`Supplements` (`Supplements_id`)
            ON DELETE NO ACTION
            ON UPDATE NO ACTION,
        CONSTRAINT `fk_Supplements_has_Nutrients_Nutrients1`
            FOREIGN KEY (`Nutrients_id`)
            REFERENCES `{config['database']}`.`Nutrients` (`Nutrients_id`)
            ON DELETE NO ACTION
            ON UPDATE NO ACTION)
        ENGINE = InnoDB;


        -- -----------------------------------------------------
        -- Table `{config['database']}`.`Medical_conditions_has_Nutrients`
        -- -----------------------------------------------------
        CREATE TABLE IF NOT EXISTS `{config['database']}`.`Medical_conditions_has_Nutrients` (
        `Medical_conditions_id` VARCHAR(45) NOT NULL,
        `Nutrients_id` INT NOT NULL,
        PRIMARY KEY (`Medical_conditions_id`, `Nutrients_id`),
        INDEX `fk_Medical_conditions_has_Nutrients_Nutrients1_idx` (`Nutrients_id` ASC) VISIBLE,
        INDEX `fk_Medical_conditions_has_Nutrients_Medical_conditions1_idx` (`Medical_conditions_id` ASC) VISIBLE,
        CONSTRAINT `fk_Medical_conditions_has_Nutrients_Medical_conditions1`
            FOREIGN KEY (`Medical_conditions_id`)
            REFERENCES `{config['database']}`.`Medical_conditions` (`Medical_conditions_id`)
            ON DELETE NO ACTION
            ON UPDATE NO ACTION,
        CONSTRAINT `fk_Medical_conditions_has_Nutrients_Nutrients1`
            FOREIGN KEY (`Nutrients_id`)
            REFERENCES `{config['database']}`.`Nutrients` (`Nutrients_id`)
            ON DELETE NO ACTION
            ON UPDATE NO ACTION)
        ENGINE = InnoDB;


        -- -----------------------------------------------------
        -- Table `{config['database']}`.`Reference_charts`
        -- -----------------------------------------------------
        CREATE TABLE IF NOT EXISTS `{config['database']}`.`Reference_charts` (
        `Reference_charts_id` INT NOT NULL,
        `name` VARCHAR(45) NOT NULL,
        `chart` JSON NOT NULL,
        `Medical_conditions_id` VARCHAR(45) NOT NULL,
        PRIMARY KEY (`Reference_charts_id`),
        INDEX `fk_Reference_charts_Medical_conditions1_idx` (`Medical_conditions_id` ASC) VISIBLE,
        CONSTRAINT `fk_Reference_charts_Medical_conditions1`
            FOREIGN KEY (`Medical_conditions_id`)
            REFERENCES `{config['database']}`.`Medical_conditions` (`Medical_conditions_id`)
            ON DELETE NO ACTION
            ON UPDATE NO ACTION)
        ENGINE = InnoDB;


        -- -----------------------------------------------------
        -- Table `{config['database']}`.`Reports`
        -- -----------------------------------------------------
        CREATE TABLE IF NOT EXISTS `{config['database']}`.`Reports` (
        `Reports_id` INT NOT NULL,
        `MRN` INT NOT NULL,
        `date` TIMESTAMP NOT NULL,
        `report` JSON NOT NULL,
        PRIMARY KEY (`Reports_id`),
        INDEX `fk_Reports_Patients1_idx` (`MRN` ASC) VISIBLE,
        CONSTRAINT `fk_Reports_Patients1`
            FOREIGN KEY (`MRN`)
            REFERENCES `{config['database']}`.`Patients` (`MRN`)
            ON DELETE NO ACTION
            ON UPDATE NO ACTION)
        ENGINE = InnoDB;


        -- -----------------------------------------------------
        -- Table `{config['database']}`.`Medications`
        -- -----------------------------------------------------
        CREATE TABLE IF NOT EXISTS `{config['database']}`.`Medications` (
        `Medications_id` INT NOT NULL,
        `name` VARCHAR(45) NOT NULL,
        PRIMARY KEY (`Medications_id`))
        ENGINE = InnoDB;


        -- -----------------------------------------------------
        -- Table `{config['database']}`.`Patients_has_Medications`
        -- -----------------------------------------------------
        CREATE TABLE IF NOT EXISTS `{config['database']}`.`Patients_has_Medications` (
        `Medications_id` INT NOT NULL,
        `MRN` INT NOT NULL,
        `dosage` VARCHAR(45) NOT NULL,
        `notes` VARCHAR(300) NULL,
        PRIMARY KEY (`Medications_id`, `MRN`),
        INDEX `fk_Medications_has_Patients_Patients1_idx` (`MRN` ASC) VISIBLE,
        INDEX `fk_Medications_has_Patients_Medications1_idx` (`Medications_id` ASC) VISIBLE,
        CONSTRAINT `fk_Medications_has_Patients_Medications1`
            FOREIGN KEY (`Medications_id`)
            REFERENCES `{config['database']}`.`Medications` (`Medications_id`)
            ON DELETE NO ACTION
            ON UPDATE NO ACTION,
        CONSTRAINT `fk_Medications_has_Patients_Patients1`
            FOREIGN KEY (`MRN`)
            REFERENCES `{config['database']}`.`Patients` (`MRN`)
            ON DELETE NO ACTION
            ON UPDATE NO ACTION)
        ENGINE = InnoDB;


        SET SQL_MODE=@OLD_SQL_MODE;
        SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
        SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
        """
        )
    cnx.commit()
    cnx.close()

def start_database(config):
    """
    Starts the database. Requires the server be started.

    * Parameters:
           * config: dict
    * Returns: 
           * cnx - the connection to the database
    """

    cnx = None

    # start database
    try:
        cnx = mysql.connector.connect(**config)
        print("Success")
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            user_input = input("Database does not exist. Create new? (y/n): ")
            if user_input[:1].lower() == "y":
                create_new_database(cnx)
                print("Creating database")
            else:
                print(":(")
        else:
            print(str(err) + "000")
    else:
        return cnx

def commit_db_changes(cnx):
    """
    Commits changes to the database.

    * Parameters:
           * cnx - the connection to the database
    * Returns: none
    """
    user_input = input("Are you sure you want to commit these changes? (y/n):")
    if user_input[:1].lower() == "y":
        cnx.commit()
        print("Changes committed.")
    else:
        print("Not committed.")

def close_database(cnx):
    """
    Closes the connection to the database.

    * Parameters:
           * cnx - the connection to the database
    * Returns: none
    """
    # close connection to database
    """
    user_input = input("Are you sure you want to close the database? (y/n):")
    if user_input[:1].lower() == "y":
        cnx.close()
        print("Database closed.")
    else:
        print("The database remains open.")
    """
    
    cnx.close()

# Database login -------------------------
def configure_login():
    """
    Builds the config.py file, containing login information for the database.
    """
    pass
    #TODO

def load_config():
    """
    Loads login information from config.json
    * Parameters: none
    * Returns: 
           * config: dict
    """

    with open('config.json') as json_file:
        config = json.load(json_file)
    
    return config

# CRUD functions ------------------------
def create(cnx, table_name: str, content: dict):
    """
    CRUD function. Creates a new entry in a table.
    * Parameters:
           * cnx - the connection to the database
           * table_name: str 
           * content: dict - contains the column names as keys, and the column content as values.
    * Returns: none
    """

    # define query
    col_names, col_values = dict_to_strings_Create(content)

    query = (f"""
        INSERT INTO {table_name} {col_names} 
        VALUES {col_values}
        """)
    
    # cursor
    #print(query)
    cursor1 = cnx.cursor()
    cursor1.execute(query)
    commit_db_changes(cnx)

def read(cnx, table_name:str, select:str = "*", where:str = "*"):
    """
    CRUD function. Returns a table's contents
    * Parameters:
           * cnx - the connection to the database
           * table_name: str 
           * select: str - the MySQL SELECT statement
           * where: str - the MySQL WHERE statement
    * Returns: 
           * DataFrame - the result of the query
    """
    query = (f"""
        SELECT 
             {select}
        FROM 
             {table_name}
        """)
    
    # add where statement if relevant
    if where != "*":
        query = query + f"WHERE {where}"
    
    query = query + ";"

    # return
    query_result = pd.read_sql(query, cnx)
    return query_result

def update(cnx, table_name: str, id: int, content: dict):
    """
    CRUD function. Updates an entry in a table.
    * Parameters:
           * cnx - the connection to the database
           * table_name: str 
           * id: int - the id of the entry to update (The primary key, the "{table_name}_id" value)
           * content: dict - the values to replace. Dict keys are column names, dict values are the replacement values.
    * Returns: none
    """
    # check for empty table
    if id == -1:
        return
    
    # convert dict to string
    set_statement = dict_to_string_Update(content)

    # define query
    query = (f"""
        UPDATE {table_name} 
        SET {set_statement} 
        WHERE {table_name}_id = {id};
        """)
    
    # cursor
    #print(query)
    cursor1 = cnx.cursor()
    cursor1.execute(query)
    commit_db_changes(cnx)

def delete(cnx, table_name: str, id: int):
    """
    CRUD function. Deletes an entry in a table.
    * Parameters:
           * cnx - the connection to the database
           * table_name: str 
           * id: int - the id of the entry to delete (The primary key, the "{table_name}_id" value)
    * Returns: none
    """
    # check for empty table
    if id == -1:
        return

    # define query
    query = (f"""
        DELETE FROM {table_name} 
        WHERE {table_name}_id = {id};
        """)
    
    # cursor
    #print(query)
    cursor1 = cnx.cursor()
    cursor1.execute(query)
    commit_db_changes(cnx)

# Supporting functions ------------------------------
def get_table_names(cnx, config):
    """
    Gets the table names, excluding connective tables.

    * Parameters:
           * cnx - the connection to the database
           * config - login information
    * Returns: 
           * DataFrame - the result of the query
    """

    # define query
    query = (f"""
        SELECT 
             table_name
        FROM 
             information_schema.tables
        WHERE 
             table_schema = '{config['database']}'
             AND table_name NOT LIKE "%has%";
        """)
    
    # query the database
    warnings.filterwarnings('ignore')

    query_result = pd.read_sql(query, cnx)
    return query_result

def get_table_names_interface(cnx, config):
    """
    Guides the user through finding table content

    * Parameters:
           * cnx - the connection to the database
           * config - login information
    * Returns: 
           * DataFrame - the table contents
    """
    table_names = get_table_names(cnx, config)
                
    # display table names
    for table_index in table_names.index:
        print(str(table_index+1) + ": " + str(table_names['TABLE_NAME'][table_index]))
                
    # choose a table to view
    print()
    num_tables = len(table_names)
    user_input = input(f"There are {num_tables} tables. Which one do you want to access? (1-{num_tables}): ")
                
    try:
        user_input = int(user_input)-1
        user_input >= 0
        user_input <= num_tables-1
    except:
        print("Invalid input.")
        return 0

    # show table contents
    return table_names['TABLE_NAME'][user_input]

def get_table_items_interface(cnx, table_name):
    """
    Guides the user through selecting an item from a table

    * Parameters:
           * cnx - the connection to the database
           * table_name: str 
    * Returns: 
           * int - the primary key for the item
    """
    warnings.filterwarnings('ignore')
    
    # get table content
    table_content = read(cnx, table_name)

    if table_content.empty:
        print("Table is empty")
        return -1

    # display table names
    print(f"Contents of {table_name} table:")
    for item_index in table_content.index:
        print(str(table_content[f'{table_name}_id'][item_index]) + ": " + str(table_content[f'name'][item_index]))
                
    # choose a table to view
    print()
    num_items = len(table_content)
    user_input = input(f"There are {num_items} items. Which one do you want to access? (Enter id): ")
                
    try:
        user_input = int(user_input)
        user_input in table_content[f'{table_name}_id']
    except:
        print("Invalid input.")
        return 0

    # return the chosen index
    return user_input

def dict_to_strings_Create(content: dict):
    """
    Converts a dict into two strings, containing the keys and values. Makes it easier to insert content into queries.
    * Parameters:
           * content: dict - contains the column names as keys, and the column content as values.
    * Returns: 
           * col_names: str - dict key values in format "(name1, name2, name3)"
           * col_values: str - dict values in format "(item1, item2, item3)"
    """
    col_names = "("
    col_values = "("

    # fill strings
    for key in content:
        col_names = col_names + key + ", "

        if isinstance(content[key], str):
            col_values = col_values + "'" + content[key] + "', "
        else:
            col_values = col_values + str(content[key]) + ", "

    # get rid of comma+space at end of strings
    col_names = col_names[:-2]
    col_values = col_values[:-2]

    # add closing parentheses 
    col_names = col_names + ")"
    col_values = col_values + ")"

    # return
    return col_names, col_values

def dict_to_string_Update(content: dict):
    """
    Converts a dict into a string for the SET in an Update statement.
    * Parameters:
           * content: dict - contains the column names as keys, and the column content as values.
    * Returns: 
           * str - format "key1 = value1, key2 = value2" etc.
    """
    final_str = ""

    # fill strings
    for key in content:
        # add key
        final_str = final_str + key + " = "

        # add value
        if isinstance(content[key], str):
            final_str = final_str + "'" + content[key] + "', "
        else:
            final_str = final_str + str(content[key]) + ", "

    # get rid of comma+space at end of strings
    final_str = final_str[:-2]

    # return
    return final_str