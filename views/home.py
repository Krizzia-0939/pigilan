from html import escape

import streamlit as st
from asset_utils import build_local_image_data_uri, resolve_asset_path

HERO_BACKGROUND_PHOTO = resolve_asset_path("BG-PHOTO.png")
RISK_ASSESSMENT_PHOTO = resolve_asset_path("risk-assessment-photo.png")
IMAGE_BASED_DETECTION_PHOTO = resolve_asset_path("Image-Based_Detection.png")
BIOSECURITY_GUIDANCE_PHOTO = resolve_asset_path("Biosecurity-photo.png")
NEARBY_CASE_ALERTS_PHOTO = resolve_asset_path("Nearby-Case-Alerts.png")


FEATURE_CARDS = [
    {
        "accent": "risk",
        "title": "ASF Risk Assessment",
        "copy": "Evaluate symptoms and receive a risk level.",
        "image_data_uri": build_local_image_data_uri(RISK_ASSESSMENT_PHOTO),
        "image_alt": "ASF risk assessment guide",
    },
    {
        "accent": "image",
        "title": "Image-Based Detection",
        "copy": "Upload pig photos for ASF detection.",
        "image_data_uri": build_local_image_data_uri(IMAGE_BASED_DETECTION_PHOTO),
        "image_alt": "Image-based ASF detection",
    },
    {
        "accent": "guide",
        "title": "Biosecurity Guidance",
        "copy": "Follow recommended practices for isolation, sanitation, and disease prevention.",
        "image_data_uri": build_local_image_data_uri(BIOSECURITY_GUIDANCE_PHOTO),
        "image_alt": "Biosecurity guidance",
    },
    {
        "accent": "alert",
        "title": "Nearby Case Alerts",
        "copy": "Get notified about possible ASF cases nearby.",
        "image_data_uri": build_local_image_data_uri(NEARBY_CASE_ALERTS_PHOTO),
        "image_alt": "Nearby case alerts",
    },
]

HOME_HERO_BACKGROUND_DATA_URI = build_local_image_data_uri(HERO_BACKGROUND_PHOTO)

FLOW_STEPS = [
    {
        "step": "1",
        "title": "Create an account",
        "copy": "Set up access to save and manage reports.",
    },
    {
        "step": "2",
        "title": "Check the pig",
        "copy": "Follow guided questions and record symptoms.",
    },
    {
        "step": "3",
        "title": "Save offline",
        "copy": "Keep reports on your device while offline.",
    },
    {
        "step": "4",
        "title": "Sync later",
        "copy": "Upload your records once internet is available.",
    },
]


