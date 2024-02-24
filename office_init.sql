DROP TABLE IF EXISTS User;
DROP TABLE IF EXISTS Lunch;
DROP TABLE IF EXISTS Company;

CREATE TABLE Company (
    id INT NOT NULL AUTO_INCREMENT,
    PRIMARY KEY (id),
    name VARCHAR(255) NOT NULL,
    employees_count INT DEFAULT 0,
    code VARCHAR(255) NOT NULL
);

CREATE TABLE Lunch (
    id INT NOT NULL AUTO_INCREMENT,
    PRIMARY KEY (id),
    name VARCHAR(255) NOT NULL,
    votes_count INT NOT NULL DEFAULT 1,
    company_id INT NOT NULL,
    FOREIGN KEY (company_id) REFERENCES Company(id)
);

CREATE TABLE User (
    id INT NOT NULL AUTO_INCREMENT,
    PRIMARY KEY (id),
    name VARCHAR(255) NOT NULL,
    chat_id VARCHAR(255) NOT NULL,
    present BOOLEAN NOT NULL DEFAULT False,
    lunch_id INT,
    company_id INT NOT NULL,
    FOREIGN KEY (lunch_id) REFERENCES Lunch(id),
    FOREIGN KEY (company_id) REFERENCES Company(id)
);

DESCRIBE Company;
DESCRIBE Lunch;
DESCRIBE User;
