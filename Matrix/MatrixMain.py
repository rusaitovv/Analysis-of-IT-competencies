import requests
import time
import pandas as pd
from collections import defaultdict


def get_city_id(city_name):
    """Поиск ID города по названию"""
    try:
        areas = requests.get("https://api.hh.ru/areas").json()
        for country in areas:
            for area in country['areas']:
                # Проверка области
                if area['name'].lower() == city_name.lower():
                    return area['id']
                # Проверка городов внутри области
                for city in area['areas']:
                    if city['name'].lower() == city_name.lower():
                        return city['id']
        return None
    except Exception as e:
        print(f"Ошибка при поиске города: {e}")
        return None


def get_user_input():
    """Ввод данных от пользователя"""
    profession = input("Введите название профессии: ").strip()

    while True:
        city = input("Введите город: ").strip()
        city_id = get_city_id(city)
        if city_id:
            return profession, city_id, city
        print(f"Город '{city}' не найден. Попробуйте еще раз.")


def fetch_vacancies(profession, area_id):
    """Сбор данных о вакансиях"""
    skills_counter = defaultdict(int)
    total_vacancies = 0

    try:
        for page in range(5):  # Анализ первых 5 страниц
            params = {
                "text": f"NAME:{profession}",
                "area": area_id,
                "page": page,
                "per_page": 50,
                "only_with_salary": True
            }

            response = requests.get("https://api.hh.ru/vacancies", params=params)
            if response.status_code != 200:
                continue

            vacancies = response.json().get('items', [])

            for vacancy in vacancies:
                if not vacancy.get('url'):
                    continue

                try:
                    vac_data = requests.get(vacancy['url']).json()
                    skills = [s['name'].lower() for s in vac_data.get('key_skills', [])]
                    for skill in skills:
                        skills_counter[skill] += 1
                    total_vacancies += 1
                except:
                    continue

                time.sleep(0.5)

            print(f"Обработано страниц: {page + 1}/5")
            time.sleep(1)

        return skills_counter, total_vacancies

    except Exception as e:
        print(f"Ошибка: {e}")
        return None, 0


def main():
    # Ввод данных
    profession, city_id, city = get_user_input()

    # Сбор данных
    print("\nНачинаем сбор данных...")
    skills, count = fetch_vacancies(profession, city_id)

    if not skills or count == 0:
        print("Не удалось собрать данные")
        return

    # Расчет рейтингов
    max_count = max(skills.values())
    min_count = min(skills.values())
    diff = max_count - min_count if max_count != min_count else 1

    ratings = {
        skill: round(1 + 9 * (count - min_count) / diff, 1)
        for skill, count in skills.items()
    }

    # Создание DataFrame
    df = pd.DataFrame(
        list(ratings.items()),
        columns=['Компетенция', 'Уровень владения']
    ).sort_values('Уровень владения', ascending=False)

    # Сохранение и вывод
    df.to_csv(f'{profession}_{city}_skills_matrix.csv', index=False)
    print(f"\nТоп-10 навыков для '{profession}':\n")
    print(df.head(10))
    print(f"\nПолные данные сохранены в {profession}_{city}_skills_matrix.csv")


if __name__ == "__main__":
    main()