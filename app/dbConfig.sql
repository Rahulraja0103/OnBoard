CREATE DATABASE onBoard;

USE onBoard

CREATE TABLE users (
    userId INT AUTO_INCREMENT PRIMARY KEY,
    firstname VARCHAR(100) NOT NULL,
    lastname VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL,
    _password VARCHAR(100) NOT NULL,
    phone_number VARCHAR(20) NOT NULL,
    _location VARCHAR(100),
    skills VARCHAR(100),
    workPermitNumber VARCHAR(100),
    SIN VARCHAR(20),
    _availability VARCHAR(100),
    registration_date DATE 
);

CREATE TABLE company (
    companyId INT AUTO_INCREMENT PRIMARY KEY,
    comp_name VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL,
    _password VARCHAR(100) NOT NULL,
    phone_number VARCHAR(20) NOT NULL,
    _location VARCHAR(100),
    industry VARCHAR(100),
    _description TEXT,
    registration_date DATE 
);

CREATE TABLE company_shifts (
    shift_id INT AUTO_INCREMENT PRIMARY KEY,
    companyId INT NOT NULL,
    shift_date DATE NOT NULL,
    shift_type VARCHAR(100),
    start_time TIME NOT NULL,
    end_time TIME NOT NULL,
    department_name VARCHAR(100),
    supervisor_name VARCHAR(100),
    num_workers INTEGER,
    notes TEXT,
    FOREIGN KEY (companyId) REFERENCES company(companyId)
);

CREATE TABLE bookedShift (
    booking_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    shift_id INT NOT NULL,
    booking_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users (userId),
    FOREIGN KEY (shift_id) REFERENCES company_shifts (shift_id)
);

CREATE TABLE shiftStatus (
    statusId INT AUTO_INCREMENT PRIMARY KEY,
    statusName VARCHAR(255) NOT NULL
);

CREATE TABLE paymentStatus (
    statusId INT AUTO_INCREMENT PRIMARY KEY,
    statusName VARCHAR(255) NOT NULL
);

ALTER TABLE company_shifts
ADD COLUMN shiftStatus_Id INT,
ADD CONSTRAINT fk_shift_status
FOREIGN KEY (shiftStatus_Id) REFERENCES shiftStatus(statusId);

ALTER TABLE bookedShift
ADD COLUMN paymentStatus_Id INT,
ADD CONSTRAINT fk_payment_status
FOREIGN KEY (paymentStatus_Id) REFERENCES paymentStatus(statusId);

ALTER TABLE company_shifts
ADD COLUMN pay_rate FLOAT

CREATE TABLE logs (
    id INT AUTO_INCREMENT PRIMARY KEY,
    timestamp DATETIME NOT NULL,
    message TEXT
);

CREATE TABLE feedbacl (
    feedbackid INT AUTO_INCREMENT PRIMARY KEY,
    Username VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL,
    feedback VARCHAR(255) NOT NULL
);











