from datetime import datetime
from config import print_info, TABLE_WIDTH, print_success, FILE_PATH, print_error
from utils import clear_console, get_non_empty_string, get_positive_int, pause_and_clear, is_garden_empty, get_int
from storage import save_garden

def display_plants(garden):
    print_info('\nСписок растений в саду:')
    print(f"\n{'№':>3} {'Название':<20} {'Количество':>12} {'Дата':>12}")
    print("-" * TABLE_WIDTH)
    for number, plant in enumerate(garden, start=1):
        print(f"{number:>3} {plant['name']:<20} {plant['quantity']:>12} {plant['date']:>12}")
    print("-" * TABLE_WIDTH)


def add_plant(garden):
    clear_console()
    plant_name = get_non_empty_string('\nВведите название растения: ', '\nВведите название для добавления растения!')
    plant_quantity = get_positive_int('\nВведите количество растений:', '\nНужно ввести количество растений!')
    today = datetime.today().strftime('%d.%m.%Y')
    garden_dict = {'name': plant_name, 'quantity': plant_quantity, 'date': today}
    garden.append(garden_dict)
    save_garden(FILE_PATH, garden)
    print_success('\nУспешно добавлено!')
    pause_and_clear()


def search_plant(garden):
    clear_console()
    plant_search = get_non_empty_string('\nКакое растение нужно найти?:', '\nНужно ввести название для поиска!')
    found = False
    for plant in garden:
        if plant_search in plant['name']:
            print(f"{plant['name']} - {plant['quantity']} шт. (добавлено {plant['date']})")
            found = True
    if not found:
        print_info('\nРастение не найдено')
    pause_and_clear()


def show_plants(garden):
    clear_console()
    if not garden:
        print_info('\nСписок растений пока пуст')
    else:
        display_plants(garden)
    pause_and_clear()


def delete_plant(garden):
    clear_console()
    if is_garden_empty(garden, 'нечего удалять'):
        pause_and_clear()
        return True
    while True:
        display_plants(garden)
        del_plant = get_int('Введите номер растения для удаления:')
        if 1 <= del_plant <= len(garden):
            index = del_plant - 1
            del_plants = get_non_empty_string('Уверены? (да/нет)', 'Введите "да" или "нет"!')
            if del_plants == 'да':
                deleted_name = garden[index]['name']
                del garden[index]
                print_success(f"Растение '{deleted_name}' удалено.")
                save_garden(FILE_PATH, garden)
                break
            elif del_plants == 'нет':
                break
            else:
                print_error('Введите "да" или "нет"')
        else:
            print_error('Ошибка, введите номер растения из списка')
    pause_and_clear()


def edit_plant(garden):
    clear_console()
    if is_garden_empty(garden, 'нечего редактировать'):
        pause_and_clear()
        return True
    while True:
        display_plants(garden)
        plant_index = get_int('Введите номер растения для изменения:')
        if 1 <= plant_index <= len(garden):
            idx = plant_index - 1
            action = get_int('Чтобы изменить название/количество растения введите 1/2')
            if action == 1:
                up_name = get_non_empty_string('Введите новое названия растения:',
                                               'Нужно ввести новое названия растения!')
                garden[idx]['name'] = up_name
                print_success(f"Растение изменено на {up_name}.")
                save_garden(FILE_PATH, garden)
                break
            elif action == 2:
                up_quantity = get_positive_int('Введите новое количество растения:',
                                               '\nНужно ввести количество растений!')
                garden[idx]['quantity'] = up_quantity
                print_success(f"Количество растения изменено на {up_quantity}")
                save_garden(FILE_PATH, garden)
                break
            else:
                print_error('Введите "1" или "2" ')
        else:
            print_error('Ошибка: введите номер растения из списка!')
    pause_and_clear()


def plants_statistics(garden):
    clear_console()
    if is_garden_empty(garden, 'Статистика недоступна: список растений пока пуст'):
        pause_and_clear()
        return True
    length = len(garden)
    print(f'Количество всех видов растений в саду: {length} шт.')
    total = sum(plant['quantity'] for plant in garden)
    print(f'\nКоличество всех растений в саду: {total} шт.')

    max_plant = max(garden, key=lambda plant: plant['quantity'])
    # Исправлены кавычки внутри f-строки (одинарные -> двойные или экранирование)
    print(f'\nСамое многочисленное растение в саду: {max_plant["name"]} - {max_plant["quantity"]} шт.')

    min_plant = min(garden, key=lambda plant: plant['quantity'])
    print(f'\nСамое малочисленное растение в саду: {min_plant["name"]} - {min_plant["quantity"]} шт.')
    pause_and_clear()


def sort_plants(garden):
    if is_garden_empty(garden, 'нечего сортировать'):
        pause_and_clear()
        return True
    clear_console()
    print('Выберите тип сортировки:')
    print('1 - сортировка по количеству (возрастание)')
    print('2 - сортировка по количеству (убывание)')
    print('3 - сортировка по дате (возрастание)')
    print('4 - сортировка по дате (убывание)')

    while True:
        choice = get_int('\nВведите:')
        if choice not in (1, 2, 3, 4):
            print_error('Ошибка: выберите число от 1 до 4')
            continue


        if choice == 1:
            sorted_garden = sorted(garden, key=lambda value: value['quantity'])
        elif choice == 2:
            sorted_garden = sorted(garden, reverse=True, key=lambda value: value['quantity'])
        elif choice == 3:
            sorted_garden = sorted(garden, key=lambda value: datetime.strptime(value['date'], '%d.%m.%Y'))
        elif choice == 4:
            sorted_garden = sorted(garden, reverse=True, key=lambda value: datetime.strptime(value['date'], '%d.%m.%Y'))
        if sorted_garden:
            display_plants(sorted_garden)
            pause_and_clear()
            break
