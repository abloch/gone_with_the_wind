"""
    the weather module
"""
from logging import getLogger
from sanic import Blueprint
from sanic.response import json
from sanic.exceptions import ServerError
from safe_http_client import safe_http_get_json
from custom_exceptions import NotFoundException


APP_ID = "c2152ce33eec94f628bcb40cda3da446"
BASE_URL = "https://api.openweathermap.org"

_logger = getLogger(__name__)
blueprint = Blueprint(__name__, url_prefix="/weather")


async def fetch_weather(city):
    """get weather for a prticular city"""
    url = f"{BASE_URL}/data/2.5/forecast?q={city}&units=metric&appid={APP_ID}"
    ret = await safe_http_get_json(url, acceptable_codes=[404, 200])
    if ret.get("message") == "city not found":
        raise NotFoundException("city not found")
    _logger.info("weather data was successfully fetched from %s", url)
    return ret


def get_icon_url(icon_code):
    """
        get the icon url
        https://openweathermap.org/weather-conditions
    """
    return f"http://openweathermap.org/img/wn/{icon_code}.png"

def format_forecast(raw_weather):
    """
        formats a single format line
        https://openweathermap.org/api/hourly-forecast
    """
    return {
        "date": raw_weather.get("dt"),
        "date_str": raw_weather.get("dt_txt"),
        "description": raw_weather.get("weather", {})[0].get("description"),
        "icon_url": get_icon_url(raw_weather.get("weather", {})[0].get("icon")),
        "min_temp": raw_weather.get("main", {}).get("temp_min"),
        "max_temp": raw_weather.get("main", {}).get("temp_max"),
        "feels_like": raw_weather.get("main", {}).get("feels_like"),
    }

def format_forecasts(raw_list):
    """
        parses the forecasts list
        https://openweathermap.org/api/hourly-forecast
    """
    return [format_forecast(i) for i in raw_list]

def format_city(raw_location):
    """
        formats the location
        https://openweathermap.org/api/hourly-forecast
    """
    return {
        "city": raw_location.get("name"),
        "country": raw_location.get("country"),
    }

def format_response(raw_response):
    """the general method formatter"""
    return {
        "city": format_city(raw_response.get("city", {})),
        "forecast": format_forecasts(raw_response.get("list"))
    }

@blueprint.route("/city/<city>")
async def weather(_, city):
    """
        fethces the forecast for a given city
    """
    try:
        response = await fetch_weather(city)
        return json(format_response(response))

    except NotFoundException as error:
        _logger.exception(error)
        return json({"error": "city was not found", "city": city})

    except Exception as error:
        _logger.exception("error %s getting weather for %s", error, city)
        raise ServerError(f"could not get weather for {city}. please try again later")
