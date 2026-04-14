from datetime import datetime
from html import escape

import streamlit as st

try:
    import pandas as pd
except Exception:  # pragma: no cover - fallback if pandas is unavailable locally
    pd = None

from backend import (
    build_case_report_pdf,
    distance_km,
    edit_case,
    list_case_markers,
    list_cases_for_user,
    list_notifications,
    mark_all_notifications_as_read,
    mark_notification_as_read,
    save_case_report_export,
)


def inject_reports_styles():
    st.markdown(
        """
        <style>
        .reports-nearby-shell {
            display: grid;
            gap: 1rem;
        }

        .reports-nearby-header {
            display: grid;
            gap: 0.22rem;
        }

        .reports-nearby-kicker {
            margin: 0;
            color: #7a7064;
            font-size: 0.78rem;
            font-weight: 700;
            letter-spacing: 0.08em;
            text-transform: uppercase;
        }

        .reports-nearby-title {
            margin: 0;
            color: #4b4137;
            font-size: clamp(1.35rem, 3vw, 1.85rem);
            line-height: 1.08;
            letter-spacing: -0.03em;
            font-weight: 800;
        }

        .reports-nearby-copy {
            margin: 0;
            color: #74695d;
            font-size: 0.96rem;
            line-height: 1.6;
        }

        .reports-nearby-summary-grid {
            display: grid;
            grid-template-columns: repeat(4, minmax(0, 1fr));
            gap: 0.85rem;
        }

        .reports-nearby-summary-card {
            padding: 0.95rem 1rem;
            border-radius: 18px;
            background: rgba(255, 251, 246, 0.92);
            border: 1px solid rgba(216, 200, 182, 0.95);
            box-shadow: 0 10px 24px rgba(83, 69, 56, 0.05);
        }

        .reports-nearby-summary-label {
            margin: 0;
            color: #7a7064;
            font-size: 0.8rem;
            line-height: 1.35;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 0.04em;
        }

        .reports-nearby-summary-value {
            margin: 0.32rem 0 0;
            color: #4b4137;
            font-size: clamp(1.45rem, 3vw, 2rem);
            line-height: 1.02;
            font-weight: 800;
        }

        .reports-nearby-summary-value--muted {
            color: #8a7f73;
        }

        .reports-nearby-panel-title {
            margin: 0 0 0.75rem;
            color: #4b4137;
            font-size: 1rem;
            line-height: 1.3;
            font-weight: 800;
        }

        .reports-nearby-panel-copy {
            margin: 0.7rem 0 0;
            color: #74695d;
            font-size: 0.9rem;
            line-height: 1.5;
        }

        .reports-nearby-panel-copy strong {
            color: #4b4137;
        }

        .reports-nearby-list {
            display: grid;
            gap: 0.75rem;
        }

        .reports-nearby-item {
            padding: 0.95rem 1rem;
            border-radius: 18px;
            border: 1px solid rgba(216, 200, 182, 0.95);
            background: rgba(255, 251, 246, 0.92);
            box-shadow: 0 10px 24px rgba(83, 69, 56, 0.05);
        }

        .reports-nearby-item--high {
            border-left: 5px solid #c95b51;
        }

        .reports-nearby-item--moderate {
            border-left: 5px solid #d59b41;
        }

        .reports-nearby-item--low {
            border-left: 5px solid #7d8f6a;
        }

        .reports-nearby-item-top {
            display: flex;
            align-items: center;
            justify-content: space-between;
            gap: 0.75rem;
            flex-wrap: wrap;
        }

        .reports-nearby-item-title {
            margin: 0;
            color: #4b4137;
            font-size: 1rem;
            line-height: 1.35;
            font-weight: 800;
        }

        .reports-nearby-risk-chip {
            display: inline-flex;
            align-items: center;
            justify-content: center;
            padding: 0.3rem 0.7rem;
            border-radius: 999px;
            font-size: 0.76rem;
            line-height: 1.2;
            font-weight: 800;
            letter-spacing: 0.03em;
            text-transform: uppercase;
        }

        .reports-nearby-risk-chip--high {
            background: rgba(247, 223, 223, 0.96);
            color: #9d433a;
        }

        .reports-nearby-risk-chip--moderate {
            background: rgba(252, 238, 208, 0.96);
            color: #946a2c;
        }

        .reports-nearby-risk-chip--low {
            background: rgba(229, 240, 224, 0.96);
            color: #53724f;
        }

        .reports-nearby-item-copy {
            margin: 0.55rem 0 0;
            color: #6f6458;
            font-size: 0.92rem;
            line-height: 1.55;
        }

        .reports-nearby-item-meta {
            display: flex;
            gap: 0.6rem;
            flex-wrap: wrap;
            margin-top: 0.75rem;
        }

        .reports-nearby-meta-chip {
            display: inline-flex;
            align-items: center;
            justify-content: center;
            padding: 0.28rem 0.65rem;
            border-radius: 999px;
            background: rgba(244, 237, 228, 0.96);
            color: #6d6256;
            font-size: 0.78rem;
            line-height: 1.2;
            font-weight: 700;
        }

        .reports-nearby-empty {
            padding: 1rem 1.05rem;
            border-radius: 18px;
            border: 1px dashed rgba(194, 177, 159, 0.9);
            background: rgba(255, 252, 248, 0.92);
            color: #786d61;
            font-size: 0.94rem;
            line-height: 1.55;
        }

        @media (max-width: 900px) {
            .reports-nearby-summary-grid {
                grid-template-columns: repeat(2, minmax(0, 1fr));
            }
        }

        @media (max-width: 520px) {
            .reports-nearby-summary-grid {
                grid-template-columns: minmax(0, 1fr);
            }
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def safe_float(value):
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def get_reference_location(user, user_cases):
    user_lat = safe_float(user.get("latitude"))
    user_lon = safe_float(user.get("longitude"))
    if user_lat is not None and user_lon is not None:
        return user_lat, user_lon, "saved farm location"

    for case in user_cases:
        case_lat = safe_float(case.get("latitude"))
        case_lon = safe_float(case.get("longitude"))
        if case_lat is not None and case_lon is not None:
            return case_lat, case_lon, "latest saved report location"

    return None, None, None


def collect_nearby_cases(user, user_cases):
    reference_lat, reference_lon, reference_label = get_reference_location(user, user_cases)
    if reference_lat is None or reference_lon is None:
        return [], reference_lat, reference_lon, reference_label

    nearby_cases = []
    for case in list_case_markers():
        if case.get("user_id") == user.get("id"):
            continue

        case_lat = safe_float(case.get("latitude"))
        case_lon = safe_float(case.get("longitude"))
        if case_lat is None or case_lon is None:
            continue

        distance = distance_km(reference_lat, reference_lon, case_lat, case_lon)
        if distance <= 10:
            case_record = dict(case)
            case_record["distance_km"] = round(distance, 1)
            nearby_cases.append(case_record)

    nearby_cases.sort(key=lambda item: (item["distance_km"], -int(item["id"])))
    return nearby_cases, reference_lat, reference_lon, reference_label


def get_reporter_name(case):
    full_name = f"{str(case.get('first_name') or '').strip()} {str(case.get('last_name') or '').strip()}".strip()
    return full_name or "Local farmer"


def build_nearby_case_map_points(reference_lat, reference_lon, nearby_cases):
    map_points = [{"latitude": reference_lat, "longitude": reference_lon}]
    for case in nearby_cases:
        case_lat = safe_float(case.get("latitude"))
        case_lon = safe_float(case.get("longitude"))
        if case_lat is None or case_lon is None:
            continue
        map_points.append({"latitude": case_lat, "longitude": case_lon})
    return map_points


def render_nearby_cases_map(reference_lat, reference_lon, nearby_cases):
    if pd is None:
        st.markdown(
            "<div class='reports-nearby-empty'>Map preview is unavailable because the local pandas package is missing.</div>",
            unsafe_allow_html=True,
        )
        return

    nearby_map_points = build_nearby_case_map_points(
        reference_lat,
        reference_lon,
        nearby_cases,
    )
    st.map(
        pd.DataFrame(nearby_map_points),
        latitude="latitude",
        longitude="longitude",
        zoom=11,
        use_container_width=True,
    )


def format_display_date(value):
    raw_value = str(value or "").strip()
    if not raw_value:
        return "Recent"
    raw_value = raw_value.replace("Z", "+00:00")
    try:
        return datetime.fromisoformat(raw_value).strftime("%b %d, %Y")
    except ValueError:
        return raw_value.split(" ")[0].split("T")[0]


def get_nearby_case_card_class(risk_level):
    normalized = str(risk_level or "LOW RISK").strip().upper()
    if normalized == "HIGH RISK":
        return "reports-nearby-item reports-nearby-item--high"
    if normalized == "MODERATE RISK":
        return "reports-nearby-item reports-nearby-item--moderate"
    return "reports-nearby-item reports-nearby-item--low"


def get_nearby_case_chip_class(risk_level):
    normalized = str(risk_level or "LOW RISK").strip().upper()
    if normalized == "HIGH RISK":
        return "reports-nearby-risk-chip reports-nearby-risk-chip--high"
    if normalized == "MODERATE RISK":
        return "reports-nearby-risk-chip reports-nearby-risk-chip--moderate"
    return "reports-nearby-risk-chip reports-nearby-risk-chip--low"


def build_nearby_summary_markup(nearby_cases):
    high_risk = sum(1 for case in nearby_cases if case.get("risk_level") == "HIGH RISK")
    moderate_risk = sum(1 for case in nearby_cases if case.get("risk_level") == "MODERATE RISK")
    closest_label = f"{nearby_cases[0]['distance_km']:.1f} km" if nearby_cases else "No nearby case"
    summary_items = [
        ("Cases within 10 km", str(len(nearby_cases)), False),
        ("High Risk", str(high_risk), False),
        ("Moderate Risk", str(moderate_risk), False),
        ("Closest Case", closest_label, not nearby_cases),
    ]

    cards = []
    for label, value, is_muted in summary_items:
        value_class = "reports-nearby-summary-value reports-nearby-summary-value--muted" if is_muted else "reports-nearby-summary-value"
        cards.append(
            (
                "<div class='reports-nearby-summary-card'>"
                f"<p class='reports-nearby-summary-label'>{escape(label)}</p>"
                f"<p class='{value_class}'>{escape(value)}</p>"
                "</div>"
            )
        )
    return "".join(cards)


def build_nearby_case_cards_markup(nearby_cases):
    if not nearby_cases:
        return (
            "<div class='reports-nearby-empty'>"
            "No nearby cases are within 10 km right now. Keep saving reports to monitor activity around your farm."
            "</div>"
        )

    items = []
    for case in nearby_cases[:5]:
        risk_level = str(case.get("risk_level") or "LOW RISK").strip().upper()
        reporter_name = get_reporter_name(case)
        distance_label = f"{case['distance_km']:.1f} km away"
        items.append(
            (
                f"<article class='{get_nearby_case_card_class(risk_level)}'>"
                "<div class='reports-nearby-item-top'>"
                f"<p class='reports-nearby-item-title'>Case #{escape(str(case.get('id', '')))} &bull; {escape(reporter_name)}</p>"
                f"<span class='{get_nearby_case_chip_class(risk_level)}'>{escape(risk_level)}</span>"
                "</div>"
                f"<p class='reports-nearby-item-copy'>Reported by {escape(reporter_name)} and detected within your 10 km alert radius.</p>"
                "<div class='reports-nearby-item-meta'>"
                f"<span class='reports-nearby-meta-chip'>{escape(distance_label)}</span>"
                f"<span class='reports-nearby-meta-chip'>{escape(format_display_date(case.get('created_at')))}</span>"
                "</div>"
                "</article>"
            )
        )
    return "".join(items)


inject_reports_styles()
st.title("My Reports")

if "user" not in st.session_state or not st.session_state.user:
    st.warning("Please sign in first to view your cases and alerts.")
    st.stop()


user = st.session_state.user
cases = list_cases_for_user(user["id"])
notifications = list_notifications(user["id"])
nearby_cases, nearby_reference_lat, nearby_reference_lon, nearby_reference_label = collect_nearby_cases(user, cases)

st.subheader("Alerts")
if notifications:
    st.markdown("##### System Alerts")
    unread_count = sum(1 for item in notifications if not item.get("is_read"))
    st.caption(f"Unread alerts: {unread_count}")
    if unread_count and st.button("Mark All Alerts as Read"):
        mark_all_notifications_as_read(user["id"])
        st.rerun()
    for item in notifications:
        label = "Unread" if not item.get("is_read") else "Read"
        cols = st.columns([5, 1])
        with cols[0]:
            if item["alert_level"] == "HIGH RISK":
                st.warning(f"[{label}] {item['alert_message']}")
            else:
                st.info(f"[{label}] {item['alert_message']}")
        with cols[1]:
            if not item.get("is_read") and st.button("Read", key=f"read_alert_{item['id']}"):
                mark_notification_as_read(item["id"])
                st.rerun()
else:
    st.caption("No system alerts yet.")

with st.container(border=True):
    st.markdown(
        """
        <div class="reports-nearby-shell">
            <div class="reports-nearby-header">
                <p class="reports-nearby-kicker">Nearby Cases</p>
                <h3 class="reports-nearby-title">Local Case Activity Around Your Farm</h3>
                <p class="reports-nearby-copy">Track nearby ASF reports within 10 km using your saved farm point or your latest report location.</p>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if nearby_reference_label is None:
        st.markdown(
            "<div class='reports-nearby-empty'>Nearby cases will appear here after you save a report with location data.</div>",
            unsafe_allow_html=True,
        )
    else:
        st.markdown(
            f"<div class='reports-nearby-summary-grid'>{build_nearby_summary_markup(nearby_cases)}</div>",
            unsafe_allow_html=True,
        )

        map_col, list_col = st.columns([1.15, 1], gap="large")
        with map_col:
            with st.container(border=True):
                st.markdown("<p class='reports-nearby-panel-title'>Map View</p>", unsafe_allow_html=True)
                if nearby_reference_lat is not None and nearby_reference_lon is not None:
                    render_nearby_cases_map(
                        nearby_reference_lat,
                        nearby_reference_lon,
                        nearby_cases,
                    )
                    st.markdown(
                        f"<p class='reports-nearby-panel-copy'><strong>Reference:</strong> Based on your {escape(nearby_reference_label)}.</p>",
                        unsafe_allow_html=True,
                    )
                    st.markdown(
                        f"<p class='reports-nearby-panel-copy'><strong>Showing:</strong> {len(nearby_cases)} nearby case(s) within 10 km.</p>",
                        unsafe_allow_html=True,
                    )
                else:
                    st.markdown(
                        "<div class='reports-nearby-empty'>Map preview is unavailable right now.</div>",
                        unsafe_allow_html=True,
                    )

        with list_col:
            with st.container(border=True):
                st.markdown("<p class='reports-nearby-panel-title'>Recent Nearby Reports</p>", unsafe_allow_html=True)
                st.markdown(
                    f"<div class='reports-nearby-list'>{build_nearby_case_cards_markup(nearby_cases)}</div>",
                    unsafe_allow_html=True,
                )

st.subheader("My Cases")
if cases:
    filter_col1, filter_col2, filter_col3 = st.columns(3)
    with filter_col1:
        selected_risk = st.selectbox(
            "Filter by Risk",
            ["All", "HIGH RISK", "MODERATE RISK", "LOW RISK"],
        )
    with filter_col2:
        selected_status = st.selectbox(
            "Filter by Status",
            ["All", "Monitoring", "Open", "Being Checked", "Closed"],
        )
    with filter_col3:
        case_search = st.text_input("Search Case Title", placeholder="Type case title")

    filtered_cases = []
    for case in cases:
        title = case.get("case_name") or ""
        if selected_risk != "All" and case["risk_level"] != selected_risk:
            continue
        if selected_status != "All" and case["case_status"] != selected_status:
            continue
        if case_search.strip() and case_search.strip().lower() not in title.lower():
            continue
        filtered_cases.append(case)

    st.caption(f"Showing {len(filtered_cases)} case(s)")
    for case in filtered_cases:
        if case["risk_level"] == "HIGH RISK":
            risk_color = "red"
        elif case["risk_level"] == "MODERATE RISK":
            risk_color = "orange"
        else:
            risk_color = "green"

        with st.expander(f"Case #{case['id']} - {case['risk_level']} - {case['case_status']}"):
            st.markdown(
                f"<span style='color:{risk_color}; font-weight:600;'>Risk Result: {case['risk_level']}</span>",
                unsafe_allow_html=True,
            )
            if case.get("sync_status", "pending") != "synced":
                st.info("This case is saved locally and still waiting for manual sync/export.")
            st.write(f"Case Title: {case['case_name'] or 'Untitled Case'}")
            st.write(f"Date Saved: {case['created_at']}")
            st.write(f"Number of Pigs Checked: {case['pig_count']}")
            st.write(f"Signs Seen: {case['symptoms']}")
            st.write(f"Signs Seen Score: {case['checklist_score']}")
            st.write(f"ASF Photo Result: {case['ml_percentage']}%")
            st.write(f"Overall Risk Score: {case['total_percentage']}%")
            st.write(f"What to do: {case['recommendation']}")
            st.write(f"Notes: {case['remarks'] or 'No notes yet.'}")
            if case["latitude"] is not None and case["longitude"] is not None:
                st.write(f"Case Map Point: {case['latitude']}, {case['longitude']}")
            if case["image_path"]:
                st.image(case["image_path"], caption="Saved pig photo", use_container_width=True)

            pdf_bytes = build_case_report_pdf(case, user)
            pdf_file_name = f"pigilan_case_{case['id']}.pdf"
            downloaded = st.download_button(
                "Download PDF Case Report",
                data=pdf_bytes,
                file_name=pdf_file_name,
                mime="application/pdf",
                key=f"download_case_pdf_{case['id']}",
            )
            if downloaded:
                export_result = save_case_report_export(case, user, pdf_bytes)
                st.success(
                    f"PDF report saved for case #{case['id']}."
                )
                st.caption(f"Saved PDF: {export_result['pdf_file_path']}")

            edit_case_name = st.text_input(
                f"Edit Case Title #{case['id']}",
                value=case["case_name"] or "",
                key=f"case_name_{case['id']}",
            )
            edit_case_remarks = st.text_area(
                f"Edit Notes #{case['id']}",
                value=case["remarks"] or "",
                key=f"case_remarks_{case['id']}",
            )
            edit_case_status = st.selectbox(
                f"Edit Case Status #{case['id']}",
                ["Monitoring", "Open", "Being Checked", "Closed"],
                index=["Monitoring", "Open", "Being Checked", "Closed"].index(case["case_status"])
                if case["case_status"] in ["Monitoring", "Open", "Being Checked", "Closed"]
                else 0,
                key=f"case_status_{case['id']}",
            )

            if st.button("Save Case Update", key=f"save_case_{case['id']}"):
                try:
                    edit_case(
                        case_id=case["id"],
                        case_name=edit_case_name.strip(),
                        remarks=edit_case_remarks.strip(),
                        case_status=edit_case_status,
                    )
                except ValueError as exc:
                    st.error(str(exc))
                else:
                    st.success(f"Case #{case['id']} was updated.")
                    st.rerun()
else:
    st.caption("No saved cases yet.")

