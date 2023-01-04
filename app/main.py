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

# @app.get("/api/data/{id}")
# def zip_by_id(id:int) -> dict:
#     results = [zip for zip in ]

if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
