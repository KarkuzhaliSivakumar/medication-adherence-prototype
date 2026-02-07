import streamlit as st
from logic import (
    parse_prescription,
    generate_adherence_plan,
    generate_nudges,
    check_basic_contraindications
)

st.set_page_config(page_title="Medication Adherence Support", layout="centered")

st.title("💊 Medication Understanding & Adherence Support System")

st.write(
    "This system converts complex prescriptions into a simple, "
    "personalized medication plan with explanations and safety checks."
)

st.subheader("📄 Enter Prescription")

prescription_text = st.text_area(
    "Paste the prescription here:",
    height=150,
    value=(
        "Paracetamol 500 mg – 1-0-1 – After food – 5 days\n"
        "Amoxicillin 250 mg – 0-1-1 – After food – 7 days"
    )
)

if st.button("Generate Adherence Plan"):
    medicines = parse_prescription(prescription_text)

    st.subheader("🔍 Extracted Medicine Information")
    st.json(medicines)

    plan = generate_adherence_plan(medicines)

    st.subheader("🗓️ Daily Medication Schedule")
    for time, meds in plan.items():
        if meds:
            st.markdown(f"**{time}**")
            for m in meds:
                st.write("•", m)

    st.subheader("🧠 Why This Schedule Matters")
    nudges = generate_nudges(medicines)
    for n in nudges:
        st.info(n)

    warnings = check_basic_contraindications(plan)
    if warnings:
        st.subheader("⚠️ Safety Alerts")
        for w in warnings:
            st.warning(w)

    st.caption(
        "Disclaimer: This tool is for informational purposes only "
        "and does not replace professional medical advice."
    )

