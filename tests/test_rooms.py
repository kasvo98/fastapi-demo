def test_create_room(client):
    response = client.post("/api/rooms", json={"name": "Альфа", "capacity": 4, "address": {"city": "Москва", "street": "Учебная, 1"}})
    assert response.status_code == 201
    room = response.json()
    assert type(room["id"]) is int
    assert room["name"] == "Альфа"
    assert room["capacity"] == 4
    response = client.get("/api/rooms")
    assert response.status_code == 200
    assert response.json() == [room]

def test_empty_rooms(client):
    response = client.get("/api/rooms")
    assert response.status_code == 200
    assert response.json() == []