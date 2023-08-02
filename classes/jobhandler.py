import json
import requests


class JobHandler:
    """
    Класс для работы с API HH.ru для добывания информации о работодателях и вакансиях
    """
    employers_info: dict[...] = {'employers': [{'employer_id': '1035394',
                                     'employer_name': 'Красное и Белое'},
                                    {'employer_id': '1740',
                                     'employer_name': 'Яндекс'},
                                    {'employer_id': '1822020',
                                     'employer_name': 'Энергосистема'},
                                    {'employer_id': '2910802',
                                     'employer_name': 'ЗооОптТорг'},
                                    {'employer_id': '4934',
                                     'employer_name': 'Билайн'},
                                    {'employer_id': '625332',
                                     'employer_name': 'Бургер Кинг'},
                                    {'employer_id': '881164',
                                     'employer_name': 'Розовый кролик'},
                                    {'employer_id': '2479394',
                                     'employer_name': 'ПивТочка'},
                                    {'employer_id': '15478',
                                     'employer_name': 'ВК'},
                                    {'employer_id': '4209271',
                                     'employer_name': 'VЛАVАШЕ'}],
                      'items': []
                      }

    @classmethod
    def get_jobs_by_employers_id(cls) -> None:
        """
        Отправляет запросы и получает информацию о вакансиях выбранных работодателей
        """
        params: dict = {'page': 0,
                  'per_page': 100}

        # объединяем все id работодателей для совмещённого запроса
        ids: str = '&employer_id='.join([employer['employer_id'] for employer in cls.employers_info['employers']])

        # получаем информацию о работодателе и количестве активных вакансий
        for employer in cls.employers_info['employers']:
            employer_response: dict = requests.get(f'https://api.hh.ru/employers/{employer["employer_id"]}').json()

            employer['site_url']: dict = employer_response.get('site_url')
            employer['open_vacancies']: int = employer_response.get('open_vacancies')

        while True:
            # получаем информацию о вакансиях работодателей
            response: dict = requests.get(f'https://api.hh.ru/vacancies/?employer_id={ids}',
                                          params=params).json().get('items')
            if response in (None, []):
                break

            for item in response:
                # добавляем необходимую информацию о вакансии в словарь
                cls.employers_info['items'].append(cls.__parse_data(item))

            params['page'] += 1

    @classmethod
    def __parse_data(cls, item: dict):
        """
        Приводит информацию о вакансии в единый вид
        :param item: информация о вакансии
        :return: отредактированная информация о вакансии
        """
        parsed_data = {
            'vacancy_id': item['id'],
            'vacancy_name': item['name'],
            'city': item['area']['name'],
            'salary': cls.__parse_salary(item['salary']),
            'currency': cls.__parse_currency(item['salary']),
            'employer_id': item['employer']['id'],
            'employment': item['employment']['name'],
            'experience': item['experience']['name'],
            'requirement': item['snippet']['requirement'],
            'responsibility': item['snippet']['responsibility'],
            'url': item['alternate_url'],
            'address': cls.__parse_address(item['address']),
            'published_at': item['published_at']
        }

        return parsed_data

    @staticmethod
    def __parse_salary(salary_info: dict) -> int:
        """
        Возвращает единый вид информации о зарплате
        :param salary_info: информация о зарплате
        :return: отредактированная информация о зарплате
        """
        if salary_info is None:
            return 0

        elif salary_info.get('to') is None:
            return salary_info.get('from', 0)

        return salary_info.get('to', 0)

    @staticmethod
    def __parse_currency(currency_info) -> None | str:
        """
        Возвращает единый вид информации о валюте зарплаты
        :param currency_info: информация о валюте зарплаты
        :return: отредактированная информация о валюте зарплаты
        """
        if currency_info is None:
            return None
        return currency_info.get('currency')

    @staticmethod
    def __parse_address(address_info) -> None | str:
        if address_info is None:
            return None
        return address_info.get('raw')

    @classmethod
    def log_saving(cls, file_path: str) -> None:
        """
        Сохраняет информацию о вакансиях и работодателе в JSON-файл
        :param file_path: путь к JSON-файлу
        """
        with open(file_path, 'w', encoding='utf-8') as json_file:
            json.dump(cls.employers_info, json_file, indent=2, ensure_ascii=False)
