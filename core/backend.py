from pathlib import Path
from datetime import datetime
from math import atan2, cos, radians, sin, sqrt
from urllib.parse import urlparse
import base64
import hashlib
import os
import secrets
import uuid
import requests

from core.database import (
    create_alert,
    create_biosecurity_check,
    create_case,
    create_case_image,
    create_case_share,
    create_notification,
    create_risk_assessment,
    create_user,
    get_admin_case_overview,
    get_all_cases_with_coordinates,
    get_alerts,
    get_biosecurity_check_by_client_record_id,
    get_biosecurity_checks_for_user,
    get_case_by_client_record_id,
    get_cases_for_user,
    get_cases,
    get_notifications_for_user,
    get_pending_sync_counts,
    get_user_by_client_record_id,
    get_user_by_id,
    get_user_by_username,
    get_users,
    mark_notification_read,
    mark_biosecurity_checks_synced_for_user,
    mark_cases_synced_for_user,
    mark_user_synced,
    update_case_details,
    update_imported_user_profile,
    update_user_coordinates,
    update_user_password,
    update_user_profile,
)
from core.pdf_utils import build_simple_pdf


PROJECT_ROOT = Path(__file__).resolve().parent.parent
DB_FILE_PATH = PROJECT_ROOT / "pigilan.db"
UPLOADS_DIR = PROJECT_ROOT / "uploads"
UPLOADS_DIR.mkdir(exist_ok=True)
EXPORTS_DIR = PROJECT_ROOT / "exports"
EXPORTS_DIR.mkdir(exist_ok=True)
DEFAULT_SYNC_SERVER_URL = os.environ.get("PIGILAN_SYNC_SERVER_URL", "http://127.0.0.1:8000")
MAX_PIG_COUNT = 100000
DEFAULT_ADMIN_USERNAME = "admin"
DEFAULT_ADMIN_PASSWORD = "admin123"
REVERSE_GEOCODE_URL = "https://nominatim.openstreetmap.org/reverse"

SYMPTOM_WEIGHTS = {
    "High Fever": 3,
    "Loss of Appetite": 3,
    "Lethargy (Weak/Inactive)": 4,
    "Huddling Behavior": 4,
    "Heavy Nasal Discharge": 6,
    "Difficulty Breathing": 8,
    "Vomiting": 6,
    "Diarrhea (May Be Bloody)": 10,
    "Gummed-up Eyes": 4,
    "Joint Swelling or Arthritis": 6,
    "Skin Discoloration (Red, Purple, or Blue)": 8,
    "Skin Ulcers": 8,
    "Bleeding From Body Openings (Nose, Mouth, Anus)": 10,
    "Sudden Death": 10,
}

SYMPTOM_ALIASES = {
    "High Fever": "High Fever",
    "Loss of Appetite": "Loss of Appetite",
    "Lethargy (Weak/Inactive)": "Lethargy (Weak/Inactive)",
    "Weakness or Lethargy": "Lethargy (Weak/Inactive)",
    "Weakness": "Lethargy (Weak/Inactive)",
    "Huddling Behavior": "Huddling Behavior",
    "Discharge From Eyes or Nose": "Heavy Nasal Discharge",
    "Heavy Nasal Discharge": "Heavy Nasal Discharge",
    "Vomiting": "Vomiting",
    "Persistent Coughing": "Huddling Behavior",
    "Diarrhea (May Be Bloody)": "Diarrhea (May Be Bloody)",
    "Difficulty Breathing": "Difficulty Breathing",
    "Bloody Diarrhea": "Diarrhea (May Be Bloody)",
    "Diarrhea (bloody)": "Diarrhea (May Be Bloody)",
    "Gummed-up Eyes": "Gummed-up Eyes",
    "Joint Swelling": "Joint Swelling or Arthritis",
    "Joint Swelling or Arthritis": "Joint Swelling or Arthritis",
    "Skin Lesions or Hemorrhages": "Skin Discoloration (Red, Purple, or Blue)",
    "Skin Discoloration (red, purple, or blue)": "Skin Discoloration (Red, Purple, or Blue)",
    "Skin Discoloration (Red, Purple, or Blue)": "Skin Discoloration (Red, Purple, or Blue)",
    "Skin Ulcers": "Skin Ulcers",
    "Bleeding From Body Openings (Nose, Mouth, Anus)": "Bleeding From Body Openings (Nose, Mouth, Anus)",
    "Sudden Death": "Sudden Death",
    "Sudden Death of Nearby Pigs": "Sudden Death",
}

