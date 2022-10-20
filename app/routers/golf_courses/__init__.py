import os
import json
from .models import GolfCourse
from typing import List, Union
from fastapi import APIRouter, Request, Path, Depends, Response
from ...utils import GeoJSONFormatArg, filter_json_results, to_geojson, GeoJSONFeatureCollection

# load courses json file
thisDir = os.path.dirname(os.path.abspath(os.path.dirname(__file__)))

coursesJson = os.path.join(os.path.dirname(thisDir), 'data', 'All_MN_Courses.json')
with open(coursesJson, 'r') as f:
    courses = json.load(f)

golf = APIRouter()

class GolfCourseParams(GolfCourse, GeoJSONFormatArg):
    pass

@golf.get('/golf-courses', response_model=Union[GeoJSONFeatureCollection[GolfCourse], List[GolfCourse]], tags=['golf-courses'])
def get_all_courses(request: Request, params: GolfCourseParams = Depends()):
    """fetches all golf courses"""
    kwargs = request.query_params
    geojson = kwargs.get('f') == 'geojson'
    filtered = filter_json_results(courses, **kwargs)
    return to_geojson(filtered) if geojson else filtered

@golf.get('/golf-courses/{id}', response_model=GolfCourse, tags=['golf-courses'])
def get_single_course(id: int = Path(..., title='the Golf Course ID')):
    """fetches a single golf course"""
    result = [c for c in courses if c.get('id') == id][0]
    return 
