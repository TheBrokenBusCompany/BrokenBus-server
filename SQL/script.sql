-- MySQL Script generated by MySQL Workbench
-- Mon Nov  4 18:42:53 2019
-- Model: New Model    Version: 1.0
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
-- Table `mydb`.`Usuario`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`Usuario` (
  `idUsuario` INT NOT NULL AUTO_INCREMENT,
  `email` VARCHAR(45) NULL,
  `username` VARCHAR(45) NULL,
  PRIMARY KEY (`idUsuario`),
  UNIQUE INDEX `idUsuario_UNIQUE` (`idUsuario` ASC) VISIBLE)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`entidadEMT`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`entidadEMT` (
  `idEntidadEMT` INT NOT NULL,
  PRIMARY KEY (`idEntidadEMT`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`Comentario`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`Comentario` (
  `Usuario_idUsuario` INT NOT NULL,
  `comentable_idEntidadEMT` INT NOT NULL,
  `texto` VARCHAR(250) NULL,
  `imagen` VARCHAR(250) NULL,
  INDEX `fk_Comentario_Usuario_idx` (`Usuario_idUsuario` ASC) VISIBLE,
  PRIMARY KEY (`Usuario_idUsuario`, `comentable_idEntidadEMT`),
  INDEX `fk_Comentario_entidadEMT1_idx` (`comentable_idEntidadEMT` ASC) VISIBLE,
  CONSTRAINT `fk_Comentario_Usuario`
    FOREIGN KEY (`Usuario_idUsuario`)
    REFERENCES `mydb`.`Usuario` (`idUsuario`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_Comentario_entidadEMT1`
    FOREIGN KEY (`comentable_idEntidadEMT`)
    REFERENCES `mydb`.`entidadEMT` (`idEntidadEMT`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`Parada`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`Parada` (
  `entidadEMT_idEntidadEMT` INT NOT NULL,
  INDEX `fk_Parada_entidadEMT1_idx` (`entidadEMT_idEntidadEMT` ASC) VISIBLE,
  PRIMARY KEY (`entidadEMT_idEntidadEMT`),
  CONSTRAINT `fk_Parada_entidadEMT1`
    FOREIGN KEY (`entidadEMT_idEntidadEMT`)
    REFERENCES `mydb`.`entidadEMT` (`idEntidadEMT`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`Autobus`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`Autobus` (
  `entidadEMT_idEntidadEMT` INT NOT NULL,
  INDEX `fk_Autobus_entidadEMT1_idx` (`entidadEMT_idEntidadEMT` ASC) VISIBLE,
  PRIMARY KEY (`entidadEMT_idEntidadEMT`),
  CONSTRAINT `fk_Autobus_entidadEMT1`
    FOREIGN KEY (`entidadEMT_idEntidadEMT`)
    REFERENCES `mydb`.`entidadEMT` (`idEntidadEMT`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
