import os
import json
import asyncio
from application import app
from unittest.mock import MagicMock, patch


current_path= os.path.dirname(os.path.abspath(__file__))


FAKE_REPLY = json.load(open("{}/fixtures/fake_movies.json".format(current_path)))
FAKE_BAD_REPLY = json.load(open("{}/fixtures/fake_bad_movies.json".format(current_path)))

future_reply = asyncio.Future()
future_reply.set_result(FAKE_REPLY)

future_bad_reply = asyncio.Future()
future_bad_reply.set_result(FAKE_BAD_REPLY)

future_empty_reply = asyncio.Future()
future_empty_reply.set_result(None)

@patch('movies.search_movies', MagicMock(return_value=future_reply))
def test_movies_found_returns_200():
    request, response = app.test_client.get('/movies/search/movie')
    assert response.status == 200
    assert "metadata" in response.json
    assert "movies" in response.json
    assert isinstance(response.json['movies'], list)


@patch('movies.search_movies', MagicMock(return_value=future_bad_reply))
def test_movies_unfound_returns_404():
    request, response = app.test_client.get('/movies/search/movie')
    assert response.status == 404
    assert "not found" in response.text


@patch('movies.search_movies', MagicMock(return_value=future_empty_reply))
def test_movies_empty_returns_500():
    request, response = app.test_client.get('/movies/search/movie')
    assert response.status == 500
    assert "try again" in response.text
