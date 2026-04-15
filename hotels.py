from fastapi import Query, Body, APIRouter
from schemas.hotels import Hotel, HotelPATCH

router = APIRouter(prefix="/hotels", tags=["Отели"])


hotels = [
    {"id": 1, "title": "Sochi", "name": "soci"},
    {"id": 2, "title": "Krim", "name": "krim"},
    {"id": 3, "title": "Anapa", "name": "anapa"},
    {"id": 4, "title": "Surgut", "name": "surgut"},
]


@router.get("", summary="Получение списка отелей", description="Получение списка отелей с возможностью фильтрации по id и названию")
def get_hotels(
    id: int | None = Query(None, description="id отеля"),
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





@router.post("", summary="Создание отеля", description="Создание отеля. id генерируется автоматически, его не нужно передавать в теле запроса")
def create_hotel(hotel_data: Hotel = Body(openapi_examples={
    "example1": {
        "summary": "Пример 1",
        "description": "Пример с названием отеля Sochi",
        "value": {
            "title": "Sochi",
            "name": "сочи отель у моря",
        },
        },
        "example2": {
            "summary": "Пример 2",
            "description": "Пример с названием отеля Krim",
            "value": {
                "title": "Krim",
                "name": "крим отель у моря",
            },
        }
    },)):
    global hotels
    hotels.append({
        "id": hotels[-1]["id"] + 1, 
        "title": hotel_data.title,
        "name": hotel_data.name,
    })
    return {"Status": "OK"}


@router.put("/{hotel_id}", summary="Полное обновление данных об отеле", description="Тут мы полностью обновляем данные об отеле")
def put_hotel(hotel_id: int, hotel_data: Hotel):
    global hotels
    for hotel in hotels:
        if hotel["id"] == hotel_id:
            hotel["title"] = hotel_data.title
            hotel["name"] = hotel_data.name
            return {"status": "OK", "hotel": hotel}
    return {"status": "error", "message": "Hotel not found"}


@router.patch(
    "/{hotel_id}",
    summary="Частичное обновление данных об отеле",
    description="Тут мы частично обновляем данные об отеле: можно отправить name, а можно title, а можно ничего",
)
def patch_hotel(
    hotel_id: int,
    hotel_data: HotelPATCH,
):
    global hotels
    for hotel in hotels:
        if hotel["id"] == hotel_id:
            if hotel_data.title is not None:
                hotel["title"] = hotel_data.title
            if hotel_data.name is not None:
                hotel["name"] = hotel_data.name
            return {"status": "ok", "hotel": hotel}


@router.delete("/{hotel_id}", summary="Удаление отеля", description="Тут мы удаляем отель по его id")
def delete_hotel(hotel_id: int):
    global hotels
    hotels = [hotel for hotel in hotels if hotel["id"] != hotel_id]
    return {"Status": "OK"}
