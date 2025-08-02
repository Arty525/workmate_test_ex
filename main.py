import argparse
import sys
from tabulate import tabulate
from src.reports import average


def table_view(report_data):
    """Выводит результат отчета в виде таблицы в консоль"""
    table_data = []

    for handler, stat in report_data.items():
        row = {"handler": handler}
        row.update(stat)
        table_data.append(row)

    print(tabulate(table_data, headers="keys", tablefmt="simple", showindex=True))


if __name__ == "__main__":
    try:
        parser = argparse.ArgumentParser()
        parser.add_argument("--file", help="Файл для обработки")
        parser.add_argument("--report", help="Тип отчета")

        args = parser.parse_args()

        reports = [
            "average",
        ]  # Список доступных отчетов

        if args.report not in reports:
            # Если введенный пользователем отчет отсутствует в списке выводим сообщение в консоль
            print(f"Отчета с именем {args.report} не существует")
            sys.exit(1)

        if args.report == "average":
            table_view(average(args.file))

    except FileNotFoundError:
        print(f"Файл с именем {args.file} не найден")
