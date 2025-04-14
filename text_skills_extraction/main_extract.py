import os
from text_skills_extraction.skills_extract import analyze_skills
from text_skills_extraction.text_extract import define_type

from text_skills_extraction.additional_inf_autoextract import phone_number_extract, email_extract
from text_skills_extraction.additional_inf_input import collect_applicant_data
# from test import *
from text_skills_extraction.university_faculty_extract import find_universities, extract_faculty


def process_folder(folder_path):
    """Обрабатывает все файлы в папке."""

    # Проходим по всем файлам в папке
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)

        # Обрабатываем только файлы (игнорируем папки)
        if os.path.isfile(file_path):
            # Обрабатываем файл
            text_from_file = define_type(file_path)

            found_skills = analyze_skills(text_from_file) # Навыки
            phone_num = phone_number_extract(text_from_file) # Номер телефона
            email_extracted = email_extract(text_from_file) # Почта
            birth_date = "0000.00.00" # Дата рождения
            name = "ФИО" # ФИО

            university = find_universities(text_from_file) # Универ
            faculties = extract_faculty(text_from_file) # Направления

            applicant_data = collect_applicant_data(
                fio=name, birthdate=birth_date, phone=phone_num, email=email_extracted)
            return applicant_data, university, faculties, found_skills



