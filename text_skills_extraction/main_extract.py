import os
from text_extract import define_type
from skills_extract import analyze_skills


def process_folder(folder_path):
    """Обрабатывает все файлы в папке."""

    # Проходим по всем файлам в папке
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)

        # Обрабатываем только файлы (игнорируем папки)
        if os.path.isfile(file_path):
            # Обрабатываем файл
            text_from_file = define_type(file_path)
            found_skills = analyze_skills(text_from_file)
            print("Найдены навыки:")
            for skill in found_skills:
                print(f"- {skill}")

folder_path = "rezyume"  # Укажите путь к папке с файлами
process_folder(folder_path)