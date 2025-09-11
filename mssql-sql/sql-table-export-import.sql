select name 
from sys.tables where type = 'U'


drop table secExpense;


select name 
from sys.databases 

-- create test_db if not exist 
IF NOT EXISTS (SELECT * FROM sys.databases WHERE name = 'test_db')
BEGIN
    CREATE DATABASE test_db
END


USE test_db



-- Create a new database
-- create test_db if not exist 
IF NOT EXISTS (SELECT * FROM sys.databases WHERE name = 'test_db')
BEGIN
    CREATE DATABASE test_db
END



-- Switch to the new database
USE test_db;


-- Create Employees table
IF NOT EXISTS (CREATE TABLE Employees (
    EmployeeID INT PRIMARY KEY,
    FirstName NVARCHAR(50),
    LastName NVARCHAR(50),
    Department NVARCHAR(50),
    HireDate DATE
);


-- Insert some test data
INSERT INTO Employees (EmployeeID, FirstName, LastName, Department, HireDate)
VALUES
(1, 'Alice', 'Smith', 'HR', '2020-01-15'),
(2, 'Bob', 'Johnson', 'IT', '2019-06-01'),
(3, 'Carol', 'Williams', 'Finance', '2021-03-20'),
(4, 'David', 'Brown', 'IT', '2018-11-11');


