import uuid
from datetime import datetime, timezone
from backend.app.core.firebase_config import get_firestore
from firebase_admin import firestore

db = get_firestore()

# ─── CONVERSATION ────────────────────────────────────────

def create_conversation(uid: str) -> str:
    conv_id = str(uuid.uuid4())
    db.collection("chats").document(uid)\
      .collection("conversations").document(conv_id).set({
          "title": "Đoạn chat mới",
          "created_at": datetime.now(timezone.utc)
      })
    return conv_id

def update_conversation_title(uid: str, conv_id: str, title: str):
    db.collection("chats").document(uid)\
      .collection("conversations").document(conv_id)\
      .update({"title": title})

def get_conversations(uid: str, limit: int = 20):
    docs = (
        db.collection("chats").document(uid)
        .collection("conversations")
        .order_by("created_at", direction=firestore.Query.DESCENDING)
        .limit(limit)
        .stream()
    )
    return [{"id": d.id, **d.to_dict()} for d in docs]

# ─── MESSAGES ────────────────────────────────────────────

def save_message(uid: str, conv_id: str, role: str, content: str):
    db.collection("chats").document(uid)\
      .collection("conversations").document(conv_id)\
      .collection("messages").add({
          "role": role,
          "content": content,
          "ts": datetime.now(timezone.utc)
      })

def load_last_messages(uid: str, conv_id: str, limit: int = 8):
    docs = list(
        db.collection("chats").document(uid)
        .collection("conversations").document(conv_id)
        .collection("messages")
        .order_by("ts", direction=firestore.Query.DESCENDING)
        .limit(limit)
        .stream()
    )
    docs.reverse()
    return [
        {
            "role": d.to_dict().get("role", "assistant"),
            "content": d.to_dict().get("content", "")
        }
        for d in docs
    ]

def clear_messages(uid: str, conv_id: str):
    docs = (
        db.collection("chats").document(uid)
        .collection("conversations").document(conv_id)
        .collection("messages")
        .stream()
    )
    for doc in docs:
        doc.reference.delete()

def delete_conversation(uid: str, conv_id: str):
    msgs = (
        db.collection("chats").document(uid)
        .collection("conversations").document(conv_id)
        .collection("messages").stream()
    )
    for msg in msgs:
        msg.reference.delete()

    db.collection("chats").document(uid)\
      .collection("conversations").document(conv_id).delete()