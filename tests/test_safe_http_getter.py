import pytest
from safe_http_client import http_get_json, safe_http_get_json

@pytest.mark.asyncio
async def test_get_url():
    response = await http_get_json("https://api.github.com/repos/vmg/redcarpet/issues?state=closed")
    assert isinstance(response, list)


@pytest.mark.asyncio
async def test_get_url():
    response = await safe_http_get_json("https://api.github.com/repos/vmg/redcarpet/issues?state=closed")
    assert isinstance(response, list)