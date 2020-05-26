import os
import json
import asyncio
from application import app
from safe_http_client import http_get_json
from unittest.mock import MagicMock, patch


current_path= os.path.dirname(os.path.abspath(__file__))


FAKE_REPLY = json.load(open("{}/fixtures/fake_response.json".format(current_path)))
FAKE_BAD_REPLY = json.load(open("{}/fixtures/fake_bad_response.json".format(current_path)))

future_reply = asyncio.Future()
future_reply.set_result(FAKE_REPLY)
future_bad_reply = asyncio.Future()
future_bad_reply.set_result(FAKE_BAD_REPLY)

@patch('weather.fetch_weather', MagicMock(return_value=future_reply))
def test_weather_passing_city_returns_200():
    request, response = app.test_client.get('/weather/city/real_city')
    assert response.status == 200
    assert "city" in response.json
    assert "forecast" in response.json
    assert isinstance(response.json['forecast'], list)

@patch('weather.fetch_weather', MagicMock(return_value=future_bad_reply))
def test_weather_failing_city_returns_500():
    request, response = app.test_client.get('/weather/city/real_city')
    assert response.status == 500
    assert "try again" in response.text
