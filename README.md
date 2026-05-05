# Ⓩ Zenith Assistant

Zenith Assistant là ứng dụng chatbot AI được xây dựng bằng **FastAPI** (backend) và **Streamlit** (frontend), tích hợp **Firebase Authentication**, **Firestore**, và mô hình ngôn ngữ **Ollama**.

## 👤 Thông tin sinh viên
* **Họ tên:** Nguyễn Lê Anh Kiên
* **MSSV:** 24120196
* **Lớp:** 24CTT3
* **Học phần:** LAB_02: APPLICATION PROGRAMMING INTERFACE AND FIREBASE STUDIO

---

## Yêu cầu hệ thống

- Python >= 3.10
- [Ollama](https://ollama.com) đã cài đặt và đang chạy local
- Tài khoản Firebase (có Firestore và Authentication được bật)
- Google OAuth 2.0 credentials (nếu dùng đăng nhập Google)

---

## Cài đặt môi trường

### 1. Clone repository

```bash
git clone https://github.com/<your-username>/zenith-assistant.git
cd zenith-assistant
```

### 2. Tạo virtual environment

```bash
python -m venv venv
```

Kích hoạt môi trường:

```bash
# Windows
venv\Scripts\activate

# macOS / Linux
source venv/bin/activate
```

### 3. Cài đặt dependencies

```bash
pip install -r requirements.txt
```

### 4. Cấu hình Firebase

Tải file `serviceAccountKey.json` từ **Firebase Console → Project Settings → Service Accounts**, sau đó đặt vào thư mục:

```
backend/app/core/serviceAccountKey.json
```

### 5. Cấu hình Streamlit Secrets

Tạo file `.streamlit/secrets.toml` ở thư mục gốc với nội dung:

```toml
[google-login]
google-url            = "http://localhost:8000/auth/google/start"
google_client_id      = "YOUR_GOOGLE_CLIENT_ID"
google_client_secret  = "YOUR_GOOGLE_CLIENT_SECRET"
google_redirect_uri   = "http://localhost:8000/auth/google/callback"
firebase_web_api_key  = "YOUR_FIREBASE_WEB_API_KEY"
frontend_url          = "http://localhost:8501"
cookie_secure         = false
```

> **Lưu ý:** Không commit file `secrets.toml` và `serviceAccountKey.json` lên Git.

### 6. Cài đặt và chạy Ollama model

```bash
ollama pull gemma3
```

> Có thể thay `gemma3` bằng model khác tùy cấu hình trong `ollama_service.py`.

---

## Chạy Backend

Backend sử dụng **FastAPI** với server **Uvicorn**.

```bash
# Đảm bảo đang ở thư mục gốc của project và đã kích hoạt venv
uvicorn backend.app.main:app --reload --port 8000
```

Backend sẽ chạy tại: [http://localhost:8000](http://localhost:8000)

Kiểm tra API docs tại: [http://localhost:8000/docs](http://localhost:8000/docs)

---

## Chạy Frontend

Frontend sử dụng **Streamlit**.

```bash
# Mở terminal mới (giữ backend đang chạy), đảm bảo đã kích hoạt venv
cd frontend
streamlit run app.py
```

Frontend sẽ chạy tại: [http://localhost:8501](http://localhost:8501)

---

## Cấu trúc thư mục

```
zenith-assistant/
├── backend/
│   └── app/
│       ├── core/
│       │   └── firebase_config.py
│       ├── dependencies/
│       │   └── auth.py
│       ├── routers/
│       │   ├── auth.py
│       │   └── chat.py
│       ├── schemas/
│       │   ├── auth.py
│       │   └── chat.py
│       ├── services/
│       │   ├── firestore_service.py
│       │   └── ollama_service.py
│       └── main.py
├── frontend/
│   ├── app.py
│   └── api_client.py
├── .streamlit/
│   └── secrets.toml
├── requirements.txt
└── README.md
```

---

## Tính năng

- Đăng ký / Đăng nhập bằng Email & Password
- Đăng nhập bằng Google OAuth
- Chat với AI (Ollama) có lưu lịch sử
- Tạo / xóa đoạn chat
- Lưu trữ hội thoại trên Firestore theo từng người dùng