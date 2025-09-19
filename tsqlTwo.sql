-- sp for creating table and insertig value 

create or alter  procedure dbo.sp_create_table_and_insert_value
as
begin
    create table dbo.Test (
        CustomerID int primary key,
        Name nvarchar(100)
    );

    insert into dbo.Test values (1, 'John Doe');
    insert into dbo.Test values (2, 'Jane Doe');
end

exec dbo.sp_create_table_and_insert_value

-- Multiple INPUT parameters
CREATE OR ALTER PROCEDURE CreateUser
    @first_name VARCHAR(50),         -- Required INPUT parameter
    @last_name VARCHAR(50),          -- Required INPUT parameter  
    @email VARCHAR(100),             -- Required INPUT parameter
    @age INT = 18,                   -- Optional INPUT parameter with default
    @is_active BIT = 1               -- Optional INPUT parameter with default
AS
BEGIN
    INSERT INTO Users (FirstName, LastName, Email, Age, IsActive)
    VALUES (@first_name, @last_name, @email, @age, @is_active)
END

-- Test with all parameters
EXEC CreateUser @first_name = 'John', @last_name = 'Doe', @email = 'john@email.com', @age = 25;

-- Test with defaults (age and is_active will use default values)
EXEC CreateUser @first_name = 'Jane', @last_name = 'Smith', @email = 'jane@email.com';



  select top (10) * from secExpense.sec.candidateRegister

select top (10) * 
from secExpense.sec.mobile_token_master 
order by * desc



/*markdown
info


*/

sp_help 'secExpense.sec.mobile_token_master'