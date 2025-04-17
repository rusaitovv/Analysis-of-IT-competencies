import spacy
from spacy.matcher import PhraseMatcher
from text_skills_extraction.dictionaries import skills

# Загрузка русской языковой модели (предварительно установите: python -m spacy download ru_core_news_sm)
nlp = spacy.load("ru_core_news_sm")
matcher = PhraseMatcher(nlp.vocab, attr="LOWER")


# Добавляем паттерны в Matcher
for category, phrases in skills.items():
    patterns = [nlp.make_doc(text) for text in phrases]
    matcher.add(category, patterns)


def analyze_skills(extracted_text):
    doc = nlp(extracted_text.lower())
    matches = matcher(doc)

    found_skills = set()
    for match_id, start, end in matches:
        category = nlp.vocab.strings[match_id]
        found_skills.add(category)

    return sorted(found_skills)

