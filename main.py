import pandas

from csv_extraction import get_vacancies_as_dataframe, base, get_study_program_as_dataframe
from text_skills_extraction.main_extract import process_folder
from text_skills_extraction.dictionaries import university_rank_values

uni_percentage = ...

def relevance(candidate_skills: list[str], required_skills: pandas.DataFrame, studied_skills: list[str],
              total_score: float, experience: bool, missing_skills: set[str], university: str):
    """
    Вычисляет релевантность кандидата на основе его навыков и требуемых навыков

    Аргументы:
    candidate_skills - список навыков кандидата
    required_skills - словарь требуемых навыков и их рейтингов
    total_score - сумма всех баллов требуемых навыков
    missing_skills - словарь для сохранения недостающих навыков

    Возвращает:
    Процент соответствия кандидата
    """
    candidate_score = 0

    for index, row in required_skills.iterrows():
        skill = row['Компетенция']
        rating = row['Уровень владения']
        if rating != 0:
            if skill in candidate_skills:
                candidate_score += rating
            else:
                missing_skills.add(skill)

            if skill in studied_skills:
                candidate_score += rating
                if skill in missing_skills:
                    missing_skills.remove(skill)
            else:
                missing_skills.add(skill)



    if university:
        candidate_score *= (1 + uni_percentage / 11 * university_rank_values[university])

    # Вычисляем процент соответствия
    if total_score == 0:
        return 0.0
    return round((candidate_score / total_score) * 100, 2)


def processing_resume(candidate_info: dict, vacancy_name: str, user_skills: list[str],
                      experience: bool, study_program: str, university: str):
    """
    Обрабатывает резюме кандидата и вычисляет его соответствие вакансии

    Аргументы:
    candidate_id - ID кандидата
    vacancy_name - название вакансии
    user_skills - массив навыков пользователя в str


    """
    # Здесь должна быть логика получения данных из БД
    # Для примера используем заглушки

    # Получаем требуемые навыки для вакансии из БД
    # В реальной программе это будет запрос к БД по vacancy_name


    required_skills_db = get_vacancies_as_dataframe(vacancy_name)

    #Если есть релевантная программа обучения
    studied_skills = []
    if study_program:
        studied_skills_db = get_study_program_as_dataframe(study_program, vacancy_name)


        for index, row in studied_skills_db:
            skill = row['Компетенция']
            rate = row[vacancy_name]
            if rate != 0:
                studied_skills.append(skill)


    total_score = 0
    for rate in required_skills_db['Уровень владения']:
        total_score += rate
    total_score += ...
    total_score *= 1 + uni_percentage
    # Получаем навыки кандидата
    pass

    # Создаем матрицу навыков кандидата

    # Словарь для недостающих навыков
    missing_skills = set()

    # Вычисляем релевантность
    percentage = relevance(user_skills, required_skills_db, studied_skills,
                           total_score, experience, missing_skills, university)

    # Получаем информацию о кандидате из БД
    # В реальной программе это будет запрос к БД по candidate_id


    # Формируем сообщение
    match_message = f"Подходит на позицию {vacancy_name} на {percentage:.2f}%"

    new_row = {
        'full_name': candidate_info['full_name'],
        'date_birth': candidate_info['birth_date'],
        'phone_number':candidate_info ['phone'],
        'email': candidate_info['email'],
        'job_title': vacancy_name,
        'points': percentage,
        'missing_skills': str(missing_skills),
        'relevant_skills': str(set(user_skills) - set(missing_skills))
    }
    base.append_row('Candidates', new_row)

    return {
        'candidate_info': candidate_info,
        'match_percentage': percentage,
        'missing_skills': missing_skills,
        'match_message': match_message
    }


# Пример использования
if __name__ == "__main__":
    # Пример входных данных
    candidate_info = {
        'full_name': 'Филькин Филя Филимонович',
        'email': 'filkin@example.com',
        'phone': '+0000000',
        'birth_date': '01.01.1900'
    }
    vacancy_name = "Аналитик данных"
    user_skills = [
                   'Языки программирования и библиотеки (Python, C++)'
                   ]
    experience = False

    # Обработка резюме
    result = processing_resume(candidate_info, vacancy_name, user_skills, experience)

    # Вывод результатов
    print(result['match_message'])
    print("Контактная информация:", result['candidate_info'])
    print("Недостающие навыки:", str(result['missing_skills']))