ACTIVE_ASSESSMENT_SYMPTOMS = [
    "High Fever",
    "Loss of Appetite",
    "Lethargy (Weak/Inactive)",
    "Huddling Behavior",
    "Heavy Nasal Discharge",
    "Difficulty Breathing",
    "Vomiting",
    "Diarrhea (May Be Bloody)",
    "Gummed-up Eyes",
    "Joint Swelling or Arthritis",
    "Skin Discoloration (Red, Purple, or Blue)",
    "Skin Ulcers",
    "Bleeding From Body Openings (Nose, Mouth, Anus)",
    "Sudden Death",
]

BIOSECURITY_ITEMS = [
    "Maintain strict biosecurity",
    "Only allow essential visitors to enter your farm, and insist that they wear clean or disposable clothing and footwear, and wash their hands (or shower in if possible)",
    "Only allow vehicles and equipment on to the farm if they have been cleaned and disinfected beforehand",
    "Do not allow people who may have been in contact with other pigs on to your farm",
    "Do not allow staff and visitors to bring pork products on to the farm",
    "Do not allow catering waste / scraps to be fed to pigs - dispose of it safely",
    "Only source pigs and semen of known health status",
]


def _normalize_coordinates(latitude, longitude):
    if latitude is None or longitude is None:
        return None, None
    if float(latitude) == 0.0 and float(longitude) == 0.0:
        return None, None
    return float(latitude), float(longitude)


def _clean_address_value(address):
    cleaned = str(address or "").strip()
    if not cleaned or cleaned.lower() == "not set yet":
        return None
    return cleaned


def _build_address_lookup_key(address):
    cleaned = _clean_address_value(address)
    if not cleaned:
        return None
    normalized = "".join(char.lower() if char.isalnum() else " " for char in cleaned)
    return " ".join(normalized.split())


def _format_address_record(record, fallback="No address saved."):
    explicit_address = _clean_address_value(record.get("address"))
    if explicit_address:
        return explicit_address

    parts = [
        str(record.get("barangay") or "").strip(),
        str(record.get("municipality") or "").strip(),
        str(record.get("province") or "").strip(),
    ]
    parts = [part for part in parts if part and part.lower() != "not set yet"]
    return ", ".join(parts) if parts else fallback


def get_coordinates_for_address(address, exclude_user_id=None):
    address_key = _build_address_lookup_key(address)
    if not address_key:
        return None, None

    matching_users = []
    for user in get_users():
        if exclude_user_id is not None and user.get("id") == exclude_user_id:
            continue
        if _build_address_lookup_key(user.get("address")) != address_key:
            continue
        matching_users.append(user)
        user_latitude, user_longitude = _normalize_coordinates(
            user.get("latitude"),
            user.get("longitude"),
        )
        if user_latitude is not None and user_longitude is not None:
            return user_latitude, user_longitude

    for user in matching_users:
        for case in get_cases_for_user(user["id"]):
            case_latitude, case_longitude = _normalize_coordinates(
                case.get("latitude"),
                case.get("longitude"),
            )
            if case_latitude is not None and case_longitude is not None:
                return case_latitude, case_longitude

    return None, None


def reverse_geocode_coordinates(latitude, longitude):
    latitude, longitude = _normalize_coordinates(latitude, longitude)
    if latitude is None or longitude is None:
        return None

    try:
        response = requests.get(
            REVERSE_GEOCODE_URL,
            params={
                "format": "jsonv2",
                "lat": latitude,
                "lon": longitude,
                "zoom": 18,
                "addressdetails": 1,
            },
            headers={
                "User-Agent": "Pigilan/1.0 (farm address reverse geocoder)",
            },
            timeout=4,
        )
        response.raise_for_status()
        payload = response.json()
    except Exception:
        return None

    address_payload = payload.get("address") or {}
    ordered_parts = [
        address_payload.get("house_number"),
        address_payload.get("road"),
        address_payload.get("neighbourhood"),
        address_payload.get("suburb"),
        address_payload.get("village"),
        address_payload.get("hamlet"),
        address_payload.get("town"),
        address_payload.get("city"),
        address_payload.get("municipality"),
        address_payload.get("county"),
        address_payload.get("state"),
    ]
    address_parts = []
    seen_parts = set()
    for part in ordered_parts:
        cleaned_part = str(part or "").strip()
        normalized_part = cleaned_part.lower()
        if not cleaned_part or normalized_part in seen_parts:
            continue
        seen_parts.add(normalized_part)
        address_parts.append(cleaned_part)

    if address_parts:
        return ", ".join(address_parts)

    display_name = str(payload.get("display_name") or "").strip()
    return display_name or None


def _hash_password(password, salt=None):
    salt = salt or secrets.token_hex(16)
    derived = hashlib.pbkdf2_hmac(
        "sha256",
        password.encode("utf-8"),
        salt.encode("utf-8"),
        120000,
    ).hex()
    return f"pbkdf2_sha256${salt}${derived}"


