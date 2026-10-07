from datetime import datetime
from config import print_info, TABLE_WIDTH, print_success, FILE_PATH, print_error
from utils import clear_console, get_non_empty_string, get_positive_int, pause_and_clear, is_garden_empty, get_int
from storage import load_garden, add_plant_in_db, delete_plant_in_db, update_name, update_quantity


def display_plants(plant_list):
    print_info('\nСписок растений в саду:')
    print(f"\n{'ID':>3} {'Название':<20} {'Количество':>12} {'Дата':>12}")
    print("-" * TABLE_WIDTH)
    for plant in (plant_list):
        print(f"{plant['id']:>3} {plant['name']:<20} {plant['quantity']:>12} {plant['date']:>12}")
    print("-" * TABLE_WIDTH)


def add_plant():
    clear_console()
    plant_name = get_non_empty_string('\nВведите название растения: ', '\nВведите название для добавления растения!')
    plant_quantity = get_positive_int('\nВведите количество растений:', '\nНужно ввести количество растений!')
    today = datetime.today().strftime('%d.%m.%Y')
    add_plant_in_db(plant_name, plant_quantity, today)
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


def show_plants():
    clear_console()
    plant_list = load_garden()
    if not plant_list:
        print_info('\nСписок растений пока пуст')
    else:
        display_plants(plant_list)
    pause_and_clear()


def delete_plant():
    clear_console()
    plant_list = load_garden()
    if is_garden_empty(plant_list, 'нечего удалять'):
        pause_and_clear()
        return True
    while True:
        found = False
        display_plants(plant_list)
        del_plant = get_int('Введите номер растения для удаления:')
        for plant in plant_list:
            if del_plant == plant['id']:
                found = True
                del_plants = get_non_empty_string('Уверены? (да/нет)', 'Введите "да" или "нет"!')
                if del_plants == 'да':
                    deleted_name = plant['name']
                    delete_plant_in_db(del_plant)
                    print_success(f"Растение '{deleted_name}' удалено.")
                    pause_and_clear()
                    return
                elif del_plants == 'нет':
                    break
        if not found:
            print_error('Ошибка, введите номер растения из списка')


def edit_plant():
    clear_console()
    plant_list = load_garden()
    if is_garden_empty(plant_list, 'нечего редактировать'):
        pause_and_clear()
        return True
    while True:
        found = False
        display_plants(plant_list)
        plant_id = get_int('Введите номер растения для изменения:')
        for plant in plant_list:
            if plant['id'] == plant_id:
                found = True
                action = get_int('Чтобы изменить название/количество растения введите 1/2')
                if action == 1:
                    up_name = get_non_empty_string('Введите новое названия растения:',
                                               'Нужно ввести новое названия растения!')
                    update_name(up_name, plant_id)
                    print_success(f"Растение изменено на {up_name}.")
                    return
                elif action == 2:
                    up_quantity = get_positive_int('Введите новое количество растения:',
                                               '\nНужно ввести количество растений!')
                    update_quantity(up_quantity, plant_id)
                    print_success(f"Количество растения изменено на {up_quantity}")
                    return
                else:
                    print_error('Введите "1" или "2" ')
        if not found:
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
