from pydantic import BaseModel
from typing import List, Optional

class LatLng(BaseModel):
    lat: float
    long: float
class TimeBase(BaseModel):
    maxTimestamp: int
    maxDateTimeISO: str
    minTimestamp: int
    minDateTimeISO: str

class Place(BaseModel):
    name: str
    state: str
    country: str

class RatingScores(BaseModel):
    temp: float
    wind: float
    precip: float 
    dew: float

class TimeRange(TimeBase):
    count: int

class Precip(TimeBase):
    maxMM: float
    minMM: float
    avgMM: float
    totalMM: float
    maxIN: float
    minIN: float
    avgIN: float
    totalIN: float

class TempLike(TimeBase):
    maxC: float
    minC: float
    avgC: float
    maxF: float
    minF: float
    avgF: float

class WindSpeed(TimeBase):
    maxKTS: float
    minKTS: float
    avgKTS: float
    maxKPH: float
    minKPH: float
    avgKPH: float

class Weather(BaseModel):
    phrase: str
    primary: str

class Period(BaseModel):
    timestamp: int
    range: TimeRange
    precip: Precip
    temp: TempLike
    dewpoint: TempLike
    windSpeed: WindSpeed
    weather: Weather

class Profile(BaseModel):
    tz: str

class IndexRange(BaseModel):
    min: int
    max: int
    reverse: bool

class RatingIndex(BaseModel):
    timestamp: int
    dateTimeISO: str
    index: int
    indexENG: str

class Indice(BaseModel):
    type: str
    range: IndexRange
    past: Optional[RatingIndex]
    current: RatingIndex


class ResponseObject(BaseModel):
    loc: LatLng
    place: Place
    profile: Profile
    indice: Indice

class RatingResponse(BaseModel):
    success: bool
    error: Optional[str]
    response: List[ResponseObject]

class ReverseIndexes(BaseModel):
    reverse: Optional[bool]=False

class WeatherConditionsResponse(BaseModel):
    loc: LatLng
    place: Place
    periods: List[Period]