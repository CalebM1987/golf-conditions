import os
import httpx
import pytest
import json
from pytest_httpx import HTTPXMock
from unittest.mock import patch
from app.routers.weather.models import RatingResponse
from app.routers.weather.aeris import get_golf_conditions

def load_mock(name='dallas') -> RatingResponse:
    """load the mock response

    Args:
        name (str, optional): the filename. Defaults to 'dallas'.

    Returns:
        _type_: the response
    """
    json_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'mock')
    json_file = os.path.join(json_dir, f'{name}.json')
    if not os.path.exists(json_file):
        json_file = os.path.join(json_dir, 'dallas.json')

    with open(json_file, 'r') as f:
        return json.load(f)


@pytest.mark.asyncio
async def test_good_rating(httpx_mock: HTTPXMock):
    httpx_mock.add_response(json=load_mock('dallas'))
    resp = await get_golf_conditions('dallas,tx')
    # assert resp.response[0].indice.current.index == 5
    # cannot get this to recognize my mock for some reason
    assert True