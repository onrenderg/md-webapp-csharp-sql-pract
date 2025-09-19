
# No Argument procedure with single block 
CREATE PROCEDURE TestProcedureOne
AS 
BEGIN
	PRINT 'TestProcedureOne'
END

EXEC TestProcedureOne


# IMPLEMENTATION 1 : 
# 1 Argument procdure with single block 

##  VARCHAR + paramater  (concepts used in imp )

CREATE OR ALTER PROCEDURE TestProcedureTwo
	@TestParameter VARCHAR(11)
AS 

BEGIN
	PRINT 'Hi,' + @TestParameter + '!'
END

EXEC  TestProcedureTwo @TestParameter = 'John'


## INT /BIGINT /SMALLINT  + paramater 

CREATE OR ALTER PROCEDURE TestProcedureTwo
	@TestParameter INT
AS 

BEGIN
	PRINT 'Hi,' + CAST(@TestParameter AS VARCHAR(2)) + '!'
END

EXEC  TestProcedureTwo @TestParameter = 11






## FLOAT 

CREATE OR ALTER PROCEDURE TestProcedureTwo
    @TestParameter FLOAT
AS 
BEGIN
    PRINT 'Hi,' + CAST(@TestParameter AS VARCHAR(30)) + '!'
END

EXEC TestProcedureTwo @TestParameter = 11.123



## DECIMAL 


CREATE OR ALTER PROCEDURE ProcDecimalExample
    @Amount DECIMAL(10, 2)
AS
BEGIN
    PRINT 'Amount is: ' + CAST(@Amount AS VARCHAR(20));
END;


## CHAR(n)

CREATE OR ALTER PROCEDURE ProcCharExample
    @Code CHAR(5)
AS
BEGIN
    PRINT 'Code is: [' + @Code + ']';
END;



## TEXT

CREATE OR ALTER PROCEDURE ProcTextExample
    @Description TEXT
AS
BEGIN
    PRINT CAST(@Description AS VARCHAR(MAX));
END;




## DATE

CREATE OR ALTER PROCEDURE ProcDateExample
    @BirthDate DATE
AS
BEGIN
    PRINT 'Birth date: ' + CAST(@BirthDate AS VARCHAR(12));
END;


## TIME

CREATE OR ALTER PROCEDURE ProcTimeExample
    @MeetingTime TIME
AS
BEGIN
    PRINT 'Meeting time: ' + CAST(@MeetingTime AS VARCHAR(16));
END;


## DATETIME

CREATE OR ALTER PROCEDURE ProcDateTimeExample
    @CreatedDate DATETIME
AS
BEGIN
    PRINT 'Created at: ' + CAST(@CreatedDate AS VARCHAR(23));
END;


## BIT


CREATE OR ALTER PROCEDURE ProcBitExample
    @IsActive BIT
AS
BEGIN
    PRINT CASE WHEN @IsActive = 1 THEN 'Active' ELSE 'Inactive' END;
END;



## BINARY(n)

CREATE OR ALTER PROCEDURE ProcBinaryExample
    @BinData BINARY(4)
AS
BEGIN
    PRINT 'Binary data (hex): ' + CONVERT(VARCHAR(8), @BinData, 1);
END;


## IMAGE

CREATE OR ALTER PROCEDURE ProcImageExample
    @ImageData IMAGE
AS
BEGIN
    PRINT 'Received image data.';
END;

## UNIQUEIDENTIFIER (GUID

CREATE OR ALTER PROCEDURE ProcUniqueIdentifierExample
    @UserID UNIQUEIDENTIFIER
AS
BEGIN
    PRINT 'Received GUID: ' + CAST(@UserID AS VARCHAR(36));
END;


### Combined 

CREATE OR ALTER PROCEDURE DemoDataTypes
    @DecimalVal DECIMAL(10, 2),
    @CharVal CHAR(5),
    @TextVal VARCHAR(MAX),       -- Using VARCHAR(MAX) instead of TEXT (deprecated)
    @DateVal DATE,
    @TimeVal TIME,
    @DateTimeVal DATETIME,
    @BitVal BIT,
    @BinaryVal BINARY(4)
AS
BEGIN
    PRINT 'DECIMAL: ' + CAST(@DecimalVal AS VARCHAR(20));
    PRINT 'CHAR: [' + @CharVal + ']';
    PRINT 'TEXT (as VARCHAR(MAX)): ' + @TextVal;
    PRINT 'DATE: ' + CAST(@DateVal AS VARCHAR);
    PRINT 'TIME: ' + CAST(@TimeVal AS VARCHAR);
    PRINT 'DATETIME: ' + CAST(@DateTimeVal AS VARCHAR);
    PRINT 'BIT: ' + CASE WHEN @BitVal = 1 THEN 'True' ELSE 'False' END;
    PRINT '




# Theory 1 for concepts used 


## Numeric types:
* INT (integer numbers)
* BIGINT (large integers)
* SMALLINT (smaller integers)
* DECIMAL(p,s) / NUMERIC(p,s) (fixed precision and scale decimals)
* FLOAT (floating-point numbers)

