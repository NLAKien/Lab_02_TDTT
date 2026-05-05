import streamlit as st
from collections import deque
import requests

from api_client import (
    signup, login, google_login,
    get_messages, send_chat,
    new_conversation, get_conversations,
    delete_conversation 
)

st.set_page_config(page_title="Zenith", page_icon="🎓")

st.markdown("<h1 style='text-align: center;'>Ⓩ Zenith Assistant</h1>", unsafe_allow_html=True)

WELCOME = {
    "role": "assistant",
    "content": "Chào bạn, mình là Zenith, trợ lý AI hỗ trợ toàn diện. Bạn có gì muốn hỏi?"
}

# ─── SESSION STATE INIT ──────────────────────────────────

if "user"        not in st.session_state: st.session_state.user = None
if "conv_id"     not in st.session_state: st.session_state.conv_id = None
if "messages"    not in st.session_state: st.session_state.messages = deque([WELCOME], maxlen=8)
if "show_signup" not in st.session_state: st.session_state.show_signup = False
if "show_login"  not in st.session_state: st.session_state.show_login = True

# ─── HELPERS ─────────────────────────────────────────────

def clear_google_query_params():
    try:
        st.query_params.clear()
    except Exception:
        pass

def load_history():
    if not st.session_state.user or not st.session_state.conv_id:
        return
    try:
        msgs = get_messages(st.session_state.user["idToken"], st.session_state.conv_id)
        st.session_state.messages = deque(msgs or [WELCOME], maxlen=8)
    except Exception:
        st.session_state.messages = deque([WELCOME], maxlen=8)

def create_new_conversation():
    """Tạo conversation mới và set vào session_state."""
    res = new_conversation(st.session_state.user["idToken"])
    st.session_state.conv_id = res["conv_id"]
    st.session_state.messages = deque([WELCOME], maxlen=8)

# ─── GOOGLE LOGIN CALLBACK ───────────────────────────────

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
        create_new_conversation()
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

# ─── FORMS ───────────────────────────────────────────────

def login_form():
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
                create_new_conversation()
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
                display: flex; align-items: center; justify-content: center;
                width: 100%; padding: 0.5rem; background-color: white;
                color: #3c4043; text-decoration: none; border-radius: 4px;
                border: 1px solid #dadce0; font-weight: 500;
                font-family: 'Google Sans',arial,sans-serif; font-size: 14px;">
                    <img src="https://www.gstatic.com/images/branding/product/1x/googleg_48dp.png"
                        style="width: 18px; height: 18px; margin-right: 10px;">
                    Tiếp tục với Google
                </a>
                ''',
                unsafe_allow_html=True,
            )


def signup_form():
    _, col, _ = st.columns([1, 2, 1])
    with col:
        st.markdown("<h3 style='text-align: center;'>Đăng ký tài khoản</h3>", unsafe_allow_html=True)

        with st.form("signup_form", clear_on_submit=True):
            email            = st.text_input("Email",            placeholder="Nhập địa chỉ Email",    label_visibility="collapsed")
            password         = st.text_input("Mật khẩu",         type="password", placeholder="Nhập mật khẩu",         label_visibility="collapsed")
            confirm_password = st.text_input("Xác nhận mật khẩu", type="password", placeholder="Xác nhận lại mật khẩu", label_visibility="collapsed")
            signup_button    = st.form_submit_button("Tạo tài khoản", use_container_width=True)

            if signup_button:
                if not email or not password or not confirm_password:
                    st.error("Vui lòng điền đầy đủ thông tin.")
                elif password != confirm_password:
                    st.error("Mật khẩu xác nhận không khớp.")
                elif len(password) < 6:
                    st.error("Mật khẩu phải có ít nhất 6 ký tự.")
                else:
                    try:
                        signup(email, password)
                        st.success("Tạo tài khoản thành công! Hãy đăng nhập.")
                        st.session_state.show_signup = False
                        st.rerun()
                    except requests.HTTPError as e:
                        st.error(f"Đăng ký thất bại: {e}")
                    except Exception as e:
                        st.error(f"Lỗi: {e}")

        if st.button("Đã có tài khoản? Đăng nhập", use_container_width=True):
            st.session_state.show_signup = False
            st.rerun()

# ─── SIDEBAR ─────────────────────────────────────────────

def show_sidebar_history():
    with st.sidebar:
        st.title("Lịch sử đoạn chat")

        if st.button("+ Đoạn chat mới", use_container_width=True):
            create_new_conversation()
            st.rerun()

        st.divider()

        try:
            convs = get_conversations(st.session_state.user["idToken"])
            for conv in convs:
                title     = conv.get("title", "Đoạn chat mới")[:22]
                is_active = conv["id"] == st.session_state.conv_id
                label     = f"▶ {title}" if is_active else title

                col_title, col_del = st.columns([5, 1])

                with col_title:
                    if st.button(label, key=f"conv_{conv['id']}", use_container_width=True):
                        st.session_state.conv_id = conv["id"]
                        msgs = get_messages(st.session_state.user["idToken"], conv["id"])
                        st.session_state.messages = deque(msgs or [WELCOME], maxlen=8)
                        st.rerun()

                with col_del:
                    if st.button("🗑", key=f"del_{conv['id']}"):
                        try:
                            delete_conversation(st.session_state.user["idToken"], conv["id"])
                            if st.session_state.conv_id == conv["id"]:
                                create_new_conversation()
                        except Exception:
                            pass
                        st.rerun()

        except Exception:
            pass
# ─── MAIN ────────────────────────────────────────────────

handle_google_login_callback()

if st.session_state.user:
    # Header: thông tin user + nút đăng xuất
    cols = st.columns([1, 1, 1, 1, 1])

    with cols[3]:
        email   = st.session_state.user.get("email", "")
        initial = email[0].upper() if email else "?"
        st.markdown(
            f"""
            <div style="display:flex; align-items:center; gap:8px;
                        justify-content:flex-end; padding-top:6px">
                <div style="width:30px; height:30px; border-radius:50%;
                            background:#6c63ff; color:white;
                            display:flex; align-items:center; justify-content:center;
                            font-weight:bold; font-size:14px; flex-shrink:0">
                    {initial}
                </div>
                <span style="font-size:13px; color:#262730;
                             white-space:nowrap; overflow:hidden;
                             text-overflow:ellipsis; max-width:160px">
                    {email}
                </span>
            </div>
            """,
            unsafe_allow_html=True
        )

    with cols[4]:
        if st.button("Đăng xuất", use_container_width=True):
            st.session_state.user    = None
            st.session_state.conv_id = None
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

    # Hiển thị messages
    for msg in list(st.session_state.messages):
        icon = "🤖" if msg["role"] == "assistant" else "👤"
        with st.chat_message(msg["role"], avatar=icon):
            st.markdown(msg["content"])

    prompt = st.chat_input("Nhập tin nhắn...")
    if prompt:
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user", avatar="👤"):
            st.markdown(prompt)

        try:
            res   = send_chat(st.session_state.user["idToken"], prompt, st.session_state.conv_id)
            reply = res["reply"]
        except Exception as e:
            reply = f"Lỗi backend: {e}"

        st.session_state.messages.append({"role": "assistant", "content": reply})
        st.rerun()

# ─── CSS ─────────────────────────────────────────────────

st.markdown("""
    <style>
    [data-testid="stSidebar"] {
        background-color: #ffffff;
        border-right: 1px solid #e0e0e0;
    }
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