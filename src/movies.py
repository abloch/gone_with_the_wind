"""
    the weather module
"""
from logging import getLogger
from sanic import Blueprint
from sanic.response import json
from sanic.exceptions import ServerError
from aiohttp_requests import requests
from custom_exceptions import NotFoundException

APP_KEY = "dce24c91"
BASE_URL = "http://www.omdbapi.com"

_logger = getLogger(__name__)
blueprint = Blueprint(__name__, url_prefix="/movies")


async def search_movies(needle, page_num):
    """search movies by title's needle"""
    url = f"{BASE_URL}/?s={needle}&type=movie&page=${page_num}&apikey={APP_KEY}"
    _logger.info("fetching %s", url)
    response = await requests.get(url)
    response_json = await response.json()
    if not response_json.get("Response") == "True":
        _logger.exception("wrong reply [%s]", response_json)
        raise NotFoundException(response_json.get("Error", f"error fetching {url}"))
    return response_json

def format_movies_list(movies_list):
    """formats the movies list"""
    return [
        {
            "title": movie.get("Title", "Unknown Title"),
            "id": movie.get("imdbID"),
            "poster_url": movie.get("Poster"),
            "year": movie.get("Year", "?"),
        }
        for movie in movies_list
    ]


def format_response(response, page_num, needle):
    """return a formatted list of movies"""
    if response.get("Response") == "True":
        movies_per_page = 10
        movies_in_this_page = len(response.get("Search"))
        total_matches = int(response.get("totalResults"))
        prev_page = page_num -1 if page_num > 1 else None
        next_page = page_num + 1 if total_matches > page_num*movies_per_page + movies_in_this_page else None
        return {
            "movies": format_movies_list(response.get("Search")),
            "metadata": {
                "total_count": total_matches,
                "current_count": movies_in_this_page,
                "current_page": page_num,
                "search_needle": needle,
                "prev_page": prev_page,
                "next_page": next_page,
            }
        }
    _logger.error("no Search in %s", response.keys())
    raise NotFoundException("could not find movies in")


@blueprint.route("/search/<needle>")
async def search(request, needle):
    """
        fethces the movies where the title matches for a given needle string
    """
    try:
        page_num = int(request.args.get("page", "1"))
        response = await search_movies(needle, page_num)
        return json(format_response(response, page_num, needle))

    except NotFoundException as error:
        _logger.exception(error)
        raise ServerError(error, status_code=404)

    except Exception as error:
        _logger.exception(error)
        raise ServerError("internal server error", status_code=500)