def _verify_password(password, stored_password):
    if not stored_password:
        return False
    if not stored_password.startswith("pbkdf2_sha256$"):
        return secrets.compare_digest(password, stored_password)

    _, salt, stored_hash = stored_password.split("$", 2)
    candidate = _hash_password(password, salt=salt).split("$", 2)[2]
    return secrets.compare_digest(candidate, stored_hash)


def _validate_case_inputs(case_name, pig_count, latitude, longitude):
    errors = []
    if not str(case_name or "").strip():
        errors.append("Please add a case title.")
    if pig_count is None or int(pig_count) < 1:
        errors.append("Please enter at least 1 pig checked.")
    if pig_count is not None and int(pig_count) > MAX_PIG_COUNT:
        errors.append(f"Please enter a pig count below {MAX_PIG_COUNT:,}.")
    if latitude is None or longitude is None:
        errors.append("Please capture the farm location using GPS, map click, or manual coordinates.")
    return errors


def register_user(
    username,
    password,
    first_name,
    last_name,
    barangay,
    municipality,
    province,
    address=None,
    latitude=None,
    longitude=None,
):
    cleaned_address = _clean_address_value(address)
    latitude, longitude = _normalize_coordinates(latitude, longitude)
    if latitude is None or longitude is None:
        latitude, longitude = get_coordinates_for_address(cleaned_address)
    hashed_password = _hash_password(password)
    user_id = create_user(
        username=username,
        password=hashed_password,
        first_name=first_name,
        last_name=last_name,
        barangay=barangay,
        municipality=municipality,
        province=province,
        address=cleaned_address,
        role="farmer",
        client_record_id=str(uuid.uuid4()),
        sync_status="pending",
    )
    if latitude is not None and longitude is not None:
        update_user_coordinates(user_id, latitude, longitude)
    return user_id


def login_user(username, password):
    user = get_user_by_username(username)
    if not user or not _verify_password(password, user.get("password", "")):
        return None

    if user.get("password") and not user["password"].startswith("pbkdf2_sha256$"):
        upgraded_password = _hash_password(password)
        update_user_password(user["id"], upgraded_password)
        user["password"] = upgraded_password
    return user


def get_user_profile(user_id):
    return get_user_by_id(user_id)


def list_users():
    return get_users()


def ensure_admin_account():
    existing_admin = get_user_by_username(DEFAULT_ADMIN_USERNAME)
    if existing_admin:
        return existing_admin

    admin_id = create_user(
        username=DEFAULT_ADMIN_USERNAME,
        password=_hash_password(DEFAULT_ADMIN_PASSWORD),
        role="admin",
        first_name="Pigilan",
        last_name="Admin",
        barangay="System",
        municipality="System",
        province="System",
        address="System",
        client_record_id="system-admin-account",
        sync_status="synced",
    )
    return get_user_by_id(admin_id)


def edit_user_profile(
    user_id,
    first_name,
    last_name,
    barangay,
    municipality,
    province,
    address=None,
    latitude=None,
    longitude=None,
):
    cleaned_address = _clean_address_value(address)
    latitude, longitude = _normalize_coordinates(latitude, longitude)
    if latitude is None or longitude is None:
        latitude, longitude = get_coordinates_for_address(
            cleaned_address,
            exclude_user_id=user_id,
        )
    update_user_profile(
        user_id=user_id,
        first_name=first_name,
        last_name=last_name,
        barangay=barangay,
        municipality=municipality,
        province=province,
        address=cleaned_address,
        latitude=latitude,
        longitude=longitude,
    )
    return get_user_by_id(user_id)


def calculate_assessment(symptoms, ml_percentage):
    normalized_symptoms = [
        SYMPTOM_ALIASES.get(symptom, symptom)
        for symptom in symptoms
    ]
    normalized_symptoms = [symptom for symptom in normalized_symptoms if symptom]

    checklist_score = sum(SYMPTOM_WEIGHTS.get(symptom, 0) for symptom in normalized_symptoms)
    reachable_symptoms = {
        SYMPTOM_ALIASES.get(symptom, symptom)
        for symptom in ACTIVE_ASSESSMENT_SYMPTOMS
    }
    reachable_symptoms.update(normalized_symptoms)
    reachable_symptoms.discard(None)
    max_symptom_score = sum(SYMPTOM_WEIGHTS.get(symptom, 0) for symptom in reachable_symptoms) or 1
    symptom_percentage = round((checklist_score / max_symptom_score) * 100, 2)
    total_percentage = round((symptom_percentage * 0.6) + (float(ml_percentage) * 0.4), 2)

    if total_percentage >= 75:
        risk_level = "HIGH RISK"
        recommendation = (
            "Isolate the pig immediately, stop pig movement, disinfect tools, "
            "and contact the Office of the City Veterinarian or the nearest veterinary clinic."
        )
    elif total_percentage >= 45:
        risk_level = "MODERATE RISK"
        recommendation = (
            "Watch the pig closely, separate any sick pigs, improve farm cleanliness, "
            "and prepare to contact a veterinarian if more signs appear."
        )
    else:
        risk_level = "LOW RISK"
        recommendation = "Keep watching the pig and continue good farm cleanliness."

    return {
        "checklist_score": checklist_score,
        "symptom_percentage": symptom_percentage,
        "ml_percentage": float(ml_percentage),
        "total_percentage": total_percentage,
        "risk_level": risk_level,
        "recommendation": recommendation,
    }


