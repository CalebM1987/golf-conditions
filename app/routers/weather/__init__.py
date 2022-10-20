import os
import json
from fastapi import APIRouter, Request, Path
from .aeris import get_current_conditions, get_golf_conditions
from .models import RatingResponse

weather = APIRouter()

@weather.get('/weather/{loc}', tags=['weather'])
async def get_weather(loc: str='minneapolis,mn'):
    resp = await get_current_conditions(loc)
    return resp

@weather.get('/golf-conditions/{loc}', tags=['weather'], response_model=RatingResponse)
async def golf_conditions(loc: str):
    return await get_golf_conditions(loc)
