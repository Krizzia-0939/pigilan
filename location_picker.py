import streamlit as st
import pandas as pd

try:
    from streamlit_js_eval import get_geolocation
except Exception as exc:
    get_geolocation = None
    _STREAMLIT_JS_EVAL_IMPORT_ERROR = exc
else:
    _STREAMLIT_JS_EVAL_IMPORT_ERROR = None


DEFAULT_LATITUDE = 10.7202
DEFAULT_LONGITUDE = 122.5621


def _format_missing_feature_message(base_message, missing_packages):
    package_list = ", ".join(missing_packages)
    return f"{base_message} Missing optional component: {package_list}."


def render_point_location_picker(
    title,
    session_prefix,
    initial_latitude,
    initial_longitude,
    caption_text,
    show_section_header=True,
):
    latitude_key = f"{session_prefix}_latitude"
    longitude_key = f"{session_prefix}_longitude"
    latitude_input_key = f"{session_prefix}_latitude_input"
    longitude_input_key = f"{session_prefix}_longitude_input"
    gps_request_key = f"{session_prefix}_gps_requested"
    gps_accuracy_key = f"{session_prefix}_gps_accuracy"
    reset_key = f"{session_prefix}_reset_location"

    if latitude_key not in st.session_state:
        st.session_state[latitude_key] = round(float(initial_latitude), 6)
    if longitude_key not in st.session_state:
        st.session_state[longitude_key] = round(float(initial_longitude), 6)
    if gps_request_key not in st.session_state:
        st.session_state[gps_request_key] = False
    if gps_accuracy_key not in st.session_state:
        st.session_state[gps_accuracy_key] = None
    if latitude_input_key not in st.session_state:
        st.session_state[latitude_input_key] = st.session_state[latitude_key]
    if longitude_input_key not in st.session_state:
        st.session_state[longitude_input_key] = st.session_state[longitude_key]

    if show_section_header:
        st.subheader(title)
        st.caption(caption_text)
        st.caption("Offline tip: GPS and manual coordinates can still be saved even if the map preview does not load.")
        st.caption("You can type the exact latitude and longitude below, or use your current location.")

    left_col, right_col = st.columns([1, 1.05], gap="large")

    with left_col:
        st.markdown(
            "Tap **Use My Current Location** or adjust the coordinates for this farm check."
        )
        st.caption(caption_text)
        st.caption("GPS and manual coordinates can still be saved even if the map preview is unavailable.")

        button_col1, button_col2 = st.columns(2, gap="small")
        with button_col1:
            if st.button(
                "Use My Current Location",
                key=f"{session_prefix}_gps_button",
                use_container_width=True,
            ):
                if get_geolocation is None:
                    st.session_state[gps_request_key] = False
                    st.info(
                        _format_missing_feature_message(
                            "Browser GPS is unavailable on this device right now.",
                            ["streamlit-js-eval"],
                        )
                    )
                else:
                    st.session_state[gps_request_key] = True

        with button_col2:
            if st.button(
                "Clear Location",
                key=reset_key,
                use_container_width=True,
            ):
                st.session_state[latitude_key] = round(float(initial_latitude), 6)
                st.session_state[longitude_key] = round(float(initial_longitude), 6)
                st.session_state[latitude_input_key] = st.session_state[latitude_key]
                st.session_state[longitude_input_key] = st.session_state[longitude_key]
                st.session_state[gps_request_key] = False
                st.session_state[gps_accuracy_key] = None
                st.rerun()

        if st.session_state[gps_request_key] and get_geolocation is not None:
            gps_result = get_geolocation(component_key=f"{session_prefix}_gps_component")
            if gps_result and "error" in gps_result:
                error_code = gps_result["error"].get("code")
                error_message = gps_result["error"].get("message", "Could not get your location.")
                if error_code == 1:
                    st.warning("Location permission was denied. Please enter the coordinates manually.")
                else:
                    st.warning(f"Could not get current location: {error_message}")
                st.session_state[gps_request_key] = False
            elif gps_result and "coords" in gps_result:
                st.session_state[latitude_key] = round(float(gps_result["coords"]["latitude"]), 6)
                st.session_state[longitude_key] = round(float(gps_result["coords"]["longitude"]), 6)
                st.session_state[latitude_input_key] = st.session_state[latitude_key]
                st.session_state[longitude_input_key] = st.session_state[longitude_key]
                accuracy = gps_result["coords"].get("accuracy")
                st.session_state[gps_accuracy_key] = round(float(accuracy), 2) if accuracy is not None else None
                st.session_state[gps_request_key] = False
                st.success("Current location loaded.")
                st.rerun()
            else:
                st.info("Waiting for location permission or GPS signal...")

        coordinate_col1, coordinate_col2 = st.columns(2, gap="small")
        with coordinate_col1:
            st.number_input(
                "Latitude",
                format="%.6f",
                key=latitude_input_key,
            )
            st.session_state[latitude_key] = round(float(st.session_state[latitude_input_key]), 6)
        with coordinate_col2:
            st.number_input(
                "Longitude",
                format="%.6f",
                key=longitude_input_key,
            )
            st.session_state[longitude_key] = round(float(st.session_state[longitude_input_key]), 6)

        st.caption(
            f"Selected exact point: {st.session_state[latitude_key]}, {st.session_state[longitude_key]}"
        )
        if st.session_state[gps_accuracy_key] is not None:
            st.caption(f"GPS accuracy: about {st.session_state[gps_accuracy_key]} meters")

    with right_col:
        try:
            st.map(
                pd.DataFrame(
                    [
                        {
                            "lat": st.session_state[latitude_key],
                            "lon": st.session_state[longitude_key],
                        }
                    ]
                ),
                size=120,
                zoom=12,
                use_container_width=True,
            )
            st.caption("Map preview updates after you change the latitude, longitude, or GPS location above.")
        except Exception:
            st.info("Map preview is unavailable right now. You can still save using GPS or the latitude/longitude fields above.")

    return float(st.session_state[latitude_key]), float(st.session_state[longitude_key])
