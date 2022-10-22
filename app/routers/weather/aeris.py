import os
import httpx
import math
from typing import Union, List
from munch import munchify
from dotenv import dotenv_values
from .models import RatingResponse, WeatherConditionsResponse
from .ratings import *
from app.utils import get_timestamp, from_milliseconds

dotfile = os.path.join(os.path.abspath(os.path.dirname(__file__)), '.env')
aries_env = dotenv_values(dotfile)

# aries base url
base = 'https://api.aerisapi.com'

def get_args(f='json', fields: Union[str, List[str]]=None, **kwargs):
    """pass in extra query string arguments"""
    CLIENT_ID = aries_env.get('AERIS_CLIENT_ID')
    CLIENT_SECRET = aries_env.get('AERIS_CLIENT_SECRET')
    params = dict(
        f=f,
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        **kwargs
    )

    # validate fields
    if fields:
        if isinstance(fields, list):
            fields = ','.join(fields)
        params['fields'] = fields 
   
    return params

RATING_CATEGORIES = ['bad', 'poor', 'good', 'very good', 'excellent']
RATINGS = dict((i+1, c) for i,c in enumerate(RATING_CATEGORIES))
RATINGS_REVERSED = dict((i+1, c) for i,c in enumerate(RATING_CATEGORIES[::-1]))

# filters for weather fields
weather_fields =  [
        'loc', 
        'place', 
        'periods.timestamp',
        'periods.dateTimeISO',
        'periods.range', 
        'periods.precip', 
        'periods.temp', 
        'periods.dewpoint',
        'periods.windSpeed',
        'periods.weather.phrase',
        'periods.weather.primary',
        'profile.tz'
    ]

async def get_current_conditions(location: str, **kwargs) -> WeatherConditionsResponse:
    """query the aeris weather api to fetch conditions for a given location

    Args:
        location (str): _description_

    Returns:
        _type_: _description_
    """
    kwargs['fields']= weather_fields

    url = f'{base}/conditions/summary/{location}'
    
    async with httpx.AsyncClient() as client:
        r = await client.get(url, params=get_args(**kwargs))
        return munchify(r.json())


async def get_golf_conditions(location: str, reverse=False) -> RatingResponse:
    """calculates a golf condition ranking from 1-5, based on weighted criteria

    https://theweatherprediction.com/habyhints2/606/

    # weights
    # 1. temp close to 72 degrees F, (25%)
    # 2. wind under 12 mph, lower the better (%30)
    # 3. precipitation (light: <.5mm/hr, mod: > .5 & < 4mm/hr, heavy, >4mm/hr) (30%)
    # 4. dew point, under 50 is comfortable lower the better (15%)

    # rank is round(weightedScore / 20)

    If temp is less than 40, the rating will automatically be set to 1

    Args:
        location (str): a place or lat/lng

    Returns:
        int: the golf condition ranking
    """
    
    error = None
    rating = None
    _min, _max = 1, 5
    indexNames = RATINGS
    period = None
    conditions = {}
    keep = ['loc', 'place', 'profile']
    if reverse:
        _min, _max = 5, 1
        indexNames = RATINGS_REVERSED
    try:
        resp = await get_current_conditions(location, to='+6hours', fields=weather_fields)
        conditions = resp.response[0]
        period = conditions.periods[0]

        # get condition elements
        tempF = period.temp.avgF
        if tempF < 40:
            rating = 1
        
        else:
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
        if reverse:
            rating = 6 - (rating or 1)
            
    except Exception as e:
        error = str(e)
        ts = get_timestamp()
        period = munchify(dict(
            timestamp=ts,
            dateTimeISO=from_milliseconds(ts)
        ))
    
    # return rating and other info
    return munchify(dict(
        success=error == None,
        error=error,
        response=[
            dict(
                indice=dict(
                    type="golf",
                    range=dict(
                        min=_min,
                        max=_max,
                        reverse=reverse
                    ),
                    past=None,
                    current=dict(
                        index=rating,
                        timestamp=period.timestamp,
                        dateTimeISO=period.dateTimeISO,
                        indexENG=indexNames.get(rating)
                    ),
                ),
                forecast=None, # not sure what this is?
                **{k:v for k,v in conditions.items() if k in keep}
            ),
        ]
    ))
