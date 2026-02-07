import streamlit as st
from logic import (
    parse_prescription,
    generate_adherence_plan,
    generate_nudges,
    check_basic_contraindications,
    get_daily_motivation
)

st.set_page_config(
    page_title="Medication Adherence Support",
    layout="centered"
)

# ─────────────────────────────────────────────
# HEADER
# ─────────────────────────────────────────────
st.title("Medication Made Simple")
st.caption("An AI-based Medication Understanding and Adherence Support System")

with st.container():
    st.markdown(
        """
        **Why this app exists**

        Many patients miss doses not because they forget,
        but because they don’t understand *why* timing matters.

        This prototype focuses on:
        - Plain-language prescription interpretation  
        - Simple daily medication planning  
        - Behavioral nudges instead of alarms  
        - Basic safety awareness  

        **Understanding comes first. Adherence follows.**
        """
    )

st.divider()

# ─────────────────────────────────────────────
# INPUT SECTION
# ─────────────────────────────────────────────
with st.container():
    st.subheader("📄 Enter Prescription")
    prescription_text = st.text_area(
        "Paste the prescription text below",
        height=150,
        value=(
            "Paracetamol 500 mg – 1-0-1 – After food – 5 days\n"
            "Amoxicillin 250 mg – 0-1-1 – After food – 7 days"
        )
    )

    generate = st.button("🔍 Generate Medication Plan")

# ─────────────────────────────────────────────
# OUTPUT SECTION
# ─────────────────────────────────────────────
if generate:
    medicines = parse_prescription(prescription_text)

    with st.container():
        st.subheader("🔍 Extracted Information")
        st.json(medicines)

    plan = generate_adherence_plan(medicines)

    st.divider()

    # Schedule + Explanation side by side
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("🗓️ Daily Schedule")
        for time, meds in plan.items():
            if meds:
                st.markdown(f"**{time}**")
                for m in meds:
                    st.write("•", m)

    with col2:
        st.subheader("🧠 Why This Schedule Matters")
        st.info(
            "Medication timing is derived directly from the prescription pattern "
            "(e.g., 1-0-1 indicates morning and night doses). "
            "Consistent timing improves effectiveness and reduces complications, "
            "especially for antibiotics."
        )

    st.divider()

    # Behavioral nudges
    with st.container():
        st.subheader("💡 Supportive Nudges")
        nudges = generate_nudges(medicines)
        for n in nudges:
            st.info(n)

    # Safety alerts
    warnings = check_basic_contraindications(plan)
    if warnings:
        with st.container():
            st.subheader("⚠️ Safety Awareness")
            for w in warnings:
                st.warning(w)

    # Daily motivation
    with st.expander("🌱 A Gentle Nudge for Today"):
        st.success(get_daily_motivation())

    st.divider()

    st.caption(
        "Disclaimer: This prototype is for informational support only and "
        "does not replace professional medical advice."
    )
