-- Create test_db if it doesn't exist 
IF NOT EXISTS (SELECT * FROM sys.databases WHERE name = 'test_db')
BEGIN
    CREATE DATABASE test_db
END
GO

-- Switch to the new database
USE test_db
GO

-- Check what tables exist
SELECT name 
FROM sys.tables WHERE type = 'U'
GO

-- Create Employees table if it doesn't exist
IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'Employees')
BEGIN
    CREATE TABLE Employees (
        EmployeeID INT PRIMARY KEY,
        FirstName NVARCHAR(50),
        LastName NVARCHAR(50),
        Department NVARCHAR(50),
        HireDate DATE
    )
END
GO

-- Insert some test data (only if table is empty)
IF (SELECT COUNT(*) FROM Employees) = 0
BEGIN
    INSERT INTO Employees (EmployeeID, FirstName, LastName, Department, HireDate)
    VALUES
    (1, 'Alice', 'Smith', 'HR', '2020-01-15'),
    (2, 'Bob', 'Johnson', 'IT', '2019-06-01'),
    (3, 'Carol', 'Williams', 'Finance', '2021-03-20'),
    (4, 'David', 'Brown', 'IT', '2018-11-11')
END
GO

-- Display all employees
SELECT * FROM Employees
GO

-- Display table information
SELECT 
    TABLE_NAME,
    COLUMN_NAME,
    DATA_TYPE,
    IS_NULLABLE
FROM INFORMATION_SCHEMA.COLUMNS 
WHERE TABLE_NAME = 'Employees'
ORDER BY ORDINAL_POSITION
GO