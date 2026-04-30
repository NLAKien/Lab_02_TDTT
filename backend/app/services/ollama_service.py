#import os
#from ollama import Client

#ODEL = os.getenv("OLLAMA_MODEL", "llama3.2:1b")
#OLLAMA_HOST = os.getenv("OLLAMA_HOST", "https://zazvz-34-126-67-14.run.pinggy-free.link")

#client = Client(host=OLLAMA_HOST)

#def chat_with_model(messages: list[dict]) -> str:

import os
from ollama import Client

# 1. Sửa lại đúng tên model bạn đã tải (llama3)
MODEL = os.getenv("OLLAMA_MODEL", "llama3") 

# 2. Sửa lại host về localhost (máy của bạn)
# Mặc định Ollama chạy ở cổng 11434
OLLAMA_HOST = os.getenv("OLLAMA_HOST", "http://localhost:11434")

client = Client(host=OLLAMA_HOST)

def chat_with_model(messages: list[dict]) -> str:
    # ... phần còn lại giữ nguyên ...
    # 1. Định nghĩa "vai diễn" cho AI
    system_instruction = {
        "role": "system",
        "content": (
            "Bạn là trợ lý học từ vựng TOEIC chuyên nghiệp. "
            "Khi nhận từ vựng, hãy: 1. Giải thích nghĩa tiếng Việt. "
            "2. Nêu loại từ. 3. Cho 1 ví dụ trong ngữ cảnh công sở. "
            "Trả lời ngắn gọn, súc tích."
        )
    }
    
    # 2. Chèn instruction này vào đầu danh sách tin nhắn
    full_messages = [system_instruction] + messages
    
    # 3. Gửi danh sách đã có chỉ dẫn cho AI
    response = client.chat(
        model=MODEL,
        messages=full_messages
    )
    return response["message"]["content"]