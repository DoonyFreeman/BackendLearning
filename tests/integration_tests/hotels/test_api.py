

async def test_get_hotels(ac):
    response = await ac.get(
        "/hotels",
        params={
            "date_from": "2026-06-01",
            "date_to": "2026-06-10",
        }
    )
    
    assert response.status_code == 200

