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
        user_input = input("1) Exit 2) Create 3) Read 4) Update 5) Delete 6) Generate report: ")
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
                returned = read(cnx, get_table_names_interface(cnx, config), where=f"{test_tablename}_id = 5")
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
            case 6:
                generate_report()
            case _:
                # else
                print("Invalid input.")
                continue


    # close database
    close_database(cnx)
    print("Database closed")

    # end program
    print("TERMINATED")
    
def generate_report():
    """
    creates a report
    * Parameters:none
    * Returns: 
           * report: json
    """
    report = {
        "header": {
            "name": "",
            "sex": "",
            "DOB": "",
            "age": 0.0,
            "weight_kg": 0.0,
            "current_date": "",
            "feeding_schedule": "",
            "method_of_delivery": "",
            "home_recipe": "",
            "fluids": "",
            "solids": ""
        },
        "food_and_supplements": {
            "": 0.0,
            "total_formula_only": 0.0,
            "total_food_and_formula": 0.0,
        },
        "calculations": {
            "Holliday-Segar": {
                "maintenance": 0.0,
                "sick_day": 0.0
            },
            "WHO_REE": 0.0
        }
    }

    # TODO import patient data

    # calculate Holliday-Segar formula
    hs = 0.0
    weight = report["header"]["weight_kg"]

    if weight <= 10.0:
        hs = weight * 100.0
    elif weight <= 20.0:
        hs = 1000 + (50 * (weight - 10))
    else:
        hs = 1500 + (20 * (weight - 20))

    report["calculations"]["Holliday-Segar"]["maintenance"] = hs
    report["calculations"]["Holliday-Segar"]["sick_day"] = hs * 1.5

    # calculate WHO REE formula
    sex = report["header"]["sex"]
    age = report["header"]["age"]
    wr = 0.0

    if sex == "M":
        if age <= 3:
            wr = (weight * 60.9) - 54
        elif age <= 10:
            wr = (weight * 22.7) + 495
        else:
            wr = (weight * 17.5) + 651
    elif sex == "F":
        if age <= 3:
            wr = (weight * 60.1) - 51
        elif age <= 10:
            wr = (weight * 22.5) + 499
        else:
            wr = (weight * 12.2) + 746
    else:
        print(f"Unknown sex '{sex}'")
    
    report["calculations"]["WHO_REE"] = wr
    


if __name__ == '__main__':
    main()