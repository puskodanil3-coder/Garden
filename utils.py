import os
from config import print_error, BLUE, RESET


def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')


def confirm_exit():
    while True:
        answer = get_non_empty_string('Вы уверены? (да/нет)', 'Пожалуйста, введите "да" или "нет"')
        if answer == 'да':
            return True
        elif answer == 'нет':
            return False
        else:
            print_error('\nОшибка: попробуйте еще раз')


def pause_and_clear():
    input(f'{BLUE}\nНажмите Enter, чтобы вернуться в меню...{RESET}')
    clear_console()


def get_non_empty_string(prompt, error_message):
    while True:
        value = input(prompt).strip().lower()
        if value == '':
            print_error(error_message)
        else:
            return value


def get_positive_int(prompt, error_message):
    while True:
        plant_quantity = input(prompt).strip()
        if plant_quantity == '':
            print_error(error_message)
            continue
        try:
            number = int(plant_quantity)
        except ValueError:
            print_error(error_message)
            continue
        if number <= 0:
            print_error(error_message)
            continue
        return number


def get_int(prompt):
    while True:
        choice = input(prompt).strip()
        if choice == '':
            print_error('Поле не может быть пустым!')
            continue
        try:
            number = int(choice)
        except ValueError:
            print_error('Число должно быть целым!')
            continue
        return number


def is_garden_empty(garden, message):
    if not garden:
        print_error(message)
        return True
    return False