import streamlit as st
from collections import deque
import requests

from api_client import signup, login, google_login, get_messages, send_chat

st.set_page_config(page_title="Zenith EL - NLAK", page_icon="🎓")

st.title("Ⓩ Zenith Assistant")
WELCOME = {
    "role": "assistant", 
    "content": "Chào bạn, mình là Zenith, trợ lý AI hỗ trợ học Tiếng Anh toàn diện. Bạn cần mình giải thích từ vựng, sửa lỗi ngữ pháp hay luyện giao tiếp hôm nay?"
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
            display: inline-block;
            width: 100%;
            text-align: center;
            padding: 0.6rem 1rem;
            background-color: white;
            color: black;
            text-decoration: none;
            border-radius: 0.5rem;
            border: 1px solid #ddd;
            font-weight: 600;
        ">
            Đăng nhập với Google
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
    st.subheader("Đăng ký")
    with st.form("signup_form"):
        email = st.text_input("Email")
        password = st.text_input("Mật khẩu", type="password")
        submitted = st.form_submit_button("Tạo tài khoản")
        goto_login = st.form_submit_button("Đã có tài khoản? Đăng nhập")

    if goto_login:
        st.session_state.show_signup = False
        st.session_state.show_login = True
        st.rerun()

    if submitted:
        try:
            signup(email, password)
            st.success("Tạo tài khoản thành công, hãy đăng nhập")
            st.session_state.show_signup = False
            st.session_state.show_login = True
            st.rerun()
        except requests.HTTPError as e:
            st.error(f"Đăng ký thất bại: {e}")
        except Exception as e:
            st.error(f"Lỗi đăng ký: {e}")


handle_google_login_callback()

if st.session_state.user:
    st.success(f"Đang đăng nhập: {st.session_state.user['email']}")
    if st.button("Đăng xuất"):
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
    for msg in list(st.session_state.messages):
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    prompt = st.chat_input("Nhập tin nhắn...")
    if prompt:
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        try:
            res = send_chat(st.session_state.user["idToken"], prompt)
            reply = res["reply"]
        except Exception as e:
            reply = f"Lỗi backend: {e}"

        st.session_state.messages.append({"role": "assistant", "content": reply})
        st.rerun()