CREATE TABLE IF NOT EXISTS employers (
    employer_id INTEGER PRIMARY KEY,
    employer_name VARCHAR(255) NOT NULL,
    site_url TEXT,
    open_vacancies INTEGER
);

CREATE TABLE IF NOT EXISTS vacancies (
    vacancy_id INTEGER PRIMARY KEY,
    vacancy_name VARCHAR(255) NOT NULL,
    city VARCHAR(50),
    salary INTEGER,
    currency VARCHAR(5),
    employer_id INTEGER NOT NULL,
    employment VARCHAR(30),
    experience VARCHAR(20),
    requirement TEXT,
    responsibility TEXT,
    url TEXT,
    address TEXT,
    published_at DATE,

    CONSTRAINT fk_vacancies_employer_id FOREIGN KEY(employer_id) REFERENCES employers(employer_id)
);