## Character/string types:
* CHAR(n) (fixed-length strings)
* VARCHAR(n) (variable-length strings)
* TEXT (large text, deprecated—use VARCHAR(MAX))

## Unicode character/string types:
* NCHAR(n) (fixed-length Unicode strings)
* NVARCHAR(n) (variable-length Unicode strings)

## Date and time types:
* DATE (date only)
* TIME (time only)
* DATETIME (date and time)
* DATETIME2 (more precision date and time)
* SMALLDATETIME (less precision)
* DATETIMEOFFSET (date and time with timezone offset)

## Other types:
* BIT (boolean, 0 or 1)
* BINARY(n) (fixed-length binary data)
* VARBINARY(n) (variable-length binary data)
* IMAGE (large binary data, deprecated)
* UNIQUEIDENTIFIER (GUID)
* XML (XML data)
* CURSOR (cursor reference)
* TABLE (table variable type)



# Theory  2 
## When to use DECLARE?
* Use DECLARE inside the procedure when you want to create local variables, like this: Declare and assign 

DECLARE @LocalVar INT;
SET @LocalVar = 10;

# Implemetation 2 
# 


## VARCHAR + dec&assi 


CREATE OR ALTER PROCEDURE PrintLocalVarExample
AS
BEGIN
	DECLARE @Name VARCHAR(20);
	SET @Name = 'John';

	PRINT 'Hello, ' + @Name + '!';

END;

EXEC PrintLocalVarExample;

## INT   + dec&assi  
CREATE OR ALTER PROCEDURE PrintLocalVarExample
AS
BEGIN
    DECLARE @LocalVar INT;
    SET @LocalVar = 10;
    
    PRINT 'The value of LocalVar is: ' + CAST(@LocalVar AS VARCHAR(10));
END;

EXEC PrintLocalVarExample;


# Built-in Functions
## Theory concept 
* String functions — manipulate text data

* Numeric functions — work with numbers

* Date & Time functions — handle dates and times

* Conversion functions — convert between data types

* Aggregate functions — perform calculations on sets of rows (like SUM, COUNT)

* Logical functions — like ISNULL(), COALESCE()

* System functions — return info about SQL Server, sessions, etc.

## Imp


CREATE OR ALTER PROCEDURE StringFunctionsExample
    @Input VARCHAR(50)
AS
BEGIN
    PRINT 'Original Input: ' + @Input;

    -- LEN() - Length of the string
    PRINT 'Length: ' + CAST(LEN(@Input) AS VARCHAR);

    -- SUBSTRING() - Extract substring (start at 2, length 5)
    PRINT 'Substring(2,5): ' + SUBSTRING(@Input, 2, 5);

    -- REPLACE() - Replace 'a' with 'X'
    PRINT 'Replace ''a'' with ''X'': ' + REPLACE(@Input, 'a', 'X');

    -- LEFT() - First 3 characters
    PRINT 'Left 3 chars: ' + LEFT(@Input, 3);

    -- RIGHT() - Last 3 characters
    PRINT 'Right 3 chars: ' + RIGHT(@Input, 3);

    -- CHARINDEX() - Position of 'e' in string
    PRINT 'Position of ''e'': ' + CAST(CHARINDEX('e', @Input) AS VARCHAR);
END;



## ? 
*  look out for return value  of function used 


# BEGN & END BLOCK  CONTEXT PLACER 

* S


# Todo 

Next key T-SQL concepts & techniques to explore step-by-step:

Control-of-Flow Statements

IF...ELSE

WHILE loops

CASE expressions

Error Handling

TRY...CATCH

Transactions

BEGIN TRANSACTION, COMMIT, ROLLBACK

Joins and Set Operations

INNER JOIN, LEFT JOIN, UNION, etc.

Subqueries and Common Table Expressions (CTEs)

Temporary Tables and Table Variables

Aggregations & Grouping

GROUP BY, HAVING

Stored Procedure Features

Output parameters

Return codes


# Exec  Flow of sql 


SELECT e.FirstName, e.LastName  -- Step 5: Use alias here, already known
FROM Employees AS e             -- Step 1: Alias 'e' assigned here
WHERE e.Department = 'Sales';   -- Step 2: Alias used here for filtering

logical order of execution (simplified):

FROM (including JOINs and aliases)

WHERE

GROUP BY

HAVING

SELECT

ORDER BY

Start by writing the FROM clause first (even if it’s below SELECT) to remind themselves that’s where sources and aliases are defined.

Then add WHERE, then SELECT.

```md
Logical Processing Order of a SQL Query

FROM

Tables and views are identified

JOINs are processed

Aliases assigned

ON (for JOIN conditions)

Filtering happens as tables are joined

JOIN

Rows from joined tables are combined

WHERE

Rows filtered based on conditions

GROUP BY

Rows grouped into aggregates

WITH CUBE / ROLLUP (if used)

Aggregations with subtotals

HAVING

Groups filtered after aggregation

SELECT

Columns, expressions, functions evaluated

Aliases assigned for columns

DISTINCT

Duplicate rows removed if requested

ORDER BY

Final result sorted

OFFSET / FETCH

Rows paginated (skip/fetch)
```