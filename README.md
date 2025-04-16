﻿# Кандидат тут
## Описание проекта:
Проект представляет собой разработанный алгоритм для автоматической обработки резюме, загруженных кандидатами в сервис, и получения результатов обработки HR-специалистами компании. Решение включает в себя извлечение навыков, описанных в резюме, извлечение ВУЗа, а также программы обучения, если она входит в список приоритетных. 

Выбрав вакансию, HR-специалист компании получает отсортированные по релевантности данные о кандидатах, включая процент их соответствия вакансии, контактную информацию, а также список недостающих навыков у кандидата.

Разработан концепт приложения, который позволяет пользователям (кандидатам и HR-специалистам) использовать единую платформу для подачи резюме в компанию (для соискателей) и получения готовой информации о релевантных кандидатах (для рекрутеров). 

### Установка и настройка
1. Убедитесь, что у вас установлен Python 3.11 и выше
```
python --version
```
2. Установите необходимые библиотеки: Убедитесь, что у вас есть файл requirements.txt, и выполните команду для установки всех зависимостей:
```
pip install -r requirements.txt
```
---
## Запуск проекта
### Для соискателя: 
Необходимо загрузить резюме в формате .docx в папку rezyume, запустить алгоритм через файл main_candidate.py:
```
python main_candidate.py
```
### Пример ввода

![candidate_input](https://github.com/user-attachments/assets/4f5f5b77-9994-4be4-ab93-5c312c71c469)
### Пример вывода
<img src="https://github.com/user-attachments/assets/034952ec-7a50-4113-879f-489ddf1ebc04" width="700" height="280">


### Для рекрутера: 
Запустить алгоритм через файл main_hr.py:
```
python main_hr.py
```
### Пример работы
![hr](https://github.com/user-attachments/assets/16e03d08-0340-4fff-814e-a3696cbd801c)

---
### Основной функционал
* Обработка резюме
* Сортировка кандидатов по релевантности
### Дизайн приложения
Дизайн интерфейса можно найти в следующих файлах (полный набор изображений находится в папке Design):
* Главный экран.png - главный экран приложения
* Рег кандидат.png - экран регистрации соискателя
* Рег рекрутер.png - экран регистрации рекрутера
* Кандидаты.png - экран представления релевантных кандидатов

<img src="https://github.com/user-attachments/assets/a7b40bc9-237d-442d-95fb-f913fe051cf7" width="135" height="293"> <img
src="https://github.com/user-attachments/assets/4846a952-8296-4b2c-9559-fb16d70f8e45" width="135" height="293"> <img
src="https://github.com/user-attachments/assets/8113c562-5f51-423f-92ec-7638ab7668ea" width="135" height="293"> <img
src="https://github.com/user-attachments/assets/8dc1f3e1-0111-488a-b92d-3898ca9b9392" width="135" height="293">

### Содержание файлов
Название    | Содержание 
-----------------|----------------------
