from backend.app.main import app
from backend.app.auth.dependencies import get_current_user
from backend.app.models.user import User



def test_create_room(client):
    response = client.post("/rooms/create")

    assert response.status_code == 200
    data = response.json()
    assert data.get("room_code")


def override_get_current_user(user_id: int, username: str):
    def _get_user():
        return User(id=user_id, username=username, email=f"{username}@example.com")
    return _get_user


def test_join_room(client):
    response = client.post("/rooms/create")

    data = response.json()
    room_code = data.get("room_code")

    app.dependency_overrides[get_current_user] = override_get_current_user(2, "player_two")
    response = client.post(f"/rooms/{room_code}/join")
    assert response.status_code == 200
    data = response.json()
    assert data.get("message") == "Joined room"
