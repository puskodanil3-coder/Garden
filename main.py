from storage import load_garden, save_garden, export_to_txt, init_db
from config import FILE_PATH, print_success, print_error
from utils import get_int, clear_console, confirm_exit
from garden import add_plant, search_plant, show_plants, delete_plant, edit_plant, plants_statistics, sort_plants 


def run():
    try:
        init_db()
        while True:
            print('\n---Меню---')
            print('1 - Добавить растение')
            print('2 - Поиск растения')
            print('3 - Вывести весь список растений')
            print('4 - Удалить растение')
            print('5 - Изменить данные об растении')
            print('6 - Показать статистику')
            print('7 - Сортировка')
            print('8 - Экспорт в txt')
            print('0 - Выход')

            choice = get_int('\nВведите:')
            if choice == 1:
                add_plant(garden)
                continue

            elif choice == 2:
                search_plant(garden)
                continue

            elif choice == 3:
                show_plants(garden)
                continue

            elif choice == 4:
                if delete_plant(garden):
                    continue

            elif choice == 5:
                if edit_plant(garden):
                    continue

            elif choice == 6:
                if plants_statistics(garden):
                    continue

            elif choice == 7:
                if sort_plants(garden):
                    continue

            elif choice == 8:
                if export_to_txt(garden):
                    continue

            elif choice == 0:
                if confirm_exit():
                    print_success('\nПрограмма завершена')
                    break

        save_garden(FILE_PATH, garden)

    except KeyboardInterrupt:
        clear_console()
        print_error('Программа прервана!')
        print_success('\nДанные сохранены.')


if __name__ == '__main__':
    run()