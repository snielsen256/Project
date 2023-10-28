"""
db_interface.py
Holds all the functions for interfacing with the database
"""

import mysql.connector
from mysql.connector import errorcode
from config import config
"""
Config should be in the format:
    config = {
    'user': '',
    'password': '',
    'host': 'localhost',
    'database': 'supplicore',
    'raise_on_warnings': True
    }
"""

# General -----------------------------
def create_new_database(config):
    """
    Creates a new database
    Parameters:
        * config: dict
    Returns: none
    """
    # Make sure that MySQL is installed
    pass

    # define database
    cnx = start_database(**config)
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
    cnx.close()
    
    
    
    
def start_database(config):
    """
    Establishes a connection to the database.

    Parameters:
        * config: dict
    Returns: 
        * cnx - the connection to the database
    """

    try:
        cnx = mysql.connector.connect(**config)
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print(err)
    else:
        cnx.close()
    
    return cnx
    
def close_database(cnx):
    cnx.close()

# Reports -----------------------------
def create_new_report():
    pass
    
def edit_reports(report):
    pass
    
def view_reports(report):
    pass

# Patients ----------------------------    
def create_new_patient():
    pass
    
def edit_patients(patient):
    pass

# Nutrients ---------------------------
def create_new_nutrient():
    pass
    
def edit_nutrients(nutrient):
    pass

# Supplements -------------------------    
def create_new_supplement():
    pass
    
def edit_supplements(supplement):
    pass

# Medications -------------------------    
def create_new_medication():
    pass
    
def edit_medications(medication):
    pass

# Reference charts --------------------    
def create_new_ref_chart():
    pass
    
def edit_ref_charts(ref_chart):
    pass
    