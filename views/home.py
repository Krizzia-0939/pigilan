from html import escape

import streamlit as st
from shared.asset_utils import build_local_image_data_uri, resolve_asset_path
from shared.navigation import navigate_to_feature

HERO_BACKGROUND_PHOTO = resolve_asset_path("BG-PHOTO.png")
RISK_ASSESSMENT_PHOTO = resolve_asset_path("risk-assessment-photo.png")
IMAGE_BASED_DETECTION_PHOTO = resolve_asset_path("Image-Based_Detection.png")
BIOSECURITY_GUIDANCE_PHOTO = resolve_asset_path("Biosecurity-photo.png")
NEARBY_CASE_ALERTS_PHOTO = resolve_asset_path("Nearby-Case-Alerts.png")


FEATURE_CARDS = [
    {
        "accent": "risk",
        "title": "ASF Risk Assessment",
        "copy": "Answer the symptom checklist and get a clear risk summary for the pig you checked.",
        "image_data_uri": build_local_image_data_uri(RISK_ASSESSMENT_PHOTO),
        "image_alt": "ASF risk assessment guide",
        "feature_target": "asf-risk-assessment",
    },
    {
        "accent": "image",
        "title": "Image-Based Detection",
        "copy": "Upload a pig photo and review the model's screening result alongside your notes.",
        "image_data_uri": build_local_image_data_uri(IMAGE_BASED_DETECTION_PHOTO),
        "image_alt": "Image-based ASF detection",
        "feature_target": "image-based-detection",
    },
    {
        "accent": "guide",
        "title": "Biosecurity Guidance",
        "copy": "Review practical reminders for isolation, sanitation, and reducing farm-to-farm spread.",
        "image_data_uri": build_local_image_data_uri(BIOSECURITY_GUIDANCE_PHOTO),
        "image_alt": "Biosecurity guidance",
        "feature_target": "biosecurity-guidance",
    },
    {
        "accent": "alert",
        "title": "Nearby Case Alerts",
        "copy": "See nearby reports and keep an eye on cases that may need follow-up in your area.",
        "image_data_uri": build_local_image_data_uri(NEARBY_CASE_ALERTS_PHOTO),
        "image_alt": "Nearby case alerts",
        "feature_target": "nearby-case-alerts",
    },
]

HOME_HERO_BACKGROUND_DATA_URI = build_local_image_data_uri(HERO_BACKGROUND_PHOTO)

