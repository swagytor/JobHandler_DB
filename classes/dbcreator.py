import time
import psycopg2


class DBCreator:

    @classmethod
    def create_database(cls, db_name, params):
        conn = None

        try:
            conn = psycopg2.connect(dbname='postgres', **params)
            conn.autocommit = True

            cur = conn.cursor()
            cur.execute(f"DROP DATABASE IF EXISTS {db_name};")
            cur.execute(f"CREATE DATABASE {db_name};")
            print(f'БАЗА ДАННЫХ {db_name} СОЗДАНА')

        except(Exception, psycopg2.DatabaseError) as error:
            print(error)

        finally:
            if conn is not None:
                conn.close()

    @classmethod
    def create_tables(cls, cur, script):
        with open(script, 'r', encoding='utf-8') as file:
            cur.execute(file.read())
        print('ТАБЛИЦЫ УСПЕШНО СОЗДАНЫ')

    @classmethod
    def insert_data(cls, employers_data, cur):
        for employer in employers_data['employers']:
            employer = list(employer.values())
            column_amount = ', '.join(["%s"] * len(employer))

            cur.execute(
                f"""
                INSERT INTO employers
                VALUES ({column_amount})
                """,
                employer
            )

        for vacancy in employers_data['items']:
            vacancy_values = list(vacancy.values())
            column_amount = ', '.join(["%s"] * len(vacancy_values))
            field_names = ', '.join(list(vacancy.keys()))
            updated_fields = ', '.join([f"{field_name} = EXCLUDED.{field_name}" for field_name in vacancy])
            cur.execute(
                f"""
                INSERT INTO vacancies ({field_names})
                VALUES ({column_amount})
                ON CONFLICT ({list(vacancy.keys())[0]}) DO
                UPDATE SET {updated_fields}
                """,
                vacancy_values
            )
        print('ДАННЫЕ УСПЕШНО ДОБАВЛЕНЫ')