def distance_km(lat1, lon1, lat2, lon2):
    earth_radius_km = 6371
    dlat = radians(lat2 - lat1)
    dlon = radians(lon2 - lon1)
    a = (
        sin(dlat / 2) ** 2
        + cos(radians(lat1)) * cos(radians(lat2)) * sin(dlon / 2) ** 2
    )
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    return earth_radius_km * c


def _to_portable_media_path(file_path):
    try:
        return Path(file_path).resolve().relative_to(PROJECT_ROOT).as_posix()
    except Exception:
        return str(file_path)


def resolve_media_path(path_value):
    if not path_value:
        return None

    raw_value = str(path_value).strip()
    if not raw_value:
        return None

    raw_path = Path(raw_value)
    candidate_paths = []

    if raw_path.is_absolute():
        candidate_paths.append(raw_path)
        candidate_paths.append(UPLOADS_DIR / raw_path.name)
    else:
        candidate_paths.append(PROJECT_ROOT / raw_path)
        candidate_paths.append(UPLOADS_DIR / raw_path.name)

    seen = set()
    for candidate in candidate_paths:
        normalized_candidate = str(candidate)
        if normalized_candidate in seen:
            continue
        seen.add(normalized_candidate)
        if candidate.exists():
            return str(candidate)

    return None


def _hydrate_case_media_paths(case_details):
    hydrated_case = dict(case_details)
    hydrated_case["image_path"] = resolve_media_path(case_details.get("image_path"))
    return hydrated_case


def save_case_image(case_id, uploaded_file):
    if uploaded_file is None:
        return None

    safe_name = Path(uploaded_file.name).name
    file_path = UPLOADS_DIR / f"case_{case_id}_{safe_name}"
    file_path.write_bytes(uploaded_file.getbuffer())
    stored_path = _to_portable_media_path(file_path)
    create_case_image(case_id, stored_path)
    return stored_path


def _safe_report_name(case_name):
    cleaned = "".join(
        character if character.isalnum() or character in {"-", "_"} else "_"
        for character in str(case_name or "asf_case_report").strip().lower()
    )
    return cleaned.strip("_") or "asf_case_report"


def build_case_report_pdf(case_details, user_profile):
    resolved_image_path = resolve_media_path(case_details.get("image_path"))
    symptoms = case_details.get("symptoms") or "No symptoms selected"
    notes = case_details.get("remarks") or "No notes provided."
    image_note = (
        f"Attached photo saved at: {resolved_image_path}"
        if resolved_image_path
        else "No pig photo saved for this case."
    )
    map_point = (
        f"{case_details['latitude']}, {case_details['longitude']}"
        if case_details.get("latitude") is not None and case_details.get("longitude") is not None
        else "No case map point saved."
    )
    owner_name = (
        f"{user_profile.get('first_name', '')} {user_profile.get('last_name', '')}".strip()
        or user_profile.get("username", "Unknown user")
    )
    owner_address = _format_address_record(user_profile)

    sections = [
        (
            "Case Summary",
            [
                f"Case Number: {case_details['id']}",
                f"Case Title: {case_details.get('case_name') or 'ASF Assessment Case'}",
                f"Date Saved: {case_details.get('created_at', '')}",
                f"Case Status: {case_details.get('case_status', '')}",
                f"Farmer: {owner_name}",
            ],
        ),
        (
            "Farmer Details",
            [
                f"Username: {user_profile.get('username', '')}",
                f"Address: {owner_address}",
                f"Saved Farm Point: {user_profile.get('latitude', 'No point saved')}, {user_profile.get('longitude', '')}".rstrip(", "),
            ],
        ),
        (
            "ASF Check Result",
            [
                f"Risk Result: {case_details.get('risk_level', '')}",
                f"ASF Detection Result: {case_details.get('total_percentage', 0)}%",
                f"ASF Photo Result: {case_details.get('ml_percentage', 0)}%",
                f"Number of Pigs Checked: {case_details.get('pig_count', 0)}",
                f"Signs Seen: {symptoms}",
            ],
        ),
        (
            "What To Do",
            [
                case_details.get("recommendation", ""),
                f"Notes: {notes}",
            ],
        ),
        (
            "Location And Photo",
            [
                f"Case Map Point: {map_point}",
                image_note,
            ],
        ),
    ]
    return build_simple_pdf(
        "Pigilan ASF Case Report",
        sections,
        image_path=resolved_image_path,
    )


