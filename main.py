import argparse
import json
import sys

from tabulate import tabulate

def average():
    result = {}

    if args.report == 'average':
        with open(args.file, 'r', encoding='utf-8') as f:
            for line in f:
                json_data = json.loads(line)
                if result.get(json_data['url']) is None:
                    result[json_data['url']] = {}
                if result.get(json_data['url']).get('total') is None:
                    result[json_data['url']]['total'] = 1
                else:
                    result[json_data['url']]['total'] = result[json_data['url']]['total'] + 1
                result[json_data['url']]['avg_response_time'] = json_data['response_time'] / result[json_data['url']]['total']

    table_data = []
    for handler, stat in result.items():
        row = {"handler": handler}
        row.update(stat)
        table_data.append(row)

    print(tabulate(table_data, headers="keys", tablefmt="simple", showindex=True))


if __name__ == "__main__":
    try:
        parser = argparse.ArgumentParser(description='Пример использования argparse')
        parser.add_argument('--file', help='Файл для обработки')
        parser.add_argument('--report', help='Тип отчета')

        args = parser.parse_args()

        reports = ['average',]

        if args.report not in reports:
            print(f'Отчета с именем {args.report} не существует')
            sys.exit(1)

        if args.report == 'average':
            average()

    except FileNotFoundError as fe:
        print(f'Файл с именем {args.file} не найден')
