import csv

import psycopg2

"""Скрипт для заполнения данными таблиц в БД Postgres."""
#Пароль не указан для безопасности =)
PASSWORD = ''

#Connection with PostgreSQL
conn = psycopg2.connect(host='localhost', database='north', user='postgres', password=PASSWORD)

try:
    with conn:
        #Insert data to employees table
        with conn.cursor() as cur:
            with open('north_data/employees_data.csv', encoding='UTF-8') as f:
                file_dict = csv.DictReader(f, delimiter=',')
                for id, line in enumerate(file_dict, 1):
                    cur.execute('INSERT INTO employees VALUES (%s, %s, %s, %s, %s, %s)',
                                (id, line['first_name'], line['last_name'], line['title'], line['birth_date'], line['notes']))
        cur.close()
        print('Данные успешно добавлены в таблицу Employees')

        # Insert data to customers table
        with conn.cursor() as cur:
            with open('north_data/customers_data.csv', encoding='UTF-8') as f:
                file_dict = csv.DictReader(f, delimiter=',')
                for line in file_dict:
                    cur.execute('INSERT INTO customers VALUES (%s, %s, %s)',
                                (line['customer_id'], line['company_name'], line['contact_name']))
        cur.close()
        print('Данные успешно добавлены в таблицу Customers')

        # Insert data to orders table
        with conn.cursor() as cur:
            with open('north_data/orders_data.csv', encoding='UTF-8') as f:
                file_dict = csv.DictReader(f, delimiter=',')
                for line in file_dict:
                    cur.execute('INSERT INTO orders VALUES (%s, %s, %s, %s, %s)',
                                (line['order_id'], line['customer_id'], line['employee_id'], line['order_date'], line['ship_city']))
        cur.close()
        print('Данные успешно добавлены в таблицу Orders')

finally:
    #Close connection
    conn.close()
