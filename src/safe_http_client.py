"""
     asyncio http client helper functions
"""
import json
from logging import getLogger
from aiohttp_requests import requests
from retry import retry

_logger = getLogger(__name__)


async def http_get_json(url):
    """http asyncio json getter"""
    response = await requests.get(url)
    if not isinstance(response.status, int):
        _logger.exception("internal error. wrong type status code %s", type(response.status_code))
        raise RuntimeError(f"wrong status code while fetching [{url}]")
    if not 300 > response.status >= 200:
        _logger.exception(
            "error fetching url [%s]. resp code=%d, body=%s", url, response.status, response.text()
        )
        raise RuntimeError(f"could not fetch data (status code={response.status})")
    response_json = await response.json()
    if not response_json:
        _logger.exception("could not parse json from url [%s], reply was %s", url, response.text())
        raise RuntimeError(f"wrong json reply from [{url}], (response was {response.text()})")
    _logger.info("successfully fetched json data from url [%s]", url)
    _logger.debug("fetched data is: \n{%s}", json.dumps(response_json, indent=4))
    return response_json


@retry(tries=6, backoff=2)
async def safe_http_get_json(url):
    """try really hard to fetch a json from a given url"""
    _logger.info("trying to fetch json data from [%s]", url)
    return await http_get_json(url)