import psycopg2


class DBCreator:
    """
    Класс для создания БД и таблиц,
    а так же для заполнения информации в таблицы
    """

    @classmethod
    def create_database(cls, db_name: str, params: dict) -> None:
        """
        Создаёт базу данных
        :param db_name: Название базы данных
        :param params: Информация о конфиге базы данных
        """
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
    def create_tables(cls, cur, script: str) -> None:
        """
        Создаёт таблицы employers и vacancies
        :param cur: Курсор для работы с БД
        :param script: Файл, в котором находится скрипт для создания таблиц
        """
        with open(script, 'r', encoding='utf-8') as file:
            cur.execute(file.read())
        print('ТАБЛИЦЫ УСПЕШНО СОЗДАНЫ')

    @classmethod
    def insert_data(cls, employers_data: dict, cur) -> None:
        """
        Заносит данные о работодателях и вакансиях в таблицы
        :param employers_data: информация о работодателях и вакансиях
        :param cur: Курсор для работы с БД
        """
        for employer in employers_data['employers']:
            employer = list(employer.values())
            column_amount: str = ', '.join(["%s"] * len(employer))

            cur.execute(
                f"""
                INSERT INTO employers
                VALUES ({column_amount})
                """,
                employer)

        for vacancy in employers_data['items']:
            vacancy_values: list = list(vacancy.values())
            column_amount: str = ', '.join(["%s"] * len(vacancy_values))
            field_names: str = ', '.join(list(vacancy.keys()))
            updated_fields: str = ', '.join([f"{field_name} = EXCLUDED.{field_name}" for field_name in vacancy])
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
