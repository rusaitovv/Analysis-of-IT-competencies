import spacy
from spacy.matcher import PhraseMatcher

# Загрузка русской языковой модели (предварительно установите: python -m spacy download ru_core_news_sm)
nlp = spacy.load("ru_core_news_sm")
matcher = PhraseMatcher(nlp.vocab, attr="LOWER")

# Словарь навыков (категория -> ключевые фразы)
skills = {
    "Определения, история развития и главные тренды ИИ": [
        "история искусственного интеллекта", "тренды ии", "определение ии",
        "развитие искусственного интеллекта", "ai trends"
    ],
    "Процесс, стадии и методологии разработки решений на основе ИИ": [
        "docker", "linux", "bash", "git", "ci/cd", "mlops",
        "жизненный цикл модели", "методологии разработки"
    ],
    "Статистические методы и первичный анализ данных": [
        "статистический анализ", "descriptive statistics", "eda",
        "exploratory data analysis", "анализ распределений"
    ],
    "Промпт-инжиниринг": [
        "промпт инжиниринг", "prompt engineering", "настройка промптов",
        "конструирование промптов", "оптимизация запросов llm"
    ],
    "Инструменты CitizenDS": [
        "citizend", "citizen data science", "low-code ai",
        "графический интерфейс для ml"
    ],
    "Оценка качества работы методов ИИ": [
        "метрики качества", "accuracy", "precision", "recall",
        "f1-score", "roc auc", "валидация модели"
    ],
    "Языки программирования и библиотеки": [
        "python", "c++", "numpy", "pandas", "scikit-learn",
        "tensorflow", "pytorch", "opencv", "keras"
    ],
    "Этика ИИ": [
        "этика искусственного интеллекта", "ai ethics",
        "ответственный ai", "этические принципы ии"
    ],
    "Безопасность ИИ": [
        "безопасность искусственного интеллекта", "adversarial attacks",
        "атаки на модели", "защита моделей"
    ],
    "Цифровые двойники": [
        "цифровой двойник", "digital twin", "симуляция объектов",
        "виртуальная копия"
    ],
    "Методы машинного обучения": [
        "машинное обучение", "ml", "классификация", "регрессия",
        "кластеризация", "ансамбли моделей"
    ],
    "Методы оптимизации": [
        "градиентный спуск", "оптимизация гиперпараметров",
        "bayesian optimization", "genetic algorithms"
    ],
    "Информационный поиск": [
        "information retrieval", "поисковые алгоритмы",
        "ранжирование результатов", "tf-idf", "bm25"
    ],
    "Рекомендательные системы": [
        "recommender systems", "коллаборативная фильтрация",
        "content-based filtering", "матричные разложения"
    ],
    "Анализ изображений и видео": [
        "computer vision", "cv", "обработка изображений",
        "обнаружение объектов", "yolo", "opencv"
    ],
    "Анализ естественного языка": [
        "nlp", "обработка естественного языка", "named entity recognition",
        "stemming", "lemmatization", "трансформеры"
    ],
    "Основы глубокого обучения": [
        "глубокое обучение", "нейронные сети", "активационные функции",
        "обратное распространение", "dropout"
    ],
    "Глубокое обучение для анализа и генерации изображений, видео": [
        "gan", "генеративные сети", "style transfer", "super-resolution",
        "video synthesis", "stablediffusion"
    ],
    "Глубокое обучение для анализа и генерации естественного языка": [
        "трансформеры", "bert", "gpt", "llm", "seq2seq",
        "машинный перевод", "text generation"
    ],
    "Обучение с подкреплением и глубокое обучение с подкреплением": [
        "reinforcement learning", "rl", "q-learning",
        "policy gradient", "deep q-network"
    ],
    "Гибридные модели и PIML": [
        "physics-informed ml", "piml", "гибридные модели",
        "нейросетевые дифференциальные уравнения"
    ],
    "Анализ геоданных": [
        "геоаналитика", "gis", "пространственный анализ",
        "картография", "geopandas"
    ],
    "Массово параллельные вычисления для ускорения машинного обучения (GPU)": [
        "gpu", "cuda", "tensor cores", "parallel computing",
        "nvidia", "v100", "a100"
    ],
    "Работа с распределенной кластерной системой": [
        "распределенные вычисления", "kubernetes", "k8s",
        "кластерные системы", "horovod"
    ],
    "Машинное обучение на больших данных": [
        "big data", "большие данные", "apache hadoop",
        "распределенная обработка", "mapreduce"
    ],
    "Потоковая обработка данных (data streaming, event processing)": [
        "data streaming", "kafka", "apache flink", "real-time processing",
        "event-driven architecture"
    ],
    "Графовые нейросети": [
        "графовые сети", "gnn", "graph neural network",
        "graph convolution", "node embedding"
    ],
    "SQL базы данных": [
        "sql", "greenplum", "postgres", "postgresql",
        "oracle", "реляционные базы"
    ],
    "NoSQL базы данных": [
        "nosql", "cassandra", "mongodb", "elasticsearch",
        "neo4j", "hbase", "документные базы"
    ],
    "Массово параллельная обработка и анализ данных": [
        "parallel processing", "распределенная обработка",
        "multiprocessing", "dask", "ray"
    ],
    "Hadoop, SPARK, Hive": [
        "hadoop", "spark", "apache spark", "hive",
        "hdfs", "pyspark", "spark sql"
    ],
    "Шины данных (kafka)": [
        "kafka", "apache kafka", "message broker",
        "event streaming", "шина данных"
    ],
    "Качество и предобработка данных, подходы и инструменты": [
        "предобработка данных", "data cleaning", "feature engineering",
        "missing values", "pandas", "scikit-learn"
    ],
    "Графы знаний и онтологии": [
        "knowledge graph", "граф знаний", "ontology",
        "семантические сети", "rdf", "sparql"
    ]
}

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


# Пример использования
extracted_text = """
Опыт работы с Python и C++, Docker, PostgreSQL.
Знание глубокого обучения и нейронных сетей.
Работал с Hadoop и Spark.
"""

