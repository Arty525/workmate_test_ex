import json


def average(file: str) -> dict:
    """Подсчитывает количество запросов к эндпоинтам и среднее время запроса"""
    result = {}

    with open(file, "r", encoding="utf-8") as f:
        # Открываем файл для чтения логов
        for line in f:
            json_data = json.loads(line)  # преобразуем каждую строку в формат json

            if (
                result.get(json_data["url"]) is None
            ):  # Проверяем наличие этого эндпоинта в итоговом словаре
                result[json_data["url"]] = {}

            # Проверяем наличие поля total в итоговом словаре для текущего эндпоинта
            if result.get(json_data["url"]).get("total") is None:
                result[json_data["url"]]["total"] = 1
            else:
                result[json_data["url"]]["total"] = (
                    result[json_data["url"]]["total"] + 1
                )

            # Проверяем наличие поля total_response_time в итоговом словаре для текущего эндпоинта
            # Поле необходимо для подсчета среднего времени запроса
            if result[json_data["url"]].get("total_response_time") is None:
                result[json_data["url"]]["total_response_time"] = json_data[
                    "response_time"
                ]
            else:
                result[json_data["url"]]["total_response_time"] += json_data[
                    "response_time"
                ]

            # Подсчитываем среднее время запроса
            result[json_data["url"]]["avg_response_time"] = round(
                result[json_data["url"]]["total_response_time"]
                / result[json_data["url"]]["total"],
                4,
            )

        # Удаляем лишне поле total_response_time
        for value in result.values():
            del value["total_response_time"]

    return result
