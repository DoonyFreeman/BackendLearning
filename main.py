from fastapi import FastAPI, Query, Body
import uvicorn
import threading

app = FastAPI( )




hotels = [
    {"id": 1, "title": "Sochi", "name": "soci"},
    {"id": 2, "title": "Krim", "name": "krim"},
    {"id": 3, "title": "Anapa", "name": "anapa"},
    {"id": 4 , "title": "Surgut", "name": "surgut"},
]
import time
import asyncio

@app.get("/sync/{id}")
def sync_func(id: int):
    print(f"sync ПОТОКОВ: {threading.active_count()}")
    print(f"sync Начал {id}: {time.time():.2f}")    
    time.sleep(3)
    print(f"sync Закончил {id}: {time.time():.2f}")

@app.get("/async/{id}")
async def async_func(id: int):
    print(f"async ПОТОКОВ: {threading.active_count()}")
    print(f"async Начал {id}: {time.time():.2f}")
    await asyncio.sleep(3)
    print(f"async Закончил {id}: {time.time():.2f}")






@app.get("/hotels")
def get_hotels(id: int | None = Query(None, description="id отеля"),
               title: str | None = Query(None, description="Название отеля"),
               ):
    hotels_ = []
    for hotel in hotels:
        if id and hotel["id"] != id:
            continue
        if title and hotel["title"] != title:
            continue
        hotels_.append(hotel)
    return hotels_



@app.post("/hotels")
def create_hotel(title: str = Body(embed=True,)):
    global hotels
    hotels.append(
        {"id": hotels[-1]["id"] + 1,
         "title": title
         }
    )
    return {"Status": "OK"}

@app.put("/hotels/{hotel_id}")
def put_hotel(hotel_id: int, title: str = Body(), name: str = Body()):
    global hotels
    for hotel in hotels:
        if hotel["id"] == hotel_id:
            hotel["title"] = title
            hotel["name"] = name
            return {"status": "OK", "hotel": hotel}
    return {"status": "error", "message": "Hotel not found"}

@app.patch(
        "/hotels/{hotel_id}", 
        summary="Частичное обновление данных об отеле",
        description="Тут мы частично обновляем данные об отеле: можно отправить name, а можно title, а можно ничего"
        )
def patch_hotel(hotel_id: int, title: str | None = Body(default=None), name: str | None = Body(default=None)):
    global hotels
    for hotel in hotels:
        if hotel["id"] == hotel_id:
            if title is not None:
                hotel["title"] = title
            if name is not None:
                hotel["name"] = name
            return {"status": "ok", "hotel": hotel}
    


@app.delete("/hotels/{hotel_id}")
def delete_hotel(hotel_id: int):
    global hotels
    hotels = [hotel for hotel in hotels if hotel["id"] != hotel_id]
    return {"Status": "OK"}






@app.get("/")
def func():
    return "Hello world!"



if __name__ == "__main__":
    uvicorn.run("main:app", reload = False, workers=1,)

