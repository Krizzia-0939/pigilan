import streamlit as st
import streamlit.components.v1 as components


SCROLL_TARGET_KEY = "page_scroll_target"
POST_AUTH_REDIRECT_KEY = "post_auth_redirect"

FEATURE_DESTINATIONS = {
    "asf-risk-assessment": {
        "page": "Health Assessment",
        "section": None,
        "requires_auth": True,
        "auth_notice": "Please sign in first to open ASF Risk Assessment.",
    },
    "image-based-detection": {
        "page": "Health Assessment",
        "section": "assessment-upload-photo",
        "requires_auth": True,
        "auth_notice": "Please sign in first to open Image-Based Detection.",
    },
    "biosecurity-guidance": {
        "page": "My Account",
        "section": "account-biosecurity",
        "requires_auth": True,
        "auth_notice": "Please sign in first to open the Biosecurity Checklist.",
    },
    "nearby-case-alerts": {
        "page": "My Reports",
        "section": None,
        "requires_auth": True,
        "auth_notice": "Please sign in first to open Nearby Case Alerts.",
    },
}


def queue_page_navigation(page, section=None):
    st.session_state.page = page
    if section:
        st.session_state[SCROLL_TARGET_KEY] = section
    else:
        st.session_state.pop(SCROLL_TARGET_KEY, None)


def require_auth_navigation(page, section=None, notice=None):
    st.session_state.page = "My Account"
    st.session_state.auth_mode = "signin"
    st.session_state[POST_AUTH_REDIRECT_KEY] = {
        "page": page,
        "section": section,
    }
    if notice:
        st.session_state.auth_notice = notice


def navigate_to_feature(feature_key):
    feature = FEATURE_DESTINATIONS.get(str(feature_key or "").strip())
    if not feature:
        return False

    if feature["requires_auth"] and not st.session_state.get("user"):
        require_auth_navigation(
            page=feature["page"],
            section=feature.get("section"),
            notice=feature.get("auth_notice"),
        )
    else:
        queue_page_navigation(feature["page"], feature.get("section"))
    return True


def consume_post_auth_redirect():
    redirect = st.session_state.pop(POST_AUTH_REDIRECT_KEY, None)
    if not redirect:
        return False

    queue_page_navigation(
        page=redirect.get("page") or "Home",
        section=redirect.get("section"),
    )
    return True


def clear_navigation_state():
    st.session_state.pop(SCROLL_TARGET_KEY, None)
    st.session_state.pop(POST_AUTH_REDIRECT_KEY, None)


def scroll_to_target_if_needed(target_id):
    if st.session_state.get(SCROLL_TARGET_KEY) != target_id:
        return

    safe_target_id = str(target_id).replace("\\", "\\\\").replace("'", "\\'")
    components.html(
        f"""
        <script>
        (function () {{
          const scrollToTarget = () => {{
            const target = window.parent.document.getElementById('{safe_target_id}');
            if (target) {{
              target.scrollIntoView({{ behavior: 'smooth', block: 'start' }});
            }}
          }};

          window.requestAnimationFrame(() => {{
            window.setTimeout(scrollToTarget, 120);
          }});
        }})();
        </script>
        """,
        height=0,
        width=0,
    )
    st.session_state.pop(SCROLL_TARGET_KEY, None)
