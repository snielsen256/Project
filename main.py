"""
SuppliCore - Nutrition and Supplement Database Manager
Stephen Nielsen
10/6/2023


# install mysql connector
$> pip install mysql-connector-python
$> pip install mysql-connector-python --upgrade


"""
from db_interface import *

test_tablename = "Supplements"
test_dict = {"name":"triopenin", "kcal":100.0, "displacement":50.0, "notes":"Not for human consumption"}
test_dict_2 = {"name":"canopenin", "kcal":1000.0, "displacement":5.0, "notes":"Totally safe for human consumption bro"}


def main():
    # Load config (login information)
    config = load_config()
    print("Config loaded")

    # start database
    cnx = start_database(config)
    print("Database started")
    
    # user choice
    in_main_loop = True
    while in_main_loop:
        # user input
        print("--------------------")
        print("What would you like to do?")
        user_input = input("1) Exit 2) Create 3) Read 4) Update 5) Delete: ")
        print()
        try:
            user_input = int(user_input)
        except:
            print("Invalid input.")
            continue
        
        # choice
        match user_input:
            case 1:
                #if exit
                print("Exiting")
                in_main_loop = False
                break
            case 2:
                # if create
                create(cnx, test_tablename, test_dict)
            case 3:
                # if read
                returned = read(cnx, get_table_names_interface(cnx, config))
                if returned.empty:
                    print("Table is empty")
                else:
                    print(returned)
            case 4:
                # if update
                update(cnx, test_tablename, get_table_items_interface(cnx, test_tablename), test_dict_2)
            case 5:
                # if delete
                delete(cnx, test_tablename, get_table_items_interface(cnx, test_tablename))
                #print(get_table_items_interface(cnx, test_tablename))
            case _:
                # else
                print("Invalid input.")
                continue


    # close database
    close_database(cnx)
    print("Database closed")

    # end program
    print("TERMINATED")
    



if __name__ == '__main__':
    main()