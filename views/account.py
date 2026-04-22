from html import escape
from datetime import datetime

import streamlit as st

from core.backend import (
    BIOSECURITY_ITEMS,
    edit_user_profile,
    get_admin_dashboard_data,
    get_database_backup,
    get_latest_biosecurity_state,
    get_sync_status_summary,
    login_user,
    register_user,
    save_biosecurity_check,
    sync_with_server,
)


if "user" not in st.session_state:
    st.session_state.user = None
if "show_edit_profile" not in st.session_state:
    st.session_state.show_edit_profile = False
if "auth_notice" not in st.session_state:
    st.session_state.auth_notice = ""
if "auth_mode" not in st.session_state:
    st.session_state.auth_mode = "signin"


def inject_auth_styles():
    st.markdown(
        """
        <style>
        .auth-hero {
            position: relative;
            max-width: 760px;
            margin: 0 auto 1.15rem;
            padding: 0.5rem 0 1.25rem;
        }

        .auth-hero::after {
            content: "";
            position: absolute;
            right: -1rem;
            bottom: -0.25rem;
            width: min(42vw, 320px);
            height: 140px;
            border-radius: 999px;
            background:
                radial-gradient(circle at 68% 45%, rgba(255, 255, 255, 0.28) 0, rgba(255, 255, 255, 0.18) 18%, transparent 21%),
                radial-gradient(circle at 54% 56%, rgba(255, 255, 255, 0.22) 0, rgba(255, 255, 255, 0.12) 16%, transparent 18%),
                linear-gradient(135deg, rgba(145, 152, 124, 0.20), rgba(222, 211, 198, 0.05));
            filter: blur(1px);
            opacity: 0.78;
            pointer-events: none;
        }

        .auth-hero h1 {
            margin: 0 0 0.45rem;
            color: #4b4137;
            font-size: clamp(2rem, 5vw, 3rem);
            line-height: 1.05;
            letter-spacing: -0.03em;
        }

        .auth-hero p {
            max-width: 560px;
            margin: 0;
            color: #74695d;
            font-size: 1.02rem;
            line-height: 1.6;
        }

        div[data-testid="stVerticalBlockBorderWrapper"] {
            max-width: 760px;
            margin: 0 auto 1rem;
            background: rgba(255, 251, 247, 0.90);
            border: 1px solid rgba(216, 200, 182, 0.96);
            border-radius: 24px;
            box-shadow: 0 16px 34px rgba(83, 69, 56, 0.10);
        }

        .auth-brand-row {
            display: flex;
            align-items: center;
            gap: 0.95rem;
            margin: -0.15rem -0.1rem 1rem;
            padding: 0.15rem 0 1rem;
            border-bottom: 1px solid rgba(216, 200, 182, 0.65);
        }

        .auth-shield {
            position: relative;
            width: 3.45rem;
            height: 3.8rem;
            display: flex;
            align-items: center;
            justify-content: center;
            clip-path: polygon(50% 0%, 86% 12%, 86% 48%, 50% 100%, 14% 48%, 14% 12%);
            background: linear-gradient(160deg, #5a6047, #8b8f78);
            box-shadow: 0 10px 20px rgba(89, 96, 71, 0.16);
        }

        .auth-shield::before {
            content: "";
            position: absolute;
            inset: 0.2rem;
            clip-path: polygon(50% 0%, 86% 12%, 86% 48%, 50% 100%, 14% 48%, 14% 12%);
            border: 1px solid rgba(255, 255, 255, 0.42);
        }

        .auth-shield::after {
            content: "";
            width: 1rem;
            height: 0.5rem;
            border-left: 0.24rem solid #fff;
            border-bottom: 0.24rem solid #fff;
            transform: rotate(-45deg) translateY(-0.05rem);
            z-index: 1;
        }

        .auth-brand-title {
            margin: 0;
            color: #4b4137;
            font-size: clamp(1.65rem, 4vw, 2.35rem);
            line-height: 1;
            font-weight: 800;
            letter-spacing: -0.03em;
        }

        .auth-brand-subtitle {
            margin: 0.18rem 0 0;
            color: #74695d;
            font-size: 0.86rem;
            line-height: 1.35;
        }

        .auth-section-title {
            margin: 0;
            color: #4b4137;
            font-size: clamp(1.55rem, 3.5vw, 2.15rem);
            line-height: 1.08;
            font-weight: 800;
            letter-spacing: -0.03em;
        }

        .auth-section-copy {
            margin: 0.42rem 0 1rem;
            color: #74695d;
            font-size: 1rem;
            line-height: 1.55;
        }

        .auth-input-icon {
            display: flex;
            align-items: center;
            justify-content: center;
            min-height: 2.95rem;
            border-radius: 12px;
            background: linear-gradient(180deg, rgba(239, 229, 219, 0.94), rgba(231, 219, 206, 0.88));
            border: 1px solid rgba(216, 200, 182, 0.96);
            color: #827563;
            font-size: 1rem;
            font-weight: 700;
        }

        div[data-testid="stTextInput"] input {
            min-height: 2.95rem;
            border-radius: 12px;
            border: 1px solid rgba(216, 200, 182, 0.96);
            background: rgba(255, 252, 249, 0.96);
            color: #4b4137;
        }

        div[data-testid="stTextInput"] input::placeholder {
            color: #8a7d70;
        }

        div[data-testid="stFormSubmitButton"] > button {
            min-height: 3rem;
            border-radius: 10px;
            border: none;
            background: linear-gradient(180deg, #677056, #5a6047);
            color: #fff;
            font-size: 1.08rem;
            font-weight: 700;
            box-shadow: 0 12px 24px rgba(89, 96, 71, 0.16);
        }

        div[data-testid="stFormSubmitButton"] > button:hover {
            background: linear-gradient(180deg, #5b634b, #50573f);
            color: #fff;
        }

        div[data-testid="stButton"] > button[kind="tertiary"] {
            min-height: auto;
            padding: 0;
            border: none;
            background: transparent;
            box-shadow: none;
            color: #5a6047;
            font-size: 1rem;
            font-weight: 700;
            text-decoration: underline;
            text-underline-offset: 0.14rem;
        }

        div[data-testid="stButton"] > button[kind="tertiary"]:hover {
            background: transparent;
            color: #4f5640;
        }

        .auth-switch-copy {
            margin: 1rem 0 0.1rem;
            color: #74695d;
            font-size: 1rem;
            line-height: 1.5;
            text-align: center;
        }

        .auth-switch-row {
            display: flex;
            justify-content: center;
            align-items: center;
            gap: 0.35rem;
            flex-wrap: wrap;
            margin-top: 1rem;
        }

        .auth-footer {
            max-width: 760px;
            margin: 2rem auto 0;
            display: flex;
            justify-content: space-between;
            gap: 0.8rem;
            flex-wrap: wrap;
            color: #817569;
            font-size: 0.92rem;
        }

        .auth-footer-links {
            display: flex;
            gap: 0.95rem;
            flex-wrap: wrap;
        }

        .auth-footer-links span {
            color: #817569;
        }

        .auth-helper-note {
            margin: 0.4rem 0 0.2rem;
            color: #817569;
            font-size: 0.85rem;
            line-height: 1.45;
        }

        @media (max-width: 768px) {
            .auth-hero {
                padding-bottom: 0.9rem;
            }

            .auth-hero::after {
                width: 180px;
                height: 100px;
                right: 0;
            }

            .auth-footer {
                flex-direction: column;
                align-items: flex-start;
            }
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def get_auth_mode():
    raw_mode = str(st.session_state.get("auth_mode", "signin")).strip().lower()
    if raw_mode not in {"signin", "signup"}:
        raw_mode = "signin"
    return raw_mode


def set_auth_mode(mode):
    if mode not in {"signin", "signup"}:
        mode = "signin"
    st.session_state.auth_mode = mode
    st.session_state.page = "My Account"


def render_logout_confirmation(trigger_label, state_key, button_prefix):
    if st.session_state.get(state_key, False):
        st.warning("Are you sure you want to log out?")
        confirm_col, cancel_col = st.columns(2, gap="small")
        with confirm_col:
            if st.button("Confirm", key=f"{button_prefix}_logout_confirm", use_container_width=True):
                st.session_state[state_key] = False
                return True
        with cancel_col:
            if st.button("Cancel", key=f"{button_prefix}_logout_cancel", use_container_width=True):
                st.session_state[state_key] = False
                st.rerun()
        return False

    if st.button(trigger_label, key=f"{button_prefix}_logout", use_container_width=True):
        st.session_state[state_key] = True
        st.rerun()
    return False


def split_full_name(full_name):
    parts = [part for part in str(full_name).split() if part]
    if len(parts) < 2:
        return None, None
    return parts[0], " ".join(parts[1:])


def render_auth_input(icon_markup, label, placeholder, key, field_type="default"):
    icon_col, field_col = st.columns([0.12, 0.88], gap="small")
    with icon_col:
        st.markdown(
            f"<div class='auth-input-icon'>{icon_markup}</div>",
            unsafe_allow_html=True,
        )
    with field_col:
        return st.text_input(
            label,
            placeholder=placeholder,
            key=key,
            type=field_type,
            label_visibility="collapsed",
        )


ACCOUNT_BIOSECURITY_ITEMS = [
    "Maintain strict biosecurity",
    "Only allow essential visitors to enter your farm, and insist that they wear clean or disposable clothing and footwear, and wash their hands (or shower in if possible)",
    "Only allow vehicles and equipment on to the farm if they have been cleaned and disinfected beforehand",
    "Do not allow people who may have been in contact with other pigs on to your farm",
    "Do not allow staff and visitors to bring pork products on to the farm",
    "Do not allow catering waste / scraps to be fed to pigs - dispose of it safely",
    "Only source pigs and semen of known health status",
]


def inject_profile_styles():
    st.markdown(
        """
        <style>
        .profile-shell {
            max-width: 860px;
            margin: 0 auto;
        }

        .profile-title {
            margin: 0 0 0.9rem;
            color: #4b4137;
            font-size: clamp(1.95rem, 4vw, 2.7rem);
            line-height: 1.05;
            letter-spacing: -0.03em;
        }

        .profile-card {
            display: grid;
            grid-template-columns: auto 1fr;
            gap: 1rem;
            align-items: start;
        }

        .profile-avatar {
            display: flex;
            align-items: center;
            justify-content: center;
            width: 4.4rem;
            height: 4.4rem;
            border-radius: 50%;
            background: linear-gradient(180deg, rgba(233, 225, 214, 0.95), rgba(213, 199, 182, 0.95));
            border: 1px solid rgba(183, 168, 149, 0.75);
            color: #6a6657;
            font-size: 1.38rem;
            font-weight: 800;
            box-shadow: inset 0 1px 0 rgba(255, 255, 255, 0.55);
        }

        .profile-card-name {
            margin: 0;
            color: #4b4137;
            font-size: clamp(1.35rem, 2.5vw, 1.8rem);
            line-height: 1.15;
            font-weight: 800;
        }

        .profile-card-subtitle {
            margin: 0.2rem 0 0;
            color: #74695d;
            font-size: 0.98rem;
            line-height: 1.45;
        }

        .profile-meta {
            margin-top: 1rem;
            display: grid;
            gap: 0.4rem;
        }

        .profile-meta p {
            margin: 0;
            color: #5e5449;
            font-size: 1rem;
            line-height: 1.5;
        }

        .profile-bar {
            display: flex;
            align-items: center;
            justify-content: space-between;
            gap: 0.8rem;
            margin: -0.1rem -0.1rem 0.9rem;
            padding: 0.62rem 0.95rem;
            border-radius: 14px;
            background: linear-gradient(180deg, #6d7359, #5a6047);
            color: #fff;
            font-size: 1rem;
            font-weight: 700;
            letter-spacing: 0.01em;
        }

        .profile-bar span,
        .profile-bar div {
            color: inherit;
        }

        .profile-overview-row {
            display: flex;
            align-items: center;
            gap: 0.6rem;
            flex-wrap: wrap;
            margin-bottom: 0.8rem;
            color: #5c5247;
            font-size: 1rem;
        }

        .profile-protection-chip {
            display: inline-flex;
            align-items: center;
            gap: 0.45rem;
            padding: 0.38rem 0.72rem;
            border-radius: 999px;
            background: rgba(245, 238, 230, 0.9);
            border: 1px solid rgba(216, 200, 182, 0.92);
        }

        .profile-protection-chip--high {
            background: rgba(226, 244, 230, 0.9);
            border-color: rgba(128, 169, 132, 0.6);
        }

        .profile-protection-chip--moderate {
            background: rgba(251, 240, 216, 0.92);
            border-color: rgba(214, 177, 88, 0.58);
        }

        .profile-protection-chip--low {
            background: rgba(251, 226, 226, 0.92);
            border-color: rgba(199, 110, 110, 0.55);
        }

        .profile-protection-chip--pending {
            background: rgba(245, 238, 230, 0.92);
            border-color: rgba(183, 168, 149, 0.55);
        }

        .profile-count-grid {
            display: grid;
            grid-template-columns: repeat(2, minmax(0, 1fr));
            gap: 0.8rem;
        }

        .profile-count-card {
            padding: 0.75rem 0.9rem;
            border-radius: 14px;
            background: rgba(255, 252, 248, 0.88);
            border: 1px solid rgba(216, 200, 182, 0.95);
        }

        .profile-count-card p {
            margin: 0;
            color: #786d61;
            font-size: 0.94rem;
        }

        .profile-count-card strong {
            display: block;
            margin-top: 0.15rem;
            color: #4b4137;
            font-size: 1.4rem;
            line-height: 1.1;
        }

        .profile-muted-line {
            margin: 0.8rem 0 0;
            color: #7a7064;
            font-size: 0.92rem;
            line-height: 1.5;
        }

        .profile-checklist-note {
            margin: 0 0 0.9rem;
            color: #7a7064;
            font-size: 0.95rem;
            line-height: 1.5;
        }

        div[data-testid="stCheckbox"] {
            padding: 0.18rem 0.1rem;
        }

        div[data-testid="stCheckbox"] label p {
            color: #5f5549;
            font-size: 0.98rem;
            line-height: 1.45;
        }

        div[data-testid="stCheckbox"] input[type="checkbox"] {
            accent-color: #6d7359;
        }

        div[data-testid="stFormSubmitButton"] > button,
        div[data-testid="stDownloadButton"] > button {
            min-height: 2.95rem;
            border-radius: 10px;
            border: none;
            background: linear-gradient(180deg, #677056, #5a6047);
            color: #fff;
            font-size: 1rem;
            font-weight: 700;
            box-shadow: 0 12px 24px rgba(89, 96, 71, 0.16);
        }

        div[data-testid="stFormSubmitButton"] > button:hover,
        div[data-testid="stDownloadButton"] > button:hover {
            background: linear-gradient(180deg, #5b634b, #50573f);
            color: #fff;
        }

        .profile-action-tile {
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            gap: 0.35rem;
            min-height: 7.8rem;
            margin-bottom: 0.85rem;
            border-radius: 18px;
            background: linear-gradient(180deg, rgba(255, 251, 246, 0.9), rgba(245, 236, 226, 0.92));
            border: 1px solid rgba(216, 200, 182, 0.95);
            color: #74695d;
            text-align: center;
        }

        .profile-action-tile strong {
            color: #4b4137;
            font-size: 1.02rem;
        }

        .profile-action-icon {
            font-size: 2.45rem;
            line-height: 1;
            color: #9a876a;
        }

        .profile-action-stack {
            display: grid;
            gap: 0.85rem;
        }

        .profile-edit-panel-title {
            margin: 0 0 0.45rem;
            color: #4b4137;
            font-size: 1.35rem;
            font-weight: 800;
            line-height: 1.15;
        }

        .profile-edit-panel-copy {
            margin: 0 0 0.9rem;
            color: #7a7064;
            font-size: 0.95rem;
            line-height: 1.5;
        }

        @media (max-width: 768px) {
            .profile-card {
                grid-template-columns: 1fr;
            }

            .profile-avatar {
                width: 4rem;
                height: 4rem;
            }

            .profile-count-grid {
                grid-template-columns: 1fr;
            }

            .profile-action-tile {
                min-height: 6.8rem;
            }
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def format_address(user):
    explicit_address = str(user.get("address") or "").strip()
    if explicit_address and explicit_address.lower() != "not set yet":
        return explicit_address

    parts = [
        str(user.get("barangay") or "").strip(),
        str(user.get("municipality") or "").strip(),
        str(user.get("province") or "").strip(),
    ]
    parts = [part for part in parts if part and part.lower() != "not set yet"]
    return ", ".join(parts) if parts else "Not set yet"


def get_profile_initials(user):
    first_name = str(user.get("first_name") or "").strip()
    last_name = str(user.get("last_name") or "").strip()
    initials = f"{first_name[:1]}{last_name[:1]}".strip().upper()
    return initials or "U"


def get_protection_chip_class(protection):
    if protection == "High protection from ASF":
        return "profile-protection-chip profile-protection-chip--high"
    if protection == "Moderate protection from ASF":
        return "profile-protection-chip profile-protection-chip--moderate"
    if protection == "Low protection from ASF":
        return "profile-protection-chip profile-protection-chip--low"
    return "profile-protection-chip"


def inject_admin_styles():
    st.markdown(
        """
        <style>
        .admin-shell {
            max-width: 1080px;
            margin: 0 auto;
        }

        .admin-title {
            margin: 0 0 0.95rem;
            color: #4b4137;
            font-size: clamp(2rem, 4.5vw, 2.9rem);
            line-height: 1.06;
            letter-spacing: -0.03em;
        }

        .admin-banner {
            margin: 0 0 0.85rem;
            padding: 1rem 1.15rem;
            border-radius: 16px;
            border: 1px solid rgba(216, 200, 182, 0.92);
            font-size: 0.97rem;
            line-height: 1.55;
        }

        .admin-banner--success {
            background: rgba(231, 242, 221, 0.96);
            color: #526146;
        }

        .admin-banner--info {
            background: rgba(236, 231, 245, 0.94);
            color: #665e74;
        }

        .admin-banner--warning {
            background: rgba(251, 240, 216, 0.95);
            color: #7c6430;
        }

        .admin-banner--error {
            background: rgba(251, 226, 226, 0.95);
            color: #8f4343;
        }

        .admin-card {
            height: 100%;
            padding: 1.15rem 1.15rem 1.05rem;
            border-radius: 18px;
            background: rgba(255, 251, 246, 0.92);
            border: 1px solid rgba(216, 200, 182, 0.95);
            box-shadow: 0 14px 26px rgba(83, 69, 56, 0.08);
        }

        .admin-card-title {
            margin: 0;
            color: #665c50;
            font-size: 1rem;
            line-height: 1.35;
            font-weight: 700;
        }

        .admin-card-value {
            margin: 0.45rem 0 0;
            color: #4b4137;
            font-size: clamp(2rem, 3vw, 2.7rem);
            line-height: 1.02;
            font-weight: 800;
        }

        .admin-card-copy {
            margin: 0.22rem 0 0;
            color: #7a7064;
            font-size: 0.9rem;
            line-height: 1.45;
        }

        .admin-card-inline {
            display: flex;
            align-items: center;
            gap: 0.55rem;
            flex-wrap: wrap;
            margin-top: 0.55rem;
        }

        .admin-card-kicker {
            margin: 0.85rem 0 0;
            color: #6f6458;
            font-size: 0.88rem;
            line-height: 1.45;
            font-weight: 700;
        }

        .admin-stat-chip {
            display: inline-flex;
            align-items: center;
            justify-content: center;
            padding: 0.28rem 0.6rem;
            border-radius: 999px;
            font-size: 0.78rem;
            line-height: 1.2;
            font-weight: 700;
        }

        .admin-stat-chip--high {
            background: rgba(248, 220, 220, 0.95);
            color: #9b4136;
        }

        .admin-stat-chip--moderate {
            background: rgba(251, 237, 208, 0.95);
            color: #9a6f2f;
        }

        .admin-stat-chip--low {
            background: rgba(227, 241, 227, 0.95);
            color: #4b7651;
        }

        .admin-sync-footnote {
            margin: 0.8rem 0 0;
            padding-top: 0.8rem;
            border-top: 1px solid rgba(216, 200, 182, 0.82);
        }

        .admin-upload-copy {
            margin: 0.38rem 0 0.8rem;
            color: #7a7064;
            font-size: 0.92rem;
            line-height: 1.55;
        }

        .admin-section-header {
            display: flex;
            align-items: center;
            justify-content: space-between;
            gap: 1rem;
            flex-wrap: wrap;
            margin: 2rem 0 0.9rem;
        }

        .admin-section-title {
            margin: 0;
            color: #4b4137;
            font-size: clamp(1.7rem, 3vw, 2.35rem);
            line-height: 1.1;
            letter-spacing: -0.03em;
        }

        .admin-table {
            width: 100%;
            border-collapse: collapse;
            overflow: hidden;
            border-radius: 18px;
            border: 1px solid rgba(216, 200, 182, 0.92);
            background: rgba(255, 251, 246, 0.92);
        }

        .admin-table thead th {
            padding: 0.9rem 0.9rem;
            background: rgba(247, 240, 232, 0.95);
            border-bottom: 1px solid rgba(216, 200, 182, 0.9);
            color: #6a6054;
            font-size: 0.85rem;
            line-height: 1.3;
            font-weight: 700;
            text-align: left;
        }

        .admin-table tbody td {
            padding: 0.9rem;
            border-bottom: 1px solid rgba(234, 224, 214, 0.9);
            vertical-align: top;
        }

        .admin-table tbody tr:last-child td {
            border-bottom: none;
        }

        .admin-table-main {
            margin: 0;
            color: #4b4137;
            font-size: 0.95rem;
            line-height: 1.45;
            font-weight: 700;
        }

        .admin-table-sub {
            margin: 0.24rem 0 0;
            color: #7b7064;
            font-size: 0.85rem;
            line-height: 1.45;
        }

        .admin-meta-grid {
            display: grid;
            gap: 0.85rem;
            margin-top: 1.2rem;
        }

        .admin-meta-card {
            padding: 1rem 1.05rem;
            border-radius: 16px;
            background: rgba(255, 251, 246, 0.9);
            border: 1px solid rgba(216, 200, 182, 0.92);
        }

        .admin-meta-card h3 {
            margin: 0 0 0.55rem;
            color: #4b4137;
            font-size: 1.05rem;
            line-height: 1.3;
        }

        .admin-meta-card p {
            margin: 0.35rem 0 0;
            color: #74695d;
            font-size: 0.92rem;
            line-height: 1.55;
        }

        .admin-empty-state {
            padding: 1rem 1.05rem;
            border-radius: 16px;
            background: rgba(255, 252, 248, 0.92);
            border: 1px solid rgba(216, 200, 182, 0.92);
            color: #74695d;
            font-size: 0.95rem;
            line-height: 1.55;
        }

        .admin-footer {
            display: flex;
            align-items: center;
            justify-content: space-between;
            gap: 0.9rem;
            flex-wrap: wrap;
            margin: 2rem 0 0.25rem;
            color: #827669;
            font-size: 0.92rem;
        }

        .admin-footer-links {
            display: flex;
            gap: 0.95rem;
            flex-wrap: wrap;
        }

        div[data-testid="stFileUploader"] section,
        section[data-testid="stFileUploaderDropzone"],
        div[data-testid="stFileUploaderDropzone"] {
            border-radius: 18px;
            border: 2px dashed rgba(164, 154, 138, 0.62);
            background: rgba(255, 252, 248, 0.94);
        }

        div[data-testid="stFileUploader"] small {
            color: #85796d;
        }

        div[data-testid="stSelectbox"] > div[data-baseweb="select"] > div {
            min-height: 2.8rem;
            border-radius: 12px;
            border-color: rgba(216, 200, 182, 0.95);
            background: rgba(255, 252, 248, 0.96);
            color: #4b4137;
        }

        div[data-testid="stButton"] > button,
        div[data-testid="stDownloadButton"] > button {
            border-radius: 11px;
        }

        @media (max-width: 900px) {
            .admin-table {
                display: block;
                overflow-x: auto;
                white-space: nowrap;
            }
        }

        @media (max-width: 640px) {
            .admin-footer {
                flex-direction: column;
                align-items: flex-start;
            }
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def format_display_date(value):
    raw_value = str(value or "").strip()
    if not raw_value:
        return "No date"
    raw_value = raw_value.replace("Z", "+00:00")
    for pattern in ("%Y-%m-%d %H:%M:%S", "%Y-%m-%d"):
        try:
            return datetime.strptime(raw_value.split("+")[0], pattern).strftime("%b %d, %Y")
        except ValueError:
            continue
    try:
        return datetime.fromisoformat(raw_value).strftime("%b %d, %Y")
    except ValueError:
        return raw_value.split(" ")[0]


def get_admin_risk_chip_class(risk_level):
    normalized = str(risk_level or "").strip().upper()
    if normalized == "HIGH RISK":
        return "admin-stat-chip admin-stat-chip--high"
    if normalized == "MODERATE RISK":
        return "admin-stat-chip admin-stat-chip--moderate"
    return "admin-stat-chip admin-stat-chip--low"


def format_admin_risk_label(risk_level):
    normalized = str(risk_level or "").strip().upper()
    if not normalized:
        return "Low Risk"
    return normalized.title()


def build_admin_case_table_rows(cases):
    rows = []
    for case in cases:
        case_name = str(case.get("case_name") or "Untitled Case").strip()
        farmer_name = (
            f"{str(case.get('first_name') or '').strip()} {str(case.get('last_name') or '').strip()}".strip()
            or str(case.get("username") or "Farmer")
        )
        rows.append(
            (
                "<tr>"
                "<td>"
                f"<p class=\"admin-table-main\">Case #{escape(str(case.get('id', '')))} - {escape(format_admin_risk_label(case.get('risk_level')))}</p>"
                f"<p class=\"admin-table-sub\">{escape(case_name)}</p>"
                "</td>"
                "<td>"
                f"<span class=\"{get_admin_risk_chip_class(case.get('risk_level'))}\">{escape(format_admin_risk_label(case.get('risk_level')))}</span>"
                "</td>"
                "<td>"
                f"<p class=\"admin-table-main\">{escape(farmer_name)}</p>"
                f"<p class=\"admin-table-sub\">{escape(format_address(case))}</p>"
                "</td>"
                "<td>"
                f"<p class=\"admin-table-main\">{escape(str(case.get('case_status') or 'Open'))}</p>"
                f"<p class=\"admin-table-sub\">{escape(format_display_date(case.get('created_at')))}</p>"
                "</td>"
                "</tr>"
            )
        )
    return "".join(rows)


def render_admin_footer():
    return


if st.session_state.user:
    user = st.session_state.user
    if user.get("role") == "admin":
        inject_admin_styles()
        admin_data = get_admin_dashboard_data()
        backup = get_database_backup()
        risk_filter = "All"
        filtered_cases = admin_data["recent_cases"]
        latest_alert = admin_data["recent_alerts"][0] if admin_data["recent_alerts"] else None
        alert_label = "No recent alert"
        alert_message = "Recent risk notifications will show here."
        alert_chip_class = "admin-stat-chip admin-stat-chip--low"

        if latest_alert:
            alert_label = format_admin_risk_label(latest_alert.get("alert_level"))
            alert_message = str(latest_alert.get("alert_message") or "New alert received.")
            alert_chip_class = get_admin_risk_chip_class(latest_alert.get("alert_level"))

        st.markdown("<h1 class='admin-title'>Dashboard</h1>", unsafe_allow_html=True)
        st.markdown(
            "<div class='admin-banner admin-banner--success'>Admin account signed in.</div>",
            unsafe_allow_html=True,
        )
        st.markdown(
            (
                "<div class='admin-banner admin-banner--info'>"
                f"Default admin login: {escape(admin_data['admin_credentials']['username'])} / "
                f"{escape(admin_data['admin_credentials']['password'])}. Change this in code before deployment."
                "</div>"
            ),
            unsafe_allow_html=True,
        )

        card_col1, card_col2, card_col3 = st.columns([1, 1, 1.7], gap="medium")
        with card_col1:
            st.markdown(
                (
                    "<div class='admin-card'>"
                    "<p class='admin-card-title'>Farmers</p>"
                    f"<p class='admin-card-value'>{escape(str(admin_data['total_farmers']))}</p>"
                    "<p class='admin-card-copy'>Registered farmer accounts</p>"
                    "<p class='admin-card-kicker'>Risk Level</p>"
                    "<div class='admin-card-inline'>"
                    f"<span class='{get_admin_risk_chip_class('MODERATE RISK')}'>{escape(str(admin_data['moderate_risk_count']))} Moderate</span>"
                    f"<span class='{get_admin_risk_chip_class('LOW RISK')}'>{escape(str(admin_data['unread_alerts']))} Alerts</span>"
                    "</div>"
                    "</div>"
                ),
                unsafe_allow_html=True,
            )

        with card_col2:
            st.markdown(
                (
                    "<div class='admin-card'>"
                    "<p class='admin-card-title'>Recent Cases</p>"
                    f"<p class='admin-card-value'>{escape(str(admin_data['recent_case_count']))}</p>"
                    "<p class='admin-card-copy'>Saved assessments on this device</p>"
                    "<p class='admin-card-kicker'>Risk Level</p>"
                    "<div class='admin-card-inline'>"
                    f"<span class='{get_admin_risk_chip_class('HIGH RISK')}'>{escape(str(admin_data['high_risk_count']))} High</span>"
                    f"<span class='{get_admin_risk_chip_class('LOW RISK')}'>{escape(str(admin_data['low_risk_count']))} Low</span>"
                    "</div>"
                    "</div>"
                ),
                unsafe_allow_html=True,
            )

        with card_col3:
            with st.container(border=True):
                st.markdown(
                    (
                        "<div class='admin-card'>"
                        "<p class='admin-card-title'>Database Backup</p>"
                        "<p class='admin-upload-copy'>Download a full backup of the local Pigilan database on this device.</p>"
                        "</div>"
                    ),
                    unsafe_allow_html=True,
                )

                st.download_button(
                    "Download Backup",
                    data=backup["bytes"],
                    file_name=backup["file_name"],
                    mime="application/octet-stream",
                    key="download_backup_db_admin",
                    use_container_width=True,
                )

                st.markdown(
                    (
                        "<div class='admin-sync-footnote'>"
                        f"<span class='{alert_chip_class}'>{escape(alert_label)}</span>"
                        f"<p class='admin-upload-copy' style='margin-bottom: 0;'>{escape(alert_message)}</p>"
                        "</div>"
                    ),
                    unsafe_allow_html=True,
                )

        header_col, filter_col = st.columns([4, 1.15], gap="medium")
        with header_col:
            st.markdown("<div class='admin-section-header'><h2 class='admin-section-title'>All Cases</h2></div>", unsafe_allow_html=True)
        with filter_col:
            risk_filter = st.selectbox(
                "Filter Cases",
                ["All", "High Risk", "Moderate Risk", "Low Risk"],
                key="admin_case_filter",
                label_visibility="collapsed",
            )

        if risk_filter != "All":
            filtered_cases = [
                case for case in admin_data["recent_cases"]
                if str(case.get("risk_level") or "").strip().upper() == risk_filter.upper()
            ]

        if filtered_cases:
            st.markdown(
                (
                    "<table class='admin-table'>"
                    "<thead><tr>"
                    "<th>Case #</th>"
                    "<th>Risk Level</th>"
                    "<th>Farmer</th>"
                    "<th>Status</th>"
                    "</tr></thead>"
                    f"<tbody>{build_admin_case_table_rows(filtered_cases)}</tbody>"
                    "</table>"
                ),
                unsafe_allow_html=True,
            )
        else:
            st.markdown(
                "<div class='admin-empty-state'>No cases match the selected filter yet.</div>",
                unsafe_allow_html=True,
            )

        meta_col1, meta_col2 = st.columns(2, gap="medium")
        with meta_col1:
            if admin_data["recent_alerts"]:
                alert_items = []
                for alert in admin_data["recent_alerts"][:3]:
                    alert_items.append(
                        f"<p><span class='{get_admin_risk_chip_class(alert.get('alert_level'))}'>{escape(format_admin_risk_label(alert.get('alert_level')))}</span> {escape(str(alert.get('alert_message') or ''))}</p>"
                    )
                st.markdown(
                    f"<div class='admin-meta-card'><h3>Recent Alerts</h3>{''.join(alert_items)}</div>",
                    unsafe_allow_html=True,
                )
            else:
                st.markdown(
                    "<div class='admin-meta-card'><h3>Recent Alerts</h3><p>No alerts yet.</p></div>",
                    unsafe_allow_html=True,
                )

        with meta_col2:
            if admin_data["users"]:
                farmer_lines = []
                for farmer in admin_data["users"][:5]:
                    full_name = (
                        f"{str(farmer.get('first_name') or '').strip()} {str(farmer.get('last_name') or '').strip()}".strip()
                        or str(farmer.get("username") or "Farmer")
                    )
                    farmer_lines.append(
                        f"<p><strong>{escape(full_name)}</strong><br>{escape(format_address(farmer))}</p>"
                    )
                st.markdown(
                    f"<div class='admin-meta-card'><h3>Farmer Accounts</h3>{''.join(farmer_lines)}</div>",
                    unsafe_allow_html=True,
                )
            else:
                st.markdown(
                    "<div class='admin-meta-card'><h3>Farmer Accounts</h3><p>No farmer accounts yet.</p></div>",
                    unsafe_allow_html=True,
                )

        if render_logout_confirmation("Logout", "admin_logout_confirm", "admin"):
            st.session_state.user = None
            st.session_state.auth_mode = "signin"
            st.rerun()

        render_admin_footer()
        st.stop()

    inject_profile_styles()

    biosecurity_state = get_latest_biosecurity_state(user["id"])
    sync_summary = get_sync_status_summary(user_id=user["id"])
    latest_check = biosecurity_state.get("latest_check") or {}
    latest_checklist = latest_check.get("checklist") or {}
    profile_feedback_message = None
    profile_feedback_kind = "success"

    for index, item in enumerate(ACCOUNT_BIOSECURITY_ITEMS):
        checkbox_key = f"account_bio_{user['id']}_{index}"
        if checkbox_key not in st.session_state:
            st.session_state[checkbox_key] = bool(latest_checklist.get(item, False))

    st.markdown("<div class='profile-shell'><h1 class='profile-title'>Account</h1></div>", unsafe_allow_html=True)

    with st.container(border=True):
        full_name = f"{user.get('first_name', '').strip()} {user.get('last_name', '').strip()}".strip()
        if not full_name:
            full_name = user.get("username", "Farmer")
        st.markdown(
            f"""
            <div class="profile-card">
                <div class="profile-avatar">{escape(get_profile_initials(user))}</div>
                <div>
                    <p class="profile-card-name">Welcome, {escape(full_name)}</p>
                    <p class="profile-card-subtitle">Signed in as {escape(user.get('username', 'farmer'))}</p>
                    <div class="profile-meta">
                        <p><strong>Username:</strong> {escape(user.get('username', 'Not set yet'))}</p>
                        <p><strong>Address:</strong> {escape(format_address(user))}</p>
                    </div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        if format_address(user) == "Not set yet":
            st.caption("Complete your farm address in Edit My Details so your account matches the full design data.")

    with st.container(border=True):
        st.markdown("<div class='profile-bar'>Overview</div>", unsafe_allow_html=True)
        protection = biosecurity_state["protection_label"]
        has_saved_checklist = bool(latest_check)
        if has_saved_checklist:
            protection_label = protection
            protection_class = get_protection_chip_class(protection)
            overview_note = biosecurity_state["warning_message"]
        else:
            protection_label = "No checklist yet"
            protection_class = "profile-protection-chip profile-protection-chip--pending"
            overview_note = "Complete your first checklist below to see your current farm protection level."
        st.markdown(
            f"""
            <div class="profile-overview-row">
                <strong>Protection level:</strong>
                <div class="{protection_class}">
                    <span>&#128737;</span>
                    <span>{escape(protection_label)}</span>
                </div>
            </div>
            <div class="profile-count-grid">
                <div class="profile-count-card">
                    <p>Checked items</p>
                    <strong>{biosecurity_state['checked_count']}</strong>
                </div>
                <div class="profile-count-card">
                    <p>Unchecked items</p>
                    <strong>{biosecurity_state['unchecked_count']}</strong>
                </div>
            </div>
            <p class="profile-muted-line">{escape(overview_note)}</p>
            <p class="profile-muted-line">Local sync status: {escape(sync_summary['status_label'])}</p>
            """,
            unsafe_allow_html=True,
        )

    with st.container(border=True):
        header_col, sync_col = st.columns([4, 1.15], gap="medium")
        with header_col:
            st.markdown("<div class='profile-bar'>Biosecurity Checklist</div>", unsafe_allow_html=True)
        with sync_col:
            st.write("")
            if st.button("Sync", key="account_sync_button_header", use_container_width=True):
                try:
                    sync_result = sync_with_server(user_id=user["id"])
                except ValueError as exc:
                    profile_feedback_message = str(exc)
                    profile_feedback_kind = "warning"
                else:
                    sync_summary = get_sync_status_summary(user_id=user["id"])
                    profile_feedback_message = (
                        f"Sync completed for {sync_result.get('username', user['username'])}."
                    )

        st.markdown(
            "<p class='profile-checklist-note'>Review the checklist below and save your latest farm biosecurity status before syncing.</p>",
            unsafe_allow_html=True,
        )

        with st.form("biosecurity_account_form", clear_on_submit=False):
            checks = {}
            for index, item in enumerate(ACCOUNT_BIOSECURITY_ITEMS):
                checkbox_key = f"account_bio_{user['id']}_{index}"
                checks[item] = st.checkbox(item, key=checkbox_key)

            save_submitted = st.form_submit_button("Save Biosecurity Checklist", use_container_width=True)

        if save_submitted:
            result = save_biosecurity_check(
                user_id=user["id"],
                checklist=checks,
                remarks="Saved from My Account",
            )
            biosecurity_state = get_latest_biosecurity_state(user["id"])
            sync_summary = get_sync_status_summary(user_id=user["id"])
            profile_feedback_message = result["warning_message"]
            profile_feedback_kind = "success"

        if profile_feedback_message:
            if profile_feedback_kind == "warning":
                st.warning(profile_feedback_message)
            else:
                st.success(profile_feedback_message)

        backup = get_database_backup()
        action_col1, action_col2 = st.columns([1, 1], gap="medium")
        with action_col1:
            st.markdown(
                """
                <div class="profile-action-tile">
                    <div class="profile-action-icon">&#9729;</div>
                    <strong>Backup</strong>
                    <div>Download a copy of your local app data.</div>
                </div>
                """,
                unsafe_allow_html=True,
            )
            st.download_button(
                "Backup",
                data=backup["bytes"],
                file_name=backup["file_name"],
                mime="application/octet-stream",
                key="download_backup_db",
                use_container_width=True,
            )

        with action_col2:
            st.markdown(
                """
                <div class="profile-action-tile">
                    <div class="profile-action-icon">&#9998;</div>
                    <strong>Edit My Details</strong>
                    <div>Update the farm information saved from your sign up and account profile.</div>
                </div>
                """,
                unsafe_allow_html=True,
            )
            if st.button("EDIT MY DETAILS", key="toggle_edit_profile", use_container_width=True):
                st.session_state.show_edit_profile = not st.session_state.show_edit_profile
                st.rerun()

    if st.session_state.show_edit_profile:
        with st.container(border=True):
            st.markdown("<div class='profile-bar'>Edit My Details</div>", unsafe_allow_html=True)
            st.markdown(
                """
                <p class="profile-edit-panel-title">Update your farmer profile</p>
                <p class="profile-edit-panel-copy">Use this form to complete the account details that are shown on the My Account page.</p>
                """,
                unsafe_allow_html=True,
            )
            edit_first_name = st.text_input("First Name", value=user["first_name"])
            edit_last_name = st.text_input("Last Name", value=user["last_name"])
            edit_address = st.text_input("Address", value=user.get("address") or "")
            st.caption("Address is shown in your account profile.")
            edit_barangay = st.text_input("Barangay (optional)", value=user["barangay"])
            edit_municipality = st.text_input("Municipality (optional)", value=user["municipality"])
            edit_province = st.text_input("Province (optional)", value=user["province"])

            if st.button("Save My Changes", key="save_profile_changes", use_container_width=True):
                updated_user = edit_user_profile(
                    user_id=user["id"],
                    first_name=edit_first_name.strip(),
                    last_name=edit_last_name.strip(),
                    barangay=edit_barangay.strip(),
                    municipality=edit_municipality.strip(),
                    province=edit_province.strip(),
                    address=edit_address.strip(),
                    latitude=user.get("latitude"),
                    longitude=user.get("longitude"),
                )
                st.session_state.user = updated_user
                st.session_state.show_edit_profile = False
                st.success("Your details were updated successfully.")
                st.rerun()

else:
    inject_auth_styles()
    auth_mode = get_auth_mode()

    if auth_mode == "signup":
        st.markdown(
            """
            <div class="auth-hero">
                <h1>Sign Up</h1>
                <p>Create a new account to start monitoring your pigs.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

        with st.container(border=True):
            st.markdown(
                """
                <div class="auth-brand-row">
                    <div class="auth-shield"></div>
                    <div>
                        <p class="auth-brand-title">Sign Up</p>
                        <p class="auth-brand-subtitle">Local-first ASF monitoring for farmers</p>
                    </div>
                </div>
                <p class="auth-section-title">Create an account</p>
                <p class="auth-section-copy">Add your farm details below so Pigilan can save reports under your profile.</p>
                """,
                unsafe_allow_html=True,
            )

            with st.form("signup_form"):
                full_name = render_auth_input("&#128100;", "Full Name", "Full Name *", "signup_full_name")
                username = render_auth_input("&#128100;", "Username", "Username *", "signup_username")
                email_address = render_auth_input("&#9993;", "Email Address", "Email Address *", "signup_email")
                address = render_auth_input("&#127968;", "Address", "Farm Address *", "signup_address")
                password = render_auth_input("&#128274;", "Password", "Password *", "signup_password", field_type="password")
                confirm_password = render_auth_input(
                    "&#128274;",
                    "Confirm Password",
                    "Confirm Password *",
                    "signup_confirm_password",
                    field_type="password",
                )
                st.caption("This address will appear in My Account. You can add the farm map point later.")
                submitted = st.form_submit_button("Sign Up", use_container_width=True)

            st.markdown(
                "<p class='auth-switch-copy'>Already have an account?</p>",
                unsafe_allow_html=True,
            )
            switch_cols = st.columns([1.2, 1, 1.2])
            with switch_cols[1]:
                if st.button("Sign In", key="auth_switch_to_signin", type="tertiary", use_container_width=True):
                    set_auth_mode("signin")
                    st.rerun()

            if submitted:
                first_name, last_name = split_full_name(full_name)
                if not all(
                    [
                        str(full_name).strip(),
                        str(username).strip(),
                        str(email_address).strip(),
                        str(address).strip(),
                        str(password).strip(),
                        str(confirm_password).strip(),
                    ]
                ):
                    st.error("Please complete all fields.")
                elif first_name is None or last_name is None:
                    st.error("Please enter your full name using at least a first name and last name.")
                elif "@" not in email_address or "." not in email_address:
                    st.error("Please enter a valid email address.")
                elif password != confirm_password:
                    st.error("Password and Confirm Password do not match.")
                elif len(password) < 6:
                    st.error("Please use a password with at least 6 characters.")
                else:
                    try:
                        register_user(
                            username=username.strip(),
                            password=password,
                            first_name=first_name.strip(),
                            last_name=last_name.strip(),
                            barangay="Not set yet",
                            municipality="Not set yet",
                            province="Not set yet",
                            address=address.strip(),
                        )
                        st.session_state.auth_notice = "Account created successfully. You can now sign in."
                        set_auth_mode("signin")
                        st.rerun()
                    except Exception:
                        st.error("Username already exists or the account could not be created.")
    else:
        st.markdown(
            """
            <div class="auth-hero">
                <h1>Sign In or Sign Up</h1>
                <p>Please sign in first before running an ASF assessment.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

        with st.container(border=True):
            st.markdown(
                """
                <div class="auth-brand-row">
                    <div class="auth-shield"></div>
                    <div>
                        <p class="auth-brand-title">Pigilan</p>
                        <p class="auth-brand-subtitle">Local-first ASF monitoring for farmers</p>
                    </div>
                </div>
                <p class="auth-section-title">Sign in to continue</p>
                <p class="auth-section-copy">Use your account to open saved reports, update farm details, and run a pig check.</p>
                """,
                unsafe_allow_html=True,
            )

            if st.session_state.auth_notice:
                st.success(st.session_state.auth_notice)
                st.session_state.auth_notice = ""

            with st.form("signin_form"):
                username = render_auth_input("&#128100;", "Username", "Username", "signin_username")
                password = render_auth_input("&#128274;", "Password", "Password", "signin_password", field_type="password")
                submitted = st.form_submit_button("Sign In", use_container_width=True)

            st.markdown(
                "<p class='auth-switch-copy'>Don't have an account?</p>",
                unsafe_allow_html=True,
            )
            switch_cols = st.columns([1.2, 1, 1.2])
            with switch_cols[1]:
                if st.button("Sign Up", key="auth_switch_to_signup", type="tertiary", use_container_width=True):
                    set_auth_mode("signup")
                    st.rerun()

            if submitted:
                user = login_user(username.strip(), password)
                if user:
                    st.session_state.user = user
                    st.success("Sign in successful.")
                    st.rerun()
                else:
                    st.error("Invalid username or password.")

