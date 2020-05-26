import pytest
import aresponses 
from safe_http_client import http_get_json, safe_http_get_json


@pytest.mark.asyncio
async def test_get_url_fails():
    with pytest.raises(Exception):
        response = await http_get_json("http://trililili")


@pytest.mark.asyncio
async def test_mocked_error_response(aresponses):
    aresponses.add("blabla", "/api/v1", "GET", response={"status": "ok"})
    response = await http_get_json('http://blabla/api/v1')
    assert "status" in response
    aresponses.assert_called_in_order()


@pytest.mark.asyncio
async def test_safe_mocked_error_response_eventually_passes(aresponses):
    # first try will fail - second try will pass. should pass
    aresponses.add("blabla", "/", "GET", aresponses.Response(status=500, text="Error"), repeat=1)
    aresponses.add("blabla", "/", "GET", response={"status": "ok"})
    response = await safe_http_get_json('http://blabla/')
    assert "status" in response
    aresponses.assert_called_in_order()
    

@pytest.mark.asyncio
async def test_safe_mocked_error_response_eventually_fails(aresponses):
    # first try will fail - second try will pass. should pass
    aresponses.add("blabla", "/", "GET", aresponses.Response(status=500, text="Error"))
    with pytest.raises(Exception):
        response = await safe_http_get_json('http://blabla/')
    aresponses.assert_called_in_order()