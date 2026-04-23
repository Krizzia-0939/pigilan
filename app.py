import streamlit as st
import runpy
from shared.asset_utils import ROOT_DIR, build_local_image_data_uri, resolve_asset_path
from shared.pwa import inject_pwa_support

PIGILAN_LOGO = resolve_asset_path("PIGilan-Logo.png")
PIGILAN_ICON = ROOT_DIR / "static" / "icon.svg"
#hello
page_config = {
    "page_title": "Pigilan",
    "layout": "wide",
    "initial_sidebar_state": "collapsed",
}
if PIGILAN_ICON.exists():
    page_config["page_icon"] = str(PIGILAN_ICON)

st.set_page_config(**page_config)
inject_pwa_support()

PIGILAN_LOGO_DATA_URI = build_local_image_data_uri(PIGILAN_LOGO) or build_local_image_data_uri(PIGILAN_ICON)


def inject_shell_styles():
    st.markdown(
        """
        <style>
        :root {
            --pigilan-olive: #6d7359;
            --pigilan-olive-deep: #596047;
            --pigilan-olive-soft: #8d9178;
            --pigilan-cream: #f8f1e8;
            --pigilan-paper: #fbf7f1;
            --pigilan-sand: #d8c8b6;
            --pigilan-sand-soft: rgba(216, 200, 182, 0.34);
            --pigilan-text: #4b4137;
            --pigilan-muted: #7d7367;
            --pigilan-shadow: 0 14px 32px rgba(85, 70, 56, 0.10);
        }

        [data-testid="stAppViewContainer"] {
            background:
                radial-gradient(circle at top right, rgba(198, 182, 164, 0.20), transparent 24%),
                linear-gradient(180deg, #f6efe6 0%, #f7f0e8 38%, #efe4d8 100%);
            color: var(--pigilan-text);
        }

        .main .block-container {
            max-width: 1120px;
        }

        .pigilan-header-card {
            display: flex;
            align-items: center;
            gap: 1.05rem;
            padding: 0.25rem 0;
            min-height: 5.15rem;
        }

        .pigilan-logo-image {
            width: clamp(4rem, 5vw, 4.5rem);
            height: clamp(4.3rem, 5.4vw, 4.9rem);
            display: block;
            flex-shrink: 0;
            object-fit: contain;
            filter: drop-shadow(0 10px 20px rgba(89, 96, 71, 0.18));
        }

        .pigilan-brand-copy {
            display: flex;
            flex-direction: column;
            justify-content: center;
            gap: 0.12rem;
        }

        .pigilan-brand-title {
            margin: 0;
            display: flex;
            align-items: center;
            color: var(--pigilan-text);
            font-size: clamp(3.55rem, 4.75vw, 4.2rem) !important;
            font-weight: 900 !important;
            letter-spacing: -0.055em;
            line-height: 0.9 !important;
        }

        .pigilan-brand-subtitle {
            margin: 0;
            color: var(--pigilan-muted);
            font-size: 0.78rem;
            line-height: 1.25;
        }

        h1, h2, h3, h4, h5, h6 {
            color: var(--pigilan-text);
        }

        p, label, span, div {
            color: inherit;
        }

        [data-testid="stCaptionContainer"] {
            color: var(--pigilan-muted);
        }

        .stTextInput label p,
        .stTextArea label p,
        .stNumberInput label p,
        .stSelectbox label p,
        .stMultiSelect label p,
        .stDateInput label p,
        .stFileUploader label p,
        .stRadio label p,
        .stCheckbox label p,
        .stMarkdown,
        .stMarkdown p,
        .stAlert,
        .stAlert p {
            color: var(--pigilan-text);
        }

        div[data-testid="stTextInput"] input,
        div[data-testid="stTextArea"] textarea,
        div[data-testid="stNumberInput"] input,
        div[data-testid="stDateInput"] input,
        div[data-testid="stSelectbox"] input,
        div[data-testid="stMultiSelect"] input,
        div[data-testid="stSelectbox"] div[data-baseweb="select"] > div,
        div[data-testid="stMultiSelect"] div[data-baseweb="select"] > div,
        div[data-testid="stFileUploader"] section,
        section[data-testid="stFileUploaderDropzone"],
        div[data-testid="stFileUploaderDropzone"] {
            color: var(--pigilan-text);
        }

        div[data-testid="stTextInput"] input::placeholder,
        div[data-testid="stTextArea"] textarea::placeholder,
        div[data-testid="stNumberInput"] input::placeholder,
        div[data-testid="stDateInput"] input::placeholder {
            color: var(--pigilan-muted);
            opacity: 1;
        }

        div[data-testid="stSelectbox"] svg,
        div[data-testid="stMultiSelect"] svg,
        div[data-testid="stDateInput"] svg,
        div[data-testid="stFileUploader"] small,
        div[data-testid="stFileUploader"] span,
        div[data-testid="stFileUploaderDropzone"] small,
        div[data-testid="stFileUploaderDropzone"] span {
            color: var(--pigilan-muted);
        }

        div[data-testid="stVerticalBlockBorderWrapper"] {
            background: rgba(255, 251, 246, 0.84);
            border: 1px solid rgba(216, 200, 182, 0.96);
            border-radius: 26px;
            box-shadow: var(--pigilan-shadow);
        }

        div[data-testid="stRadio"] > div {
            padding: 0;
            background: transparent;
            border: none;
            box-shadow: none;
        }

        div[data-testid="stRadio"] [role="radiogroup"] {
            justify-content: center;
            gap: 1.35rem;
            flex-wrap: wrap;
        }

        div[data-testid="stRadio"] label {
            min-height: auto;
            padding: 0;
            border-radius: 0;
            background: transparent;
            border: none;
        }

        div[data-testid="stRadio"] label > div {
            position: relative;
            padding: 0.55rem 0 0.9rem;
        }

        div[data-testid="stRadio"] label p {
            color: var(--pigilan-muted);
            font-size: 0.95rem;
            font-weight: 600;
        }

        div[data-testid="stRadio"] label:hover p {
            color: var(--pigilan-text);
        }

        div[data-testid="stRadio"] input:checked + div {
            background: transparent;
            box-shadow: none;
        }

        div[data-testid="stRadio"] input:checked + div p {
            color: var(--pigilan-text);
            font-weight: 700;
        }

        div[data-testid="stRadio"] input:checked + div::after {
            content: "";
            position: absolute;
            left: 0;
            right: 0;
            bottom: 0.25rem;
            height: 3px;
            border-radius: 999px;
            background: linear-gradient(90deg, var(--pigilan-olive-deep), var(--pigilan-olive));
        }

        div[data-testid="stButton"] > button {
            background: linear-gradient(135deg, var(--pigilan-olive-deep), var(--pigilan-olive));
            color: #fff;
            border: none;
            border-radius: 12px;
            box-shadow: 0 10px 22px rgba(89, 96, 71, 0.18);
        }

        div[data-testid="stButton"] > button:hover {
            background: linear-gradient(135deg, #50573f, #666d53);
            color: #fff;
        }

        .pigilan-nav-status {
            margin-top: 0.35rem;
            color: var(--pigilan-muted);
            font-size: 0.78rem;
            text-align: right;
        }

        .pigilan-admin-nav {
            display: flex;
            align-items: center;
            height: 100%;
            padding: 0.2rem 0;
        }

        .pigilan-admin-nav-item {
            position: relative;
            display: inline-flex;
            align-items: center;
            gap: 0.45rem;
            padding: 0.55rem 0 0.9rem;
            color: var(--pigilan-text);
            font-size: 0.98rem;
            font-weight: 700;
            line-height: 1.2;
        }

        .pigilan-admin-nav-item::after {
            content: "";
            position: absolute;
            left: 0;
            right: 0;
            bottom: 0.25rem;
            height: 3px;
            border-radius: 999px;
            background: linear-gradient(90deg, var(--pigilan-olive-deep), var(--pigilan-olive));
        }

        .pigilan-admin-nav-dot {
            width: 0.62rem;
            height: 0.62rem;
            border-radius: 50%;
            background: #e16b63;
            box-shadow: 0 0 0 0.22rem rgba(225, 107, 99, 0.18);
        }

        @media (max-width: 900px) {
            .pigilan-brand-title {
                font-size: clamp(2.8rem, 7.8vw, 3.35rem) !important;
            }

            .pigilan-brand-subtitle {
                font-size: 0.72rem;
            }

            div[data-testid="stRadio"] [role="radiogroup"] {
                gap: 0.9rem;
            }
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


inject_shell_styles()

PAGE_ALIASES = {
    "Check Pig": "Health Assessment",
    "Cases": "My Reports",
    "Account": "My Account",
}

# Initialize page
if "page" not in st.session_state:
    st.session_state.page = "Home"

st.session_state.page = PAGE_ALIASES.get(st.session_state.page, st.session_state.page)

user = st.session_state.get("user")
is_admin = bool(user and user.get("role") == "admin")


def logout_current_user():
    st.session_state.user = None
    st.session_state.page = "Home"
    st.session_state.top_nav_page = "Home"
    st.session_state.auth_mode = "signin"
    st.session_state.show_edit_profile = False
    st.session_state.nav_logout_confirm = False
    st.session_state.account_logout_confirm = False
    st.session_state.admin_logout_confirm = False


def sync_page_from_top_nav():
    selected_page = st.session_state.get("top_nav_page")
    if selected_page:
        st.session_state.page = selected_page


if is_admin:
    st.session_state.page = "Dashboard"
elif st.session_state.page == "Dashboard":
    st.session_state.page = "My Account"
elif st.session_state.page == "About":
    st.session_state.page = "Home"


if is_admin:
    pages_list = ["Dashboard"]
else:
    pages_list = ["Home", "Health Assessment", "My Reports", "My Account"]

with st.container(border=True):
    brand_col, nav_col, action_col = st.columns([1.9, 2.6, 1.0], gap="medium")

    with brand_col:
        logo_markup = (
            f'<img class="pigilan-logo-image" src="{PIGILAN_LOGO_DATA_URI}" alt="PIGilan logo">'
            if PIGILAN_LOGO_DATA_URI
            else '<div class="pigilan-brand-title">PG</div>'
        )
        st.markdown(
            f"""
            <div class="pigilan-header-card">
                {logo_markup}
                <div class="pigilan-brand-copy">
                    <div class="pigilan-brand-title">Pigilan</div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with nav_col:
        if is_admin:
            st.markdown(
                """
                <div class="pigilan-admin-nav">
                    <div class="pigilan-admin-nav-item">
                        <span class="pigilan-admin-nav-dot"></span>
                        <span>Dashboard</span>
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )
        else:
            current_nav_page = st.session_state.page if st.session_state.page in pages_list else pages_list[0]
            if st.session_state.get("top_nav_page") != current_nav_page:
                st.session_state.top_nav_page = current_nav_page
            st.radio(
                "Go to",
                pages_list,
                key="top_nav_page",
                horizontal=True,
                label_visibility="collapsed",
                on_change=sync_page_from_top_nav,
            )

    with action_col:
        if is_admin:
            if st.session_state.get("nav_logout_confirm", False):
                st.caption("Are you sure you want to log out?")
                confirm_col, cancel_col = st.columns(2, gap="small")
                with confirm_col:
                    if st.button("Confirm", key="top_nav_admin_logout_confirm", use_container_width=True):
                        logout_current_user()
                        st.rerun()
                with cancel_col:
                    if st.button("Cancel", key="top_nav_admin_logout_cancel", use_container_width=True):
                        st.session_state.nav_logout_confirm = False
                        st.rerun()
            else:
                if st.button("Log Out", key="top_nav_admin_logout", use_container_width=True):
                    st.session_state.nav_logout_confirm = True
                    st.rerun()
            st.markdown("<div class='pigilan-nav-status'>Admin dashboard</div>", unsafe_allow_html=True)
        elif user:
            if st.session_state.get("nav_logout_confirm", False):
                st.caption("Are you sure you want to log out?")
                confirm_col, cancel_col = st.columns(2, gap="small")
                with confirm_col:
                    if st.button("Confirm", key="top_nav_logout_confirm", use_container_width=True):
                        logout_current_user()
                        st.rerun()
                with cancel_col:
                    if st.button("Cancel", key="top_nav_logout_cancel", use_container_width=True):
                        st.session_state.nav_logout_confirm = False
                        st.rerun()
            else:
                if st.button("Log Out", key="top_nav_logout", use_container_width=True):
                    st.session_state.nav_logout_confirm = True
                    st.rerun()
            first_name = user.get("first_name", user.get("username", "Farmer"))
            st.markdown(
                f"<div class='pigilan-nav-status'>Signed in as {first_name}</div>",
                unsafe_allow_html=True,
            )
        else:
            st.session_state.nav_logout_confirm = False
            if st.button("Sign In", key="top_nav_signin", use_container_width=True):
                st.session_state.page = "My Account"
                st.session_state.auth_mode = "signin"
                st.rerun()
            st.markdown("<div class='pigilan-nav-status'>Open My Account to sign up</div>", unsafe_allow_html=True)

# -------- DISPLAY PAGE CONTENT ---------
page = st.session_state.page

# Run the actual page file
if page == "Home":
    runpy.run_path("views/home.py")
elif page == "Health Assessment":
    runpy.run_path("views/asf_detection.py")
elif page == "My Reports":
    runpy.run_path("views/cases.py")
elif page == "Dashboard" or page == "My Account":
    runpy.run_path("views/account.py")
