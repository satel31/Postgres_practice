import json

import psycopg2

from config import config


def main():
    script_file = 'fill_db.sql'
    json_file = 'suppliers.json'
    db_name = 'my_new_db'

    params = config()
    conn = None

    create_database(params, db_name)
    print(f"БД {db_name} успешно создана")

    params.update({'dbname': db_name})
    try:
        with psycopg2.connect(**params) as conn:
            with conn.cursor() as cur:
                execute_sql_script(cur, script_file)
                print(f"БД {db_name} успешно заполнена")

                create_suppliers_table(cur)
                print("Таблица suppliers успешно создана")

                suppliers = get_suppliers_data(json_file)
                insert_suppliers_data(cur, suppliers)
                print("Данные в suppliers успешно добавлены")

                add_foreign_keys(cur, json_file)
                print(f"FOREIGN KEY успешно добавлены")

    except(Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()


def create_database(params, db_name) -> None:
    """Создает новую базу данных."""
    conn = psycopg2.connect(dbname='postgres', **params)
    conn.autocommit = True
    cur = conn.cursor()

    cur.execute(f"DROP DATABASE {db_name}")
    cur.execute(f"CREATE DATABASE {db_name}")

    conn.close()


def execute_sql_script(cur, script_file) -> None:
    """Выполняет скрипт из файла для заполнения БД данными."""
    with open(script_file, 'r') as f:
        cur.execute(f.read())


def create_suppliers_table(cur) -> None:
    """Создает таблицу suppliers."""
    cur.execute("""
                CREATE TABLE suppliers (
                    supplier_id SERIAL PRIMARY KEY,
                    company_name VARCHAR(255) NOT NULL,
                    contact VARCHAR(255) NOT NULL,
                    address VARCHAR(255) NOT NULL,
                    phone VARCHAR(100) NOT NULL,
                    fax VARCHAR(100),
                    homepage VARCHAR(255),
                    product_name TEXT
                )
            """)


def get_suppliers_data(json_file: str) -> list[dict]:
    """Извлекает данные о поставщиках из JSON-файла и возвращает список словарей с соответствующей информацией."""
    with open(json_file, 'r', encoding='UTF-8') as f:
        text = f.read()
    return json.loads(text)


def insert_suppliers_data(cur, suppliers: list[dict]) -> None:
    """Добавляет данные из suppliers в таблицу suppliers."""
    for supplier in suppliers:
        cur.execute(
            f"""
                INSERT INTO suppliers (company_name, contact, address, phone, fax, homepage, product_name)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                """,
            (supplier['company_name'], supplier['contact'], supplier['address'],
             supplier['phone'], supplier['fax'], supplier['homepage'], supplier['products'])
        )


def add_foreign_keys(cur, json_file) -> None:
    """Добавляет foreign key со ссылкой на supplier_id в таблицу products."""
    with open(json_file, 'r', encoding='UTF-8') as f:
        text = f.read()
    data = json.loads(text)
    cur.execute("""ALTER TABLE products ADD COLUMN supplier_id INT""")
    for d in range(1, len(data)+1):
        cur.execute(f"""UPDATE products SET supplier_id= CASE WHEN product_name IN(product_name FROM suppliers) THEN {d} END""")
    cur.execute("""ALTER TABLE products ADD CONSTRAINT fk_products_suppliers FOREIGN KEY (supplier_id) REFERENCES suppliers(supplier_id)""")


if __name__ == '__main__':
    main()
