from fastapi import APIRouter, Depends, HTTPException, Query

from backend.app.dependencies.auth import get_current_user
from backend.app.schemas.chat import ChatRequest
from backend.app.services.firestore_service import save_message, load_last_messages
from backend.app.services.ollama_service import chat_with_model

router = APIRouter(prefix="/chat", tags=["chat"])

WELCOME_MESSAGE = {
    "role": "assistant",
    "content": "Chào Kiên! 👋 Tôi là trợ lý ôn thi TOEIC của bạn. Hãy nhập một từ hoặc một câu tiếng Anh, tôi sẽ giải thích nghĩa và lưu vào sổ tay cho bạn!"
}

@router.post("")
def chat(payload: ChatRequest, user=Depends(get_current_user)):
    try:
        # 1. Lưu tin nhắn của người dùng
        save_message(user["uid"], "user", payload.message)

        # 2. Tạo "System Prompt" để ép Bot chỉ nói về TOEIC (Nếu ollama_service hỗ trợ)
        # Nếu chat_with_model chỉ nhận history, bạn có thể chèn thêm hướng dẫn vào đầu history
        history = load_last_messages(user["uid"], limit=5)
        
        # Thêm hướng dẫn chuyên biệt cho TOEIC
        toeic_instruction = "Bạn là chuyên gia TOEIC. Giải thích ngắn gọn từ vựng trong câu sau, nêu loại từ và ví dụ công sở."
        reply = chat_with_model([{"role": "system", "content": toeic_instruction}] + history)

        # 3. Lưu câu trả lời của Bot
        save_message(user["uid"], "assistant", reply)

        return {"reply": reply}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))