def save_case_report_export(case_details, user_profile, pdf_bytes, shared_to="Downloaded PDF"):
    resolved_image_path = resolve_media_path(case_details.get("image_path"))
    report_name = _safe_report_name(case_details.get("case_name"))
    file_path = EXPORTS_DIR / f"case_{case_details['id']}_{report_name}.pdf"
    file_path.write_bytes(pdf_bytes)
    share_id = create_case_share(
        case_id=case_details["id"],
        pdf_file_path=str(file_path),
        image_file_path=resolved_image_path,
        shared_to=shared_to,
    )
    return {
        "share_id": share_id,
        "pdf_file_path": str(file_path),
    }


def submit_assessment(
    user_id,
    pig_count,
    symptoms,
    ml_percentage,
    uploaded_file=None,
    case_latitude=None,
    case_longitude=None,
    case_name=None,
    remarks=None,
):
    case_latitude, case_longitude = _normalize_coordinates(case_latitude, case_longitude)
    validation_errors = _validate_case_inputs(case_name, pig_count, case_latitude, case_longitude)
    if validation_errors:
        raise ValueError("\n".join(validation_errors))
    result = calculate_assessment(symptoms, ml_percentage)
    symptoms_text = ", ".join(symptoms) if symptoms else "No symptoms selected"

    assessment_id = create_risk_assessment(
        user_id=user_id,
        pig_count=pig_count,
        symptoms=symptoms_text,
        checklist_score=result["checklist_score"],
        ml_percentage=result["ml_percentage"],
        total_percentage=result["total_percentage"],
        risk_level=result["risk_level"],
        recommendation=result["recommendation"],
        client_record_id=str(uuid.uuid4()),
        sync_status="pending",
    )

    case_status = "Open" if result["risk_level"] != "LOW RISK" else "Monitoring"
    case_id = create_case(
        user_id=user_id,
        assessment_id=assessment_id,
        case_status=case_status,
        case_name=case_name,
        remarks=remarks,
        latitude=case_latitude,
        longitude=case_longitude,
        client_record_id=str(uuid.uuid4()),
        sync_status="pending",
    )
    image_path = save_case_image(case_id, uploaded_file)

    alert_id = None
    user = get_user_by_id(user_id)
    if (
        user
        and case_latitude is not None
        and case_longitude is not None
        and result["risk_level"] in {"HIGH RISK", "MODERATE RISK"}
    ):
        alert_id = create_alert(
            case_id=case_id,
            barangay=user["barangay"],
            municipality=user["municipality"],
            province=user["province"],
            alert_message=f"{result['risk_level']} ASF case detected nearby.",
            alert_level=result["risk_level"],
        )

        for nearby_user in get_users():
            if nearby_user["id"] == user_id:
                create_notification(nearby_user["id"], alert_id)
                continue

            user_lat = nearby_user.get("latitude")
            user_lon = nearby_user.get("longitude")
            if user_lat is None or user_lon is None:
                continue

            if distance_km(case_latitude, case_longitude, user_lat, user_lon) <= 10:
                create_notification(nearby_user["id"], alert_id)

    result["assessment_id"] = assessment_id
    result["case_id"] = case_id
    result["image_path"] = image_path
    result["alert_id"] = alert_id
    return result


def list_notifications(user_id):
    return get_notifications_for_user(user_id)


def mark_notification_as_read(notification_id):
    mark_notification_read(notification_id)


def mark_all_notifications_as_read(user_id):
    for notification in get_notifications_for_user(user_id):
        if not notification.get("is_read"):
            mark_notification_read(notification["id"])


def list_cases_for_user(user_id):
    return [_hydrate_case_media_paths(case) for case in get_cases_for_user(user_id)]


def list_case_markers():
    return get_all_cases_with_coordinates()


def edit_case(case_id, case_name, remarks, case_status):
    if not str(case_name or "").strip():
        raise ValueError("Please add a case title before saving the update.")
    update_case_details(
        case_id=case_id,
        case_name=case_name,
        remarks=remarks,
        case_status=case_status,
    )


def calculate_biosecurity_state(checked_count, unchecked_count):
    total_items = checked_count + unchecked_count
    if total_items == 0:
        return {
            "protection_label": "No checklist yet",
            "warning_message": "No biosecurity check has been saved yet.",
        }

    ratio = checked_count / total_items

    if ratio < 0.5:
        return {
            "protection_label": "Low protection from ASF",
            "warning_message": "At risk of ASF spreading or contamination.",
        }
    if ratio < 0.75:
        return {
            "protection_label": "Moderate protection from ASF",
            "warning_message": "Moderate protection from ASF.",
        }
    return {
        "protection_label": "High protection from ASF",
        "warning_message": "High protection from ASF.",
    }


