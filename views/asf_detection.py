from html import escape

import streamlit as st

from core.backend import distance_km, submit_assessment
from shared.location_picker import (
    DEFAULT_LATITUDE,
    DEFAULT_LONGITUDE,
    render_point_location_picker,
)
from shared.navigation import scroll_to_target_if_needed
from ml.ml_model import predict_uploaded_image, start_model_warmup


MAX_IMAGE_SIZE_BYTES = 500 * 1024 * 1024
SYMPTOM_OPTIONS = [
    {"label": "High Fever", "key": "assessment_symptom_high_fever"},
    {"label": "Loss of Appetite", "key": "assessment_symptom_loss_of_appetite"},
    {"label": "Lethargy (Weak/Inactive)", "key": "assessment_symptom_lethargy"},
    {"label": "Huddling Behavior", "key": "assessment_symptom_huddling_behavior"},
    {"label": "Heavy Nasal Discharge", "key": "assessment_symptom_heavy_nasal_discharge"},
    {"label": "Difficulty Breathing", "key": "assessment_symptom_difficulty_breathing"},
    {"label": "Vomiting", "key": "assessment_symptom_vomiting"},
    {"label": "Diarrhea (May Be Bloody)", "key": "assessment_symptom_diarrhea"},
    {"label": "Gummed-up Eyes", "key": "assessment_symptom_gummed_up_eyes"},
    {"label": "Joint Swelling or Arthritis", "key": "assessment_symptom_joint_swelling"},
    {"label": "Skin Discoloration (Red, Purple, or Blue)", "key": "assessment_symptom_skin_discoloration"},
    {"label": "Skin Ulcers", "key": "assessment_symptom_skin_ulcers"},
    {"label": "Bleeding From Body Openings (Nose, Mouth, Anus)", "key": "assessment_symptom_bleeding"},
    {"label": "Sudden Death", "key": "assessment_symptom_sudden_death"},
]

DISTRICT_REFERENCE_POINTS = {
    "Jaro": (10.74472, 122.56667),
    "Mandurriao": (10.71750, 122.53639),
    "Pavia": (10.77500, 122.54170),
    "City Proper": (10.693341, 122.573217),
}

VETERINARY_CONTACTS = [
    {
        "kind": "private",
        "priority": 1,
        "name": "Cornerstone Veterinary Clinic",
        "address": "Reginaville, 69 Jalandoni St, Jaro, Iloilo City",
        "contact": "(033) 320 9981",
        "facebook_label": "Cornerstone Animal Hospital and Veterinary Supply",
        "facebook_url": None,
        "area": "Jaro",
    },
    {
        "kind": "private",
        "priority": 2,
        "name": "Cornerstone Animal Hospital and Veterinary Supply",
        "address": "Faith Bldg., Jalandoni St., Brgy. Our Lady of Lourdes, Jaro, Iloilo City",
        "contact": "(033) 509 0693 / 0917 633 8278",
        "facebook_label": "Cornerstone Animal Hospital and Veterinary Supply",
        "facebook_url": "https://facebook.com/112513206895337",
        "area": "Jaro",
    },
    {
        "kind": "private",
        "priority": 1,
        "name": "Petvaluecare Veterinary Centre",
        "address": "80 Guzman St, Mandurriao, Iloilo City",
        "contact": "(033) 508 2122 / 0942 977 8844",
        "facebook_label": "Visit business page",
        "facebook_url": "https://petvaluecare-veterinary-centre.business.site",
        "area": "Mandurriao",
    },
    {
        "kind": "private",
        "priority": 3,
        "name": "Rebadulla Animal Care",
        "address": "Commission Civil St, Jaro, Iloilo City",
        "contact": "(033) 320 6744 / 0975 504 7818",
        "facebook_label": "Rebadulla Animal Care",
        "facebook_url": "https://www.facebook.com/RebAnimalCare/",
        "area": "Jaro",
    },
    {
        "kind": "private",
        "priority": 1,
        "name": "Ilonggo Vets Animal Clinic",
        "address": "Road 5, Don Julio Village, Pavia, Iloilo",
        "contact": "0998 542 2094",
        "facebook_label": "Ilonggo Vets Animal Clinic",
        "facebook_url": "https://m.me/IlonggoVetsAnimalClinic",
        "area": "Pavia",
    },
    {
        "kind": "government",
        "priority": 1,
        "name": "Office of the City Veterinarian Iloilo",
        "address": "Iloilo City Hall Complex, Iloilo City Proper",
        "contact": "(033) 336 8237",
        "facebook_label": "Iloilo City Government",
        "facebook_url": None,
        "area": "City Proper",
        "handles": [
            "ASF investigation",
            "Reporting suspected cases",
            "Coordination with DA",
        ],
    },
]

