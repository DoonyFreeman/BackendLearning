from fastapi import Query, Body, APIRouter


router = APIRouter(prefix="/hotels", tags=["Отели"])


hotels = [
    {"id": 1, "title": "Sochi", "name": "soci"},
    {"id": 2, "title": "Krim", "name": "krim"},
    {"id": 3, "title": "Anapa", "name": "anapa"},
    {"id": 4, "title": "Surgut", "name": "surgut"},
]


@router.get("")
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


@router.post("")
def create_hotel(
    title: str = Body(
        embed=True,
    ),
):
    global hotels
    hotels.append({"id": hotels[-1]["id"] + 1, "title": title})
    return {"Status": "OK"}


@router.put("/{hotel_id}")
def put_hotel(hotel_id: int, title: str = Body(), name: str = Body()):
    global hotels
    for hotel in hotels:
        if hotel["id"] == hotel_id:
            hotel["title"] = title
            hotel["name"] = name
            return {"status": "OK", "hotel": hotel}
    return {"status": "error", "message": "Hotel not found"}


@router.patch(
    "/{hotel_id}",
    summary="Частичное обновление данных об отеле",
    description="Тут мы частично обновляем данные об отеле: можно отправить name, а можно title, а можно ничего",
)
def patch_hotel(
    hotel_id: int,
    title: str | None = Body(default=None),
    name: str | None = Body(default=None),
):
    global hotels
    for hotel in hotels:
        if hotel["id"] == hotel_id:
            if title is not None:
                hotel["title"] = title
            if name is not None:
                hotel["name"] = name
            return {"status": "ok", "hotel": hotel}


@router.delete("/{hotel_id}")
def delete_hotel(hotel_id: int):
    global hotels
    hotels = [hotel for hotel in hotels if hotel["id"] != hotel_id]
    return {"Status": "OK"}
