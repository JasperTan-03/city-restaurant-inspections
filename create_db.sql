-- 1. Create the database and switch to it
CREATE DATABASE IF NOT EXISTS restaurant_inspections;
USE restaurant_inspections;

-- 2. Lookup / supporting tables

CREATE TABLE Cuisine (
  CuisineID        INT AUTO_INCREMENT PRIMARY KEY,
  CuisineDescription VARCHAR(100)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE InspectionType (
  InspectionTypeID INT AUTO_INCREMENT PRIMARY KEY,
  TypeName         VARCHAR(100),
  Description      VARCHAR(100)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE Action (
  ActionID         INT AUTO_INCREMENT PRIMARY KEY,
  ActionDescription VARCHAR(255)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE Facility (
  FacilityID       INT AUTO_INCREMENT PRIMARY KEY,
  LicenseNumber    VARCHAR(50),
  FacilityType     VARCHAR(100),
  Risk             VARCHAR(50)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 3. Address table

CREATE TABLE Address (
  AddressID        INT AUTO_INCREMENT PRIMARY KEY,
  AddressLine1     VARCHAR(255)   NOT NULL,
  ZipCode          VARCHAR(20)    NOT NULL,
  Borough          VARCHAR(50),
  City             VARCHAR(100)   NOT NULL,
  State            VARCHAR(50)    NOT NULL,
  CommunityBoard   VARCHAR(50),
  CouncilDistrict  VARCHAR(50),
  CensusTract      VARCHAR(50),
  BIN              VARCHAR(50),
  BBL              VARCHAR(50),
  NTA              VARCHAR(50),
  Latitude         DOUBLE,
  Longitude        DOUBLE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 4. Core entity: Restaurant

CREATE TABLE Restaurant (
  RestaurantID     INT AUTO_INCREMENT PRIMARY KEY,
  ExternalID       VARCHAR(50),
  DBA_Name         VARCHAR(255)   NOT NULL,
  AKA_Name         VARCHAR(255),
  Phone            VARCHAR(50),
  CuisineID        INT,
  FacilityID       INT,
  AddressID        INT           NOT NULL,
  FOREIGN KEY (CuisineID)  REFERENCES Cuisine(CuisineID),
  FOREIGN KEY (FacilityID) REFERENCES Facility(FacilityID),
  FOREIGN KEY (AddressID)  REFERENCES Address(AddressID)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 5. Inspections

CREATE TABLE Inspection (
  InspectionID        INT AUTO_INCREMENT PRIMARY KEY,
  RestaurantID        INT           NOT NULL,
  ExternalInspectionID VARCHAR(50),
  InspectionTypeID    INT           NOT NULL,
  InspectionDate      DATETIME      NOT NULL,
  Score               INT,
  Grade               VARCHAR(5),
  GradeDate           DATETIME,
  RecordDate          DATETIME,
  ActionID            INT,
  Results             VARCHAR(100),
  FOREIGN KEY (RestaurantID)     REFERENCES Restaurant(RestaurantID),
  FOREIGN KEY (InspectionTypeID) REFERENCES InspectionType(InspectionTypeID),
  FOREIGN KEY (ActionID)         REFERENCES Action(ActionID)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 6. Violations

CREATE TABLE Violation (
  ViolationID        INT AUTO_INCREMENT PRIMARY KEY,
  InspectionID       INT,
  ViolationCode      VARCHAR(50),
  ViolationDescription TEXT,
  CriticalFlag       VARCHAR(50),
  ViolationText      TEXT,
  FOREIGN KEY (InspectionID) REFERENCES Inspection(InspectionID)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
