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
