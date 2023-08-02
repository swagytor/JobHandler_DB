import psycopg2


class DBManager:
    """
    Класс для работы с базами данных,
    и для получения информации из них
    """
    conn = None

    @classmethod
    def connect(cls, params) -> None:
        """
        Подключается к базе данных
        :param params: Информация о конфиге базы данных
        """
        cls.conn = psycopg2.connect(dbname='hh_jobs', **params)

    @classmethod
    def get_companies_and_vacancies_count(cls) -> list[...]:
        """
        Получает список всех компаний и количество вакансий у каждой компании
        """
        with cls.conn.cursor() as cur:
            cur.execute("""SELECT * FROM employers
                        ORDER BY open_vacancies DESC;""")
            data: list[...] = [['employer_id', 'employer_name', 'site_url', 'open_vacancies']] + cur.fetchall()
        return data

    @classmethod
    def get_all_vacancies(cls) -> list[...]:
        """
        Получает список всех вакансий с указанием названия компании,
        названия вакансии и зарплаты и ссылки на вакансию
        """
        with cls.conn.cursor() as cur:
            cur.execute(
                """
                SELECT vacancy_id, vacancy_name, city, salary, currency, employer_name, employment, url, published_at
                FROM vacancies
                JOIN employers USING (employer_id)
                ORDER BY salary DESC, city;
                """)

            data: list[...] = [['vacancy_id', 'vacancy_name', 'city', 'salary', 'currency',
                                'employer_name', 'employment', 'url', 'published_at']] + cur.fetchall()

        return data

    @classmethod
    def get_avg_salary(cls) -> list[...]:
        """
        Получает среднюю зарплату по вакансиям
        """
        with cls.conn.cursor() as cur:
            cur.execute(
                """
                SELECT ROUND(AVG(salary))
                FROM vacancies
                WHERE salary <> 0;
                """)
            data: list[...] = [['average_salary']] + cur.fetchall()

        return data

    @classmethod
    def get_vacancies_with_higher_salary(cls) -> list[...]:
        """
        Получает список всех вакансий, у которых зарплата выше средней по всем вакансиям
        """
        with cls.conn.cursor() as cur:
            cur.execute(
                """
                SELECT vacancy_id, vacancy_name, city, salary, currency, employer_name, employment, url, published_at
                FROM vacancies
                JOIN employers USING (employer_id)
                WHERE salary > (SELECT AVG(salary) FROM vacancies WHERE salary <> 0)
                ORDER BY salary DESC;
                """)

            data: list[...] = [['vacancy_id', 'vacancy_name', 'city', 'salary', 'currency',
                                'employer_name', 'employment', 'url', 'published_at']] + cur.fetchall()

        return data

    @classmethod
    def get_vacancies_with_keyword(cls, user_keyword: str) -> list[...]:
        """
        Получает список всех вакансий, в названии которых содержатся переданные в метод слова
        :param user_keyword: ключевое слово
        """
        with cls.conn.cursor() as cur:
            cur.execute(
                f"""
                SELECT vacancy_id, vacancy_name, city, salary, currency, employer_name, employment, url, published_at
                FROM vacancies
                JOIN employers USING (employer_id)
                WHERE LOWER(vacancy_name) LIKE '%{user_keyword}%'
                ORDER BY salary DESC; 
                """)

            data: list[...] = [['vacancy_id', 'vacancy_name', 'city', 'salary', 'currency',
                                'employer_name', 'employment', 'url', 'published_at']] + cur.fetchall()

        return data
