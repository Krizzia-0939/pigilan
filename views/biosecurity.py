import streamlit as st

from backend import (
    BIOSECURITY_ITEMS,
    save_biosecurity_check,
)


st.title("Biosecurity Checklist")

if "user" not in st.session_state or not st.session_state.user:
    st.warning("Please sign in first to use the biosecurity checklist.")
    st.stop()


st.caption("Check the items your farm is already doing to reduce the spread of ASF.")

with st.form("biosecurity_form", clear_on_submit=False):
    checks = {item: st.checkbox(item) for item in BIOSECURITY_ITEMS}
    remarks = st.text_area("Notes")
    submitted = st.form_submit_button("Save Biosecurity Check")

if submitted:
    result = save_biosecurity_check(
        user_id=st.session_state.user["id"],
        checklist=checks,
        remarks=remarks.strip(),
    )

    st.write(f"Checked items: **{result['checked_count']}**")
    st.write(f"Unchecked items: **{result['unchecked_count']}**")

    if result["protection_label"] == "Low protection from ASF":
        st.error(result["warning_message"])
    elif result["protection_label"] == "Moderate protection from ASF":
        st.warning(result["warning_message"])
    else:
        st.success(result["warning_message"])

    st.caption(f"Saved biosecurity check #{result['record_id']}.")
    st.caption("This checklist is stored locally first and can be synced later.")
