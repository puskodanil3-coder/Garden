import json
from config import TABLE_WIDTH, print_error, print_success
from utils import pause_and_clear, is_garden_empty, clear_console


def load_garden(filepath, default):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return default


def save_garden(filepath, garden):
    try:
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(garden, f, ensure_ascii=False, indent=4)
    except OSError:
        print_error('Ошибка сохранения: диск переполнен или у вас нет прав!')


def export_to_txt(garden):
    if is_garden_empty(garden, 'нечего экспортировать'):
        pause_and_clear()
        return True
    with open('garden_report.txt', 'w', encoding='utf-8') as f:
        f.write('Список растений в саду:\n')
        f.write("-" * TABLE_WIDTH+ "\n")
        f.write(f"\n{'№':>3} {'Название':<20} {'Количество':>12} {'Дата':>12}\n")

        for number, plant in enumerate(garden, start=1):
            f.write(f"{number:>3} {plant['name']:<20} {plant['quantity']:>12} {plant['date']:>12}\n")
        f.write("-" * TABLE_WIDTH+ "\n")
        length = len(garden)
        f.write(f'\nКоличество всех видов растений в саду: {length} шт.')
        total = sum(plant['quantity'] for plant in garden)
        f.write(f'\nКоличество всех растений в саду: {total} шт.')

        max_plant = max(garden, key=lambda plant: plant['quantity'])
        f.write(f'\nСамое многочисленное растение в саду: {max_plant["name"]} - {max_plant["quantity"]} шт.')

        min_plant = min(garden, key=lambda plant: plant['quantity'])
        f.write(f'\nСамое малочисленное растение в саду: {min_plant["name"]} - {min_plant["quantity"]} шт.')
        
    clear_console()
    print_success('Экспорт успешно завершен')
    pause_and_clear()