for contact in VETERINARY_CONTACTS:
    area_latitude, area_longitude = DISTRICT_REFERENCE_POINTS[contact["area"]]
    contact["latitude"] = area_latitude
    contact["longitude"] = area_longitude


def safe_float(value):
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def get_nearest_private_vet(case_latitude, case_longitude):
    reference_latitude = safe_float(case_latitude)
    reference_longitude = safe_float(case_longitude)
    if reference_latitude is None or reference_longitude is None:
        return None

    ranked_contacts = []
    for contact in VETERINARY_CONTACTS:
        if contact["kind"] != "private":
            continue
        area_distance_km = distance_km(
            reference_latitude,
            reference_longitude,
            contact["latitude"],
            contact["longitude"],
        )
        ranked_contacts.append((area_distance_km, contact["priority"], contact["name"], contact))

    if not ranked_contacts:
        return None

    _, _, _, nearest_contact = sorted(ranked_contacts, key=lambda item: (item[0], item[1], item[2]))[0]
    return nearest_contact


def get_asf_reporting_contact():
    for contact in VETERINARY_CONTACTS:
        if contact["kind"] == "government":
            return contact
    return None


def format_contact_link(contact):
    label = str(contact.get("facebook_label") or "").strip()
    url = str(contact.get("facebook_url") or "").strip()
    if not label:
        return ""
    if url:
        return f"<a href=\"{escape(url, quote=True)}\" target=\"_blank\">{escape(label)}</a>"
    return escape(label)


def build_contact_card_markup(label, contact, description, show_handles=False):
    if not contact:
        return ""

    handles_markup = ""
    if show_handles and contact.get("handles"):
        handle_items = "".join(
            f"<li>{escape(item)}</li>"
            for item in contact["handles"]
        )
        handles_markup = (
            "<div class=\"assessment-contact-support\">"
            "<strong>Can help with:</strong>"
            f"<ul>{handle_items}</ul>"
            "</div>"
        )

    link_markup = format_contact_link(contact)
    facebook_row = ""
    if link_markup:
        facebook_row = (
            "<p class=\"assessment-contact-meta\">"
            f"<strong>Page:</strong> {link_markup}"
            "</p>"
        )

    return (
        "<article class=\"assessment-contact-card\">"
        f"<p class=\"assessment-contact-label\">{escape(label)}</p>"
        f"<h4>{escape(contact['name'])}</h4>"
        f"<p class=\"assessment-contact-copy\">{escape(description)}</p>"
        f"<p class=\"assessment-contact-meta\"><strong>Address:</strong> {escape(contact['address'])}</p>"
        f"<p class=\"assessment-contact-meta\"><strong>Contact:</strong> {escape(contact['contact'])}</p>"
        f"{facebook_row}"
        f"{handles_markup}"
        "</article>"
    )


