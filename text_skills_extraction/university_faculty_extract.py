import re
from fuzzywuzzy import fuzz
from pymorphy3 import MorphAnalyzer
from dictionaries import university_synonyms, faculty_synonyms

# Инициализация анализатора
morph = MorphAnalyzer()


def prepare_synonym_dict_uni(university_synonyms):
    """Создает словарь для поиска: синоним -> каноническое название"""
    synonym_map = {}
    for uni, synonyms in university_synonyms.items():
        # Добавляем само каноническое название
        synonym_map[uni.lower()] = uni

        # Добавляем все синонимы
        for synonym in synonyms:
            synonym_map[str(synonym).lower()] = uni
    return synonym_map


def find_universities(text, threshold=85):
    """Ищет вузы в тексте с учетом синонимов и опечаток"""
    synonym_map = prepare_synonym_dict_uni(university_synonyms)
    text = re.sub(r'[^\w\s]', '', text.lower())  # Очистка текста
    found = set()

    # 1. Поиск по точным совпадениям
    for syn, uni in synonym_map.items():
        if re.search(r'\b' + re.escape(syn) + r'\b', text):
            found.add(uni)

    # 2. Нечеткий поиск для сложных случаев
    if not found:
        words = text.split()
        for syn, uni in synonym_map.items():
            syn_words = syn.split()

            # Проверяем все возможные последовательности слов
            for i in range(len(words) - len(syn_words) + 1):
                phrase = ' '.join(words[i:i + len(syn_words)])
                if fuzz.ratio(phrase, syn) > threshold:
                    found.add(uni)

    return list(found)

#                      ||
# Извлечение факультета||
#                     \||/
#                      \/

def prepare_synonym_dict_faculties(synonyms_dict):
    """Создает словарь для поиска: синоним -> каноническое название факультета"""
    synonym_map = {}
    for name, synonyms in synonyms_dict.items():
        synonym_map[name.lower()] = name  # Основное название
        for synonym in synonyms:
            synonym_map[str(synonym).lower()] = name  # Все синонимы
    return synonym_map


def find_faculties(text, threshold=85):
    """Ищет факультеты в тексте с учетом синонимов и опечаток"""
    synonym_map = prepare_synonym_dict_faculties(faculty_synonyms)
    text = re.sub(r'[^\w\s]', '', text.lower())  # Очистка текста
    found = set()

    # 1. Поиск по точным совпадениям
    for syn, faculty in synonym_map.items():
        if re.search(r'\b' + re.escape(syn) + r'\b', text):
            found.add(faculty)

    # 2. Нечеткий поиск (если точных совпадений нет)
    if not found:
        words = text.split()
        for syn, faculty in synonym_map.items():
            syn_words = syn.split()
            for i in range(len(words) - len(syn_words) + 1):
                phrase = ' '.join(words[i:i + len(syn_words)])
                if fuzz.ratio(phrase, syn) > threshold:
                    found.add(faculty)

    return list(found)


# Подготовка словаря факультетов



def extract_faculty(text):
    """Извлекает ТОЛЬКО факультет из текста"""
    return find_faculties(text)