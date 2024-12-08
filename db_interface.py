"""
db_interface.py
Holds all the functions for interfacing with the database
"""

# from GUI import confirm_commit_popup # imported in commit_db_changes
from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError, OperationalError
from sqlalchemy.orm import Session
import pymysql
import json
import pandas as pd
import warnings
# from sqlalchemy import create_engine # imported in start_database
# from sqlalchemy.exc import SQLAlchemyError, OperationalError # imported in start_database
# from GUI import show_db_error_popup # imported in start_database
# import logging # imported in start_database


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
    with cnx.connect() as connection:
        query_result = pd.read_sql(query, connection)
    
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

    #TODO

    # define database
    # cnx = mysql.connector.connect(**config)
    # cursor1 = cnx.cursor()
    # cursor1.execute(
    #     f"""
    #     """
    #     )
    # cnx.commit()
    # cnx.close()

def start_database(config):
    """
    Starts the database. Requires the server be started.

    * Parameters:
           * config: dict
    * Returns: 
           * cnx: the connection to the database
    """
    from sqlalchemy import create_engine
    from sqlalchemy.exc import SQLAlchemyError, OperationalError
    from GUI import show_db_error_popup
    import logging
    logging.basicConfig()
    logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)

    cnx = None

    try:
        # Extract database credentials and connection info
        user = config['user']
        password = config['password']
        host = config['host']
        database = config['database']
        port = int(config.get('port', 3306))  # Ensure port is integer

        # Create the SQLAlchemy engine (connection to the database)
        cnx = create_engine(f"mysql+pymysql://{user}:{password}@{host}:{port}/{database}")
        print("Successfully connected to the database")
        return cnx
    
    except OperationalError as err:
        # Handle specific SQLAlchemy OperationalErrors
        if "Access denied" in str(err):
            show_db_error_popup("access_denied")
        elif "Unknown database" in str(err):
            user_choice = show_db_error_popup("unknown_db")
            if user_choice:
                create_new_database(config)  # Use config, not cnx, since cnx is None
                print("Creating database")
            else:
                print("Database creation cancelled")
        else:
            show_db_error_popup("generic", err)
    
    except SQLAlchemyError as err:
        # Generic SQLAlchemy error handling
        show_db_error_popup("generic", err)
    
    return cnx

def commit_db_changes(cnx, parent_window):
    """
    Prompts the user to confirm committing database changes and commits them if confirmed.

    * Parameters:
        * cnx - the connection to the database (raw connection or session)
        * parent_window - the parent of the popup window
    * Returns: bool - True if committed, False otherwise
    """
    from GUI import confirm_commit_popup

    # Call the confirmation popup function
    confirm = confirm_commit_popup(parent_window)

    if confirm:
        try:
            if isinstance(cnx, Session):
                # Commit using SQLAlchemy session
                cnx.commit()
                print("Changes successfully committed via session.")
            else:
                # Commit using raw connection
                with cnx.connect() as connection:
                    connection.commit()
                print("Changes successfully committed via raw connection.")
            return True
        except Exception as e:
            print(f"Error committing changes: {e}")
            raise
    else:
        # User cancels commit
        print("Commit cancelled by the user.")
        return False


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
    
    if cnx:
        cnx.dispose()

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

def update_config(settings):
    """
    Loads settings into config.json, replacing existing values
    * Parameters: 
        * settings: dict of values (such as str and int, not fields such as tk entry)
    * Returns: none
    """

    settings["raise_on_warnings"] = True

    json_settings = json.dumps(settings, indent=1)

    with open('config.json', "w") as json_file:
        json_file.write(json_settings)

# CRUD functions ------------------------   
def create(cnx, parent_window, table_name: str, content: dict):
    col_names = ", ".join(f"`{col}`" for col in content.keys())
    placeholders = ", ".join([f":{col}" for col in content.keys()])

    query = text(f"""
        INSERT INTO {table_name} ({col_names}) 
        VALUES ({placeholders})
    """)

    try:
        with cnx.connect() as connection:
            # Debugging: Print query and content
            print(f"Executing query: {query}")
            print(f"With data: {content}")
            
            # Execute the insert query
            connection.execute(query, content)
            
            # Manually commit the transaction
            connection.commit()
            
            # Proceed with commit confirmation
            commit_db_changes(cnx, parent_window)
            print("Entry successfully inserted.")
    except Exception as e:
        print(f"Error during create function: {e}")
        messagebox.showerror("Database Error", f"An error occurred while inserting the entry: {str(e)}")
        raise

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
    warnings.filterwarnings('ignore')
    
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
    with cnx.connect() as connection:
        query_result = pd.read_sql(query, connection)
    return query_result

