from datetime import datetime
from config import print_info, TABLE_WIDTH, print_success, print_error
from utils import clear_console, get_non_empty_string, get_positive_int, pause_and_clear, is_garden_empty, get_int
from storage import load_garden, add_plant_in_db, delete_plant_in_db, update_name, update_quantity, search_plants_in_db, length_and_total_plant, max_and_min_plant, sort_quantity_increase_and_decrease, sort_date_increase_and_decrease


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


def search_plant():
    clear_console()
    plant_search = get_non_empty_string('\nКакое растение нужно найти?:', '\nНужно ввести название для поиска!')
    plant_list = search_plants_in_db(plant_search)
    found = False
    for plant in plant_list:
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


def plants_statistics():
    plant_list = load_garden()
    clear_console()
    if is_garden_empty(plant_list, 'Статистика недоступна: список растений пока пуст'):
        pause_and_clear()
        return True
    result_length_and_total = length_and_total_plant()
    length = result_length_and_total[0]
    total = result_length_and_total[1]
    print(f'Количество всех видов растений в саду: {length} шт.')
    print(f'\nКоличество всех растений в саду: {total} шт.')

    result_max_and_min = max_and_min_plant()
    plant_name_max = result_max_and_min[0]
    plant_max = result_max_and_min[1]
    plant_name_min = result_max_and_min[2]
    plant_min = result_max_and_min[3]
    print(f'\nСамое многочисленное растение в саду: {plant_name_max} - {plant_max} шт.')
    print(f'\nСамое малочисленное растение в саду: {plant_name_min} - {plant_min} шт.')
    pause_and_clear()


def sort_plants():
    plant_list = load_garden()
    if is_garden_empty(plant_list, 'нечего сортировать'):
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

        plants_increase_quantity, plants_decrease_quantity = sort_quantity_increase_and_decrease()
        plants_increase_date, plants_decrease_date = sort_date_increase_and_decrease()
        if choice == 1:
            sorted_garden = plants_increase_quantity
        elif choice == 2:
            sorted_garden = plants_decrease_quantity
        elif choice == 3:
            sorted_garden = plants_increase_date
        else:
            sorted_garden = plants_decrease_date
        if sorted_garden:
            display_plants(sorted_garden)
            pause_and_clear()
            break