def inject_home_styles():
    st.markdown(
        """
        <style>
        .home-shell {
            max-width: 1080px;
            margin: 0 auto;
        }

        .home-hero-card {
            position: relative;
            overflow: hidden;
            min-height: 420px;
            padding: clamp(1.45rem, 3.8vw, 2.2rem);
            border-radius: 28px;
            border: 1px solid rgba(216, 200, 182, 0.72);
            background:
                linear-gradient(135deg, rgba(255, 251, 247, 0.98) 0%, rgba(247, 240, 233, 0.96) 46%, rgba(237, 226, 214, 0.92) 100%);
            box-shadow:
                0 24px 42px rgba(83, 69, 56, 0.08),
                inset 0 1px 0 rgba(255, 255, 255, 0.35);
        }

        .home-hero-card::before {
            content: "";
            position: absolute;
            inset: 0;
            background:
                radial-gradient(circle at 12% 16%, rgba(255, 255, 255, 0.62), transparent 28%),
                linear-gradient(180deg, rgba(255, 255, 255, 0.16), rgba(255, 255, 255, 0) 34%);
            pointer-events: none;
        }

        .home-hero-card::after {
            content: "";
            position: absolute;
            inset: 0;
            background: linear-gradient(90deg, rgba(250, 244, 238, 0.28) 0%, rgba(250, 244, 238, 0.08) 32%, rgba(112, 84, 69, 0.10) 100%);
            pointer-events: none;
        }

        .home-hero {
            position: relative;
            z-index: 1;
            display: grid;
            grid-template-columns: minmax(0, 0.96fr) minmax(360px, 1.04fr);
            gap: clamp(1.2rem, 3vw, 2.6rem);
            align-items: stretch;
            min-height: 340px;
        }

        .home-hero-copy {
            position: relative;
            z-index: 1;
            max-width: 34rem;
            display: flex;
            flex-direction: column;
            justify-content: center;
            padding: 0.5rem 0;
        }

        .home-hero-kicker {
            display: inline-flex;
            align-items: center;
            gap: 0.5rem;
            padding: 0.42rem 0.82rem;
            border-radius: 999px;
            border: 1px solid rgba(186, 170, 153, 0.66);
            background: rgba(255, 251, 247, 0.84);
            color: #6e6458;
            font-size: 0.76rem;
            font-weight: 800;
            letter-spacing: 0.08em;
            text-transform: uppercase;
            box-shadow: 0 10px 18px rgba(83, 69, 56, 0.06);
        }

        .home-hero-kicker::before {
            content: "";
            width: 0.55rem;
            height: 0.55rem;
            border-radius: 50%;
            background: linear-gradient(135deg, #76805e, #5d654a);
            box-shadow: 0 0 0 0.22rem rgba(118, 128, 94, 0.16);
        }

        .home-hero-title {
            margin: 1.1rem 0 0;
            color: #493d35;
            font-size: clamp(2.35rem, 5vw, 4rem);
            line-height: 0.98;
            letter-spacing: -0.06em;
            text-wrap: balance;
        }

        .home-hero-title span {
            display: block;
        }

        .home-hero-highlight {
            max-width: 26rem;
            margin: 1rem 0 0;
            color: #5b6248;
            font-size: clamp(1.18rem, 2.25vw, 1.7rem);
            line-height: 1.12;
            font-weight: 900;
            letter-spacing: -0.035em;
        }

        .home-hero-copy-text {
            max-width: 31rem;
            margin: 1rem 0 0;
            color: #5d5148;
            font-size: 1.04rem;
            line-height: 1.66;
        }

        .home-hero-note {
            margin: 1rem 0 0;
            color: #665a50;
            font-size: 0.95rem;
            line-height: 1.55;
            font-weight: 600;
        }

        .home-hero-visual {
            position: relative;
            min-height: 340px;
            height: 100%;
            display: flex;
            align-items: stretch;
            justify-content: flex-end;
            align-self: stretch;
            overflow: hidden;
        }

        .home-hero-visual::before {
            content: none;
        }

        .home-hero-photo-wrap {
            position: relative;
            width: calc(100% + 2.4rem);
            min-height: 100%;
            height: 100%;
            margin: -0.35rem -2.2rem -0.35rem auto;
            border-radius: 0;
            overflow: hidden;
            border: none;
            box-shadow: none;
            background: transparent;
        }

        .home-hero-photo-wrap::before {
            content: "";
            position: absolute;
            inset: 0;
            z-index: 1;
            background:
                linear-gradient(90deg, rgba(247, 240, 233, 1) 0%, rgba(247, 240, 233, 0.98) 20%, rgba(247, 240, 233, 0.78) 38%, rgba(247, 240, 233, 0.28) 64%, rgba(247, 240, 233, 0) 84%),
                linear-gradient(180deg, rgba(247, 240, 233, 0.82) 0%, rgba(247, 240, 233, 0.12) 14%, rgba(247, 240, 233, 0.05) 82%, rgba(247, 240, 233, 0.62) 100%);
            pointer-events: none;
        }

        .home-hero-photo-wrap::after {
            content: none;
        }

        .home-hero-photo {
            position: absolute;
            inset: 0;
            width: 100%;
            height: 100%;
            object-fit: cover;
            object-position: 80% center;
            transform: scale(1.06);
            filter: saturate(0.94) contrast(1.04);
        }

        .home-section-intro {
            max-width: 760px;
            margin: 2.4rem auto 1rem;
            text-align: center;
        }

        .home-section-intro h2 {
            margin: 0;
            color: #4b4137;
            font-size: clamp(1.7rem, 3vw, 2.3rem);
            line-height: 1.15;
            letter-spacing: -0.03em;
        }

        .home-section-intro p {
            margin: 0.55rem 0 0;
            color: #74695d;
            font-size: 1rem;
            line-height: 1.6;
        }

        .home-feature-grid {
            display: grid;
            grid-template-columns: repeat(4, minmax(0, 1fr));
            gap: 1rem;
            margin-top: 1.3rem;
        }

        .home-feature-card {
            position: relative;
            overflow: hidden;
            min-height: 220px;
            padding: 1.15rem;
            border-radius: 22px;
            background: rgba(255, 251, 246, 0.92);
            border: 1px solid rgba(216, 200, 182, 0.95);
            box-shadow: 0 18px 28px rgba(83, 69, 56, 0.09);
        }

        .home-feature-image-wrap {
            margin: -1.15rem -1.15rem 1rem;
            aspect-ratio: 16 / 10;
            overflow: hidden;
            background: linear-gradient(180deg, rgba(255, 244, 236, 0.92), rgba(244, 233, 221, 0.78));
            border-bottom: 1px solid rgba(216, 200, 182, 0.95);
        }

        .home-feature-image {
            display: block;
            width: 100%;
            height: 100%;
            object-fit: cover;
        }

        .home-feature-card::before {
            content: "";
            position: absolute;
            right: -1rem;
            top: -1rem;
            width: 7.5rem;
            height: 7.5rem;
            border-radius: 50%;
            opacity: 0.65;
        }

        .home-feature-card--risk::before {
            background: radial-gradient(circle, rgba(235, 116, 85, 0.30), transparent 68%);
        }

        .home-feature-card--image::before {
            background: radial-gradient(circle, rgba(85, 139, 137, 0.28), transparent 68%);
        }

        .home-feature-card--guide::before {
            background: radial-gradient(circle, rgba(111, 146, 111, 0.25), transparent 68%);
        }

        .home-feature-card--alert::before {
            background: radial-gradient(circle, rgba(225, 144, 92, 0.30), transparent 68%);
        }

        .home-feature-card h3 {
            margin: 0;
            color: #4b4137;
            font-size: 1.12rem;
            line-height: 1.25;
        }

        .home-feature-card p {
            margin: 0.65rem 0 0;
            color: #786d61;
            font-size: 0.95rem;
            line-height: 1.62;
        }

        .home-sync-note {
            margin: 1.7rem 0 1rem;
            text-align: center;
            color: #655b50;
            font-size: 1rem;
            line-height: 1.6;
            font-weight: 600;
        }

        .home-flow-card {
            padding: clamp(1.2rem, 3vw, 1.7rem);
            border-radius: 24px;
            background: rgba(255, 251, 246, 0.88);
        }

        .home-flow-grid {
            display: grid;
            grid-template-columns: repeat(4, minmax(0, 1fr));
            gap: 0.95rem;
            margin-top: 1.3rem;
        }

        .home-flow-step {
            min-height: 152px;
            padding: 1rem;
            border-radius: 18px;
            background: linear-gradient(180deg, rgba(255, 255, 255, 0.96), rgba(248, 241, 232, 0.92));
            border: 1px solid rgba(216, 200, 182, 0.92);
        }

        .home-flow-number {
            display: inline-flex;
            align-items: center;
            justify-content: center;
            width: 2rem;
            height: 2rem;
            border-radius: 50%;
            background: linear-gradient(180deg, #6d7359, #596047);
            color: #fff;
            font-size: 0.92rem;
            font-weight: 700;
        }

        .home-flow-step h3 {
            margin: 0.85rem 0 0;
            color: #4b4137;
            font-size: 1rem;
            line-height: 1.3;
        }

        .home-flow-step p {
            margin: 0.55rem 0 0;
            color: #7a7064;
            font-size: 0.92rem;
            line-height: 1.56;
        }

        .home-nearby-card {
            padding: clamp(1.2rem, 3vw, 1.6rem);
            border-radius: 24px;
            background: rgba(255, 251, 246, 0.88);
        }

        .home-nearby-summary-grid {
            display: grid;
            grid-template-columns: repeat(4, minmax(0, 1fr));
            gap: 0.9rem;
            margin: 1.1rem 0 1rem;
        }

        .home-summary-card {
            padding: 0.95rem 1rem;
            border-radius: 16px;
            background: rgba(255, 252, 248, 0.96);
            border: 1px solid rgba(216, 200, 182, 0.95);
        }

        .home-summary-label {
            margin: 0;
            color: #7b7064;
            font-size: 0.88rem;
            line-height: 1.35;
        }

        .home-summary-value {
            margin: 0.3rem 0 0;
            color: #4b4137;
            font-size: 1.65rem;
            line-height: 1.05;
            font-weight: 800;
        }

        .home-summary-value--muted {
            font-size: 1.15rem;
            line-height: 1.3;
        }

        .home-nearby-caption {
            margin: 0.7rem 0 0;
            color: #7a7064;
            font-size: 0.9rem;
            line-height: 1.5;
        }

        .home-nearby-list-title {
            margin: 0 0 0.8rem;
            color: #4b4137;
            font-size: 1.1rem;
            line-height: 1.25;
            font-weight: 700;
        }

        .home-case-list {
            display: grid;
            gap: 0.8rem;
        }

        .home-case-item {
            padding: 0.95rem 1rem;
            border-radius: 16px;
            background: rgba(255, 252, 248, 0.92);
            border: 1px solid rgba(216, 200, 182, 0.92);
        }

        .home-case-top {
            display: flex;
            align-items: center;
            justify-content: space-between;
            gap: 0.75rem;
            flex-wrap: wrap;
        }

        .home-case-top strong {
            color: #4b4137;
            font-size: 0.98rem;
            line-height: 1.3;
        }

        .home-case-item p {
            margin: 0.55rem 0 0;
            color: #74695d;
            font-size: 0.92rem;
            line-height: 1.55;
        }

        .home-case-meta {
            display: flex;
            gap: 0.8rem;
            flex-wrap: wrap;
            margin-top: 0.6rem;
            color: #877b6f;
            font-size: 0.84rem;
            line-height: 1.45;
        }

        .home-risk-badge {
            display: inline-flex;
            align-items: center;
            justify-content: center;
            padding: 0.32rem 0.62rem;
            border-radius: 999px;
            font-size: 0.78rem;
            line-height: 1.2;
            font-weight: 700;
            letter-spacing: 0.02em;
        }

        .home-risk-badge--high {
            background: rgba(248, 220, 220, 0.92);
            color: #9b4136;
        }

        .home-risk-badge--moderate {
            background: rgba(251, 237, 208, 0.94);
            color: #98722d;
        }

        .home-risk-badge--low {
            background: rgba(227, 241, 227, 0.94);
            color: #4c7650;
        }

        .home-empty-state {
            padding: 1rem 1.05rem;
            border-radius: 16px;
            background: rgba(255, 252, 248, 0.92);
            border: 1px solid rgba(216, 200, 182, 0.92);
            color: #74695d;
            font-size: 0.95rem;
            line-height: 1.6;
        }

        .home-footer {
            display: flex;
            align-items: center;
            justify-content: space-between;
            gap: 1rem;
            flex-wrap: wrap;
            margin: 2.2rem 0 0.45rem;
            color: #83776a;
            font-size: 0.92rem;
        }

        .home-footer-links {
            display: flex;
            gap: 0.95rem;
            flex-wrap: wrap;
        }

        @media (max-width: 980px) {
            .home-feature-grid,
            .home-flow-grid,
            .home-nearby-summary-grid {
                grid-template-columns: repeat(2, minmax(0, 1fr));
            }
        }

        @media (max-width: 900px) {
            .home-hero {
                grid-template-columns: 1fr;
            }

            .home-hero-copy {
                max-width: none;
            }

            .home-hero-visual {
                min-height: 260px;
                height: auto;
            }

            .home-hero-visual::before,
            .home-hero-photo-wrap {
                width: 100%;
            }

            .home-hero-photo-wrap {
                min-height: 260px;
                height: auto;
                margin: 0;
            }
        }

        @media (max-width: 640px) {
            .home-feature-grid,
            .home-flow-grid,
            .home-nearby-summary-grid {
                grid-template-columns: 1fr;
            }

            .home-hero-card {
                padding: 1.2rem;
            }

            .home-hero-title {
                font-size: clamp(2rem, 11vw, 2.7rem);
            }

            .home-hero-highlight {
                max-width: 18rem;
            }

            .home-hero-kicker {
                font-size: 0.72rem;
                letter-spacing: 0.06em;
            }

            .home-hero-visual {
                min-height: 220px;
            }

            .home-hero-photo-wrap {
                min-height: 220px;
            }

            .home-footer {
                flex-direction: column;
                align-items: flex-start;
            }
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def render_feature_cards():
    cards_markup = []
    for card in FEATURE_CARDS:
        image_markup = ""
        if card.get("image_data_uri"):
            image_alt = escape(card.get("image_alt", card["title"]))
            image_markup = (
                "<div class=\"home-feature-image-wrap\">"
                f"<img class=\"home-feature-image\" src=\"{card['image_data_uri']}\" alt=\"{image_alt}\">"
                "</div>"
            )

        cards_markup.append(
            (
                f"<article class=\"home-feature-card home-feature-card--{card['accent']}\">"
                f"{image_markup}"
                f"<h3>{escape(card['title'])}</h3>"
                f"<p>{escape(card['copy'])}</p>"
                "</article>"
            )
        )

    st.markdown(
        "<div class='home-feature-grid'>" + "".join(cards_markup) + "</div>",
        unsafe_allow_html=True,
    )


def render_flow_steps():
    steps_markup = []
    for item in FLOW_STEPS:
        steps_markup.append(
            (
                "<article class=\"home-flow-step\">"
                f"<div class=\"home-flow-number\">{escape(item['step'])}</div>"
                f"<h3>{escape(item['title'])}</h3>"
                f"<p>{escape(item['copy'])}</p>"
                "</article>"
            )
        )

    st.markdown(
        "<div class='home-flow-grid'>" + "".join(steps_markup) + "</div>",
        unsafe_allow_html=True,
    )


def render_footer():
    st.markdown(
        """
        <div class="home-footer">
            <div class="home-footer-links">
                <span>About</span>
                <span>Privacy</span>
                <span>Support</span>
            </div>
            <div>Version 1.0</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


inject_home_styles()
user = st.session_state.get("user")
is_logged_in = bool(user)
hero_visual_markup = (
    "<div class=\"home-hero-visual\">"
    "<div class=\"home-hero-photo-wrap\">"
    f"<img class=\"home-hero-photo\" src=\"{HOME_HERO_BACKGROUND_DATA_URI}\" alt=\"\" aria-hidden=\"true\">"
    "</div>"
    "</div>"
    if HOME_HERO_BACKGROUND_DATA_URI
    else ""
)

with st.container(border=True):
    st.markdown(
        f"""
        <section class="home-hero-card">
            <div class="home-hero">
                <div class="home-hero-copy">
                    <div class="home-hero-kicker">Offline-Ready ASF Monitoring</div>
                    <h1 class="home-hero-title">
                        <span>Early Detection of</span>
                        <span>African Swine Fever</span>
                        <span>Starts Here.</span>
                    </h1>
                    <p class="home-hero-highlight">Detect Early. Act Fast. Protect Your Herd.</p>
                    <p class="home-hero-copy-text">
                        Identify ASF symptoms, receive risk assessments, and access guidance to protect your pigs and
                        prevent disease spread, even without internet access.
                    </p>
                    <p class="home-hero-note">Built for offline-ready farm monitoring so your reports stay useful even with limited internet.</p>
                </div>
                {hero_visual_markup}
            </div>
        </section>
        """,
        unsafe_allow_html=True,
    )

    primary_col, secondary_col = st.columns(2, gap="small")
    with primary_col:
        if st.button("Start Health Assessment", key="home_cta_primary", use_container_width=True):
            st.session_state.page = "Health Assessment"
            st.rerun()
    with secondary_col:
        secondary_label = "Open My Reports" if is_logged_in else "Create Account"
        if st.button(secondary_label, key="home_cta_secondary", use_container_width=True):
            if is_logged_in:
                st.session_state.page = "My Reports"
            else:
                st.session_state.page = "My Account"
                st.session_state.auth_mode = "signup"
            st.rerun()

st.markdown(
    """
    <div class="home-section-intro">
        <h2>Protect Your Farm with Smart Tools</h2>
        <p>Key features to help monitor, assess, and manage pig health.</p>
    </div>
    """,
    unsafe_allow_html=True,
)
render_feature_cards()

st.markdown(
    "<p class='home-sync-note'>Works offline. Sync your reports when internet is available.</p>",
    unsafe_allow_html=True,
)

with st.container(border=True):
    st.markdown(
        """
        <div class="home-flow-card">
            <div class="home-section-intro" style="margin-top: 0; margin-bottom: 0.5rem;">
                <h2>How PIGilan Works</h2>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    render_flow_steps()

render_footer()
