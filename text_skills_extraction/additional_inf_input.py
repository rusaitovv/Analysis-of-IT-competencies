"""Модуль для сбора данных соискателя с валидацией ввода и предзаполнением."""
import re
from datetime import datetime
from typing import Dict, Optional, Callable

# Константы
VACANCIES = {
    1: "Аналитик данных",
    2: "Инженер данных",
    3: "Технический аналитик в ИИ",
    4: "Менеджер в ИИ"
}

PHONE_LENGTH = 12
EMAIL_PATTERN = r'^[a-zA-Z0-9][\w.-]+@([a-zA-Z0-9-]+\.)+[a-zA-Z]{2,}$'


def collect_applicant_data(
    fio: Optional[str] = None,
    birthdate: Optional[str] = None,
    phone: Optional[str] = None,
    email: Optional[str] = None,
    vacancy: Optional[str] = None
) -> Dict[str, str]:
    """Собирает данные соискателя с возможностью предзаполнения."""

    def validate_fio(raw: str) -> Optional[str]:
        parts = raw.strip().split()
        if len(parts) == 3 and all(re.match(r'^[a-zA-Zа-яА-ЯёЁ-]+$', p) for p in parts):
            return ' '.join(parts)
        return None

    def validate_birthdate(raw: str) -> Optional[str]:
        try:
            date = datetime.strptime(raw, '%Y-%m-%d')
            if date.date() > datetime.today().date():
                return None
            return raw
        except ValueError:
            return None

    def validate_phone(raw: str) -> Optional[str]:
        cleaned = re.sub(r'[^\d+]', '', raw)
        if cleaned.startswith('+7') and len(cleaned) == 12:
            return cleaned
        if len(cleaned) == 11:
            if cleaned.startswith('7'):
                return f"+7{cleaned[1:]}"
            if cleaned.startswith('8'):
                return f"+7{cleaned[1:]}"
        return None

    def validate_email(raw: str) -> Optional[str]:
        return raw if re.fullmatch(EMAIL_PATTERN, raw) else None

    def get_input(
            prompt: str, validator: Callable[[str], Optional[str]],
            error_msg: str, field_name: str, initial: Optional[str] = None) -> str:
        if initial is not None and initial.strip():
            normalized = validator(initial)
            if normalized is not None:
                print(f"✅ Использовано предзаполненное значение для '{field_name}': {normalized}")
                return normalized
            print(f"⚠️ Некорректное предзаполненное значение для '{field_name}': {initial}")

        while True:
            try:
                value = input(prompt).strip()
                normalized = validator(value)
                if normalized is not None:
                    return normalized
                print(f"❌ Ошибка в поле '{field_name}': {error_msg}")
            except KeyboardInterrupt:
                print("\n\n⚠️ Ввод прерван. Попробуйте еще раз...")
            except Exception as e:
                print(f"⚠️ Неожиданная ошибка: {str(e)}")

    def handle_vacancy(initial: Optional[str]) -> str:
        if initial:
            if initial.isdigit():
                num = int(initial)
                if num in VACANCIES:
                    print(f"✅ Использовано предзаполненное значение для 'Вакансия': {VACANCIES[num]}")
                    return VACANCIES[num]
            if initial in VACANCIES.values():
                print(f"✅ Использовано предзаполненное значение для 'Вакансия': {initial}")
                return initial
            print(f"⚠️ Некорректное предзаполненное значение для 'Вакансия': {initial}")

        print("\nДоступные вакансии:")
        for num, title in VACANCIES.items():
            print(f"{num} - {title}")

        return VACANCIES[int(get_input(
            "Выберите номер вакансии (1-4): ",
            lambda x: x if x.isdigit() and 1 <= int(x) <= 4 else None,
            "требуется число от 1 до 4",
            "Вакансия",
            None
        ))]

    data = {}

    data['fio'] = get_input(
        "Введите ФИО (3 слова через пробел, только буквы и дефисы): ",
        validate_fio,
        "требуется формат: 'Иванов Иван Иванович'",
        "ФИО",
        fio
    )

    data['birthdate'] = get_input(
        "Введите дату рождения (ГГГГ-ММ-ДД): ",
        validate_birthdate,
        "некорректная дата или дата в будущем",
        "Дата рождения",
        birthdate
    )

    data['phone'] = get_input(
        "Введите телефон (форматы: +7XXXXXXXXXX, 8XXXXXXXXXX или 7XXXXXXXXXX): ",
        validate_phone,
        "неверный формат номера. Пример: +79001234567 или 89001234567",
        "Телефон",
        phone
    )

    data['email'] = get_input(
        "Введите email: ",
        validate_email,
        "некорректный формат email",
        "Email",
        email
    )

    data['vacancy'] = handle_vacancy(vacancy)

    print("\nИтоговые данные:")
    for key, value in data.items():
        print(f"{key.capitalize()}: {value}")

    return data
