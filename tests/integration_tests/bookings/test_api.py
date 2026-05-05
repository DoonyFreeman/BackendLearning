import pytest


@pytest.mark.parametrize("room_id, date_from, date_to, status_code", [
    (1, "2026-06-01", "2026-06-10", 200),
    (1, "2026-06-01", "2026-06-11", 200),
    (1, "2026-06-01", "2026-06-12", 200),
    (1, "2026-06-01", "2026-06-13", 200),
    (1, "2026-06-01", "2026-06-14", 200),
    (1, "2026-06-01", "2026-06-15", 500),
    (1, "2026-06-16", "2026-06-25", 200),
])
async def test_add_booking(
    room_id, date_from, date_to, status_code,
    db, 
    authenticated_ac):
    # room_id = (await db.rooms.get_all())[0].id
    response = await authenticated_ac.post(
        "/bookings",
        json={
            "room_id": room_id,
            "date_from": date_from,
            "date_to": date_to,
        }
    )
    assert response.status_code == status_code
    if status_code == 200:
        res = response.json()
        assert isinstance(res, dict)
        assert res["status"] == "OK"
        assert "data" in res