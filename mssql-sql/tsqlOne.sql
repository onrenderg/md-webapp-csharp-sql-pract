-- select name from sys.databases
-- select name from sys.tables

    -- check all schemas in db
-- select name from sys.schemas

    -- create table in schema dbo
-- create table dbo.test (id int)
-- insert into dbo.test values (1)
-- select * from dbo.test

    -- check all tables in schema dbo
-- select name from sys.tables where schema_id = (select schema_id from sys.schemas where name = 'dbo')

    
 




    -- create schema test
-- create schema test

    -- create table test.test (id int primary key, name varchar(255))
-- create table test.test (id int primary key, name varchar(255))
-- insert into test.test values (1, 'one')
-- insert into test.test values (2, 'two')
-- insert into test.test values (3, 'three')
-- insert into test.test values (4, 'four')
-- insert into test.test values (5, 'five')
-- insert into test.test values (6, 'six')
-- insert into test.test values (7, 'seven')
-- insert into test.test values (8, 'eight')
-- insert into test.test values (9, 'nine')

-- select * from test.test



/*markdown
Let’s say you have two tables:

Customers (CustomerID, Name)

Orders (OrderID, CustomerID, Amount)

And you want to show all customers along with their orders, even if they haven’t placed any orders (using a LEFT JOIN).
*/



-- Create the Customers table
CREATE TABLE Customers (
    CustomerID INT PRIMARY KEY,
    Name NVARCHAR(100)
);

-- Create the Orders table
CREATE TABLE Orders (
    OrderID INT PRIMARY KEY,
    CustomerID INT,
    Amount DECIMAL(10, 2),
    FOREIGN KEY (CustomerID) REFERENCES Customers(CustomerID)
);


-- Insert some sample data into Customers
INSERT INTO Customers (CustomerID, Name)
VALUES
    (1, 'Alice'),
    (2, 'Bob'),
    (3, 'Charlie');

-- Insert some sample data into Orders
INSERT INTO Orders (OrderID, CustomerID, Amount)
VALUES
    (101, 1, 250.00),
    (102, 2, 180.50);


select * from dbo.Customers

select * from dbo.Orders

create or alter procedure dbo.tst_one
as 

begin
    select 
        c.CustomerID,
        c.Name,
        o.OrderID,
        o.Amount
    from 
        Customers c
    left join 
        Orders o on c.CustomerID = o.CustomerID;
end



exec dbo.tst_one

/*markdown
"Show all customers along with their orders, even if they haven’t placed any orders."

But here's the key point:

That description — "show all customers, even if they haven’t placed any orders" — is best achieved using a LEFT JOIN (from Customers to Orders), not a RIGHT JOIN.
*/

create or alter procedure dbo.tst_one
as 

begin
    select 
        c.CustomerID,
        c.Name,
        o.OrderID,
        o.Amount
    from 
        Customers c
    right join 
        Orders o on c.CustomerID = o.CustomerID;
end



exec dbo.tst_one



