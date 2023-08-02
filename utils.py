from configparser import ConfigParser
from classes.dbmanager import DBManager


def config(filename: str = "database.ini", section: str = "postgresql") -> dict:
    """
    Возвращает информацию о базе данных из .ini файла
    :param filename:
    :param section:
    """
    # create a parser
    parser = ConfigParser()
    # read config file
    parser.read(filename)
    db: dict = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            db[param[0]] = param[1]
    else:
        raise Exception(
            'Section {0} is not found in the {1} file.'.format(section, filename))
    return db


def get_vacancies(params: dict) -> None | list[...]:
    """
    :param params: Информация о конфиге базы данных
    :return: Результат запроса пользователя
    """
    DBManager.connect(params)

    while True:
        user_input: str = input('Что вас интересует?\n'
                                '1. Показать все вакансии\n'
                                '2. Показать информацию о работодателях\n'
                                'и количестве активных вакансий\n'
                                '3. Показать среднюю зарплату по вакансиям\n'
                                '4. Показать вакансии с зарплатами выше средней\n'
                                '5. Показать вакансии по ключевому слову\n'
                                '0. Выход\n'
                                )

        if user_input == '0':
            return

        elif user_input == '1':
            return DBManager.get_all_vacancies()

        elif user_input == '2':
            return DBManager.get_companies_and_vacancies_count()

        elif user_input == '3':
            return DBManager.get_avg_salary()

        elif user_input == '4':
            return DBManager.get_vacancies_with_higher_salary()

        elif user_input == '5':
            user_keyword = input('Введите ключевое слово: ').strip().lower()
            return DBManager.get_vacancies_with_keyword(user_keyword)
        else:
            print('Неизвестная команда, повторите запрос!')