def render_high_risk_guidance(case_latitude, case_longitude):
    nearest_private = get_nearest_private_vet(case_latitude, case_longitude)
    city_vet_contact = get_asf_reporting_contact()

    steps = [
        "Isolate the pig immediately and keep it away from healthy pigs.",
        "Stop moving pigs, pork products, feeds, tools, and visitors in and out of the area until a veterinarian gives instructions.",
        "Use separate boots, clothing, feeders, and equipment for the affected area, then disinfect them after use.",
        "Do not sell, slaughter, or transport the suspected pig while waiting for veterinary advice.",
        "Check the rest of the herd for fever, weakness, loss of appetite, bleeding, diarrhea, skin discoloration, or sudden death.",
        "Keep this report, the uploaded photo, and the farm location ready for the nearest veterinarian and the city veterinarian.",
    ]
    steps_markup = "".join(f"<li>{escape(step)}</li>" for step in steps)

    nearest_private_markup = build_contact_card_markup(
        "Nearest clinic",
        nearest_private,
        (
            f"Best nearby clinic match based on your selected farm point and the clinic area in {nearest_private['area']}."
            if nearest_private
            else "No nearby clinic match is available right now."
        ),
    )
    city_vet_markup = build_contact_card_markup(
        "Recommended for ASF reporting",
        city_vet_contact,
        "Contact this office right away for suspected ASF investigation, reporting, and quarantine guidance.",
        show_handles=True,
    )

    st.markdown(
        f"""
        <div class="assessment-urgent-panel">
            <p class="assessment-urgent-kicker">High-risk follow-up</p>
            <h3>What to do now</h3>
            <p class="assessment-urgent-copy">
                This case needs immediate action. Follow the steps below first, then contact the recommended veterinary support near you.
            </p>
            <ol class="assessment-urgent-steps">
                {steps_markup}
            </ol>
            <div class="assessment-contact-grid">
                {nearest_private_markup}
                {city_vet_markup}
            </div>
            <p class="assessment-urgent-note">
                Nearest clinic matching is estimated from your selected farm point and the clinic area provided for Iloilo City and nearby Pavia.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def inject_assessment_styles():
    st.markdown(
        """
        <style>
        :root {
            --assessment-sage: #6d7359;
            --assessment-sage-dark: #596047;
            --assessment-sage-soft: #8d9178;
            --assessment-paper: #f7efe6;
            --assessment-card: rgba(255, 251, 246, 0.94);
            --assessment-border: #d8c8b6;
            --assessment-border-soft: rgba(216, 200, 182, 0.48);
            --assessment-text: #4b4137;
            --assessment-muted: #7a7064;
            --assessment-highlight: #ede1d3;
            --assessment-shadow: 0 16px 38px rgba(84, 70, 56, 0.11);
        }

        [data-testid="stAppViewContainer"] {
            background:
                radial-gradient(circle at top right, rgba(197, 180, 163, 0.20), transparent 27%),
                linear-gradient(180deg, #f6eee4 0%, #f7efe7 36%, #ede1d4 100%);
        }

        .main .block-container {
            max-width: 1120px;
            padding-top: 1.35rem;
            padding-bottom: 3.5rem;
        }

        .assessment-hero {
            position: relative;
            overflow: hidden;
            padding: 1.7rem 1.6rem;
            border-radius: 24px;
            margin-bottom: 1rem;
            background:
                linear-gradient(110deg, rgba(255, 252, 248, 0.97) 0%, rgba(249, 241, 232, 0.92) 56%, rgba(227, 214, 201, 0.88) 100%);
            border: 1px solid rgba(216, 200, 182, 0.96);
            box-shadow: var(--assessment-shadow);
        }

        .assessment-hero::after {
            content: "";
            position: absolute;
            inset: auto -3rem -4rem auto;
            width: 260px;
            height: 260px;
            border-radius: 50%;
            background: radial-gradient(circle, rgba(109, 115, 89, 0.18) 0%, rgba(109, 115, 89, 0.02) 70%, transparent 72%);
        }

        .assessment-kicker {
            display: inline-flex;
            align-items: center;
            gap: 0.4rem;
            padding: 0.35rem 0.7rem;
            border-radius: 999px;
            background: rgba(109, 115, 89, 0.13);
            color: var(--assessment-sage-dark);
            font-size: 0.84rem;
            font-weight: 700;
            letter-spacing: 0.02em;
        }

        .assessment-hero h1 {
            margin: 0.7rem 0 0.45rem;
            color: var(--assessment-text);
            font-size: clamp(1.95rem, 4vw, 2.55rem);
            line-height: 1.05;
        }

        .assessment-hero p {
            max-width: 700px;
            margin: 0;
            color: var(--assessment-muted);
            font-size: 1rem;
            line-height: 1.65;
        }

        .assessment-callout {
            display: grid;
            grid-template-columns: auto 1fr;
            gap: 0.85rem;
            margin: 0 0 1.1rem;
            padding: 1rem 1.05rem;
            border-radius: 18px;
            background: linear-gradient(180deg, rgba(255, 252, 248, 0.94), rgba(244, 235, 225, 0.92));
            border: 1px solid rgba(216, 200, 182, 0.95);
            box-shadow: 0 10px 26px rgba(84, 70, 56, 0.08);
        }

        .assessment-callout__icon {
            display: flex;
            align-items: center;
            justify-content: center;
            width: 2rem;
            height: 2rem;
            border-radius: 12px;
            background: linear-gradient(135deg, var(--assessment-sage-dark), var(--assessment-sage));
            color: #fff;
            font-weight: 700;
            font-size: 1rem;
        }

        .assessment-callout h3 {
            margin: 0;
            color: var(--assessment-text);
            font-size: 1.05rem;
        }

        .assessment-callout p {
            margin: 0.28rem 0 0;
            color: var(--assessment-muted);
            line-height: 1.58;
        }

        div[data-testid="stVerticalBlockBorderWrapper"] {
            background: var(--assessment-card);
            border: 1px solid rgba(216, 200, 182, 0.95);
            border-radius: 20px;
            box-shadow: 0 10px 30px rgba(84, 70, 56, 0.08);
        }

        .assessment-step-bar {
            margin: -0.15rem -0.15rem 1rem;
            padding: 0.72rem 0.95rem;
            border-radius: 14px;
            background: linear-gradient(90deg, var(--assessment-sage-dark) 0%, var(--assessment-sage) 100%);
            color: #fff;
            font-weight: 700;
            letter-spacing: 0.01em;
        }

        .assessment-field-label {
            margin: 0 0 0.25rem;
            color: var(--assessment-text);
            font-size: 0.92rem;
            font-weight: 700;
        }

        .assessment-photo-copy h4 {
            margin: 0 0 0.35rem;
            color: var(--assessment-text);
            font-size: 1.05rem;
        }

        .assessment-photo-copy p {
            margin: 0 0 0.5rem;
            color: var(--assessment-muted);
            line-height: 1.6;
        }

        .assessment-photo-copy small {
            color: var(--assessment-muted);
            font-size: 0.84rem;
        }

        .assessment-result-title {
            margin: 0;
            color: var(--assessment-text);
            font-size: 1.02rem;
            font-weight: 700;
        }

        .assessment-result-copy {
            margin: 0.25rem 0 0;
            color: var(--assessment-muted);
            line-height: 1.58;
        }

        .assessment-urgent-panel {
            margin-top: 1rem;
            padding: 1.05rem 1.1rem;
            border-radius: 18px;
            background: linear-gradient(180deg, rgba(255, 246, 242, 0.98), rgba(252, 236, 231, 0.95));
            border: 1px solid rgba(213, 151, 137, 0.55);
            box-shadow: 0 12px 30px rgba(129, 73, 60, 0.10);
        }

        .assessment-urgent-kicker {
            margin: 0;
            color: #9b4f45;
            font-size: 0.82rem;
            font-weight: 800;
            letter-spacing: 0.04em;
            text-transform: uppercase;
        }

        .assessment-urgent-panel h3 {
            margin: 0.3rem 0 0;
            color: var(--assessment-text);
            font-size: 1.18rem;
            line-height: 1.25;
        }

        .assessment-urgent-copy {
            margin: 0.45rem 0 0;
            color: #735d52;
            line-height: 1.6;
        }

        .assessment-urgent-steps {
            margin: 0.9rem 0 0;
            padding-left: 1.2rem;
            color: var(--assessment-text);
        }

        .assessment-urgent-steps li {
            margin-bottom: 0.55rem;
            line-height: 1.56;
        }

        .assessment-contact-grid {
            display: grid;
            grid-template-columns: repeat(2, minmax(0, 1fr));
            gap: 0.9rem;
            margin-top: 1rem;
        }

        .assessment-contact-card {
            padding: 0.95rem 1rem;
            border-radius: 16px;
            background: rgba(255, 252, 249, 0.95);
            border: 1px solid rgba(216, 200, 182, 0.92);
        }

        .assessment-contact-label {
            margin: 0;
            color: #9b4f45;
            font-size: 0.8rem;
            font-weight: 800;
            letter-spacing: 0.04em;
            text-transform: uppercase;
        }

        .assessment-contact-card h4 {
            margin: 0.35rem 0 0;
            color: var(--assessment-text);
            font-size: 1.05rem;
            line-height: 1.3;
        }

        .assessment-contact-copy {
            margin: 0.45rem 0 0.6rem;
            color: var(--assessment-muted);
            line-height: 1.55;
        }

        .assessment-contact-meta {
            margin: 0.3rem 0 0;
            color: #6f6257;
            line-height: 1.5;
            font-size: 0.92rem;
        }

        .assessment-contact-meta strong,
        .assessment-contact-support strong {
            color: var(--assessment-text);
        }

        .assessment-contact-meta a {
            color: var(--assessment-sage-dark);
            text-decoration: none;
            font-weight: 700;
        }

        .assessment-contact-support {
            margin-top: 0.65rem;
            color: #6f6257;
            font-size: 0.92rem;
            line-height: 1.5;
        }

        .assessment-contact-support ul {
            margin: 0.35rem 0 0;
            padding-left: 1.15rem;
        }

        .assessment-contact-support li {
            margin-bottom: 0.3rem;
        }

        .assessment-urgent-note {
            margin: 0.8rem 0 0;
            color: #8a6e62;
            font-size: 0.86rem;
            line-height: 1.5;
        }

        div[data-testid="stTextInput"] input,
        div[data-testid="stTextArea"] textarea,
        div[data-testid="stNumberInput"] input,
        div[data-testid="stFileUploaderDropzone"] {
            background: rgba(255, 253, 250, 0.96);
            border-radius: 14px;
            border: 1px solid rgba(216, 200, 182, 0.95);
        }

        div[data-testid="stTextInput"] input,
        div[data-testid="stNumberInput"] input {
            min-height: 2.85rem;
        }

        div[data-testid="stTextArea"] textarea {
            min-height: 110px;
        }

        div[data-testid="stCheckbox"] {
            padding: 0.2rem 0.65rem;
            border-radius: 14px;
            border: 1px solid rgba(216, 200, 182, 0.90);
            background: linear-gradient(180deg, rgba(255, 252, 248, 0.90), rgba(246, 238, 229, 0.82));
            margin-bottom: 0.35rem;
        }

        div[data-testid="stCheckbox"] label {
            width: 100%;
        }

        div[data-testid="stCheckbox"] p,
        .stNumberInput label p,
        .stTextInput label p,
        .stTextArea label p {
            color: var(--assessment-text);
            font-weight: 600;
        }

        div[data-testid="stButton"] > button {
            border-radius: 999px;
            min-height: 2.85rem;
            border: none;
            background: linear-gradient(135deg, var(--assessment-sage-dark), var(--assessment-sage));
            color: #fff;
            font-weight: 700;
            box-shadow: 0 10px 22px rgba(89, 96, 71, 0.18);
        }

        div[data-testid="stButton"] > button:hover {
            background: linear-gradient(135deg, #50573f, #666d53);
            color: #fff;
        }

        div[data-testid="stFileUploaderDropzone"] {
            padding: 1.15rem;
            border-style: dashed;
            border-width: 1.5px;
        }

        div[data-testid="stDeckGlJsonChart"] {
            border-radius: 18px;
            overflow: hidden;
            border: 1px solid rgba(216, 200, 182, 0.95);
        }

        @media (max-width: 768px) {
            .main .block-container {
                padding-top: 1rem;
                padding-right: 0.9rem;
                padding-left: 0.9rem;
            }

            .assessment-hero {
                padding: 1.25rem 1rem;
                border-radius: 20px;
            }

            .assessment-callout {
                grid-template-columns: 1fr;
            }

            .assessment-step-bar {
                margin-bottom: 0.85rem;
            }

            .assessment-contact-grid {
                grid-template-columns: 1fr;
            }
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def render_step_bar(title):
    st.markdown(f"<div class='assessment-step-bar'>{title}</div>", unsafe_allow_html=True)


def get_selected_symptoms():
    return [
        option["label"]
        for option in SYMPTOM_OPTIONS
        if st.session_state.get(option["key"], False)
    ]


inject_assessment_styles()

if "user" not in st.session_state or not st.session_state.user:
    st.warning("Please sign in first before opening the Health Assessment page.")
    st.stop()

if "case_latitude" not in st.session_state:
    st.session_state.case_latitude = float(
        st.session_state.user.get("latitude") or DEFAULT_LATITUDE
    )
if "case_longitude" not in st.session_state:
    st.session_state.case_longitude = float(
        st.session_state.user.get("longitude") or DEFAULT_LONGITUDE
    )

start_model_warmup()

st.markdown(
    """
    <div class="assessment-hero">
        <span class="assessment-kicker">Pigilan Health Assessment</span>
        <h1>Health Assessment</h1>
        <p>
            Assess your pigs for possible signs of African Swine Fever (ASF).
            Complete the steps below to identify risk factors and record necessary
            details even when offline.
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div class="assessment-callout">
        <div class="assessment-callout__icon">&#10003;</div>
        <div>
            <h3>Follow the steps below to evaluate your pigs' condition.</h3>
            <p>
                Providing accurate symptoms and a clear photo will help detect potential
                ASF cases more effectively and offer guidance on protecting your herd.
                Each completed assessment contributes to better monitoring and disease control.
            </p>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

with st.container(border=True):
    render_step_bar("Step 1: Case Details")
    st.markdown("<div class='assessment-field-label'>Case Title</div>", unsafe_allow_html=True)
    case_name = st.text_input(
        "Case Title",
        placeholder="Enter case title",
        label_visibility="collapsed",
    )
    st.markdown("<div class='assessment-field-label'>Notes</div>", unsafe_allow_html=True)
    case_remarks = st.text_area(
        "Notes",
        placeholder="Enter any additional notes (optional)",
        label_visibility="collapsed",
    )
    pig_count = st.number_input(
        "Number of Pigs Checked",
        min_value=1,
        value=1,
        step=1,
        help="Use this to record how many pigs were included in this farm visit.",
    )

with st.container(border=True):
    render_step_bar("Step 2: Choose the Signs You See")
    st.caption("Select all signs that apply to the pig being assessed or nearby pigs on the farm.")
    symptom_col1, symptom_col2 = st.columns(2, gap="medium")
    for index, option in enumerate(SYMPTOM_OPTIONS):
        target_column = symptom_col1 if index % 2 == 0 else symptom_col2
        with target_column:
            st.checkbox(option["label"], key=option["key"])

with st.container(border=True):
    render_step_bar("Step 3: Farm Location")
    st.session_state.case_latitude, st.session_state.case_longitude = render_point_location_picker(
        title="Farm Location",
        session_prefix="case_location",
        initial_latitude=st.session_state.case_latitude,
        initial_longitude=st.session_state.case_longitude,
        caption_text="Use the current location button or review the coordinates of this farm check below.",
        show_section_header=False,
    )

st.markdown("<div id='assessment-upload-photo' style='scroll-margin-top: 1rem;'></div>", unsafe_allow_html=True)
scroll_to_target_if_needed("assessment-upload-photo")

with st.container(border=True):
    render_step_bar("Step 4: Upload a Pig Photo")
    upload_col, details_col = st.columns([1.05, 1], gap="large")
    with upload_col:
        image = st.file_uploader(
            "Upload a pig photo",
            type=["jpg", "jpeg", "png"],
            label_visibility="collapsed",
        )
        if image is not None:
            st.image(image.getvalue(), caption="Selected pig photo", use_container_width=True)

    with details_col:
        st.markdown(
            """
            <div class="assessment-photo-copy">
                <h4>Drag &amp; drop or select a photo of your pig.</h4>
                <p>Blurry or dark photos may affect the result.</p>
                <small>PNG, JPG, and JPEG files up to 500 MB.</small>
            </div>
            """,
            unsafe_allow_html=True,
        )
        if image is not None:
            image_size_mb = len(image.getvalue()) / (1024 * 1024)
            st.caption(f"Selected file: {image.name} ({image_size_mb:.2f} MB)")

if st.button("Analyze Health Condition", type="primary", use_container_width=True):
    selected_symptoms = get_selected_symptoms()

    if not case_name.strip():
        st.error("Please enter a case title before analyzing the health condition.")
        st.stop()

    if int(pig_count) > 100000:
        st.error("Please enter a realistic number of pigs checked.")
        st.stop()

    if image is None:
        st.error("Please upload a pig photo before analyzing the health condition.")
        st.stop()

    image_size_bytes = len(image.getvalue())
    if image_size_bytes > MAX_IMAGE_SIZE_BYTES:
        st.error("The uploaded photo is too large. Please use a PNG, JPG, or JPEG file up to 500 MB.")
        st.stop()

    with st.spinner(
        "Analyzing health condition. The first run after opening the app may take longer while the image AI finishes loading."
    ):
        ml_result = predict_uploaded_image(image)

    ml_is_available = ml_result["label"] != "Model unavailable"
    ml_percentage = ml_result["asf_confidence"] if ml_is_available else 0.0

    if not ml_result["is_valid_image"] and ml_is_available:
        st.error(ml_result["message"])
        st.stop()

    image.seek(0)

    try:
        result = submit_assessment(
            user_id=st.session_state.user["id"],
            pig_count=int(pig_count),
            symptoms=selected_symptoms,
            ml_percentage=float(ml_percentage),
            uploaded_file=image,
            case_latitude=float(st.session_state.case_latitude),
            case_longitude=float(st.session_state.case_longitude),
            case_name=case_name.strip(),
            remarks=case_remarks.strip(),
        )
    except ValueError as exc:
        st.error(str(exc))
        st.stop()

    with st.container(border=True):
        render_step_bar("Assessment Result")
        st.markdown(
            """
            <p class="assessment-result-title">Health assessment saved successfully.</p>
            <p class="assessment-result-copy">
                Review the AI result, the symptom-based score, and the recommended next step below.
            </p>
            """,
            unsafe_allow_html=True,
        )

        metric_row1 = st.columns(3, gap="medium")
        with metric_row1[0]:
            st.metric("Photo Result", ml_result["label"])
        with metric_row1[1]:
            if ml_is_available:
                st.metric("Photo Confidence", f"{ml_result['confidence']}%")
            else:
                st.metric("Photo Confidence", "Unavailable")
        with metric_row1[2]:
            st.metric("ASF Photo Result", f"{ml_percentage}%")

        metric_row2 = st.columns(3, gap="medium")
        with metric_row2[0]:
            st.metric("Signs Seen Score", result["checklist_score"])
        with metric_row2[1]:
            st.metric("Signs Seen Level", f"{result['symptom_percentage']}%")
        with metric_row2[2]:
            st.metric("Overall Risk Score", f"{result['total_percentage']}%")

        st.write(f"Risk Result: **{result['risk_level']}**")
        st.write(f"Recommended Action: {result['recommendation']}")

        if not ml_is_available:
            st.warning(
                "Image AI is unavailable on this computer right now. The case was saved using the symptom checklist score only."
            )
            st.caption(ml_result["message"])

        st.caption(
            f"Saved check #{result['assessment_id']} and case #{result['case_id']}."
        )
        if result["image_path"]:
            st.caption(f"Saved photo: {result['image_path']}")

        if result["risk_level"] == "HIGH RISK":
            st.warning("High risk found. Follow the urgent steps below. A nearby alert was also created.")
            render_high_risk_guidance(
                case_latitude=st.session_state.case_latitude,
                case_longitude=st.session_state.case_longitude,
            )
        elif result["risk_level"] == "MODERATE RISK":
            st.info("Moderate risk found. Please watch closely and check notifications.")
        else:
            st.success("Low risk case saved successfully.")
