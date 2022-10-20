import os
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from app.utils import customize_openapi
from app.routers import golf, weather

routers = [
    golf,
    weather
]

app = FastAPI()

origins = [
    'http://localhost:5173'
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# include routers
for router in routers:
    app.include_router(router)

def custom_openapi():
    return customize_openapi(
        app,
        title='Golf Courses Condtions API',
        description='an API for determining golf conditions for a given location'
    )

app.openapi = custom_openapi

# mount static directory to serve built app
staticDir = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'static')
app.mount('/app', StaticFiles(directory=staticDir, html=True), name="static")

# @app.get('/')
# def serve_app(request: Request)