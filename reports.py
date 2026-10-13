from db import get_all_plants, length_and_total_plant, max_and_min_plant
from config import TABLE_WIDTH, print_success
from utils import pause_and_clear, is_garden_empty, clear_console


def export_to_txt():
    plant_list = get_all_plants()
    if is_garden_empty(plant_list, 'нечего экспортировать'):
        pause_and_clear()
        return True
    with open('garden_report.txt', 'w', encoding='utf-8') as f:
        f.write('Список растений в саду:\n')
        f.write("-" * TABLE_WIDTH+ "\n")
        f.write(f"\n{'№':>3} {'Название':<20} {'Количество':>12} {'Дата':>12}\n")
        for number, plant in enumerate(plant_list, start=1):
            f.write(f"{number:>3} {plant['name']:<20} {plant['quantity']:>12} {plant['date']:>12}\n")
        f.write("-" * TABLE_WIDTH+ "\n")
        length, total = length_and_total_plant()
        f.write(f'\nКоличество всех видов растений в саду: {length} шт.')
        f.write(f'\nКоличество всех растений в саду: {total} шт.')

        plant_name_max, plant_max, plant_name_min, plant_min = max_and_min_plant()
        f.write(f'\nСамое многочисленное растение в саду: {plant_name_max} - {plant_max} шт.')
        f.write(f'\nСамое малочисленное растение в саду: {plant_name_min} - {plant_min} шт.')

    clear_console()
    print_success('Экспорт успешно завершен')
    pause_and_clear()