def save_biosecurity_check(user_id, checklist, remarks):
    checked_count = sum(1 for value in checklist.values() if value)
    unchecked_count = sum(1 for value in checklist.values() if not value)
    score = checked_count
    record_id = create_biosecurity_check(
        user_id=user_id,
        checklist=checklist,
        checked_count=checked_count,
        unchecked_count=unchecked_count,
        checklist_score=score,
        remarks=remarks,
        client_record_id=str(uuid.uuid4()),
        sync_status="pending",
    )
    state = calculate_biosecurity_state(checked_count, unchecked_count)
    state["record_id"] = record_id
    state["checked_count"] = checked_count
    state["unchecked_count"] = unchecked_count
    return state


def get_latest_biosecurity_state(user_id):
    checks = get_biosecurity_checks_for_user(user_id)
    if not checks:
        return {
            "protection_label": "No checklist yet",
            "warning_message": "No biosecurity check has been saved yet.",
            "checked_count": 0,
            "unchecked_count": 0,
            "latest_check": None,
        }

    latest = checks[0]
    state = calculate_biosecurity_state(
        latest.get("checked_count", 0),
        latest.get("unchecked_count", 0),
    )
    state["checked_count"] = latest.get("checked_count", 0)
    state["unchecked_count"] = latest.get("unchecked_count", 0)
    state["latest_check"] = latest
    return state


def list_biosecurity_checks(user_id):
    return get_biosecurity_checks_for_user(user_id)


def get_database_backup():
    return {
        "file_name": "pigilan_backup.db",
        "bytes": DB_FILE_PATH.read_bytes(),
    }


def get_admin_dashboard_data():
    users = get_users()
    farmers = [user for user in users if user.get("role", "farmer") != "admin"]
    recent_cases = get_admin_case_overview(limit=20)
    recent_alerts = get_alerts(limit=20)

    high_risk_count = sum(1 for case in recent_cases if case.get("risk_level") == "HIGH RISK")
    moderate_risk_count = sum(1 for case in recent_cases if case.get("risk_level") == "MODERATE RISK")
    low_risk_count = sum(1 for case in recent_cases if case.get("risk_level") == "LOW RISK")
    unread_alerts = 0
    for farmer in farmers:
        unread_alerts += sum(
            1 for item in get_notifications_for_user(farmer["id"]) if not item.get("is_read")
        )

    return {
        "total_farmers": len(farmers),
        "recent_case_count": len(recent_cases),
        "high_risk_count": high_risk_count,
        "moderate_risk_count": moderate_risk_count,
        "low_risk_count": low_risk_count,
        "unread_alerts": unread_alerts,
        "recent_cases": recent_cases,
        "recent_alerts": recent_alerts,
        "users": farmers,
        "admin_credentials": {
            "username": DEFAULT_ADMIN_USERNAME,
            "password": DEFAULT_ADMIN_PASSWORD,
        },
    }


def get_sync_status_summary(user_id=None):
    counts = get_pending_sync_counts(user_id=user_id)
    pending_total = counts["users"] + counts["cases"] + counts["biosecurity_checks"]
    return {
        "pending_total": pending_total,
        "counts": counts,
        "status_label": "Pending local changes" if pending_total else "Everything exported",
    }


