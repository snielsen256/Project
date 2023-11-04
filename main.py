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
        print()
        print("What would you like to do?")
        user_input = input("1) Exit 2) Create 3) Read: ")
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
                pass
            case 3:
                # if read
                table_name = content_interface(cnx, config)
                try:
                    table_name != 0
                except:
                    continue
                else:
                    print(read(cnx, table_name))
                    #print(read(cnx, content))
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