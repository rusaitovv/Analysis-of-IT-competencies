import re
import time
from datetime import datetime
from re import match, sub

phone_pattern = r'(?:\+7|8|7)\d{10}\b'
email_pattern = r'\b[\w.-]+@[\w.-]+\.\w{2,}\b'
birthday_pattern = r'\b(?:\d{2}[._-]\d{2}[._-]\d{4}|\d{4}[._-]\d{2}[._-]\d{2})\b'


def phone_number_extract(text):
    global phone_pattern
    phones = re.findall(phone_pattern, text)
    if phones:
        phone_num = str(phones[0])
        if len(phone_num) != 12:
            phone_num = "+7" + phone_num[1:]
        return phone_num
    return "-1"


def email_extract(text):
    global email_pattern
    emails = re.findall(email_pattern, text)
    if emails:
        email = emails[0]
        if len(email) < 254:
            return email
    return "Invalid email"


def standardize_date(match):
    date_str = match.group()

    # Определяем формат исходной даты
    if '_' in date_str:
        sep = '_'
    elif '.' in date_str:
        sep = '.'
    elif '/' in date_str:
        sep = '/'
    else:
        sep = '-'

    parts = date_str.split(sep)

    # Если формат DD_MM_YYYY
    if len(parts[0]) == 2:
        day, month, year = parts
    else:  # Формат YYYY_MM_DD
        year, month, day = parts

    # Форматируем в YYYY-MM-DD
    return f"{year}-{month}-{day}"
