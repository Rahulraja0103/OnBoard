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


