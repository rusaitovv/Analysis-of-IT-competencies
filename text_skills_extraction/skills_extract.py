import spacy
from spacy.matcher import PhraseMatcher
from dictionaries import skills  # Импорт вашего словаря навыков

# Загрузка модели с явным указанием нужных компонентов
nlp = spacy.load("ru_core_news_lg", exclude=["parser", "ner"])
matcher = PhraseMatcher(nlp.vocab, attr="LOWER")  # Изменили на LOWER для стабильности


def prepare_patterns():
    """Подготавливает паттерны для поиска с предварительной лемматизацией"""
    for category, phrases in skills.items():
        patterns = []
        for phrase in phrases:
            # Полная обработка текста через nlp()
            doc = nlp(phrase.lower())
            # Сбор лемм, удаление стоп-слов и пунктуации
            lemmas = [token.lemma_ for token in doc
                      if not token.is_stop and not token.is_punct and token.lemma_.strip()]
            lemma_phrase = " ".join(lemmas)
            # Полная обработка для создания паттерна
            patterns.append(nlp(lemma_phrase))
        matcher.add(category, patterns)


# Инициализация паттернов
prepare_patterns()


def analyze_skills(extracted_text: str) -> list:
    """Анализирует текст и возвращает найденные навыки"""
    doc = nlp(extracted_text.lower())
    matches = matcher(doc)

    found_skills = set()
    for match_id, _, _ in matches:
        found_skills.add(nlp.vocab.strings[match_id])

    return sorted(found_skills)
