--
-- Запросы для выдачи данных из БД
--

--
-- Вывести список всех компаний и количество вакансий у каждой компании
--
SELECT employer_id, employer_name, site_url, open_vacancies
FROM employers
ORDER BY open_vacancies DESC;

--
-- Вывести список всех вакансий с указанием названия компании
--

SELECT vacancy_id, vacancy_name, city, salary, currency, employer_name, employment, url, published_at
FROM vacancies
JOIN employers USING (employer_id)
ORDER BY salary DESC, city;

--
-- Вывести среднюю зарплату по вакансиям
--

SELECT ROUND(AVG(salary))
FROM vacancies
WHERE salary <> 0;

--
-- Вывести список всех вакансий, у которых зарплата выше средней по всем вакансиям
--

SELECT vacancy_id, vacancy_name, city, salary, currency, employer_name, employment, url, published_at
FROM vacancies
JOIN employers USING (employer_id)
WHERE salary > (
    SELECT AVG(salary)
    FROM vacancies
    WHERE salary <> 0)
ORDER BY salary DESC;

--
-- Вывести список всех вакансий, в названии которых содержится указанное слово, например 'python'
--

SELECT vacancy_id, vacancy_name, city, salary, currency, employer_name, employment, url, published_at
FROM vacancies
JOIN employers USING (employer_id)
WHERE vacancy_name LIKE '%placeholder%'
ORDER BY salary DESC;