"""
SuppliCore - Nutrition and Supplement Database Manager
Stephen Nielsen
10/6/2023


# install mysql connector
$> pip install mysql-connector-python
$> pip install mysql-connector-python --upgrade


"""
from db_interface import *


def main():
    
    print("Check 1")
    # Load config (login information)
    config = load_config()
    print("Check 2")

    # start database, create if not exists
    """
    create_new_database(config)
    print("Check 2.5")
    """
    cnx = start_database(config)
    print("Check 3")

    close_database(cnx)

    print("TERMINATED")
    



if __name__ == '__main__':
    main()