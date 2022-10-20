import os
import httpx
import math
from typing import Union
from munch import munchify
from dotenv import dotenv_values
from .models import RatingResponse

dotfile = os.path.join(os.path.abspath(os.path.dirname(__file__)), '.env')
aries_env = dotenv_values(dotfile)

# aries base url
base = 'https://api.aerisapi.com'

def get_args(f='json', **kwargs):
    """pass in extra query string arguments"""
    CLIENT_ID = aries_env.get('AERIS_CLIENT_ID')
    CLIENT_SECRET = aries_env.get('AERIS_CLIENT_SECRET')
    extra = '&'.join(['='.join([k,v]) for k,v in kwargs.items()])
    b = f'format=json&client_id={CLIENT_ID}&client_secret={CLIENT_SECRET}'
    return '&'.join([b, extra]).rstrip('&')


async def get_current_conditions(location: str, **kwargs):
    """query the aeris weather api to fetch conditions for a given location

    Args:
        location (str): _description_

    Returns:
        _type_: _description_
    """
    
    url = f'{base}/conditions/summary/{location}?{get_args(**kwargs)}'
    
    async with httpx.AsyncClient() as client:
        r = await client.get(url)
        return munchify(r.json())


def normalize(v: Union[int, float], l: Union[int, float], h: Union[int, float]):
    return (v - l) / (h - l)

def get_temp_rating(t: float, ideal=75) -> float:
    """get a rating from 0-1, where 1 is ideal conditions. Rating deteriorates the further
    you get from ideal

    Args:
        t (float): the temp to test
        ideal (int, optional): the ideal temperature. Defaults to 75.

    Returns:
        float: _description_
    """
    if t < 45 or t >= 100:
        return 0.0
    if t < ideal:
        low = 45
        high = ideal
    else:
        low = ideal
        high = 100
    norm = normalize(t, low, high)
    return norm if t < ideal else 1 - norm

def get_wind_rating(w: float, temp: float, ideal=5) -> float:
    """gets the wind rating

    Args:
        s (float): wind value to check (in MPH)
        temp (float): the avg temp (in F)
        ideal (float): the ideal wind (in MPH)

    Returns:
        float: the rating on a 0-1 scale
    """
    if w < 5 and temp >= 85:
        # no wind is not quite ideal, still want a breeze
        return .8
    elif w > 20:
        return 0.0
    high = 20
    low = ideal
    return min(abs(1 - normalize(w, low, high)), 1)

def get_precip_rating(p: float) -> float:
    """gets the precipitation rating, dryer is better

    Args:
        p (float): precipitation value to check (in MM)

    Returns:
        float: the rating on a 0-1 scale
    """
    if p == 0:
        return 1.0
    elif p >= 4:
        return 0
    return 1 - normalize(p, 0, 4)

def get_dew_rating(d: float, temp: float) -> float:
    """gets the dew rating

    Args:
        d (float): dew point value to check (in F)
        temp (float): the avg temp (in F)

    Returns:
        float: the rating on a 0-1 scale
    """
    if temp >= 85 and d >= 60:
        # this is getting muggy, no thanks
        return 0.0

    ideal = 40
    high = 70
    if d < ideal:
        low = 0
    else:
        low = ideal

    return normalize(d, low, high)


async def get_golf_conditions(location: str) -> RatingResponse:
    """calculates a golf condition ranking from 1-5, based on weighted criteria

    https://theweatherprediction.com/habyhints2/606/

    # weights
    # 1. temp close to 72 degrees F, (25%)
    # 2. wind under 12 mph, lower the better (%30)
    # 3. precipitation (light: <.5mm/hr, mod: > .5 & < 4mm/hr, heavy, >4mm/hr) (30%)
    # 4. dew point, under 50 is comfortable lower the better (15%)

    # rank is round(weightedScore / 20)

    Args:
        location (str): a place or lat/lng

    Returns:
        int: the golf condition ranking
    """
    fields = [
        'loc', 
        'place', 
        'periods.timestamp',
        'periods.range', 
        'periods.precip', 
        'periods.temp', 
        'periods.dewpoint',
        'periods.windSpeed',
        'periods.weather.phrase',
        'periods.weather.primary'
    ]
    resp = await get_current_conditions(location, to='+6hours', fields=','.join(fields))
    conditions = resp.response[0]
    period = conditions.periods[0]

    # get condition elements
    tempF = period.temp.avgF
    windMph = period.windSpeed.avgMPH
    precipMM = period.precip.avgMM
    dewF = period.dewpoint.avgF

    # get temp ratings
    temp = get_temp_rating(tempF) * 25
    wind = get_wind_rating(windMph, tempF) * 30
    precip = get_precip_rating(precipMM) * 30
    dew = get_dew_rating(dewF, tempF) * 15

    # get rank
    rating = min(5, round(sum([temp, wind, precip, dew]) / 20))

    # return rating and other info
    return dict(
        scores=dict(
            temp=temp,
            wind=wind,
            precip=precip,
            dew=dew
        ),
        rating=rating,
        **conditions
    )
