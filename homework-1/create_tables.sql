CREATE TABLE employees
(
	employee_id serial PRIMARY KEY,
	first_name varchar(10) NOT NULL,
	last_name varchar(10) NOT NULL,
	title varchar(50) NOT NULL,
	birth_date date NOT NULL,
	notes text
);

CREATE TABLE customers
(
	customer_id varchar(5) PRIMARY KEY,
	company_name text NOT NULL,
	contact_name text
);

CREATE TABLE orders
(
	order_id serial PRIMARY KEY,
	customer_id varchar(5) REFERENCES customers(customer_id) NOT NULL,
	employee_id serial REFERENCES employees(employee_id) NOT NULL,
	order_date date NOT NULL,
	ship_city varchar(100) NOT NULL
);-- SQL-команды для создания таблиц
