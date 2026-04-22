from html import escape

import streamlit as st


ABOUT_HIGHLIGHTS = [
    {
        "label": "Case Screening",
        "title": "Capture warning signs in one report.",
        "copy": "Pigilan combines a symptom checklist and photo screening so suspected cases are documented in a consistent way.",
    },
    {
        "label": "Offline Saving",
        "title": "Keep working even with weak signal.",
        "copy": "Assessments are saved on the device first, which makes the app more practical during farm visits.",
    },
    {
        "label": "Follow-up",
        "title": "Keep the next step easy to find.",
        "copy": "Each report keeps the risk level, notes, and recommended action together for later review or export.",
    },
]

ABOUT_FLOW = [
    {
        "step": "1",
        "title": "Sign in or create an account",
        "copy": "Create a farm profile so your assessments stay tied to your account.",
    },
    {
        "step": "2",
        "title": "Check the pig",
        "copy": "Record symptoms, upload a photo, and confirm the farm location before saving.",
    },
    {
        "step": "3",
        "title": "Save the assessment",
        "copy": "Store the report on the device right away, even when internet is unavailable.",
    },
    {
        "step": "4",
        "title": "Review and sync later",
        "copy": "Open My Reports for follow-up, exports, and syncing once the connection is stable.",
    },
]


