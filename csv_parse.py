import csv


def parse_result(result_path):
    """
    Парсит csv файл и возращает строки и столбцы
    """
    rows = []

    # Читаем CSV
    with open(result_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)

        for row in reader:
            rows.append([cell.strip() for cell in row])

    # Считаем максимальное число колонок
    max_cols = max((len(row) for row in rows), default=0)
    
    # Назначаем поля: Col 1, Col 2, ..., Col N
    fields = [f"Col {i+1}" for i in range(max_cols)]

    # Дополняем короткие строки пустыми ячейками
    for i in range(3, len(rows)):
        while len(rows[i]) < max_cols:
            rows[i].append("")

    return fields, rows