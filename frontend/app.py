import streamlit as st
from collections import deque
import requests

from api_client import signup, login, google_login, get_messages, send_chat

st.set_page_config(page_title="Zenith", page_icon="🎓")

st.markdown("<h1 style='text-align: center;'>Ⓩ Zenith Assistant</h1>", unsafe_allow_html=True)
WELCOME = {
    "role": "assistant", 
    "content": "Chào bạn, mình là Zenith, trợ lý AI hỗ trợ toàn diện. Bạn có gì muốn hỏi?"
}

if "user" not in st.session_state:
    st.session_state.user = None

if "messages" not in st.session_state:
    st.session_state.messages = deque([WELCOME], maxlen=8)

if "show_signup" not in st.session_state:
    st.session_state.show_signup = False

if "show_login" not in st.session_state:
    st.session_state.show_login = True


def load_history():
    if not st.session_state.user:
        return
    try:
        msgs = get_messages(st.session_state.user["idToken"], limit=8)
        st.session_state.messages = deque(msgs, maxlen=8)
    except Exception:
        st.session_state.messages = deque([WELCOME], maxlen=8)


def clear_google_query_params():
    try:
        st.query_params.clear()
    except Exception:
        pass


def handle_google_login_callback():
    if st.session_state.user:
        return

    params = st.query_params
    raw_token = params.get("id_token")

    if not raw_token:
        return

    id_token = raw_token[0] if isinstance(raw_token, list) else raw_token

    try:
        user = google_login(id_token)
        st.session_state.user = user
        load_history()
        clear_google_query_params()
        st.success("Đăng nhập Google thành công")
        st.rerun()
    except requests.HTTPError as e:
        st.error(f"Đăng nhập Google thất bại: {e}")
        clear_google_query_params()
    except Exception as e:
        st.error(f"Lỗi xử lý Google login: {e}")
        clear_google_query_params()


def login_form():
    #Căn giữa
    _, col, _ = st.columns([1, 2, 1])
    with col:
        st.subheader("Đăng nhập")

        with st.form("login_form"):
            email = st.text_input("Email")
            password = st.text_input("Mật khẩu", type="password")
            submitted = st.form_submit_button("Đăng nhập")
            goto_signup = st.form_submit_button("Chưa có tài khoản? Đăng ký")

        if goto_signup:
            st.session_state.show_signup = True
            st.session_state.show_login = False
            st.rerun()

        if submitted:
            try:
                user = login(email, password)
                st.session_state.user = user
                load_history()
                st.success("Đăng nhập thành công")
                st.rerun()
            except requests.HTTPError as e:
                st.error(f"Đăng nhập thất bại: {e}")
            except Exception as e:
                st.error(f"Lỗi đăng nhập: {e}")

        st.markdown("### Hoặc")

        google_login_url = dict(st.secrets["google-login"])["google-url"]

        if google_login_url:
            st.markdown(
            f'''
            <a href="{google_login_url}" target="_self" style="
            display: flex;
            align-items: center;
            justify-content: center;
            width: 100%;
            padding: 0.5rem;
            background-color: white;
            color: #3c4043;
            text-decoration: none;
            border-radius: 4px;
            border: 1px solid #dadce0;
            font-weight: 500;
            font-family: 'Google Sans',arial,sans-serif;
            font-size: 14px;
            transition: background-color .2s ease;
        " onmouseover="this.style.backgroundColor='#f8f9fa'" onmouseout="this.style.backgroundColor='white'">
            <img src="https://www.gstatic.com/images/branding/product/1x/googleg_48dp.png" 
                style="width: 18px; height: 18px; margin-right: 10px;">
            Tiếp tục với Google
        </a>
            ''',
            unsafe_allow_html=True,
        )
        else:
            st.info(
                "Chưa cấu hình Google-login trong secrets. "
                "Hãy thêm URL đăng nhập Google để dùng tính năng này."
            )