def _build_sync_payload(user_id):
    user = get_user_by_id(user_id)
    if not user:
        raise ValueError("User account not found.")

    case_records = []
    all_cases = get_cases()
    cases_for_user = {case["id"]: case for case in all_cases if case["user_id"] == user_id}
    detailed_cases = list_cases_for_user(user_id)

    for detailed_case in detailed_cases:
        base_case = cases_for_user.get(detailed_case["id"], {})
        image_payload = None
        image_path = resolve_media_path(detailed_case.get("image_path"))
        if image_path:
            image_file = Path(image_path)
            if image_file.exists():
                image_payload = {
                    "file_name": image_file.name,
                    "content_base64": base64.b64encode(image_file.read_bytes()).decode("ascii"),
                }

        case_records.append(
            {
                "case": {
                    "id": base_case.get("id"),
                    "client_record_id": base_case.get("client_record_id"),
                    "case_name": base_case.get("case_name"),
                    "remarks": base_case.get("remarks"),
                    "case_status": base_case.get("case_status"),
                    "latitude": base_case.get("latitude"),
                    "longitude": base_case.get("longitude"),
                    "created_at": base_case.get("created_at"),
                    "updated_at": base_case.get("updated_at"),
                    "sync_status": base_case.get("sync_status", "pending"),
                },
                "assessment": {
                    "pig_count": detailed_case.get("pig_count"),
                    "symptoms": detailed_case.get("symptoms"),
                    "checklist_score": detailed_case.get("checklist_score"),
                    "ml_percentage": detailed_case.get("ml_percentage"),
                    "total_percentage": detailed_case.get("total_percentage"),
                    "risk_level": detailed_case.get("risk_level"),
                    "recommendation": detailed_case.get("recommendation"),
                },
                "image": image_payload,
            }
        )

    biosecurity_checks = get_biosecurity_checks_for_user(user_id)
    sync_package = {
        "app": "Pigilan",
        "format_version": 1,
        "generated_at": datetime.now().isoformat(),
        "user": {
            "username": user.get("username"),
            "first_name": user.get("first_name"),
            "last_name": user.get("last_name"),
            "barangay": user.get("barangay"),
            "municipality": user.get("municipality"),
            "province": user.get("province"),
            "address": _clean_address_value(user.get("address")),
            "latitude": user.get("latitude"),
            "longitude": user.get("longitude"),
            "client_record_id": user.get("client_record_id"),
            "sync_status": user.get("sync_status", "pending"),
            "updated_at": user.get("updated_at"),
        },
        "cases": case_records,
        "biosecurity_checks": [
            {
                "id": item.get("id"),
                "client_record_id": item.get("client_record_id"),
                "checklist": item.get("checklist", {}),
                "checked_count": item.get("checked_count"),
                "unchecked_count": item.get("unchecked_count"),
                "checklist_score": item.get("checklist_score"),
                "remarks": item.get("remarks"),
                "created_at": item.get("created_at"),
                "updated_at": item.get("updated_at"),
                "sync_status": item.get("sync_status", "pending"),
            }
            for item in biosecurity_checks
        ],
        "sync_summary": get_sync_status_summary(user_id=user_id),
    }
    return sync_package


def import_sync_payload(payload):
    if payload.get("app") != "Pigilan":
        raise ValueError("This payload is not a Pigilan sync package.")
    if payload.get("format_version") != 1:
        raise ValueError("Unsupported sync package version.")

    user_payload = payload.get("user") or {}
    username = str(user_payload.get("username") or "").strip()
    if not username:
        raise ValueError("The sync package is missing the farmer username.")

    client_record_id = user_payload.get("client_record_id") or f"imported-user-{username}"
    imported_user = get_user_by_client_record_id(client_record_id) or get_user_by_username(username)

    if imported_user is None:
        imported_user_id = create_user(
            username=username,
            password=_hash_password(f"imported::{username}"),
            first_name=user_payload.get("first_name") or "Imported",
            last_name=user_payload.get("last_name") or "Farmer",
            barangay=user_payload.get("barangay") or "Unknown",
            municipality=user_payload.get("municipality") or "Unknown",
            province=user_payload.get("province") or "Unknown",
            address=(
                _clean_address_value(user_payload.get("address"))
                or _format_address_record(user_payload, fallback=None)
            ),
            role="farmer",
            client_record_id=client_record_id,
            sync_status="synced",
        )
        imported_user = get_user_by_id(imported_user_id)
        created_user = 1
    else:
        created_user = 0

    update_imported_user_profile(
        user_id=imported_user["id"],
        first_name=user_payload.get("first_name") or imported_user.get("first_name") or "Imported",
        last_name=user_payload.get("last_name") or imported_user.get("last_name") or "Farmer",
        barangay=user_payload.get("barangay") or imported_user.get("barangay") or "Unknown",
        municipality=user_payload.get("municipality") or imported_user.get("municipality") or "Unknown",
        province=user_payload.get("province") or imported_user.get("province") or "Unknown",
        address=(
            _clean_address_value(user_payload.get("address"))
            or _clean_address_value(imported_user.get("address"))
            or _format_address_record(imported_user, fallback=None)
        ),
        latitude=user_payload.get("latitude"),
        longitude=user_payload.get("longitude"),
        client_record_id=client_record_id,
        updated_at=user_payload.get("updated_at"),
    )

    imported_cases = 0
    skipped_cases = 0
    imported_biosecurity = 0
    skipped_biosecurity = 0

    for case_record in payload.get("cases", []):
        case_payload = case_record.get("case") or {}
        assessment_payload = case_record.get("assessment") or {}
        case_client_record_id = case_payload.get("client_record_id")

        if case_client_record_id and get_case_by_client_record_id(case_client_record_id):
            skipped_cases += 1
            continue

        assessment_id = create_risk_assessment(
            user_id=imported_user["id"],
            pig_count=int(assessment_payload.get("pig_count") or 1),
            symptoms=assessment_payload.get("symptoms") or "No symptoms selected",
            checklist_score=int(assessment_payload.get("checklist_score") or 0),
            ml_percentage=float(assessment_payload.get("ml_percentage") or 0),
            total_percentage=float(assessment_payload.get("total_percentage") or 0),
            risk_level=assessment_payload.get("risk_level") or "LOW RISK",
            recommendation=assessment_payload.get("recommendation") or "",
            client_record_id=(
                f"{case_client_record_id}-assessment"
                if case_client_record_id
                else str(uuid.uuid4())
            ),
            sync_status="synced",
        )

        case_id = create_case(
            user_id=imported_user["id"],
            assessment_id=assessment_id,
            case_status=case_payload.get("case_status") or "Open",
            case_name=case_payload.get("case_name"),
            remarks=case_payload.get("remarks"),
            latitude=case_payload.get("latitude"),
            longitude=case_payload.get("longitude"),
            client_record_id=case_client_record_id or str(uuid.uuid4()),
            sync_status="synced",
        )

        image_payload = case_record.get("image")
        if image_payload and image_payload.get("content_base64"):
            file_name = Path(image_payload.get("file_name") or "imported_case_image.jpg").name
            image_bytes = base64.b64decode(image_payload["content_base64"])
            image_path = UPLOADS_DIR / f"case_{case_id}_{file_name}"
            image_path.write_bytes(image_bytes)
            create_case_image(case_id, _to_portable_media_path(image_path))

        risk_level = assessment_payload.get("risk_level")
        if risk_level in {"HIGH RISK", "MODERATE RISK"}:
            create_alert(
                case_id=case_id,
                barangay=imported_user.get("barangay") or "Unknown",
                municipality=imported_user.get("municipality") or "Unknown",
                province=imported_user.get("province") or "Unknown",
                alert_message=f"{risk_level} ASF case imported from sync package.",
                alert_level=risk_level,
            )

        imported_cases += 1

    for biosecurity_payload in payload.get("biosecurity_checks", []):
        bio_client_record_id = biosecurity_payload.get("client_record_id")
        if bio_client_record_id and get_biosecurity_check_by_client_record_id(bio_client_record_id):
            skipped_biosecurity += 1
            continue

        create_biosecurity_check(
            user_id=imported_user["id"],
            checklist=biosecurity_payload.get("checklist") or {},
            checked_count=int(biosecurity_payload.get("checked_count") or 0),
            unchecked_count=int(biosecurity_payload.get("unchecked_count") or 0),
            checklist_score=int(biosecurity_payload.get("checklist_score") or 0),
            remarks=biosecurity_payload.get("remarks") or "",
            client_record_id=bio_client_record_id or str(uuid.uuid4()),
            sync_status="synced",
        )
        imported_biosecurity += 1

    return {
        "username": username,
        "created_user": created_user,
        "imported_cases": imported_cases,
        "skipped_cases": skipped_cases,
        "imported_biosecurity": imported_biosecurity,
        "skipped_biosecurity": skipped_biosecurity,
    }


