"""
     asyncio http client helper functions
"""
import json
from logging import getLogger
from aiohttp_requests import requests
from tenacity import retry, stop_after_delay, wait_fixed

_logger = getLogger(__name__)




async def http_get_json(url, acceptable_codes=None):
    """http asyncio json getter"""
    response = await requests.get(url)

    if not isinstance(response.status, int):
        _logger.exception("internal error. wrong type status code %s", type(response.status_code))
        raise RuntimeError(f"wrong status code while fetching [{url}]")

    if acceptable_codes:
        if response.status not in acceptable_codes:
            _logger.exception(
                "error fetching url [%s]. resp code=%d not in [%s], body=%s",
                url, response.status, acceptable_codes, response.text()
            )
            raise RuntimeError(f"could not fetch data (status code={response.status})")

    else:
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


@retry(stop=stop_after_delay(8), wait=wait_fixed(2))  # retry up to 8 seconds, 2 seconds delay between attempts
async def safe_http_get_json(url, acceptable_codes=None):
    """try really hard to fetch a json from a given url"""
    _logger.info("trying to fetch json data from [%s]", url)
    return await http_get_json(url, acceptable_codes=acceptable_codes)
