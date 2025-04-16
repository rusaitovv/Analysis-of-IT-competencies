import pandas

from csv_extraction import get_vacancies_as_dataframe, base, get_study_program_as_dataframe
from text_skills_extraction.main_extract import process_folder
from text_skills_extraction.dictionaries import university_rank_values

uni_percentage = 0.3

def relevance(candidate_skills: list[str], required_skills: pandas.DataFrame, studied_programs: list[str],
              total_score: float, missing_skills: set[str], universities: list[str], vacancy: str):
    """
    Вычисляет релевантность кандидата на основе его навыков и требуемых навыков

    Аргументы:


    Возвращает:
    Процент соответствия кандидата
    """
    candidate_score = 0

    #Берем навыки с программ обучения
    studied_skills = set()
    for program in studied_programs:
        # Если есть релевантная программа обучения, достаем оттуда навыки

        if program:
            studied_skills_db = get_study_program_as_dataframe(program, vacancy)

            for index, row in studied_skills_db.iterrows():
                skill = row['Компетенция']
                rate = row[vacancy]
                if rate != 0:
                    studied_skills.add(skill)

    for index, row in required_skills.iterrows():
        skill = row['Компетенция']
        rating = row['Уровень владения']
        if rating != 0:
            if (skill in candidate_skills) or (skill in studied_skills):
                candidate_score += rating
            else:
                missing_skills.add(skill)



    if universities:
        uni_add = 0
        for university in universities:
            uni_add = max(uni_add, university_rank_values[university])
        candidate_score *= (1 + uni_percentage / 11 * uni_add)

    # Вычисляем процент соответствия
    if total_score == 0:
        return 0.0
    return round((candidate_score / total_score) * 100, 2)


def processing_resume(candidate_info: dict, user_skills: list[str],
                      studied_programs: list[str], universities: list[str]):
    """
    Обрабатывает резюме кандидата и вычисляет его соответствие вакансии

    Аргументы:



    """


    #Достаем навыки с вакансии
    vacancy_name = candidate_info['vacancy']
    required_skills_db = get_vacancies_as_dataframe(vacancy_name)


    #Собираем знаменатель метрики
    total_score = 0
    for rate in required_skills_db['Уровень владения']:
        total_score += rate
    total_score *= (1 + uni_percentage)




    # Словарь для недостающих навыков
    missing_skills = set()

    # Вычисляем релевантность
    percentage = relevance(user_skills, required_skills_db, studied_programs,
                           total_score, missing_skills, universities, vacancy_name)




    # Формируем сообщение
    match_message = f"Подходит на позицию {vacancy_name} на {percentage:.2f}%"

    new_row = {
        'full_name': candidate_info['fio'],
        'date_birth': candidate_info['birthdate'],
        'phone_number':candidate_info ['phone'],
        'email': candidate_info['email'],
        'job_title': vacancy_name,
        'points': percentage,
        'missing_skills': str(missing_skills)
    }
    base.append_row('Candidates', new_row)

    return {
        'candidate_info': candidate_info,
        'match_percentage': percentage,
        'missing_skills': missing_skills,
        'match_message': match_message
    }


# Пример использования

# Пример входных данных
candidate_info = {'fio': 'Егоров Кирилл Романович',
                  'birthdate': '2000-10-10',
                  'phone': '+71112223344',
                  'email': 'egorkirillov@gmail.com',
                  'vacancy': 'Аналитик данных'}

studied_programs = []
candidate_universities = ["Московский физико-технический институт"]

user_skills = ['Качество и предобработка данных, подходы и инструменты',
               'Методы машинного обучения', 'Процесс, стадии и методологии разработки решений на основе ИИ',
               'Языки программирования и библиотеки (Python, C++)']

# candidate_data = process_folder('rezyume')
# print(candidate_data)
# candidate_info, candidate_universities, studied_programs, user_skills = candidate_data

studied_programs += []
# Обработка резюме
result = processing_resume(candidate_info, user_skills, studied_programs, candidate_universities)

# Вывод результатов
print(result['match_message'])
print("Контактная информация:", result['candidate_info'])
print("Недостающие навыки:", str(result['missing_skills']))