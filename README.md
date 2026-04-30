# 🛡️ Zenith AI - Multipurpose Assistant (LAB_02)

**Zenith** là một ứng dụng trợ lý AI đa năng được phát triển trong khuôn khổ bài tập Lab 02. Ứng dụng kết hợp sức mạnh của mô hình ngôn ngữ lớn chạy cục bộ (Local LLM) cùng hệ thống lưu trữ đám mây để hỗ trợ người dùng trong nhiều lĩnh vực từ học thuật đến kỹ thuật chuyên sâu.

## 👤 Thông tin sinh viên
* **Họ tên:** Nguyễn Lê Anh Kiên
* **MSSV:** 24120196
* **Lớp:** 24CTT3
* **Học phần:** LAB_02: APPLICATION PROGRAMMING INTERFACE AND FIREBASE STUDIO

---

## 🚀 Tính năng chính (Features)

* **Học tập đa năng (Multipurpose EL & Academic Support):** Không chỉ dừng lại ở học Tiếng Anh (giải nghĩa, sửa lỗi ngữ pháp), Zenith còn hỗ trợ giải toán (Đại số tuyến tính, ma trận) và phân tích thuật toán.
* **Trợ lý lập trình chuyên sâu:** Hỗ trợ viết và tối ưu mã nguồn cho các ngôn ngữ C++, Go, và truy vấn SQL Server.
* **Hệ thống xác thực người dùng:** Tích hợp Firebase Authentication để quản lý đăng ký/đăng nhập cá nhân hóa.
* **Lưu trữ dữ liệu đám mây:** Toàn bộ lịch sử trò chuyện được đồng bộ hóa và lưu trữ bền vững trên Firebase Firestore.
* **Hỗ trợ kiến thức CS:** Giải đáp các thắc mắc về cấu trúc dữ liệu và giải thuật (như cây AVL, bảng băm...).

---

## 🏗️ Kiến trúc hệ thống (Tech Stack)

* **Frontend:** [Streamlit](https://streamlit.io/) - Giao diện chat hiện đại, trực quan.
* **Backend:** [FastAPI](https://fastapi.tiangolo.com/) - Xử lý logic API và kết nối dịch vụ.
* **AI Engine:** [Ollama](https://ollama.com/) (Model: **Llama 3**) - Chạy offline để đảm bảo quyền riêng tư và tốc độ xử lý.
* **Database & Auth:** [Firebase Studio](https://firebase.google.com/) (Firestore & Authentication).

---

## ⚙️ Cài đặt & Khởi chạy (Installation)

### 1. Yêu cầu hệ thống
* Python 3.12+
* Ollama (đã cài đặt model `llama3`)

### 2. Cài đặt thư viện
```bash
pip install -r requirements.txt