import os
import httpx
import pytest
import json
from pytest_httpx import HTTPXMock
from unittest.mock import patch
from app.routers.weather.models import RatingResponse
from app.routers.weather.aeris import get_golf_conditions, get_args
from munch import munchify

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
        return munchify(json.load(f))


def test_get_args():
    params = get_args(to='+6hours')
    assert len(params.keys()) == 4

@pytest.mark.asyncio
async def test_good_rating(httpx_mock: HTTPXMock):
    httpx_mock.add_response(json=load_mock('dallas'))
    resp = await get_golf_conditions('dallas,tx')
    assert resp.response[0].indice.current.index == 5

@pytest.mark.asyncio
async def test_good_rating_reversed(httpx_mock: HTTPXMock):
    httpx_mock.add_response(json=load_mock('dallas'))
    resp = await get_golf_conditions('dallas,tx', reverse=True)
    assert resp.response[0].indice.current.index == 1

@pytest.mark.asyncio
async def test_fair_rating(httpx_mock: HTTPXMock):
    httpx_mock.add_response(json=load_mock('echo'))
    resp = await get_golf_conditions('echo,or')
    assert resp.response[0].indice.current.index == 3

@pytest.mark.asyncio
async def test_poor_conditions(httpx_mock: HTTPXMock):
    httpx_mock.add_response(json=load_mock('pleasant-valley'))
    resp = await get_golf_conditions('pleasant valley,ak')
    assert resp.response[0].indice.current.index == 1
    