def update(cnx, parent_window, table_name: str, id: int, content: dict):
    """
    CRUD function. Updates an entry in a table.
    * Parameters:
           * cnx - the connection to the database
           * parent_window: The GUI window, passed to commit_db_changes
           * table_name: str 
           * id: int - the id of the entry to update (The primary key, the "{table_name}_id" value)
           * content: dict - the values to replace. Dict keys are column names, dict values are the replacement values.
    * Returns: none
    """
    # determine the name of the primary key
    p_key_name = f'{table_name}_id'

    if table_name == "Patients":
        p_key_name = "MRN"

    # check for empty table
    if id == -1:
        return
    
    # convert dict to string
    set_statement = dict_to_string_Update(content)

    # define query
    query = (f"""
        UPDATE {table_name} 
        SET {set_statement} 
        WHERE {p_key_name} = {id};
        """)
    
    # cursor
    #print(query)
    with cnx.connect() as connection:
        connection.execute(query)
    commit_db_changes(cnx, parent_window)

from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError

from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from tkinter import messagebox

from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from tkinter import messagebox

from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from tkinter import messagebox

def delete(cnx, parent_window, table_name: str, entry_id: int, primary_key: str):
    delete_query = text(f"""
        DELETE FROM {table_name} 
        WHERE {primary_key} = :entry_id;
    """)

    verify_query = text(f"""
        SELECT 1 FROM {table_name} 
        WHERE {primary_key} = :entry_id;
    """)

    try:
        with cnx.connect() as connection:
            connection.execution_options(isolation_level="AUTOCOMMIT")  # Ensure immediate commit

            # Debugging: Log queries and parameters
            print(f"Executing DELETE query: {delete_query}, Parameters: {{entry_id: {entry_id}}}")
            result = connection.execute(delete_query, {"entry_id": entry_id})
            print(f"Rows affected by DELETE: {result.rowcount}")

            if result.rowcount == 0:
                raise ValueError(f"Entry with ID {entry_id} does not exist in {table_name}.")

            # Verify deletion
            print(f"Executing VERIFY query: {verify_query}, Parameters: {{entry_id: {entry_id}}}")
            verify_result = connection.execute(verify_query, {"entry_id": entry_id}).fetchone()
            print(f"Verification result: {verify_result}")

            if verify_result is None:
                # Successful deletion
                if commit_db_changes(cnx, parent_window):
                    print(f"Entry {entry_id} successfully deleted from {table_name}.")
                    messagebox.showinfo("Success", f"Entry with ID {entry_id} deleted successfully.")
                else:
                    print("Deletion not committed by user.")
            else:
                raise ValueError(f"Failed to delete entry with ID {entry_id} from {table_name}.")

    except Exception as e:
        print(f"Error during delete operation: {e}")
        messagebox.showerror("Error", f"Failed to delete entry: {str(e)}")


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
    with cnx.connect() as connection:
        query_result = pd.read_sql(query, connection)
    return query_result

def get_table_names_interface(cnx, config):
    """
    Guides the user through finding table content

    * Parameters:
           * cnx - the connection to the database
           * config - login information
    * Returns: 
           * str - the table name
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
    Guides the user through selecting an item from a table.
    Made to be used with get_table_names_interface()

    * Parameters:
           * cnx - the connection to the database
           * table_name: str (can get this with get_table_names_interface())
    * Returns: 
           * int - the primary key for the item
    """
    warnings.filterwarnings('ignore')

    # determine the name of the primary key
    p_key_name = f'{table_name}_id'

    if table_name == "Patients":
        p_key_name = "MRN"
    
    # get table content
    table_content = read(cnx, table_name)

    if table_content.empty:
        print("Table is empty")
        return -1

    # display items
    print(f"Contents of {table_name} table:")
    for item_index in table_content.index:
        print(str(table_content.loc[[item_index]]))
                
    # choose an item to view
    print()
    num_items = len(table_content)
    user_input = input(f"There are {num_items} items. Which one do you want to access? (Enter id): ")

    # make sure the user input is one of the primary keys          
    try:
        user_input = int(user_input)
        result = table_content[f'{p_key_name}'][user_input]
    except:
        print("Invalid input.")
        return 0
    
    # return the primary key
    return result

def fill_table_interface(cnx, table_name: str):
    """
    Walks the user through filling an entry for a table.
    * Parameters:
           * cnx - the connection to the database
           * table_name: str 
    * Returns: 
           * dict - The content of the entry
    """

    data = read(cnx, table_name)
    # TODO
    
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

def get_primary_key(cnx, table_name):
    """
    Returns the primary key column name for a given table.
    """
    query = f"SHOW KEYS FROM {table_name} WHERE Key_name = 'PRIMARY'"
    with cnx.connect() as connection:
        result = pd.read_sql(query, connection)

    if not result.empty:
        return result['Column_name'].iloc[0]  # Returns the primary key column
    else:
        raise ValueError(f"No primary key found for table {table_name}")