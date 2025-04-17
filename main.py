from main_candidate import main_candidate
from main_hr import main_hr

while True:
    num_status = int(input(
        'Введите число, соотвествующее вашему статусу (Рекрутер - 1, Соискатель - 2): '))
    if num_status < 3 and num_status > 0:
        break
    else:
        print('Неправильный ввод. Попробуйте еще раз')

if num_status == 1:
    main_hr()
elif num_status == 2:
    main_candidate()