def _is_local_sync_url(base_url):
    normalized_url = base_url if "://" in base_url else f"http://{base_url}"
    hostname = urlparse(normalized_url).hostname
    return hostname in {"127.0.0.1", "localhost"}


def _extract_sync_error_detail(response):
    if response is None:
        return "The sync server did not return a response."

    try:
        payload = response.json()
    except ValueError:
        text = response.text.strip()
        return text or f"{response.status_code} {response.reason}"

    if isinstance(payload, dict):
        detail = payload.get("detail") or payload.get("message")
        if detail:
            return str(detail)

    return str(payload)


def _mark_sync_complete(user_id):
    mark_user_synced(user_id)
    mark_cases_synced_for_user(user_id)
    mark_biosecurity_checks_synced_for_user(user_id)


def sync_with_server(user_id, server_url=None, timeout_seconds=15):
    payload = _build_sync_payload(user_id)
    base_url = (server_url or DEFAULT_SYNC_SERVER_URL).rstrip("/")
    allow_local_fallback = _is_local_sync_url(base_url)

    try:
        response = requests.post(
            f"{base_url}/sync/push",
            json=payload,
            timeout=timeout_seconds,
        )
        response.raise_for_status()
        result = response.json()
    except requests.HTTPError as exc:
        error_detail = _extract_sync_error_detail(exc.response)
        if allow_local_fallback and exc.response is not None and exc.response.status_code >= 500:
            try:
                result = import_sync_payload(payload)
            except Exception as fallback_exc:
                raise ValueError(f"Could not sync right now: {error_detail}") from fallback_exc
        else:
            raise ValueError(f"Could not sync right now: {error_detail}") from exc
    except requests.RequestException as exc:
        if allow_local_fallback:
            try:
                result = import_sync_payload(payload)
            except Exception as fallback_exc:
                raise ValueError(f"Could not sync right now: {fallback_exc}") from fallback_exc
        else:
            raise ValueError(f"Could not sync right now: {exc}") from exc

    _mark_sync_complete(user_id)
    return result


ensure_admin_account()