def signup_form():
    # Căn giữa nội dung bằng columns giống form đăng nhập
    _, col, _ = st.columns([1, 2, 1])
    
    with col:
        st.markdown("<h3 style='text-align: center; color: #262730;'>Đăng ký tài khoản</h3>", unsafe_allow_html=True)
        
        with st.form("signup_form", clear_on_submit=True):
            # Ô nhập Email
            email = st.text_input("Email", placeholder="Nhập địa chỉ Email", label_visibility="collapsed")
            
            # Ô nhập mật khẩu
            password = st.text_input("Mật khẩu", type="password", placeholder="Nhập mật khẩu", label_visibility="collapsed")
            
            # Ô xác nhận mật khẩu (thường có trong form đăng ký)
            confirm_password = st.text_input("Xác nhận mật khẩu", type="password", placeholder="Xác nhận lại mật khẩu", label_visibility="collapsed")
            
            # Nút Tạo tài khoản (Màu đỏ giống nút Đăng Nhập Ngay)
            signup_button = st.form_submit_button("Tạo tài khoản", use_container_width=True)
            
            # CSS để giữ màu đỏ đồng bộ cho dự án Zenith
            st.markdown("""
                <style>
                /* Nút submit màu đen */
                div[data-testid="stForm"] button {
                    background-color: #000000 !important;
                    color: #ffffff !important;
                    border-radius: 4px !important;
                    border: none !important;
                    height: 45px !important;
                    font-weight: 600 !important;
                }
                /* Hiệu ứng khi rê chuột vào nút */
                div[data-testid="stForm"] button:hover {
                    background-color: #333333 !important;
                }
                /* Làm trắng nền của các ô input */
                div[data-testid="stTextInput"] input {
                    background-color: #ffffff !important;
                    color: #000000 !important;
                    border: 1px solid #e0e0e0 !important;
                }
                </style>
            """, unsafe_allow_html=True)

        # Nút Quay lại đăng nhập (Nút trắng viền xám)
        if st.button("Đã có tài khoản? Đăng nhập", use_container_width=True):
            st.session_state.show_signup = False
            st.rerun()

        # Dòng điều khoản cuối cùng giống form login
        st.markdown(
            """
            <div style='text-align: center; margin-top: 20px; font-size: 13px;'>
                <span style='color: #666;'>Bằng cách đăng ký, bạn đồng ý với </span> 
                <a href='#' style='color: #007BFF; text-decoration: none;'>Điều Khoản</a> 
            </div>
            """, 
            unsafe_allow_html=True
        )


def show_sidebar_history():
    with st.sidebar:
        st.title("Lịch sử đoạn chat")
        st.divider()
        
        # Duyệt qua các tin nhắn trong deque (bỏ qua lời chào đầu tiên nếu muốn)
        for i, msg in enumerate(list(st.session_state.messages)):
            if msg["role"] == "user":
                # Hiển thị 20 ký tự đầu của câu hỏi để làm tiêu đề
                short_text = msg["content"][:20] + "..." if len(msg["content"]) > 20 else msg["content"]
                st.button(f" {short_text}", key=f"hist_{i}", use_container_width=True)

handle_google_login_callback()

if st.session_state.user:
    cols = st.columns([1, 1, 1, 1, 1])
    
    with cols[4]:
        if st.button("Đăng xuất", use_container_width=True):
            st.session_state.user = None
            st.session_state.messages = deque([WELCOME], maxlen=8)
            clear_google_query_params()
            st.rerun()
else:
    if st.session_state.show_signup:
        signup_form()
    else:
        login_form()

st.divider()

if st.session_state.user:
    show_sidebar_history()
    
    # Phần hiển thị khung chat chính (giữ nguyên logic cũ của Kiên)
    for msg in list(st.session_state.messages):
        icon = "🤖" if msg["role"] == "assistant" else "👤"
        # with st.chat_message(msg["role"], avatar=icon):
        #     st.markdown(msg["content"])

    for msg in list(st.session_state.messages):
        # Tự động chọn icon và hướng dựa trên vai trò
        if msg["role"] == "assistant":
            icon = "🤖"  # Icon Zenith
        else:
            icon = "👤"  # Icon của bạn
            
        with st.chat_message(msg["role"], avatar=icon):
            st.markdown(msg["content"])

    prompt = st.chat_input("Nhập tin nhắn...")
    if prompt:
        # Lưu vào lịch sử với role 'user' để nó nằm bên phải
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        # Hiển thị ngay lập tức lên màn hình ở phía bên phải
        with st.chat_message("user", avatar="👤"):
            st.markdown(prompt)

        # ... (phần code gọi API gửi đến Backend vẫn giữ nguyên)

        try:
            res = send_chat(st.session_state.user["idToken"], prompt)
            reply = res["reply"]
        except Exception as e:
            reply = f"Lỗi backend: {e}"

        st.session_state.messages.append({"role": "assistant", "content": reply})
        st.rerun()

st.markdown("""
    <style>
    /* Chỉnh màu nền Sidebar thành trắng tinh */
    [data-testid="stSidebar"] {
        background-color: #ffffff;
        border-right: 1px solid #e0e0e0;
    }
    /* Chỉnh màu chữ các nút trong Sidebar */
    [data-testid="stSidebar"] button {
        background-color: transparent !important;
        color: #000000 !important;
        text-align: left !important;
        border: none !important;
    }
    [data-testid="stSidebar"] button:hover {
        background-color: #f8f9fa !important;
    }
    </style>
""", unsafe_allow_html=True)