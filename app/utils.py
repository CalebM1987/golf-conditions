from fastapi import FastAPI
from typing import List, TypeVar, Generic, Optional
from fastapi.openapi.utils import get_openapi
from pydantic import BaseModel
import datetime

T = TypeVar('T')

class PointGeometry(BaseModel):
    type: str
    coordinates: List[float]

class PointFeature(BaseModel, Generic[T]):
    type: str
    geometry: PointGeometry
    properties: T

class GeoJSONFeatureCollection(BaseModel, Generic[T]):
    type: str
    features: List[PointFeature[T]]

class GeoJSONFormatArg(BaseModel):
    f: Optional[str]
    
SKIP_KWARGS = ['f']

def filter_json_results(data: List[T], **kwargs) -> List[T]:
    """filters json results by given kwargs

    Args:
        data (List[T]): the data to filter
        **kwargs: the key, value pairs of filters

    Returns:
        List[T]: the filtered results
    """
    if not kwargs:
        return data
    keys = [k for k in kwargs.keys() if k not in SKIP_KWARGS]
    return [ft for ft in data if all(map(lambda k: kwargs[k] == ft.get(k), keys))]

def customize_openapi(app: FastAPI, title: str, description: str=None, version: str='1.0.0'):
    if app.openapi_schema:
        return app.openapi_schema

    # create custom openapi_schema
    openapi_schema = get_openapi(title=title, version=version, description=description, routes=app.routes)
    app.openapi_schema = openapi_schema
    return app.openapi_schema

def to_geojson(data: List[T]) -> GeoJSONFeatureCollection[T]:
    """converts a data set into geojson

    Args:
        data (List[T]): the data to convert to geojson

    Returns:
        GeoJSONFeatureCollection[T]: the output feature collection
    """
    return dict(
        type='FeatureCollection',
        features=[
            dict(
                type='Feature',
                properties=ft,
                geometry=dict(
                    type='Point',
                    coordinates=[ft.get('Longitude', 0.0), ft.get('Latitude', 0.0)]
                )
            ) for ft in data
        ]
    )

def get_timestamp() -> int:
    """return current time in milliseconds"""
    date = datetime.datetime.utcnow() - datetime.datetime(1970, 1, 1)
    return round(date.total_seconds() * 1000)

def from_milliseconds(ts: int) -> str:
    dt = datetime.datetime.fromtimestamp(ts / 1000.0, tz=datetime.timezone.utc)
    return dt.isoformat()