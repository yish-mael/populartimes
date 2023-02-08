from fastapi import FastAPI, HTTPException, Depends
import requests
from fastapi.middleware.cors import CORSMiddleware
from typing import Union
import os
from dotenv import dotenv_values, load_dotenv
from fastapi.security import OAuth2PasswordBearer
import livepopulartimes
import re
import urllib.parse

load_dotenv()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
# config = {
#     **dotenv_values(".env.shared"),  # load shared development variables
#     **dotenv_values(".env.secret"),  # load sensitive variables
#     **os.environ,  # override loaded values with environment variables
# }

# name = "amoeba"
# location_lon = "37.76999"
# location_lat = "-122.44696"
# radius = "500"
# secretkey =""
# google_place_url = f"https://maps.googleapis.com/maps/api/place/autocomplete/json?input={name}&types=establishment&location={location_lon}%2C-122.location_lat&radius={radius}&key={secretkey}"


googleapikey = os.getenv('GOOGLEAPIKEY', None)

app = FastAPI(title="Backend API")
origins= [
    "http://localhost:3000",
    "localhost:3000",
    "http://127.0.0.1:5173",
    "127.0.0.1:5173"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

@app.get("/", tags=["root"])
async def read_root() -> dict:
    return {"message": "Welcome to root app"}


async def request():
    url = f"https://services.arcgis.com/su8ic9KbA7PYVxPS/arcgis/rest/services/Download_COVID_Cases_By_Zip_Codes/FeatureServer/0/query?outFields=*&where=1%3D1&f=geojson"
    r = requests.get(url)
    return r.json()

@app.get("/api/data", tags=["Harris County API"])
async def data() -> dict:
    results = await request()
    return { "data": results}


def url_bulder(name: str, location: str, radius: str, secretkey: str):
    google_place_url = f"https://maps.googleapis.com/maps/api/place/autocomplete/json?input={name}&types=establishment&location={location}&radius={radius}&key={secretkey}"
    return google_place_url

# Busy Time Api Implementation
@app.get("/api/busy", tags=["Busy Times API"])
async def Populartime(address: str):
    data = livepopulartimes.get_populartimes_by_address(address, proxy=False)
    return data

def placerequest():
    payload={}
    headers = {}
    #response = requests.get(google_place_url, headers=headers, data=payload)
    name = "amoeba"
    location = "37.76999 -122.44696"
    radius = "500"
    secretkey = googleapikey
    google_place_url = url_bulder(name, location, radius,secretkey)
    response = requests.get(google_place_url)
    return response.text
    
@app.get("/api/google/place", tags=["google place API"])
async def place():
    results =  placerequest()
    return {"data": results}
# API bulding dynamic fast API url 
@app.get("/items/{item_id}")
async def read_item(item_id: str, types: Union[str, None] = "establishment", location: Union[str, None] = "37.76999 -122.44696",  radius: Union[str, None] = "500", key: Union[str, None] = googleapikey):
    item = {"input": item_id}
    if types:
        item.update({"types": types})
    if location:
        item.update({"location": location})
    if radius: 
        item.update({"raduis": radius})
    if key:
        item.update({"key": key})
    return {"data": item}

# Google API
async def get_place_by_name(name: str,key: str):
    item = {"input": name}
    if item["input"]:
        item.update({"key": key})
    # if key: 
    #     item.update({"key": key})
    if item["key"] == None:
        raise HTTPException(status_code=404, detail="Missing  API Secret for google API")
    if item["key"] and item["input"]:
        url = f"https://maps.googleapis.com/maps/api/place/autocomplete/json?input={item['input']}&key={item['key']}"
        print(url)
        response = requests.get(url)
        return response.text
# Google API 
@app.get("/api/google/{name}", tags=["google API name"])
async def googlename(name: str,key: Union [str, None]):
    if key == None:
        raise HTTPException(status_code=404, detail="Missing  API Secret for google API")
    if name == None: 
        raise HTTPException(status_code=404, detail="Missing attribute")

    if name and key:
        result = await get_place_by_name(name, key)
        return result

#Todo: google API busytime https://github.com/m-wrzr/populartimes/blob/master/README.md

# @app.get("/api/google/populartime", tags=["google populartime API"])
# def googlebusytimeapi(name: str):
#     # name = urllib.parse(name)
#     # new = re.sub(r"^\s+","",name)
#     poptime = livepopulartimes.get_populartimes_by_address(name, proxy=False)
#     print(poptime)
#     return {"data": poptime}



#AUthentication
#Todo: https://fastapi.tiangolo.com/tutorial/security/simple-oauth2/
@app.get("/authtest/",tags=['authentication'])
async def testauth(token: str = Depends(oauth2_scheme)):
    return {"token": token}

#todo: Push entrie to postgres DB


