--@block
-- PostgreSQL syntax to list databases
SELECT datname FROM pg_database;
--@block
-- PostgreSQL syntax for creating database (remove IF NOT EXISTS)
CREATE DATABASE Employees;