def inject_about_styles():
    st.markdown(
        """
        <style>
        .about-shell {
            max-width: 1080px;
            margin: 0 auto;
        }

        .about-hero-card {
            position: relative;
            overflow: hidden;
            padding: clamp(1.4rem, 4vw, 2.4rem);
            border-radius: 28px;
            background:
                linear-gradient(135deg, rgba(255, 251, 246, 0.96), rgba(245, 236, 226, 0.9)),
                radial-gradient(circle at 84% 20%, rgba(140, 151, 120, 0.16), transparent 22%),
                radial-gradient(circle at 70% 72%, rgba(222, 188, 159, 0.18), transparent 24%);
        }

        .about-hero-card::before {
            content: "";
            position: absolute;
            inset: 0;
            background:
                linear-gradient(115deg, rgba(255, 255, 255, 0.3), rgba(255, 255, 255, 0) 42%),
                radial-gradient(circle at 80% 78%, rgba(209, 179, 151, 0.16), transparent 22%);
            pointer-events: none;
        }

        .about-hero {
            position: relative;
            display: grid;
            grid-template-columns: minmax(0, 1.08fr) minmax(260px, 0.92fr);
            gap: clamp(1.2rem, 3vw, 2.5rem);
            align-items: center;
        }

        .about-kicker {
            display: inline-flex;
            align-items: center;
            gap: 0.45rem;
            padding: 0.38rem 0.72rem;
            border-radius: 999px;
            background: rgba(109, 115, 89, 0.12);
            color: #596047;
            font-size: 0.82rem;
            font-weight: 700;
            letter-spacing: 0.02em;
        }

        .about-title {
            margin: 0.95rem 0 0;
            color: #4b4137;
            font-size: clamp(2.15rem, 5vw, 3.4rem);
            line-height: 1.03;
            letter-spacing: -0.04em;
        }

        .about-subtitle {
            max-width: 34rem;
            margin: 0.95rem 0 0;
            color: #6f6458;
            font-size: 1.02rem;
            line-height: 1.7;
        }

        .about-note {
            margin: 0.8rem 0 0;
            color: #7e7266;
            font-size: 0.92rem;
            line-height: 1.55;
        }

        .about-action-row {
            display: flex;
            gap: 0.75rem;
            flex-wrap: wrap;
            margin-top: 1.2rem;
        }

        .about-visual {
            position: relative;
            min-height: 320px;
            border-radius: 26px;
            background:
                linear-gradient(180deg, rgba(255, 255, 255, 0.25), rgba(242, 229, 216, 0.12)),
                radial-gradient(circle at 52% 45%, rgba(255, 236, 219, 0.62), transparent 24%),
                linear-gradient(145deg, rgba(106, 115, 87, 0.12), rgba(255, 255, 255, 0));
        }

        .about-visual::before {
            content: "";
            position: absolute;
            inset: 0;
            background:
                linear-gradient(90deg, rgba(118, 124, 102, 0.1) 1px, transparent 1px),
                linear-gradient(rgba(118, 124, 102, 0.1) 1px, transparent 1px);
            background-size: 32px 32px;
            mask-image: linear-gradient(180deg, transparent 0, rgba(0, 0, 0, 0.9) 18%, rgba(0, 0, 0, 0.7) 100%);
            opacity: 0.34;
        }

        .about-orb {
            position: absolute;
            border-radius: 50%;
        }

        .about-orb--one {
            width: 210px;
            height: 210px;
            right: 8%;
            top: 8%;
            background: radial-gradient(circle, rgba(255, 225, 207, 0.86), rgba(255, 225, 207, 0.05) 72%);
        }

        .about-orb--two {
            width: 170px;
            height: 170px;
            left: 8%;
            bottom: 6%;
            background: radial-gradient(circle, rgba(175, 186, 152, 0.34), rgba(175, 186, 152, 0.03) 75%);
        }

        .about-chip {
            position: absolute;
            display: inline-flex;
            align-items: center;
            justify-content: center;
            min-width: 6rem;
            padding: 0.46rem 0.86rem;
            border-radius: 999px;
            background: rgba(255, 252, 248, 0.94);
            border: 1px solid rgba(216, 200, 182, 0.95);
            box-shadow: 0 10px 24px rgba(89, 96, 71, 0.1);
            color: #6a604f;
            font-size: 0.82rem;
            font-weight: 700;
            letter-spacing: 0.02em;
        }

        .about-chip--top {
            top: 1.1rem;
            right: 0.8rem;
        }

        .about-chip--bottom {
            left: 0.8rem;
            bottom: 1rem;
        }

        .about-shield {
            position: absolute;
            inset: 2rem 2rem 2rem auto;
            width: min(100%, 300px);
            display: flex;
            align-items: center;
            justify-content: center;
        }

        .about-shield-outer {
            position: relative;
            width: 100%;
            max-width: 260px;
            aspect-ratio: 0.88;
            display: flex;
            align-items: center;
            justify-content: center;
            clip-path: polygon(50% 0%, 90% 14%, 84% 70%, 50% 100%, 16% 70%, 10% 14%);
            background: linear-gradient(170deg, #de7052, #bf4d33 40%, #8c3323 100%);
            box-shadow: 0 24px 34px rgba(116, 71, 44, 0.18);
        }

        .about-shield-outer::before {
            content: "";
            position: absolute;
            inset: 0.5rem;
            clip-path: polygon(50% 0%, 90% 14%, 84% 70%, 50% 100%, 16% 70%, 10% 14%);
            background: linear-gradient(180deg, rgba(255, 248, 243, 0.98), rgba(255, 241, 231, 0.96));
        }

        .about-shield-inner {
            position: relative;
            width: 74%;
            aspect-ratio: 0.88;
            display: flex;
            align-items: center;
            justify-content: center;
            clip-path: polygon(50% 0%, 90% 14%, 84% 70%, 50% 100%, 16% 70%, 10% 14%);
            background:
                radial-gradient(circle at 50% 62%, rgba(255, 230, 212, 0.95), rgba(255, 230, 212, 0.5) 32%, transparent 34%),
                linear-gradient(160deg, #3d6f6e, #244847);
            overflow: hidden;
        }

        .about-shield-inner::before {
            content: "";
            position: absolute;
            inset: 0;
            background:
                radial-gradient(circle at 62% 28%, rgba(255, 255, 255, 0.28), transparent 18%),
                radial-gradient(circle at 40% 72%, rgba(255, 255, 255, 0.12), transparent 26%);
        }

        .about-shield-inner::after {
            content: "Pigilan";
            position: absolute;
            bottom: 17%;
            left: 50%;
            transform: translateX(-50%);
            color: rgba(255, 255, 255, 0.84);
            font-size: 0.98rem;
            font-weight: 800;
            letter-spacing: 0.02em;
        }

        .about-pig {
            position: relative;
            width: 48%;
            height: 30%;
            border-radius: 50% 48% 42% 44%;
            background: linear-gradient(180deg, #ffc8b8, #f0a38f);
            box-shadow: 0 10px 18px rgba(60, 44, 40, 0.16);
        }

        .about-pig::before {
            content: "";
            position: absolute;
            width: 20%;
            height: 18%;
            left: 16%;
            bottom: -8%;
            border-radius: 999px;
            background: #d98672;
            box-shadow: 54px 0 0 #d98672;
        }

        .about-pig::after {
            content: "";
            position: absolute;
            width: 34%;
            height: 28%;
            left: -18%;
            top: 32%;
            border-radius: 50% 44% 44% 50%;
            background: linear-gradient(180deg, #ffcbbd, #f2a898);
        }

        .about-pig-ear {
            position: absolute;
            width: 14%;
            height: 16%;
            top: 28%;
            left: 12%;
            border-radius: 22% 78% 34% 66%;
            background: #ea9988;
            transform: rotate(-24deg);
        }

        .about-shield-signal {
            position: absolute;
            top: 20%;
            right: 14%;
            width: 22%;
            aspect-ratio: 1;
            border-radius: 50%;
            background: radial-gradient(circle, #ef5a47 30%, #ca3e2d 72%);
            box-shadow: 0 10px 22px rgba(142, 49, 36, 0.22);
        }

        .about-shield-signal::before,
        .about-shield-signal::after {
            content: "";
            position: absolute;
            inset: -18%;
            border-radius: 50%;
            border: 3px dotted rgba(239, 90, 71, 0.85);
        }

        .about-section-intro {
            max-width: 760px;
            margin: 0 0 1rem;
        }

        .about-section-intro h2 {
            margin: 0;
            color: #4b4137;
            font-size: clamp(1.75rem, 3vw, 2.3rem);
            line-height: 1.12;
            letter-spacing: -0.03em;
        }

        .about-section-intro p {
            margin: 0.55rem 0 0;
            color: #74695d;
            font-size: 1rem;
            line-height: 1.62;
        }

        .about-highlight-grid {
            display: grid;
            grid-template-columns: repeat(3, minmax(0, 1fr));
            gap: 1rem;
            margin-top: 1.15rem;
        }

        .about-highlight-card {
            height: 100%;
            padding: 1.15rem;
            border-radius: 20px;
            background: rgba(255, 251, 246, 0.94);
            border: 1px solid rgba(216, 200, 182, 0.95);
            box-shadow: 0 16px 28px rgba(83, 69, 56, 0.08);
        }

        .about-highlight-label {
            display: inline-flex;
            align-items: center;
            justify-content: center;
            min-width: 5rem;
            padding: 0.4rem 0.76rem;
            border-radius: 999px;
            background: rgba(255, 252, 248, 0.94);
            border: 1px solid rgba(216, 200, 182, 0.95);
            color: #6d7359;
            font-size: 0.78rem;
            font-weight: 700;
            letter-spacing: 0.02em;
        }

        .about-highlight-card h3 {
            margin: 0.95rem 0 0;
            color: #4b4137;
            font-size: 1.1rem;
            line-height: 1.28;
        }

        .about-highlight-card p {
            margin: 0.65rem 0 0;
            color: #786d61;
            font-size: 0.94rem;
            line-height: 1.62;
        }

        .about-mission-grid {
            display: grid;
            grid-template-columns: minmax(0, 1.2fr) minmax(280px, 0.8fr);
            gap: 1rem;
            margin-top: 1rem;
        }

        .about-panel {
            height: 100%;
            padding: 1.2rem;
            border-radius: 22px;
            background: rgba(255, 251, 246, 0.9);
            border: 1px solid rgba(216, 200, 182, 0.95);
        }

        .about-panel-title {
            margin: 0;
            color: #4b4137;
            font-size: 1.12rem;
            line-height: 1.3;
            font-weight: 800;
        }

        .about-panel-copy {
            margin: 0.7rem 0 0;
            color: #74695d;
            font-size: 0.96rem;
            line-height: 1.68;
        }

        .about-checklist {
            display: grid;
            gap: 0.75rem;
            margin-top: 0.95rem;
        }

        .about-check-item {
            display: grid;
            grid-template-columns: auto 1fr;
            gap: 0.7rem;
            align-items: start;
            padding: 0.85rem 0.95rem;
            border-radius: 16px;
            background: linear-gradient(180deg, rgba(255, 255, 255, 0.96), rgba(248, 241, 232, 0.92));
            border: 1px solid rgba(216, 200, 182, 0.92);
        }

        .about-check-icon {
            display: flex;
            align-items: center;
            justify-content: center;
            width: 1.95rem;
            height: 1.95rem;
            border-radius: 12px;
            background: linear-gradient(135deg, #596047, #6d7359);
            color: #fff;
            font-size: 0.92rem;
            font-weight: 800;
        }

        .about-check-item strong {
            color: #4b4137;
            font-size: 0.96rem;
            line-height: 1.35;
        }

        .about-check-item p {
            margin: 0.2rem 0 0;
            color: #7a7064;
            font-size: 0.9rem;
            line-height: 1.55;
        }

        .about-flow-grid {
            display: grid;
            grid-template-columns: repeat(4, minmax(0, 1fr));
            gap: 0.95rem;
            margin-top: 1.15rem;
        }

        .about-flow-step {
            min-height: 170px;
            padding: 1rem;
            border-radius: 18px;
            background: linear-gradient(180deg, rgba(255, 255, 255, 0.96), rgba(248, 241, 232, 0.92));
            border: 1px solid rgba(216, 200, 182, 0.92);
        }

        .about-flow-number {
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

        .about-flow-step h3 {
            margin: 0.85rem 0 0;
            color: #4b4137;
            font-size: 1rem;
            line-height: 1.3;
        }

        .about-flow-step p {
            margin: 0.55rem 0 0;
            color: #7a7064;
            font-size: 0.92rem;
            line-height: 1.56;
        }

        .about-footer-note {
            margin: 1.1rem 0 0;
            color: #7a7064;
            font-size: 0.92rem;
            line-height: 1.6;
        }

        @media (max-width: 980px) {
            .about-highlight-grid,
            .about-flow-grid {
                grid-template-columns: repeat(2, minmax(0, 1fr));
            }
        }

        @media (max-width: 900px) {
            .about-hero,
            .about-mission-grid {
                grid-template-columns: 1fr;
            }

            .about-visual {
                min-height: 270px;
            }

            .about-shield {
                inset: 1.4rem auto 1.4rem 50%;
                transform: translateX(-50%);
                width: min(100%, 270px);
            }

            .about-chip--top {
                right: 1rem;
            }

            .about-chip--bottom {
                left: 1rem;
            }
        }

        @media (max-width: 640px) {
            .about-highlight-grid,
            .about-flow-grid {
                grid-template-columns: 1fr;
            }

            .about-visual {
                min-height: 235px;
            }
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def render_highlights():
    cards = []
    for item in ABOUT_HIGHLIGHTS:
        cards.append(
            (
                "<article class='about-highlight-card'>"
                f"<span class='about-highlight-label'>{escape(item['label'])}</span>"
                f"<h3>{escape(item['title'])}</h3>"
                f"<p>{escape(item['copy'])}</p>"
                "</article>"
            )
        )

    st.markdown(
        "<div class='about-highlight-grid'>" + "".join(cards) + "</div>",
        unsafe_allow_html=True,
    )


def render_flow():
    steps = []
    for item in ABOUT_FLOW:
        steps.append(
            (
                "<article class='about-flow-step'>"
                f"<div class='about-flow-number'>{escape(item['step'])}</div>"
                f"<h3>{escape(item['title'])}</h3>"
                f"<p>{escape(item['copy'])}</p>"
                "</article>"
            )
        )

    st.markdown(
        "<div class='about-flow-grid'>" + "".join(steps) + "</div>",
        unsafe_allow_html=True,
    )


inject_about_styles()

st.markdown(
    """
    <div class="about-shell">
        <section class="about-hero-card">
            <div class="about-hero">
                <div>
                    <span class="about-kicker">Why Pigilan matters</span>
                    <h1 class="about-title">A simple ASF monitoring tool built for real farm work.</h1>
                    <p class="about-subtitle">
                        Pigilan helps farmers record observations, screen pig photos with AI,
                        save reports on the device, and return to them later for follow-up or sync.
                    </p>
                    <p class="about-note">
                        The goal is practical support: detect early, save the assessment, and make the next action clearer.
                    </p>
                </div>
                <div class="about-visual" aria-hidden="true">
                    <div class="about-orb about-orb--one"></div>
                    <div class="about-orb about-orb--two"></div>
                    <div class="about-chip about-chip--top">Offline-ready</div>
                    <div class="about-chip about-chip--bottom">Local reports</div>
                    <div class="about-shield">
                        <div class="about-shield-outer">
                            <div class="about-shield-inner">
                                <div class="about-pig">
                                    <div class="about-pig-ear"></div>
                                </div>
                                <div class="about-shield-signal"></div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </section>
    </div>
    """,
    unsafe_allow_html=True,
)

hero_action_col1, hero_action_col2, _ = st.columns([1, 1, 2], gap="small")
with hero_action_col1:
    if st.button("Start a Pig Check", key="about_open_assessment", use_container_width=True):
        st.session_state.page = "Health Assessment"
        st.rerun()
with hero_action_col2:
    if st.button("View Saved Reports", key="about_open_reports", use_container_width=True):
        st.session_state.page = "My Reports"
        st.rerun()

with st.container(border=True):
    st.markdown(
        """
        <div class="about-section-intro">
            <h2>What Pigilan helps you do</h2>
            <p>
                The app is focused on fast reporting, safer monitoring, and keeping case records usable
                whether the device is online or offline.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    render_highlights()

with st.container(border=True):
    st.markdown(
        """
        <div class="about-section-intro">
            <h2>Built for everyday monitoring</h2>
            <p>
                Pigilan is designed to support farm owners, caretakers, and local responders who need a
                lightweight way to document possible ASF cases and keep the information organized.
            </p>
        </div>
        <div class="about-mission-grid">
            <section class="about-panel">
                <h3 class="about-panel-title">The mission</h3>
                <p class="about-panel-copy">
                    Support earlier reporting and better record keeping for suspected ASF cases by making
                    assessments easier to complete, save, and review later.
                </p>
                <p class="about-panel-copy">
                    Instead of relying on memory or paper notes alone, Pigilan keeps symptoms, pig counts,
                    photos, map points, and recommended actions together in one place.
                </p>
            </section>
            <section class="about-panel">
                <h3 class="about-panel-title">What gets saved in each report</h3>
                <div class="about-checklist">
                    <div class="about-check-item">
                        <div class="about-check-icon">1</div>
                        <div>
                            <strong>Symptoms and observations</strong>
                            <p>Checklist signs, extra notes, and the number of pigs checked.</p>
                        </div>
                    </div>
                    <div class="about-check-item">
                        <div class="about-check-icon">2</div>
                        <div>
                            <strong>Photo and AI screening result</strong>
                            <p>Uploaded pig image plus the photo-based confidence result when available.</p>
                        </div>
                    </div>
                    <div class="about-check-item">
                        <div class="about-check-icon">3</div>
                        <div>
                            <strong>Location and next action</strong>
                            <p>Farm map point, saved case status, and the recommended response.</p>
                        </div>
                    </div>
                </div>
            </section>
        </div>
        """,
        unsafe_allow_html=True,
    )

with st.container(border=True):
    st.markdown(
        """
        <div class="about-section-intro">
            <h2>How the workflow works</h2>
            <p>
                Pigilan is meant to keep the reporting flow short: assess, save, review, and sync when ready.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    render_flow()