FLOW_STEPS = [
    {
        "step": "1",
        "title": "Create your account",
        "copy": "Save reports under your farm profile so you can return to them later.",
        "icon": "user",
    },
    {
        "step": "2",
        "title": "Record the case",
        "copy": "Answer the checklist, add a photo, and confirm the farm location.",
        "icon": "checklist",
    },
    {
        "step": "3",
        "title": "Save it on the device",
        "copy": "Keep the report locally even if the connection is weak or unavailable.",
        "icon": "device",
    },
    {
        "step": "4",
        "title": "Sync later",
        "copy": "Send records to the server later when you have a stable internet connection.",
        "icon": "sync",
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
            --home-hero-pad: clamp(1.35rem, 4vw, 2.25rem);
            position: relative;
            overflow: hidden;
            min-height: clamp(360px, 45vw, 430px);
            padding: var(--home-hero-pad);
            border-radius: 28px;
            border: none;
            background:
                linear-gradient(138deg, rgba(255, 251, 247, 0.98) 0%, rgba(248, 242, 235, 0.95) 44%, rgba(236, 226, 214, 0.82) 100%);
            box-shadow:
                0 26px 44px rgba(83, 69, 56, 0.08),
                inset 0 1px 0 rgba(255, 255, 255, 0.32);
        }

        .home-hero-card::before {
            content: "";
            position: absolute;
            inset: 0;
            background:
                radial-gradient(circle at 12% 16%, rgba(255, 255, 255, 0.58), transparent 28%),
                linear-gradient(180deg, rgba(255, 255, 255, 0.14), rgba(255, 255, 255, 0) 34%);
            pointer-events: none;
        }

        .home-hero-card::after {
            content: "";
            position: absolute;
            inset: 0;
            background: linear-gradient(90deg, rgba(250, 244, 238, 0.22) 0%, rgba(250, 244, 238, 0.05) 34%, rgba(112, 84, 69, 0.08) 100%);
            pointer-events: none;
        }

        .home-hero {
            position: relative;
            z-index: 1;
            display: grid;
            grid-template-columns: minmax(0, 1.04fr) minmax(300px, 0.96fr);
            gap: clamp(1rem, 3vw, 2.35rem);
            align-items: stretch;
            min-height: clamp(300px, 40vw, 372px);
        }

        .home-hero-copy {
            position: relative;
            z-index: 1;
            max-width: 34rem;
            display: flex;
            flex-direction: column;
            justify-content: center;
            padding: clamp(0.15rem, 1vw, 0.5rem) 0;
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
            margin: 1rem 0 0;
            color: #493d35;
            font-size: clamp(2.35rem, 5vw, 4rem);
            line-height: 0.94;
            letter-spacing: -0.06em;
            text-wrap: balance;
        }

        .home-hero-title span {
            display: block;
        }

        .home-hero-highlight {
            max-width: 26rem;
            margin: 0.9rem 0 0;
            color: #5b6248;
            font-size: clamp(1.18rem, 2.25vw, 1.7rem);
            line-height: 1.16;
            font-weight: 900;
            letter-spacing: -0.035em;
        }

        .home-hero-copy-text {
            max-width: 31rem;
            margin: 0.9rem 0 0;
            color: #5d5148;
            font-size: 1.04rem;
            line-height: 1.66;
        }

        .home-hero-note {
            max-width: 29rem;
            margin: 0.9rem 0 0;
            color: #665a50;
            font-size: 0.95rem;
            line-height: 1.55;
            font-weight: 600;
        }

        .home-hero-visual {
            position: relative;
            min-height: clamp(300px, 42vw, 380px);
            height: 100%;
            display: flex;
            align-items: stretch;
            justify-content: stretch;
            align-self: stretch;
            overflow: hidden;
        }

        .home-hero-visual::before {
            content: none;
        }

        .home-hero-photo-wrap {
            position: relative;
            width: calc(100% + var(--home-hero-pad));
            min-height: 100%;
            height: 100%;
            margin:
                calc(var(--home-hero-pad) * -1)
                calc(var(--home-hero-pad) * -1)
                calc(var(--home-hero-pad) * -1)
                auto;
            border-radius: 0;
            overflow: hidden;
            border: none;
            box-shadow: none;
            background: transparent;
            isolation: isolate;
        }

        .home-hero-photo-wrap::before {
            content: "";
            position: absolute;
            inset: 0;
            z-index: 1;
            background:
                linear-gradient(90deg, rgba(247, 240, 233, 0.92) 0%, rgba(247, 240, 233, 0.72) 13%, rgba(247, 240, 233, 0.28) 31%, rgba(247, 240, 233, 0.08) 56%, rgba(247, 240, 233, 0) 80%),
                linear-gradient(180deg, rgba(247, 240, 233, 0.26) 0%, rgba(247, 240, 233, 0.05) 18%, rgba(247, 240, 233, 0.01) 74%, rgba(247, 240, 233, 0.16) 100%);
            pointer-events: none;
        }

        .home-hero-photo-wrap::after {
            content: "";
            position: absolute;
            inset: 0;
            z-index: 1;
            background: linear-gradient(140deg, rgba(103, 112, 86, 0.08) 0%, rgba(103, 112, 86, 0) 44%, rgba(255, 255, 255, 0.06) 100%);
            pointer-events: none;
        }

        .home-hero-photo {
            position: absolute;
            inset: 0;
            width: 100%;
            height: 100%;
            object-fit: cover;
            object-position: 80% center;
            transform: scale(1.02);
            filter: saturate(0.98) contrast(1.04) brightness(1);
        }

        .home-cta-row-anchor {
            height: 0;
            margin: 0.95rem 0 0;
        }

        div[data-testid="stElementContainer"]:has(.home-cta-row-anchor) + div[data-testid="stHorizontalBlock"] {
            align-items: stretch;
            gap: 0.85rem;
        }

        div[data-testid="stElementContainer"]:has(.home-cta-row-anchor) + div[data-testid="stHorizontalBlock"] > div[data-testid="column"] {
            display: flex;
        }

        div[data-testid="stElementContainer"]:has(.home-cta-row-anchor) + div[data-testid="stHorizontalBlock"] > div[data-testid="column"] > div {
            width: 100%;
        }

        div[data-testid="stElementContainer"]:has(.home-cta-row-anchor) + div[data-testid="stHorizontalBlock"] div[data-testid="stButton"] > button {
            min-height: 3.25rem;
            border-radius: 16px;
        }

        div[data-testid="stElementContainer"]:has(.home-cta-row-anchor) + div[data-testid="stHorizontalBlock"] > div[data-testid="column"]:last-child div[data-testid="stButton"] > button {
            background: linear-gradient(180deg, rgba(255, 252, 248, 0.98), rgba(245, 237, 228, 0.92));
            color: #564c41;
            border: 1px solid rgba(184, 170, 152, 0.76);
            box-shadow: 0 12px 22px rgba(83, 69, 56, 0.09);
        }

        div[data-testid="stElementContainer"]:has(.home-cta-row-anchor) + div[data-testid="stHorizontalBlock"] > div[data-testid="column"]:last-child div[data-testid="stButton"] > button:hover {
            background: linear-gradient(180deg, rgba(255, 250, 245, 1), rgba(241, 231, 221, 0.96));
            color: #4f4439;
            border-color: rgba(166, 150, 132, 0.78);
            box-shadow: 0 14px 24px rgba(83, 69, 56, 0.11);
        }

        .home-section-intro {
            max-width: 760px;
            margin: 2.55rem auto 1.1rem;
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

        .home-feature-grid-anchor {
            height: 0;
            margin: 0;
        }

        div[data-testid="stElementContainer"]:has(.home-feature-grid-anchor) + div[data-testid="stHorizontalBlock"] {
            align-items: stretch;
            gap: 1rem;
            margin-top: 1.2rem;
        }

        div[data-testid="stElementContainer"]:has(.home-feature-grid-anchor) + div[data-testid="stHorizontalBlock"] > div[data-testid="column"] {
            display: flex;
            min-width: 0;
        }

        div[data-testid="stElementContainer"]:has(.home-feature-grid-anchor) + div[data-testid="stHorizontalBlock"] > div[data-testid="column"] > div {
            width: 100%;
            height: 100%;
        }

        .home-feature-card {
            position: relative;
            min-height: 224px;
            padding: 0.65rem 0.65rem 2.85rem;
            border-radius: 0;
            background: transparent;
            border: none;
            box-shadow: none;
            display: flex;
            flex-direction: column;
            gap: 0.75rem;
            box-sizing: border-box;
        }

        div[data-testid="stVerticalBlockBorderWrapper"]:has(.home-feature-card-panel) {
            position: relative;
            min-height: 224px;
            border-radius: 20px;
            background: linear-gradient(180deg, rgba(255, 255, 255, 0.99), rgba(251, 247, 241, 0.96));
            border: 1px solid rgba(223, 213, 199, 0.92);
            box-shadow: 0 10px 20px rgba(83, 69, 56, 0.06);
            overflow: hidden;
            box-sizing: border-box;
            transition:
                transform 160ms ease,
                border-color 160ms ease,
                box-shadow 160ms ease;
        }

        div[data-testid="stVerticalBlockBorderWrapper"]:has(.home-feature-card-panel) > div {
            height: 100%;
        }

        div[data-testid="stVerticalBlockBorderWrapper"]:has(.home-feature-card-panel) div[data-testid="stVerticalBlock"] {
            height: 100%;
            gap: 0;
        }

        div[data-testid="stVerticalBlockBorderWrapper"]:has(.home-feature-card-panel) div[data-testid="element-container"] {
            margin: 0;
        }

        .home-feature-card-panel {
            min-height: 100%;
            display: flex;
            flex-direction: column;
            gap: 0.75rem;
        }

        .home-feature-card-copy {
            display: flex;
            flex: 1 1 auto;
            flex-direction: column;
            justify-content: flex-start;
            gap: 0.45rem;
            min-width: 0;
            padding: 0 0.1rem;
        }

        .home-feature-image-wrap {
            min-height: 116px;
            border-radius: 14px;
            overflow: hidden;
            display: flex;
            align-items: center;
            justify-content: center;
            padding: 0.15rem;
            background: radial-gradient(circle at center, rgba(244, 241, 228, 0.92) 0%, rgba(244, 241, 228, 0.56) 58%, rgba(244, 241, 228, 0.06) 100%);
            box-sizing: border-box;
        }

        .home-feature-image {
            display: block;
            width: 100%;
            height: 100%;
            object-fit: contain;
            object-position: center;
            box-sizing: border-box;
        }

        .home-feature-card::before {
            content: none;
        }

        .home-feature-card--risk .home-feature-image-wrap {
            background: radial-gradient(circle at center, rgba(242, 238, 220, 0.94) 0%, rgba(242, 238, 220, 0.54) 60%, rgba(242, 238, 220, 0.08) 100%);
        }

        .home-feature-card--image .home-feature-image-wrap {
            background: radial-gradient(circle at center, rgba(239, 237, 220, 0.94) 0%, rgba(239, 237, 220, 0.52) 60%, rgba(239, 237, 220, 0.08) 100%);
        }

        .home-feature-card--guide .home-feature-image-wrap {
            background: radial-gradient(circle at center, rgba(236, 242, 223, 0.94) 0%, rgba(236, 242, 223, 0.54) 60%, rgba(236, 242, 223, 0.08) 100%);
        }

        .home-feature-card--alert .home-feature-image-wrap {
            background: radial-gradient(circle at center, rgba(247, 231, 224, 0.94) 0%, rgba(247, 231, 224, 0.54) 60%, rgba(247, 231, 224, 0.08) 100%);
        }

        .home-feature-card-panel h3 {
            margin: 0;
            color: #3f5b34;
            font-size: clamp(0.84rem, 1.08vw, 0.95rem);
            font-weight: 700;
            line-height: 1.3;
        }

        .home-feature-card-panel p {
            margin: 0;
            color: #6f655a;
            font-size: clamp(0.7rem, 0.9vw, 0.77rem);
            line-height: 1.52;
        }

        .home-feature-card-button-anchor {
            display: block;
            height: 0;
            margin: 0;
        }

        div[data-testid="stElementContainer"]:has(.home-feature-card-button-anchor) + div[data-testid="stButton"] {
            position: absolute;
            inset: 0;
            margin: 0;
            z-index: 3;
        }

        div[data-testid="stElementContainer"]:has(.home-feature-card-button-anchor) + div[data-testid="stButton"] > button {
            position: relative;
            width: 100%;
            height: 100%;
            min-height: 100%;
            padding: 0;
            border-radius: 0;
            background: transparent;
            color: transparent;
            border: none;
            box-shadow: none;
            font-size: 0;
            font-weight: 700;
            line-height: 1;
            box-sizing: border-box;
            cursor: pointer;
        }

        div[data-testid="stElementContainer"]:has(.home-feature-card-button-anchor) + div[data-testid="stButton"] > button::before {
            content: "→";
            font-size: 0.95rem;
            line-height: 1;
        }

        div[data-testid="stElementContainer"]:has(.home-feature-card-button-anchor) + div[data-testid="stButton"] > button:hover {
            background: rgba(95, 117, 75, 0.22);
            color: #3f5b34;
            box-shadow: 0 6px 14px rgba(83, 69, 56, 0.08);
            transform: translateY(-1px);
        }

        div[data-testid="stElementContainer"]:has(.home-feature-card-button-anchor) + div[data-testid="stButton"] > button:focus-visible {
            outline: 3px solid rgba(109, 115, 89, 0.24);
            outline-offset: 2px;
        }

        div[data-testid="stElementContainer"]:has(.home-feature-card-button-anchor) + div[data-testid="stButton"] > button::before {
            content: "\\2192";
            position: absolute;
            left: 0.82rem;
            bottom: 0.78rem;
            display: inline-flex;
            align-items: center;
            justify-content: center;
            width: 2rem;
            height: 1.45rem;
            border-radius: 999px;
            background: rgba(126, 148, 96, 0.16);
            color: #4f6941;
            font-size: 0.94rem;
            line-height: 1;
            transition:
                transform 160ms ease,
                background 160ms ease,
                color 160ms ease,
                box-shadow 160ms ease;
        }

        div[data-testid="stElementContainer"]:has(.home-feature-card-button-anchor) + div[data-testid="stButton"] > button:hover {
            background: transparent;
            color: transparent;
            box-shadow: none;
            transform: none;
        }

        div[data-testid="stElementContainer"]:has(.home-feature-card-button-anchor) + div[data-testid="stButton"] > button:hover::before {
            background: rgba(95, 117, 75, 0.22);
            color: #3f5b34;
            box-shadow: 0 6px 14px rgba(83, 69, 56, 0.08);
            transform: translateY(-1px);
        }

        div[data-testid="stElementContainer"]:has(.home-feature-card-button-anchor) + div[data-testid="stButton"] > button:focus-visible {
            outline: 3px solid rgba(109, 115, 89, 0.24);
            outline-offset: -3px;
        }

        div[data-testid="stElementContainer"]:has(.home-feature-card-button-anchor) + div[data-testid="stButton"] > button p {
            margin: 0;
            font-size: 0;
            opacity: 0;
        }

        div[data-testid="stVerticalBlockBorderWrapper"]:has(.home-feature-card-panel):hover {
            transform: translateY(-2px);
            border-color: rgba(203, 191, 172, 0.96);
            box-shadow: 0 16px 28px rgba(83, 69, 56, 0.09);
        }

        .home-sync-note {
            display: flex;
            align-items: center;
            gap: 0.7rem;
            max-width: 100%;
            margin: 1.05rem 0 0.95rem;
            padding: 0.72rem 1rem;
            border-radius: 999px;
            background: linear-gradient(180deg, rgba(245, 242, 230, 0.96), rgba(240, 236, 223, 0.92));
            border: 1px solid rgba(222, 212, 198, 0.82);
            box-shadow: 0 10px 18px rgba(83, 69, 56, 0.05);
            color: #655b50;
            font-size: 0.98rem;
            line-height: 1.65;
            font-weight: 600;
        }

        .home-sync-note-icon {
            flex-shrink: 0;
            display: inline-flex;
            align-items: center;
            justify-content: center;
            width: 1.45rem;
            height: 1.45rem;
            border-radius: 50%;
            background: #5f754b;
            color: #fff;
            font-size: 0.92rem;
            font-weight: 800;
            line-height: 1;
        }

        .home-flow-card {
            --workflow-card-padding: 1.5rem;
            --workflow-card-gap: 1.25rem;
            --workflow-card-radius: 20px;
            --workflow-card-border: 1px solid rgba(222, 212, 198, 0.9);
            padding: clamp(1.35rem, 3vw, 1.85rem);
            border-radius: 28px;
            background: linear-gradient(180deg, rgba(255, 255, 255, 0.98), rgba(251, 247, 241, 0.95));
            border: 1px solid rgba(216, 200, 182, 0.88);
            box-shadow: 0 16px 30px rgba(83, 69, 56, 0.06);
            box-sizing: border-box;
        }

        .home-flow-header {
            text-align: center;
            margin-bottom: 1.35rem;
        }

        .home-flow-header h2 {
            margin: 0;
            color: #2f2f2f;
            font-size: clamp(1.95rem, 3vw, 2.55rem);
            line-height: 1.08;
            letter-spacing: -0.04em;
        }

        .home-flow-header p {
            max-width: 32rem;
            margin: 0.65rem auto 0;
            color: #74695d;
            font-size: 1rem;
            line-height: 1.55;
        }

        .home-flow-grid {
            display: grid;
            grid-template-columns: repeat(4, minmax(0, 1fr));
            gap: var(--workflow-card-gap);
            margin-top: 0;
            align-items: stretch;
            grid-auto-rows: 1fr;
            box-sizing: border-box;
        }

        .home-flow-step {
            position: relative;
            min-height: 156px;
            height: 100%;
            padding: var(--workflow-card-padding);
            display: flex;
            align-items: flex-start;
            gap: 1rem;
            border-radius: var(--workflow-card-radius);
            background: linear-gradient(180deg, rgba(255, 255, 255, 0.99), rgba(251, 247, 241, 0.96));
            border: var(--workflow-card-border);
            box-shadow: 0 12px 24px rgba(83, 69, 56, 0.06);
            box-sizing: border-box;
        }

        .home-flow-step,
        .home-flow-step * {
            box-sizing: border-box;
        }

        .home-flow-step::after {
            content: "";
            position: absolute;
            top: 50%;
            right: calc(var(--workflow-card-gap) * -1);
            width: var(--workflow-card-gap);
            border-top: 2px dashed rgba(93, 120, 74, 0.72);
            transform: translateY(-50%);
        }

        .home-flow-step:last-child::after {
            content: none;
        }

        .home-flow-number {
            position: absolute;
            top: -0.72rem;
            left: var(--workflow-card-padding);
            display: flex;
            align-items: center;
            justify-content: center;
            width: 2rem;
            height: 2rem;
            border-radius: 50%;
            background: linear-gradient(180deg, #6d7359, #596047);
            color: #fff;
            font-size: 0.88rem;
            font-weight: 700;
            box-shadow: 0 8px 18px rgba(89, 96, 71, 0.18);
        }

        .home-flow-icon {
            flex: 0 0 3rem;
            width: 3rem;
            height: 3rem;
            border-radius: 16px;
            background: rgba(110, 132, 86, 0.14);
            display: inline-flex;
            align-items: center;
            justify-content: center;
            color: #667d52;
        }

        .home-flow-icon svg {
            width: 1.8rem;
            height: 1.8rem;
            stroke: currentColor;
            fill: none;
            stroke-width: 1.8;
            stroke-linecap: round;
            stroke-linejoin: round;
        }

        .home-flow-copy {
            min-width: 0;
            display: flex;
            flex: 1 1 auto;
            flex-direction: column;
            justify-content: flex-start;
            gap: 0.45rem;
            margin: 0;
        }

        .home-flow-step h3 {
            margin: 0;
            color: #35512d;
            font-size: 1rem;
            line-height: 1.3;
        }

        .home-flow-step p {
            margin: 0;
            color: #7a7064;
            font-size: 0.9rem;
            line-height: 1.52;
        }

        .home-nearby-card {
            padding: clamp(1.2rem, 3vw, 1.6rem);
            border-radius: 24px;
            background: rgba(255, 251, 246, 0.88);
        }

        .home-nearby-summary-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
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

        @media (max-width: 1024px) {
            .home-hero {
                grid-template-columns: minmax(0, 1fr) minmax(260px, 0.88fr);
            }

            .home-feature-grid,
            .home-flow-grid {
                grid-template-columns: repeat(2, minmax(0, 1fr));
            }

            div[data-testid="stElementContainer"]:has(.home-feature-grid-anchor) + div[data-testid="stHorizontalBlock"] > div[data-testid="column"] {
                min-width: calc(50% - 0.45rem) !important;
                flex: 1 1 calc(50% - 0.45rem) !important;
            }

            div[data-testid="stVerticalBlockBorderWrapper"]:has(.home-feature-card-panel) {
                min-height: 220px;
            }

            .home-feature-card {
                min-height: 220px;
            }

            .home-flow-step::after {
                content: none;
            }
        }

        @media (max-width: 900px) {
            .home-hero {
                grid-template-columns: 1fr;
                min-height: auto;
            }

            .home-hero-copy {
                max-width: none;
            }

            .home-hero-visual {
                min-height: clamp(240px, 48vw, 340px);
                height: auto;
            }

            .home-hero-visual::before,
            .home-hero-photo-wrap {
                width: 100%;
            }

            .home-hero-photo-wrap {
                min-height: inherit;
                height: auto;
                margin: 0;
                border-radius: 22px;
            }

            .home-hero-photo-wrap::before {
                background:
                    linear-gradient(180deg, rgba(247, 240, 233, 0.16) 0%, rgba(247, 240, 233, 0.03) 30%, rgba(247, 240, 233, 0.24) 100%),
                    linear-gradient(360deg, rgba(247, 240, 233, 0.40) 0%, rgba(247, 240, 233, 0) 42%);
            }

            .home-hero-photo {
                object-position: center 28%;
                transform: scale(1.01);
            }
        }

        @media (max-width: 640px) {
            .home-hero-card {
                --home-hero-pad: 1.1rem;
                min-height: auto;
            }

            .home-feature-grid,
            .home-flow-grid {
                grid-template-columns: 1fr;
            }

            div[data-testid="stElementContainer"]:has(.home-feature-grid-anchor) + div[data-testid="stHorizontalBlock"] {
                gap: 0.8rem;
            }

            div[data-testid="stElementContainer"]:has(.home-feature-grid-anchor) + div[data-testid="stHorizontalBlock"] > div[data-testid="column"] {
                min-width: 100% !important;
                flex: 1 1 100% !important;
            }

            div[data-testid="stVerticalBlockBorderWrapper"]:has(.home-feature-card-panel) {
                min-height: 214px;
                border-radius: 18px;
            }

            .home-feature-card {
                min-height: 214px;
                padding: 0.58rem 0.58rem 2.6rem;
                gap: 0.65rem;
            }

            .home-feature-card-copy {
                padding: 0;
            }

            .home-feature-image-wrap {
                min-height: 102px;
            }

            .home-feature-card-panel h3 {
                font-size: 0.88rem;
            }

            .home-feature-card-panel p {
                font-size: 0.75rem;
            }

            div[data-testid="stElementContainer"]:has(.home-feature-card-button-anchor) + div[data-testid="stButton"] > button::before {
                left: 0.74rem;
                bottom: 0.72rem;
                width: 1.9rem;
                height: 1.38rem;
            }

            .home-hero-title {
                font-size: clamp(2rem, 11vw, 2.7rem);
            }

            .home-hero-highlight {
                max-width: none;
                font-size: clamp(1.02rem, 4.7vw, 1.3rem);
            }

            .home-hero-kicker {
                font-size: 0.72rem;
                letter-spacing: 0.06em;
            }

            .home-hero-copy-text,
            .home-hero-note {
                font-size: 0.95rem;
            }

            .home-sync-note {
                margin: 1.2rem 0 0.95rem;
                padding: 0.8rem 0.9rem;
                font-size: 0.94rem;
                line-height: 1.55;
                border-radius: 22px;
                align-items: flex-start;
            }

            .home-hero-visual {
                min-height: 220px;
            }

            .home-hero-photo-wrap {
                min-height: 220px;
            }

            div[data-testid="stElementContainer"]:has(.home-cta-row-anchor) + div[data-testid="stHorizontalBlock"] > div[data-testid="column"] {
                min-width: 100% !important;
                flex: 1 1 100% !important;
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


def get_workflow_icon_svg(icon_name):
    icons = {
        "user": (
            "<svg viewBox='0 0 24 24' aria-hidden='true'>"
            "<path d='M12 12a4 4 0 1 0 0-8a4 4 0 0 0 0 8Z'/>"
            "<path d='M5 20a7 7 0 0 1 14 0'/>"
            "</svg>"
        ),
        "checklist": (
            "<svg viewBox='0 0 24 24' aria-hidden='true'>"
            "<rect x='7' y='4' width='10' height='16' rx='2'/>"
            "<path d='M10 4.5h4'/>"
            "<path d='M10 9h4'/>"
            "<path d='M10 13h4'/>"
            "<path d='M10 17h4'/>"
            "<path d='M8.5 9l.7.7 1.3-1.4'/>"
            "<path d='M8.5 13l.7.7 1.3-1.4'/>"
            "</svg>"
        ),
        "device": (
            "<svg viewBox='0 0 24 24' aria-hidden='true'>"
            "<rect x='7' y='3.5' width='10' height='17' rx='2'/>"
            "<path d='M10 7.5h4'/>"
            "<path d='M12 10v5'/>"
            "<path d='m9.8 13.4 2.2 2.2 2.2-2.2'/>"
            "</svg>"
        ),
        "sync": (
            "<svg viewBox='0 0 24 24' aria-hidden='true'>"
            "<path d='M7 18a4 4 0 0 1-.4-8A6 6 0 0 1 18 8.8A3.5 3.5 0 1 1 18 18'/>"
            "<path d='M12 10v7'/>"
            "<path d='m9.5 14.5 2.5 2.5 2.5-2.5'/>"
            "</svg>"
        ),
    }
    return icons.get(icon_name, "")


def render_feature_cards():
    st.markdown("<div class='home-feature-grid-anchor'></div>", unsafe_allow_html=True)
    feature_columns = st.columns(len(FEATURE_CARDS), gap="small")
    for column, card in zip(feature_columns, FEATURE_CARDS):
        with column:
            with st.container(border=True):
                image_markup = ""
                if card.get("image_data_uri"):
                    image_alt = escape(card.get("image_alt", card["title"]))
                    image_markup = (
                        "<div class=\"home-feature-image-wrap\">"
                        f"<img class=\"home-feature-image\" src=\"{card['image_data_uri']}\" alt=\"{image_alt}\">"
                        "</div>"
                    )

                st.markdown(
                    (
                        f"<article class=\"home-feature-card home-feature-card-panel home-feature-card--{card['accent']}\">"
                        f"{image_markup}"
                        "<div class=\"home-feature-card-copy\">"
                        f"<h3>{escape(card['title'])}</h3>"
                        f"<p>{escape(card['copy'])}</p>"
                        "</div>"
                        "</article>"
                    ),
                    unsafe_allow_html=True,
                )
                st.markdown("<div class='home-feature-card-button-anchor'></div>", unsafe_allow_html=True)
                if st.button(
                    "→",
                    key=f"home_feature_{card['feature_target']}",
                    help=f"Open {card['title']}",
                ):
                    navigate_to_feature(card["feature_target"])
                    st.rerun()


def render_flow_steps():
    steps_markup = []
    for item in FLOW_STEPS:
        icon_markup = get_workflow_icon_svg(item.get("icon", ""))
        steps_markup.append(
            (
                "<article class=\"home-flow-step\">"
                f"<div class=\"home-flow-number\">{escape(item['step'])}</div>"
                f"<div class=\"home-flow-icon\" aria-hidden=\"true\">{icon_markup}</div>"
                "<div class=\"home-flow-copy\">"
                f"<h3>{escape(item['title'])}</h3>"
                f"<p>{escape(item['copy'])}</p>"
                "</div>"
                "</article>"
            )
        )

    return "<div class='home-flow-grid'>" + "".join(steps_markup) + "</div>"


def render_footer():
    return


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
                    <div class="home-hero-kicker">Built for field use</div>
                    <h1 class="home-hero-title">
                        <span>Record possible</span>
                        <span>ASF cases</span>
                        <span>without the clutter.</span>
                    </h1>
                    <p class="home-hero-highlight">One place for symptoms, photos, location, and next steps.</p>
                    <p class="home-hero-copy-text">
                        Pigilan helps farmers and caretakers document suspicious cases, review the photo screening
                        result, and keep reports organized on the device before syncing them later.
                    </p>
                    <p class="home-hero-note">Use it during farm visits, then upload records once your connection is back.</p>
                </div>
                {hero_visual_markup}
            </div>
        </section>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("<div class='home-cta-row-anchor'></div>", unsafe_allow_html=True)
    primary_col, secondary_col = st.columns(2, gap="small")
    with primary_col:
        if st.button("Start a Pig Check", key="home_cta_primary", type="primary", use_container_width=True):
            st.session_state.page = "Health Assessment"
            st.rerun()
    with secondary_col:
        secondary_label = "View Saved Reports" if is_logged_in else "Set Up an Account"
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
        <h2>What you can do inside Pigilan</h2>
        <p>Core tools for checking pigs, saving reports, and reviewing case information later.</p>
    </div>
    """,
    unsafe_allow_html=True,
)
render_feature_cards()

st.markdown(
    (
        "<div class='home-sync-note'>"
        "<span class='home-sync-note-icon' aria-hidden='true'>i</span>"
        "<span>Reports stay on the device first. Sync them when internet is available.</span>"
        "</div>"
    ),
    unsafe_allow_html=True,
)

with st.container():
    st.markdown(
        f"""
        <div class="home-flow-card">
            <div class="home-flow-header">
                <h2>Pigilan workflow</h2>
                <p>Simple steps to check, save, and sync your reports.</p>
            </div>
            {render_flow_steps()}
        </div>
        """,
        unsafe_allow_html=True,
    )

render_footer()
