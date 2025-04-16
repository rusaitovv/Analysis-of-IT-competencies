import seatable_api

base = seatable_api.Base("db7264bef2843939860fbb9301eb1e62eb551603", "https://cloud.seatable.io")

# Рекрутер выбирает, какая вакансия его интересует (сделано на основе БМПК)
while True:
    vacancy_name = int(input('Введите число, соотвествующее вакансии (Аналитик данных - 1, Инженер данных - 2, Технический аналитик - 3, Менеджер в ИИ - 4): '))
    if vacancy_name < 5 and vacancy_name > 0:
        break
    else:
        print('Такой вакансии не существует. Попробуйте еще раз')

print("\n=== Процесс обработки ===")

# Аутентификация
base.auth()
print("1. Успешное подключение к SeaTable")

# Загрузка кандидатов
print(f"2. Поиск вакансии '{vacancy_name}'...")
rows = base.list_rows('Candidates')

# Сортировка кандидатов
rows.sort(reverse = True, key = lambda x: x['points'] )

vacancy = rows[0]['job_title']

# Вывод кандидатов
print(f"3. Вывод кандидатов (от самого подходящего к самому неподходящему) на вакансию '{vacancy_name}'")
for row in rows:
    print(f"ФИО: {row['full_name']}, Дата рождения: {row['date_birth'][:10]}, Контактные данные: {row['phone_number']}/ {row['email']}")
    print(f"Кандидат подходит на вакансию '{vacancy}' на {row['points']}%")
    print("Недостающие навыки:")
    skills = row['missing_skills']
    for num, skill in enumerate(list(eval(skills))):
        print(num + 1, skill)
    print()