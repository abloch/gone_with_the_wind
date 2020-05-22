from aioresponses import aioresponses
from application import app

def test_weather_real_city_returns_200():
    request, response = app.test_client.get('/weather/Jerusalem')
    assert response.status == 200

def test_weather_unreal_city_returns_200():
    request, response = app.test_client.get('/weather/Jerm')
    assert response.status == 404
