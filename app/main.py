from fastapi import FastAPI
import requests
import uvicorn

app = FastAPI(title="Backend API")

url = f"https://services.arcgis.com/su8ic9KbA7PYVxPS/arcgis/rest/services/Download_COVID_Cases_By_Zip_Codes/FeatureServer/0/query?outFields=*&where=1%3D1&f=geojson"

async def request():
    r = requests.get(url)
    return r.text

@app.get("/api/data")
async def data():
    results = await request()
    return { "data": results}


google_place_url = f"https://maps.googleapis.com/maps/api/place/autocomplete/json?input=amoeba&types=establishment&location=37.76999%2C-122.44696&radius=500&key=AIzaSyCFRoQAMWl1TXH5la1csQdf34jYJ8OYxm8"



async def placerequest():
    payload={}
    headers = {}
    #response = requests.get(google_place_url, headers=headers, data=payload)
    response = requests.get(google_place_url)
    return response.text
    
@app.get("/api/google/place")
async def place():
    results = await placerequest()
    return {"data": results}


# def zip_by_id(id:int) -> dict:
#     results = [zip for zip in ]

if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
