import psycopg2


class DBManager:
    conn = None

    @classmethod
    def connect(cls, params):
        cls.conn = psycopg2.connect(dbname='hh_jobs', **params)

    @classmethod
    def get_companies_and_vacancies_count(cls):
        with cls.conn.cursor() as cur:
            cur.execute("""SELECT * FROM employers
                        ORDER BY open_vacancies DESC;""")
            data = [['employer_id', 'employer_name', 'site_url', 'open_vacancies']] + cur.fetchall()
        return data

    @classmethod
    def get_all_vacancies(cls):
        with cls.conn.cursor() as cur:
            cur.execute(
                """
                SELECT vacancy_id, vacancy_name, city, salary, currency, employer_name, employment, url, published_at
                FROM vacancies
                JOIN employers USING (employer_id)
                ORDER BY salary DESC, city;
                """)

            data = [['vacancy_id', 'vacancy_name', 'city', 'salary', 'currency',
                     'employer_name', 'employment', 'url', 'published_at']] + cur.fetchall()

        return data

    @classmethod
    def get_avg_salary(cls):
        with cls.conn.cursor() as cur:
            cur.execute(
                """
                SELECT ROUND(AVG(salary))
                FROM vacancies
                WHERE salary <> 0;
                """)
            data = [['average_salary']] + cur.fetchall()

        return data

    @classmethod
    def get_vacancies_with_higher_salary(cls):
        with cls.conn.cursor() as cur:
            cur.execute(
                """
                SELECT vacancy_id, vacancy_name, city, salary, currency, employer_name, employment, url, published_at
                FROM vacancies
                JOIN employers USING (employer_id)
                WHERE salary > (SELECT AVG(salary) FROM vacancies WHERE salary <> 0)
                ORDER BY salary DESC;
                """)

            data = [['vacancy_id', 'vacancy_name', 'city', 'salary', 'currency',
                     'employer_name', 'employment', 'url', 'published_at']] + cur.fetchall()

        return data

    @classmethod
    def get_vacancies_with_keyword(cls, user_keyword):
        with cls.conn.cursor() as cur:
            cur.execute(
                f"""
                SELECT vacancy_id, vacancy_name, city, salary, currency, employer_name, employment, url, published_at
                FROM vacancies
                JOIN employers USING (employer_id)
                WHERE LOWER(vacancy_name) LIKE '%{user_keyword}%'
                ORDER BY salary DESC; 
                """)

            data = [['vacancy_id', 'vacancy_name', 'city', 'salary', 'currency',
                     'employer_name', 'employment', 'url', 'published_at']] + cur.fetchall()

        return data
