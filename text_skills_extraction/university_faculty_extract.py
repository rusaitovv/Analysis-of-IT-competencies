import re
import spacy
from fuzzywuzzy import fuzz
from pymorphy3 import MorphAnalyzer
from dictionaries import university_synonyms, program_synonyms
from typing import List

# Инициализация анализатора
morph = MorphAnalyzer()
nlp = spacy.load("ru_core_news_lg", disable=["parser", "ner"])


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

def normalize_text(text: str) -> str:
    """Нормализует текст: лемматизация + очистка"""
    doc = nlp(text.lower())
    return " ".join([
        token.lemma_ for token in doc
        if not token.is_stop and not token.is_punct and token.lemma_.strip()
    ])


def prepare_program_patterns(programs: List[str]) -> dict:
    """Создает regex-паттерны для поиска направлений"""
    patterns = {}
    for program in programs:
        normalized = normalize_text(program)
        # Экранируем специальные символы и добавляем границы слов
        pattern = re.compile(rf"\b{re.escape(normalized)}\b", re.IGNORECASE)
        patterns[program] = pattern
    return patterns


# Подготовка паттернов один раз при загрузке
PROGRAM_PATTERNS = prepare_program_patterns(program_synonyms)


def extract_education_programs(text: str) -> List[str]:
    """Извлекает направления обучения из текста"""
    normalized_text = normalize_text(text)
    found_programs = []

    for program, pattern in PROGRAM_PATTERNS.items():
        if pattern.search(normalized_text):
            found_programs.append(program)

    return sorted(found_programs)
