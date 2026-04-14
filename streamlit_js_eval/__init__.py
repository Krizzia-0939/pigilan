from pathlib import Path

import streamlit.components.v1 as components


_FRONTEND_PATH = str(Path(__file__).resolve().parent)

streamlit_js_eval = components.declare_component(
    "streamlit_js_eval",
    path=_FRONTEND_PATH,
)


def get_geolocation(component_key=None):
    key = component_key or "getLocation()"
    return streamlit_js_eval(js_expressions="getLocation()", key=key)
