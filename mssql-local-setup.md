Server=localhost\SQLEXPRESS;Database=master;Trusted_Connection=True;

sqlcmd -S ROYAL-NIC-6F\SQLEXPRESS -E


ip: ROYAL-NIC-6F\SQLEXPRESS  : pcname\instancename

✅ Step 3: Enable the sa Account and Set a Password

Back in sqlcmd, execute:

ALTER LOGIN sa ENABLE;
GO
ALTER LOGIN sa WITH PASSWORD = 'YourStrongPasswordHere';
GO


Replace 'YourStrongPasswordHere' with a strong password (SQL Server enforces strong password policies by default).




✅ Step 4: Test sa Login

Now you can test sqlcmd using SQL Authentication:

sqlcmd -S ROYAL-NIC-6F\SQLEXPRESS -U sa -P YourStrongPasswordHere


# Import 

# CERS Database Import Commands for Local SQL Server

## Local SQL Server Connection
**Instance**: `ROYAL-NIC-6F\SQLEXPRESS`
**Authentication**: SQL Server Authentication (sa account)
**Connection String**: `sqlcmd -S ROYAL-NIC-6F\SQLEXPRESS -U sa -P YourStrongPasswordHere`

---

## Database Setup

### Create Database and Schemas
```sql
-- Create main database
sqlcmd -S ROYAL-NIC-6F\SQLEXPRESS -U sa -P YourStrongPasswordHere -Q "CREATE DATABASE secExpense;"

-- Create sec schema in secExpense database
sqlcmd -S ROYAL-NIC-6F\SQLEXPRESS -U sa -P YourStrongPasswordHere -d secExpense -Q "CREATE SCHEMA sec;"


# Static port ip 


SQLServerManager15.msc

net stop MSSQL$SQLEXPRESS
net start MSSQL$SQLEXPRESS




ip 10.146.2.78
port 1433 
usrn: sa
pass: YourStrongPasswordHere

mssql://sa:YourStrongPassword@ROYAL-NIC-6F/SQLEXPRESS?encrypt=true&trustServerCertificate=true

