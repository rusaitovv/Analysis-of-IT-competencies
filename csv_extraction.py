import os
from seatable_api import Base, context
import pandas as pd
import requests
import chardet
# Авторизация
server_url = "https://cloud.seatable.io"  # или ваш сервер
api_token = "db7264bef2843939860fbb9301eb1e62eb551603"        # замените на ваш API-токен
base = Base(api_token, server_url)
base.auth()

TABLE_NAME = "Vacancies"
JOB_TITLE_COLUMN = "job_title"
CSV_FILE_COLUMN = "matrix_skill"

rows = base.list_rows(TABLE_NAME)


def download_csv(url, title, save_dir="Downloads"):
    """Скачивает файл по URL в указанную директорию"""
    try:
        os.makedirs(save_dir, exist_ok=True)
        filename = f'{title}.csv'
        save_path = os.path.join(os.path.expanduser("~"), save_dir, filename)

        # Скачиваем файл

        base.download_file(url, save_path)

        return save_path

    except Exception as e:
        print(f"Ошибка при скачивании: {str(e)}")
        return None


# 2. Функция для получения CSV по названию вакансии
def get_vacancies_as_dataframe(job_title):


    # Ищем запись по названию вакансии
    rows = base.list_rows('Vacancies')
    for row in rows:
        if row.get(JOB_TITLE_COLUMN) == job_title:
            if CSV_FILE_COLUMN in row and row[CSV_FILE_COLUMN]:
                attachments = row.get('matrix_skill', [])
                if attachments:
                    file_url = attachments[0]["url"]

                    if file_url:
                        file_path = download_csv(file_url, job_title)
                        df = pd.read_csv(file_path, sep='\s*;\s*',
                                        names=['Компетенция', 'Уровень владения'], encoding = 'IBM866',
                                        skiprows=2, engine='python')

                        df = df.apply(lambda x: x.str.replace('"', '') if x.dtype == 'object' else x)

                        df['Уровень владения'] = pd.to_numeric(df['Уровень владения'], errors='coerce').fillna(0).astype(
                            int)

                        return df

    return None  # Если не найдено

def get_study_program_as_dataframe(study_program, vacancy):


    # Ищем запись по названию вакансии
    rows = base.list_rows('Study_programs')
    for row in rows:
        if row.get('study_program') == study_program:
            if CSV_FILE_COLUMN in row and row[CSV_FILE_COLUMN]:
                attachments = row.get('matrix_skill', [])
                if attachments:
                    file_url = attachments[0]["url"]

                    if file_url:
                        file_path = download_csv(file_url, study_program)
                        print(file_path)
                        with open(file_path, 'rb') as f:
                            encoding = chardet.detect(f.read(10000))['encoding']
                        df = pd.read_csv(file_path, sep='\s*;\s*',
                                        names=['Компетенция', 'Аналитик данных', 'Инженер данных',
                                               'Технический аналитик в ИИ', 'Менеджер в ИИ'],
                                        encoding = encoding, engine='python')

                        df = df.apply(lambda x: x.str.replace('"', '') if x.dtype == 'object' else x)

                        df[vacancy] = pd.to_numeric(df[vacancy], errors='coerce').fillna(0).astype(
                            int)

                        return df[['Компетенция', vacancy]]

    return None  # Если не найдено

