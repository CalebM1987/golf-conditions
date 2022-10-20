from pydantic import BaseModel
from typing import Optional

class GolfCourse(BaseModel):
    id: Optional[int]
    Region: Optional[int]
    CourseName: Optional[str]
    Address: Optional[str]
    City: Optional[str]
    Zip: Optional[str]
    State: Optional[str]
    Holes: Optional[int]
    Phone: Optional[str]
    Latitude: Optional[float]
    Longitude: Optional[float]
