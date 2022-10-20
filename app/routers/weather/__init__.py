from fastapi import APIRouter, Request, Path, Depends
from .aeris import get_current_conditions, get_golf_conditions
from .models import RatingResponse, ReverseIndexes, WeatherConditionsResponse

weather = APIRouter()

@weather.get('/weather/{loc}', response_model=WeatherConditionsResponse, tags=['weather'])
async def get_weather(loc: str='minneapolis,mn'):
    """fetch weather conditions at a given location"""
    resp = await get_current_conditions(loc)
    return resp.get('response', [])[0]

@weather.get('/golf-conditions/{loc}', tags=['weather'], response_model=RatingResponse)
async def golf_conditions(loc: str='minneapolis,mn', params: ReverseIndexes = Depends()):
    """fetch conditions for golfing at a given location"""
    return await get_golf_conditions(loc, **params.dict())
