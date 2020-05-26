import os
import re
import json
import pytest
from aioresponses import aioresponses
from application import app

current_path= os.path.dirname(os.path.abspath(__file__))


FAKE_REPLY = json.load(open("{}/fixtures/fake_response.json".format(current_path)))
FAKE_BAD_REPLY = json.load(open("{}/fixtures/fake_bad_response.json".format(current_path)))

def test_weather_real_city_returns_200():
    with aioresponses() as mocked:
        mocked.get(re.compile(r'https://api.openweathermap.org.*'), status=200, payload=FAKE_REPLY)
        request, response = app.test_client.get('/weather/city/real_city')
        assert response.status == 200
        assert len(mocked.requests)==1

def test_weather_unreal_city_fails():
    with aioresponses() as mocked:
        mocked.get(re.compile(r'https://api.openweathermap.org.*'), status=404, payload=FAKE_BAD_REPLY)
        request, response = app.test_client.get('/weather/city/fake_city')
        assert response.status == 500
        assert len(mocked.requests)==1