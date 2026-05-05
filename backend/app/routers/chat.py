from fastapi import APIRouter, Depends, HTTPException, Query

from backend.app.dependencies.auth import get_current_user
from backend.app.schemas.chat import ChatRequest
from backend.app.services.firestore_service import (
    save_message, load_last_messages,
    create_conversation, get_conversations, update_conversation_title,
    clear_messages
)
from backend.app.services.ollama_service import chat_with_model

router = APIRouter(prefix="/chat", tags=["chat"])

WELCOME_MESSAGE = {
    "role": "assistant",
    "content": "Chào bạn, mình là Zenith, trợ lý AI hỗ trợ toàn diện. Bạn có gì muốn hỏi?"
}

general_instruction = (
    "Bạn là Zenith, một trợ lý AI thông minh, thân thiện. "
    "Bạn có kiến thức sâu về lập trình (Golang, C++), toán học, đời sống và tiếng Anh. "
    "Hãy trả lời chính xác, ngắn gọn và hữu ích cho tôi."
    "Hãy trả lời câu hỏi của tôi bằng tiếng Việt nhé, chỉ dùng tiếng anh cho các danh từ riêng."
)

# ─── CONVERSATIONS ───────────────────────────────────────

@router.post("/conversations")
def new_conversation(user=Depends(get_current_user)):
    try:
        conv_id = create_conversation(user["uid"])
        return {"conv_id": conv_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/conversations")
def list_conversations(user=Depends(get_current_user)):
    try:
        return get_conversations(user["uid"])
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ─── MESSAGES ────────────────────────────────────────────

@router.post("")
def chat(payload: ChatRequest, user=Depends(get_current_user)):
    try:
        save_message(user["uid"], payload.conv_id, "user", payload.message)
        history = load_last_messages(user["uid"], payload.conv_id, limit=8)

        reply = chat_with_model(
            [{"role": "system", "content": general_instruction}] + history
        )

        save_message(user["uid"], payload.conv_id, "assistant", reply)

        # Cập nhật title = tin nhắn đầu tiên của đoạn chat
        update_conversation_title(
            user["uid"],
            payload.conv_id,
            payload.message[:30]
        )

        return {"reply": reply}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/messages")
def get_messages(
    conv_id: str,
    limit: int = Query(default=8, ge=1, le=50),
    user=Depends(get_current_user)
):
    try:
        msgs = load_last_messages(user["uid"], conv_id, limit=limit)
        return msgs if msgs else [WELCOME_MESSAGE]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/messages")
def delete_messages(conv_id: str, user=Depends(get_current_user)):
    try:
        clear_messages(user["uid"], conv_id)
        return {"message": "Đã xóa lịch sử chat"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.delete("/conversations/{conv_id}")
def remove_conversation(conv_id: str, user=Depends(get_current_user)):
    try:
        from backend.app.services.firestore_service import delete_conversation
        delete_conversation(user["uid"], conv_id)
        return {"message": "Đã xóa đoạn chat"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))