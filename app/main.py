import os

import psycopg2
from prettytable import PrettyTable
from app.utils import config, get_vacancies
from classes.dbcreator import DBCreator
from classes.dbmanager import DBManager
from classes.jobhandler import JobHandler
from os.path import abspath

BASEDIR = abspath('..')
PATH_TO_DATA = os.path.join(BASEDIR, 'data')
PATH_TO_BACKUP = os.path.join(PATH_TO_DATA, 'vacancy_log.json')


def user_interface():
    print('Происходит получение данных о вакансиях, подождите немного...')
    params = config()
    JobHandler.get_jobs_by_employers_id()
    JobHandler.log_saving(PATH_TO_BACKUP)

    print('Добро пожаловать в JobHandler!\n')

    while True:
        user_input = input('Введите команду:\n'
                           '1. Посмотреть доступные вакансии\n'
                           '0. Выход\n')

        if user_input == '0':
            print('Всего доброго!')
            exit()

        elif user_input == '1':
            print('Происходит подготовка данных о вакансиях, подождите немного...')
            DBCreator.create_database('hh_jobs', params)

            with psycopg2.connect(dbname='hh_jobs', **params) as conn:
                with conn.cursor() as cur:
                    DBCreator.create_tables(cur, os.path.join(PATH_TO_DATA, 'create_tables.sql'))
                    DBCreator.insert_data(JobHandler.employers_info, cur)
            conn.close()
            while True:
                response = get_vacancies(params)
                DBManager.conn.close()

                if response:
                    table = PrettyTable(field_names=response[0], align='l')
                    table.add_rows(response[1:])
                    print(table)
                    input('Нажмите Enter, чтобы продолжить ')
                if response is None:
                    break
        else:
            print('Неизвестная команда, повторите запрос!')


if __name__ == '__main__':
    user_interface()
