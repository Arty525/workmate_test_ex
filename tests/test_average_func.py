import json
import sys
from pathlib import Path
import pytest
from unittest.mock import patch, mock_open

sys.path.append(str(Path(__file__).parent.parent))
from src.reports import average


@pytest.fixture
def sample_logs():
    '''Тестовые данные'''
    return [
        {"@timestamp": "2025-06-22T13:57:32+00:00", "status": 200, "url": "/api/users",
         "request_method": "GET", "response_time": 0.024, "http_user_agent": "Mozilla/5.0"},
        {"@timestamp": "2025-06-22T13:57:33+00:00", "status": 200, "url": "/api/products",
         "request_method": "GET", "response_time": 0.018, "http_user_agent": "curl/7.68.0"},
        {"@timestamp": "2025-06-22T13:57:34+00:00", "status": 404, "url": "/api/users",
         "request_method": "GET", "response_time": 0.012, "http_user_agent": "Mozilla/5.0"},
        {"@timestamp": "2025-06-22T13:57:35+00:00", "status": 200, "url": "/api/orders",
         "request_method": "POST", "response_time": 0.042, "http_user_agent": "PostmanRuntime/7.28.4"},
        {"@timestamp": "2025-06-22T13:57:36+00:00", "status": 500, "url": "/api/products",
         "request_method": "GET", "response_time": 0.095, "http_user_agent": "Mozilla/5.0"},
        {"@timestamp": "2025-06-22T13:57:37+00:00", "status": 200, "url": "/api/users",
         "request_method": "GET", "response_time": 0.022, "http_user_agent": "curl/7.68.0"},
        {"@timestamp": "2025-06-22T13:57:38+00:00", "status": 200, "url": "/api/orders",
         "request_method": "POST", "response_time": 0.038, "http_user_agent": "PostmanRuntime/7.28.4"},
        {"@timestamp": "2025-06-22T13:57:39+00:00", "status": 200, "url": "/api/products",
         "request_method": "GET", "response_time": 0.015, "http_user_agent": "Mozilla/5.0"},
        {"@timestamp": "2025-06-22T13:57:40+00:00", "status": 404, "url": "/api/users",
         "request_method": "GET", "response_time": 0.011, "http_user_agent": "curl/7.68.0"},
        {"@timestamp": "2025-06-22T13:57:41+00:00", "status": 200, "url": "/api/orders",
         "request_method": "POST", "response_time": 0.045, "http_user_agent": "PostmanRuntime/7.28.4"}
    ]


@pytest.fixture
def average_results():
    '''Ожидаемый результат обработки тестовых данных'''
    return {
        "/api/users": {
            "total": 4,
            "avg_response_time": 0.0173
        },
        "/api/products": {
            "total": 3,
            "avg_response_time": 0.0427
        },
        "/api/orders": {
            "total": 3,
            "avg_response_time": 0.0417
        }
    }


def test_average(sample_logs, average_results):
    mock_file_content = "\n".join(json.dumps(item) for item in sample_logs)

    m = mock_open(read_data=mock_file_content)

    with patch("builtins.open", m):
        result = average("fake_path.json")

    assert result == average_results
