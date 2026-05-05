import requests

API_BASE = "http://localhost:8000"

def signup(email: str, password: str):
    r = requests.post(f"{API_BASE}/auth/signup", json={
        "email": email,
        "password": password
    })
    r.raise_for_status()
    return r.json()

def login(email: str, password: str):
    r = requests.post(f"{API_BASE}/auth/login", json={
        "email": email,
        "password": password
    })
    r.raise_for_status()
    return r.json()

def google_login(id_token: str):
    r = requests.post(f"{API_BASE}/auth/google", json={
        "id_token": id_token
    })
    r.raise_for_status()
    return r.json()

# ─── CONVERSATIONS ───────────────────────────────────────

def new_conversation(id_token: str):
    r = requests.post(
        f"{API_BASE}/chat/conversations",
        headers={"Authorization": f"Bearer {id_token}"}
    )
    r.raise_for_status()
    return r.json()  # {"conv_id": "..."}

def get_conversations(id_token: str):
    r = requests.get(
        f"{API_BASE}/chat/conversations",
        headers={"Authorization": f"Bearer {id_token}"}
    )
    r.raise_for_status()
    return r.json()  # [{"id": "...", "title": "..."}, ...]

# ─── MESSAGES ────────────────────────────────────────────

def get_messages(id_token: str, conv_id: str, limit: int = 8):
    r = requests.get(
        f"{API_BASE}/chat/messages",
        params={"conv_id": conv_id, "limit": limit},
        headers={"Authorization": f"Bearer {id_token}"}
    )
    r.raise_for_status()
    return r.json()

def send_chat(id_token: str, message: str, conv_id: str):
    r = requests.post(
        f"{API_BASE}/chat",
        json={"message": message, "conv_id": conv_id},
        headers={"Authorization": f"Bearer {id_token}"}
    )
    r.raise_for_status()
    return r.json()

def clear_messages(id_token: str, conv_id: str):
    r = requests.delete(
        f"{API_BASE}/chat/messages",
        params={"conv_id": conv_id},
        headers={"Authorization": f"Bearer {id_token}"}
    )
    r.raise_for_status()
    return r.json()

def delete_conversation(id_token: str, conv_id: str):
    r = requests.delete(
        f"{API_BASE}/chat/conversations/{conv_id}",
        headers={"Authorization": f"Bearer {id_token}"}
    )
    r.raise_for_status()
    return r.json()