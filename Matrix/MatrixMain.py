import requests
import time
import pandas as pd
from collections import defaultdict


def get_vacancy_skills():
    """Сбор навыков из вакансий с обработкой ошибок и пагинацией"""
    skills_counter = defaultdict(int)
    total_vacancies = 0

    try:
        # Параметры запроса (можно менять)
        search_text = "Senior Python разработчик"  # Название профессии
        region_id = 1  # 1 - Москва
        pages = 5  # Страниц для анализа
        per_page = 20  # Вакансий на странице

        for page in range(pages):
            # Формируем запрос
            params = {
                "text": f"NAME:{search_text}",
                "area": region_id,
                "page": page,
                "per_page": per_page,
                "only_with_salary": True  # Только вакансии с зарплатой
            }

            # Делаем запрос к API
            response = requests.get("https://api.hh.ru/vacancies", params=params)

            # Проверяем статус ответа
            if response.status_code != 200:
                print(f"Ошибка {response.status_code}. Пропускаем страницу {page}")
                continue

            data = response.json()
            vacancies = data.get('items', [])

            # Обрабатываем каждую вакансию
            for vacancy in vacancies:
                if not vacancy.get('url'):
                    continue

                # Запрашиваем детали вакансии
                vac_response = requests.get(vacancy['url'])
                if vac_response.status_code == 200:
                    vacancy_data = vac_response.json()
                    skills = [skill['name'].lower() for skill in vacancy_data.get('key_skills', [])]
                    for skill in skills:
                        skills_counter[skill] += 1
                    total_vacancies += 1

                # Соблюдаем лимит API - 2 запроса в секунду
                time.sleep(0.5)

            # Прогресс
            print(f"Обработано страниц: {page + 1}/{pages}")

        print(f"\nВсего обработано вакансий: {total_vacancies}")
        return skills_counter, total_vacancies

    except Exception as e:
        print(f"Критическая ошибка: {str(e)}")
        return None, 0


def calculate_ratings(skills_data, total_vacancies):
    """Рассчет рейтинга навыков от 1 до 10"""
    if total_vacancies == 0:
        return None

    # Нормализация частоты
    max_count = max(skills_data.values(), default=1)
    min_count = min(skills_data.values(), default=0)

    # Избегаем деления на ноль
    if max_count == min_count:
        return {skill: 5 for skill in skills_data}

    # Линейное преобразование
    return {
        skill: round(1 + 9 * (count - min_count) / (max_count - min_count), 1)
        for skill, count in skills_data.items()
    }


def main():
    # Сбор данных
    skills, count = get_vacancy_skills()
    if not skills:
        print("Не удалось получить данные")
        return

    # Расчет рейтингов
    ratings = calculate_ratings(skills, count)

    # Создаем DataFrame
    df = pd.DataFrame(
        list(ratings.items()),
        columns=['Навык', 'Рейтинг']
    ).sort_values('Рейтинг', ascending=False)

    # Сохраняем в CSV
    df.to_csv('skills_matrix.csv', index=False)
    print("\nРезультат сохранен в skills_matrix.csv")

    # Выводим топ-15
    print("\nТоп-15 навыков:")
    print(df.head(15))


if __name__ == "__main__":
    main()