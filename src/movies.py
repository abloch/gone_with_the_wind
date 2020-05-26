"""
    the weather module
"""
from logging import getLogger
from sanic import Blueprint
from sanic.response import json
from sanic.exceptions import ServerError
from safe_http_client import safe_http_get_json
from custom_exceptions import NotFoundException

APP_KEY = "dce24c91"
BASE_URL = "http://www.omdbapi.com"

_logger = getLogger(__name__)
blueprint = Blueprint(__name__, url_prefix="/movies")


async def search_movies(needle, page_num):
    """search movies by title's needle"""
    url = f"{BASE_URL}/?s={needle}&type=movie&page=${page_num}&apikey={APP_KEY}"
    ret = await safe_http_get_json(url)
    _logger.info("movies data was successfully fetched from %s", url)
    return ret


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
        pages_so_far = page_num*movies_per_page + movies_in_this_page
        next_page = page_num + 1 if total_matches > pages_so_far else None
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
    raise NotFoundException(f"could not find movies in {needle}")


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
        raise ServerError("movie not found", status_code=404)

    except Exception as error:
        _logger.exception(error)
        raise ServerError("error fetching movies. please try again later", status_code=500)
