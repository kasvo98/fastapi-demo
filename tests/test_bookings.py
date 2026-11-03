import pytest

@pytest.mark.parametrize("case,expected_status,expected_detail", [
    ("missing_room", 404, "Room not found"),
    ("naive_start", 422, ["body", "starts_at"]),
    ("conflict", 409, "Booking conflict"),
])
def test_booking_errors(client, case, expected_status, expected_detail):
    room_id = 999
    body = {"starts_at": "2025-10-01T10:00:00Z", "ends_at": "2025-10-01T11:00:00Z"}
    if case != "missing_room":
        created = client.post("/api/rooms", json={"name": "Альфа", "capacity": 6, "address": {"city": "Москва", "street": "Учебная, 1"}})
        assert created.status_code == 201
        room_id = created.json()["id"]
    path = f"/api/rooms/{room_id}/bookings"
    if case == "conflict":
        first = client.post(path, json=body)
        assert first.status_code == 201
    if case == "naive_start":
        body["starts_at"] = "2025-10-01T10:00:00"

    response = client.post(path, json=body)
    assert response.status_code == expected_status
    detail = response.json()["detail"]
    if expected_status == 422:
        assert isinstance(detail, list)
        assert any(error.get("loc") == expected_detail for error in detail)
    else:
        assert detail == expected_detail
    if case == "conflict":
        listing = client.get(path)
        assert listing.status_code == 200
        assert listing.json() == [first.json()]