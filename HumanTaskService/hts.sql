SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='TRADITIONAL,ALLOW_INVALID_DATES';

CREATE SCHEMA IF NOT EXISTS `HumanTaskService` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci ;
USE `HumanTaskService` ;

-- -----------------------------------------------------
-- Table `HumanTaskService`.`Applications`
-- -----------------------------------------------------
CREATE  TABLE IF NOT EXISTS `HumanTaskService`.`Applications` (
  `id` INT UNSIGNED NOT NULL AUTO_INCREMENT ,
  `OwnerUserId` INT NOT NULL ,
  `Name` VARCHAR(50) NOT NULL ,
  `Description` TEXT NULL ,
  `TaskCopies` INT UNSIGNED NOT NULL DEFAULT 1 ,
  `TaskScheduler` INT UNSIGNED NOT NULL DEFAULT 1 ,
  `MagicNumber` VARCHAR(36),
  PRIMARY KEY (`id`) ,
  UNIQUE INDEX `Name_UNIQUE` (`Name` ASC),
  UNIQUE INDEX `Magic_UNIQUE` (`MagicNumber` ASC) )
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `HumanTaskService`.`Users`
-- -----------------------------------------------------
CREATE  TABLE IF NOT EXISTS `HumanTaskService`.`Users` (
  `id` INT UNSIGNED NOT NULL AUTO_INCREMENT ,
  `ExternalId` VARCHAR(100) NULL ,
  `CreationDate` DATETIME NOT NULL ,
  `LastLogin` VARCHAR(45) NOT NULL ,
  PRIMARY KEY (`id`) )
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `HumanTaskService`.`Tasks`
-- -----------------------------------------------------
CREATE  TABLE IF NOT EXISTS `HumanTaskService`.`Tasks` (
  `id` INT UNSIGNED NOT NULL AUTO_INCREMENT ,
  `ApplicationId` INT UNSIGNED NOT NULL ,
  `Params` TEXT NOT NULL ,
  `Copies` INT UNSIGNED NOT NULL DEFAULT 1 ,
  PRIMARY KEY (`id`) )
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `HumanTaskService`.`TaskResults`
-- -----------------------------------------------------
CREATE  TABLE IF NOT EXISTS `HumanTaskService`.`TaskResults` (
  `id` INT UNSIGNED NOT NULL AUTO_INCREMENT ,
  `UserId` INT NULL ,
  `Result` TEXT NULL ,
  `FinishDate` DATETIME NOT NULL ,
  `ApplicationId` INT UNSIGNED NOT NULL ,
  `TaskId` INT UNSIGNED NULL ,
  PRIMARY KEY (`id`) )
ENGINE = InnoDB;

USE `HumanTaskService` ;

-- -----------------------------------------------------
-- INDEXES
-- -----------------------------------------------------
ALTER TABLE `HumanTaskService`.`Applications` ADD INDEX IDX_OWNUSER(`OwnerUserId`);
ALTER TABLE `HumanTaskService`.`Users` ADD INDEX IDX_EXTERNALID(`ExternalId`);
ALTER TABLE `HumanTaskService`.`Tasks` ADD INDEX IDX_APPID(`ApplicationId`);
ALTER TABLE `HumanTaskService`.`TaskResults` ADD INDEX IDX_TASKRESULTUSERID(`UserId`);
ALTER TABLE `HumanTaskService`.`TaskResults` ADD INDEX IDX_TASKRESULTAPPID(`ApplicationId`);

SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
