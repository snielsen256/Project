-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema mydb
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema mydb
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `mydb` DEFAULT CHARACTER SET utf8 ;
USE `mydb` ;

-- -----------------------------------------------------
-- Table `mydb`.`Medical_conditions`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`Medical_conditions` (
  `Medical_conditions_id` VARCHAR(45) NOT NULL,
  `name` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`Medical_conditions_id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`Supplements`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`Supplements` (
  `Supplements_id` INT NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(45) NOT NULL,
  `kcal` FLOAT NOT NULL,
  `displacement` FLOAT NULL,
  `notes` VARCHAR(300) NULL,
  PRIMARY KEY (`Supplements_id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`Nutrients`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`Nutrients` (
  `Nutrients_id` INT NOT NULL,
  `name` VARCHAR(45) NOT NULL,
  `units` ENUM("g", "mg") NOT NULL,
  `goals_chart` JSON NULL,
  PRIMARY KEY (`Nutrients_id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`Patients`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`Patients` (
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
    REFERENCES `mydb`.`Medical_conditions` (`Medical_conditions_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`Supplements_has_Nutrients`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`Supplements_has_Nutrients` (
  `Supplements_id` INT NOT NULL,
  `Nutrients_id` INT NOT NULL,
  PRIMARY KEY (`Supplements_id`, `Nutrients_id`),
  INDEX `fk_Supplements_has_Nutrients_Nutrients1_idx` (`Nutrients_id` ASC) VISIBLE,
  INDEX `fk_Supplements_has_Nutrients_Supplements_idx` (`Supplements_id` ASC) VISIBLE,
  CONSTRAINT `fk_Supplements_has_Nutrients_Supplements`
    FOREIGN KEY (`Supplements_id`)
    REFERENCES `mydb`.`Supplements` (`Supplements_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_Supplements_has_Nutrients_Nutrients1`
    FOREIGN KEY (`Nutrients_id`)
    REFERENCES `mydb`.`Nutrients` (`Nutrients_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`Medical_conditions_has_Nutrients`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`Medical_conditions_has_Nutrients` (
  `Medical_conditions_id` VARCHAR(45) NOT NULL,
  `Nutrients_id` INT NOT NULL,
  PRIMARY KEY (`Medical_conditions_id`, `Nutrients_id`),
  INDEX `fk_Medical_conditions_has_Nutrients_Nutrients1_idx` (`Nutrients_id` ASC) VISIBLE,
  INDEX `fk_Medical_conditions_has_Nutrients_Medical_conditions1_idx` (`Medical_conditions_id` ASC) VISIBLE,
  CONSTRAINT `fk_Medical_conditions_has_Nutrients_Medical_conditions1`
    FOREIGN KEY (`Medical_conditions_id`)
    REFERENCES `mydb`.`Medical_conditions` (`Medical_conditions_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_Medical_conditions_has_Nutrients_Nutrients1`
    FOREIGN KEY (`Nutrients_id`)
    REFERENCES `mydb`.`Nutrients` (`Nutrients_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`Reference_charts`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`Reference_charts` (
  `Reference_charts_id` INT NOT NULL,
  `name` VARCHAR(45) NOT NULL,
  `chart` JSON NOT NULL,
  `Medical_conditions_id` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`Reference_charts_id`),
  INDEX `fk_Reference_charts_Medical_conditions1_idx` (`Medical_conditions_id` ASC) VISIBLE,
  CONSTRAINT `fk_Reference_charts_Medical_conditions1`
    FOREIGN KEY (`Medical_conditions_id`)
    REFERENCES `mydb`.`Medical_conditions` (`Medical_conditions_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`Reports`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`Reports` (
  `Reports_id` INT NOT NULL,
  `MRN` INT NOT NULL,
  `date` TIMESTAMP NOT NULL,
  `report` JSON NOT NULL,
  PRIMARY KEY (`Reports_id`),
  INDEX `fk_Reports_Patients1_idx` (`MRN` ASC) VISIBLE,
  CONSTRAINT `fk_Reports_Patients1`
    FOREIGN KEY (`MRN`)
    REFERENCES `mydb`.`Patients` (`MRN`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`Medications`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`Medications` (
  `Medications_id` INT NOT NULL,
  `name` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`Medications_id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`Patients_has_Medications`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`Patients_has_Medications` (
  `Medications_id` INT NOT NULL,
  `MRN` INT NOT NULL,
  `dosage` VARCHAR(45) NOT NULL,
  `notes` VARCHAR(300) NULL,
  PRIMARY KEY (`Medications_id`, `MRN`),
  INDEX `fk_Medications_has_Patients_Patients1_idx` (`MRN` ASC) VISIBLE,
  INDEX `fk_Medications_has_Patients_Medications1_idx` (`Medications_id` ASC) VISIBLE,
  CONSTRAINT `fk_Medications_has_Patients_Medications1`
    FOREIGN KEY (`Medications_id`)
    REFERENCES `mydb`.`Medications` (`Medications_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_Medications_has_Patients_Patients1`
    FOREIGN KEY (`MRN`)
    REFERENCES `mydb`.`Patients` (`MRN`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
