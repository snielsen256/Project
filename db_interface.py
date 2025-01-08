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
from tkinter import messagebox

# from sqlalchemy import create_engine # imported in start_database
# from sqlalchemy.exc import SQLAlchemyError, OperationalError # imported in start_database
# from GUI import show_db_error_popup # imported in start_database
# import logging # imported in start_database


# General ----------------------------
def raw_sql(cnx, query: str):
    """
    Runs a raw SQL query on the database.

    Parameters:
        cnx: The database connection object.
        query (str): The SQL query to execute.

    Returns:
        DataFrame: The result of the query.

    Raises:
        ValueError: If the database connection is not available.
    """
    if not cnx:
        raise ValueError("Database connection is not available.")

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
    Initializes and connects to the database using the provided configuration.

    Parameters:
        config (dict): The database configuration dictionary.

    Returns:
        Engine: SQLAlchemy engine object for the database connection.

    Logs:
        Connection success or failure details.
    """
    from sqlalchemy import create_engine
    from sqlalchemy.exc import SQLAlchemyError, OperationalError
    from GUI import show_db_error_popup
    import logging
    logging.basicConfig()
    logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)

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
        if "Access denied" in str(err):
            show_db_error_popup("access_denied")
        elif "Unknown database" in str(err):
            user_choice = show_db_error_popup("unknown_db")
            if user_choice:
                create_new_database(config)
                print("Creating database")
            else:
                print("Database creation cancelled")
        else:
            show_db_error_popup("generic", err)

    except SQLAlchemyError as err:
        show_db_error_popup("generic", err)

    return cnx

def commit_db_changes(cnx, parent_window):
    """
    Prompts the user to confirm and commit database changes.

    Parameters:
        cnx: The database connection object.
        parent_window: The parent window for the confirmation dialog.

    Returns:
        bool: True if the changes were committed, False otherwise.

    Raises:
        ValueError: If the database connection is not available.
    """
    if not cnx:
        raise ValueError("Database connection is not available. Cannot commit changes.")

    from GUI import confirm_commit_popup
    confirm = confirm_commit_popup(parent_window)

    if confirm:
        try:
            if isinstance(cnx, Session):
                cnx.commit()
                print("Changes successfully committed via session.")
            else:
                with cnx.connect() as connection:
                    connection.commit()
                print("Changes successfully committed via raw connection.")
            return True
        except Exception as e:
            print(f"Error committing changes: {e}")
            raise
    else:
        print("Commit cancelled by the user.")
        return False


def close_database(cnx):
    """
    Closes the database connection if it exists.

    Parameters:
        cnx: The database connection object.

    Logs:
        A message indicating whether the connection was closed or absent.
    """
    if not cnx:
        print("No active database connection to close.")
        return

    cnx.dispose()
    print("Database connection closed.")

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
    try:
        with open('config.json') as json_file:
            config = json.load(json_file)
    except:
        config = None
        print("No config file detected")
    
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
    """
    Inserts a new entry into the specified table.

    Parameters:
        cnx: The database connection object.
        parent_window: The parent window for confirmation dialogs.
        table_name (str): The name of the table.
        content (dict): The data to insert as a dictionary.

    Raises:
        ValueError: If the database connection is not available.
        Exception: If the insertion fails.
    """
    if not cnx:
        raise ValueError("Database connection is not available. Cannot create entries.")

    col_names = ", ".join(f"`{col}`" for col in content.keys())
    placeholders = ", ".join([f":{col}" for col in content.keys()])

    query = text(f"""
        INSERT INTO {table_name} ({col_names}) 
        VALUES ({placeholders})
    """)

    try:
        with cnx.connect() as connection:
            print(f"Executing query: {query}")
            print(f"With data: {content}")
            connection.execute(query, content)
            connection.commit()
            commit_db_changes(cnx, parent_window)
            print("Entry successfully inserted.")
    except Exception as e:
        print(f"Error during create function: {e}")
        messagebox.showerror("Database Error", f"An error occurred while inserting the entry: {str(e)}")
        raise

def read(cnx, table_name: str, select: str = "*", where: str = "*"):
    """
    Reads data from the specified table.

    Parameters:
        cnx: The database connection object.
        table_name (str): The name of the table.
        select (str): The SELECT clause (default: all columns).
        where (str): The WHERE clause (default: no condition).

    Returns:
        DataFrame: The result of the query.

    Raises:
        ValueError: If the database connection is not available.
    """
    if not cnx:
        raise ValueError("Database connection is not available. Cannot read entries.")

    warnings.filterwarnings('ignore')

    query = (f"""
        SELECT 
             {select}
        FROM 
             {table_name}
        """)

    if where != "*":
        query += f"WHERE {where}"

    query += ";"

    with cnx.connect() as connection:
        query_result = pd.read_sql(query, connection)
    return query_result


def update(cnx, parent_window, table_name: str, id: int, content: dict):
    """
    Updates an entry in the specified table.

    Parameters:
        cnx: The database connection object.
        parent_window: The parent window for confirmation dialogs.
        table_name (str): The name of the table.
        id (int): The ID of the entry to update.
        content (dict): The updated data.

    Raises:
        ValueError: If the database connection is not available or invalid ID.
        Exception: If the update operation fails.
    """
    if not cnx:
        raise ValueError("Database connection is not available. Cannot update entries.")

    p_key_name = get_primary_key(cnx, table_name)
    if not p_key_name or id == -1:
        raise ValueError("Invalid table or ID provided for update.")

    set_statement = dict_to_string_Update(content)

    query = text(f"""
        UPDATE {table_name} 
        SET {set_statement} 
        WHERE {p_key_name} = :id
    """)

    try:
        with cnx.connect() as connection:
            connection.execution_options(isolation_level="AUTOCOMMIT")
            print(f"Executing query: {query}, with ID: {id} and content: {content}")
            connection.execute(query, {"id": id})
            connection.commit()
            print(f"Entry with ID {id} updated successfully in table {table_name}.")
    except Exception as e:
        print(f"Error during update operation: {e}")
        raise

def delete(cnx, parent_window, table_name: str, entry_id: int, primary_key: str):
    """
    Deletes an entry from the specified table.

    Parameters:
        cnx: The database connection object.
        parent_window: The parent window for confirmation dialogs.
        table_name (str): The name of the table.
        entry_id (int): The ID of the entry to delete.
        primary_key (str): The primary key column name.

    Raises:
        ValueError: If the database connection is not available or entry does not exist.
        Exception: If the deletion operation fails.
    """
    if not cnx:
        raise ValueError("Database connection is not available. Cannot delete entries.")

    delete_query = text(f"""
        DELETE FROM {table_name} 
        WHERE {primary_key} = :entry_id;
    """)

    try:
        with cnx.connect() as connection:
            connection.execution_options(isolation_level="AUTOCOMMIT")
            print(f"Executing DELETE query: {delete_query}, Parameters: {{entry_id: {entry_id}}}")
            result = connection.execute(delete_query, {"entry_id": entry_id})

            if result.rowcount == 0:
                raise ValueError(f"Entry with ID {entry_id} does not exist in {table_name}.")

            if commit_db_changes(cnx, parent_window):
                print(f"Entry {entry_id} successfully deleted from {table_name}.")
                messagebox.showinfo("Success", f"Entry with ID {entry_id} deleted successfully.")
    except Exception as e:
        print(f"Error during delete operation: {e}")
        messagebox.showerror("Error", f"Failed to delete entry: {str(e)}")



# Supporting functions ------------------------------
def get_table_names(cnx, config):
    """
    Retrieves the names of tables in the database.

    Parameters:
        cnx: The database connection object.
        config (dict): The database configuration dictionary.

    Returns:
        DataFrame: A DataFrame containing the table names.

    Raises:
        ValueError: If the database connection is not available.
    """
    if not cnx:
        raise ValueError("Database connection is not available. Cannot retrieve table names.")

    query = (f"""
        SELECT 
             table_name
        FROM 
             information_schema.tables
        WHERE 
             table_schema = '{config['database']}'
             AND table_name NOT LIKE "%has%";
        """)

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