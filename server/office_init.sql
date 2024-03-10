DROP TABLE IF EXISTS User;
DROP TABLE IF EXISTS Lunch;
DROP TABLE IF EXISTS Company;

CREATE TABLE Company (
    id VARCHAR(255) NOT NULL UNIQUE, -- секретный код компании
    PRIMARY KEY(id),
    name VARCHAR(255) NOT NULL,
    employees_count INT DEFAULT 0
);

CREATE TABLE Lunch (
    id INT NOT NULL AUTO_INCREMENT,
    PRIMARY KEY (id),
    name VARCHAR(255) NOT NULL,
    votes_count INT NOT NULL DEFAULT 1,
    company_id VARCHAR(255) NOT NULL,
    FOREIGN KEY (company_id) REFERENCES Company(id)
);

CREATE TABLE User (
    id VARCHAR(255) NOT NULL UNIQUE, -- chat_id пользователя
    PRIMARY KEY (id),
    name VARCHAR(255) NOT NULL,
    nickname VARCHAR(255),
    presence BOOLEAN NOT NULL DEFAULT False,
    lunch_id INT,
    company_id VARCHAR(255) NOT NULL,
    FOREIGN KEY (lunch_id) REFERENCES Lunch(id),
    FOREIGN KEY (company_id) REFERENCES Company(id)
);

DESCRIBE Company;
DESCRIBE Lunch;
DESCRIBE User;

INSERT INTO Company (id, name)
VALUES ('test-pass', 'test-company');

INSERT INTO Lunch (name, company_id)
VALUES ('test-lunch', 'test-pass');

INSERT INTO User (id, name, nickname, company_id)
VALUES ('12345678', 'test-user', 'test-nickname', 'test-pass')
