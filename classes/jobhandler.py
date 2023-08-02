import json

import requests


class JobHandler:
    employers_info = {'employers': [{'employer_id': '1035394',
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
    def get_jobs_by_employers_id(cls):
        params = {'page': 0,
                  'per_page': 100}
        ids = '&employer_id='.join([employer['employer_id'] for employer in cls.employers_info['employers']])

        for employer in cls.employers_info['employers']:
            employer_response = requests.get(f'https://api.hh.ru/employers/{employer["employer_id"]}').json()

            employer['site_url'] = employer_response.get('site_url')
            employer['open_vacancies'] = employer_response.get('open_vacancies')

        while True:
            response = requests.get(f'https://api.hh.ru/vacancies/?employer_id={ids}', params=params).json().get('items')
            if response in (None, []):
                break

            for item in response:
                cls.employers_info['items'].append(cls.__parse_data(item))

            params['page'] += 1



        return cls.employers_info

    @classmethod
    def __parse_data(cls, item):
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
    def __parse_salary(salary_info):
        if salary_info is None:
            return 0

        elif salary_info.get('to') is None:
            return salary_info.get('from', 0)

        return salary_info.get('to', 0)

    @staticmethod
    def __parse_currency(currency_info):
        if currency_info is None:
            return None
        return currency_info.get('currency')

    @staticmethod
    def __parse_address(address_info):
        if address_info is None:
            return None
        return address_info.get('raw')

    @classmethod
    def log_saving(cls, file_path):
        with open(file_path, 'w', encoding='utf-8') as json_file:
            json.dump(cls.employers_info, json_file, indent=2)
