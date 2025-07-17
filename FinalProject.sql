CREATE DATABASE CarRentalSystem;
USE CarRentalSystem;


CREATE TABLE Customer (
    CustomerID INT AUTO_INCREMENT PRIMARY KEY,
    Name VARCHAR(100),
    Phone VARCHAR(15),
    Email VARCHAR(100),
    LicenseNumber VARCHAR(50) UNIQUE
);

CREATE TABLE Vehicle (
    VehicleID INT AUTO_INCREMENT PRIMARY KEY,
    Make VARCHAR(50),
    Model VARCHAR(50),
    Year INT,
    PlateNumber VARCHAR(20) UNIQUE,
    Status VARCHAR(20) DEFAULT 'Available'
);

CREATE TABLE Rental (
    RentalID INT AUTO_INCREMENT PRIMARY KEY,
    CustomerID INT,
    VehicleID INT,
    StartDate DATE,
    EndDate DATE,
    TotalCost DECIMAL(10,2),
    FOREIGN KEY (CustomerID) REFERENCES Customer(CustomerID),
    FOREIGN KEY (VehicleID) REFERENCES Vehicle(VehicleID)
);

CREATE TABLE Payment (
    PaymentID INT AUTO_INCREMENT PRIMARY KEY,
    RentalID INT,
    Amount DECIMAL(10,2),
    PaymentDate DATE,
    PaymentMethod VARCHAR(20),
    FOREIGN KEY (RentalID) REFERENCES Rental(RentalID)
);



INSERT INTO Customer (Name, Phone, Email, LicenseNumber)
VALUES ('Alice Johnson', '909-111-2222', 'alice.johnson@example.com', 'DLX00123'),
('Brian Smith', '909-222-3333', 'brian.smith@example.com', 'DLX00456'),
('Catherine Lee', '909-333-4444', 'catherine.lee@example.com', 'DLX00789'),
('David Kim', '909-444-5555', 'david.kim@example.com', 'DLX01112'),
('Emily Chen', '909-555-6666', 'emily.chen@example.com', 'DLX01567');





insert into Vehicle (Make, Model, Year, PlateNumber)
values ('Mitsubishi', 'Lancer', 2013, '6HT745D'),
('Toyota', 'Camry', 2020, '7AB123C'),
('Honda', 'Civic', 2022, '9XY456Z'),
('Ford', 'Escape', 2019, '8ZT789X'),
('Nissan', 'Altima', 2014, '67548GHF'),
('Subaru', 'WRX', 2016, 'M656BFXZ'),
('Toyota', 'RAV4', 2021, '8TY324X'),
('Honda', 'Accord', 2020, '7PL983K'),
('Chevrolet', 'Malibu', 2019, '5ZN287J'),
('Ford', 'Explorer', 2022, '9FG623L'),
('Hyundai', 'Elantra', 2018, '4QM562C'),
('Kia', 'Sorento', 2020, '3LS785N'),
('BMW', 'X5', 2023, '1BW009X'),
('Mercedes-Benz', 'C-Class', 2022, '2MB834T'),
('Tesla', 'Model 3', 2023, '0TS789E');







