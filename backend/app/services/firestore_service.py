from datetime import datetime, timezone
from backend.app.core.firebase_config import get_firestore
from firebase_admin import firestore

db = get_firestore()

def save_message(uid: str, role: str, content: str):
    doc = {
        "role": role,
        "content": content,
        "ts": datetime.now(timezone.utc)
    }
    db.collection("chats").document(uid).collection("messages").add(doc)

def load_last_messages(uid: str, limit: int = 8):
    q = (
        db.collection("chats")
        .document(uid)
        .collection("messages")
        .order_by("ts", direction=firestore.Query.DESCENDING)
        .limit(limit)
    )

    docs = list(q.stream())
    docs.reverse()

    return [
        {
            "role": d.to_dict().get("role", "assistant"),
            "content": d.to_dict().get("content", "")
        }
        for d in docs
    ]