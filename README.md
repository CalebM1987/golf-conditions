### Golf Conditions Application

This application uses the [aeris weather api](https://www.aerisweather.com/support/docs/api/reference/endpoints) to fetch weather conditions at a given location and calculates a rating based on a few factors of how ideal the weather is for playing golf.

Things analyzed are:
 * wind (30% weight)
 * temperature (30% weight)
 * precipitation (25% weight)
 * dew point (15% weight)


## The Backend API

The backend for this app was built using Python's [FastAPI](https://fastapi.tiangolo.com/) microframework.  There are two basic services, one for Weather Conditions and another to serve up Golf Courses in Minnesota.

Before you can run this project, you must make sure you have an account with [aeris weather](https://www.aerisweather.com/signup/developer/) and [mapbox](https://docs.mapbox.com/help/getting-started/access-tokens/) and you will need to create a couple `.env` files.  Create this file in and fill in the necessary variables at `/app/routers/weather/.env`:

```env
# /app/routers/weather/.env
ARIES_CLIENT_ID=<your-id>
ARIES_CLIENT_SECRET=<your-secret>
```

To run the backend:

```sh
# source your profile
source ~/.bash_profile
# activate a virtual environment
conda activate <some virtual environment>
# install the requirements for this project using the included requirements.txt file
pip install -r requirements.txt
# run app with uvicorn
uvicorn app.main:app --reload
```

By default, this will spin up on port `8000` at [http://localhost:8000](http://localhost:8000/) or you may have to use the local address (`127.0.0.1:8000`).  To view the [Swagger](https://swagger.io/tools/swagger-ui/) docs, visit:

[http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

![swagger](./resources/images/swagger.png)

or if you prefer [ReDocs](https://redocly.github.io/redoc/):
[http://127.0.0.1:8000/redoc(http://127.0.0.1:8000/redoc)
![redoc](./resources/images/redoc.png)


### front end app
make the following env file at `/golf-conditions/.env`:

```
# /golf-conditions/.env
VITE_MAPBOX_TOKEN=<your-token>
VITE_AERIS_CLIENT_ID=<your-client>
VITE_AERIS_CLIENT_SECRET=<your-secret>
VITE_APP_PUBLIC_PATH=.
```

and then a production one, where you can change the public path if hosting from an actual server:

```
# /golf-conditions/.env.production
VITE_APP_PUBLIC_PATH=..
```