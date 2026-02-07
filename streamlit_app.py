     import streamlit as st
from logic import get_daily_motivation
from logic import (
    parse_prescription,
    generate_adherence_plan,
    generate_nudges,
    check_basic_contraindications
)

# ------------------ PAGE CONFIG ------------------
st.set_page_config(
    page_title="Medication Made Simple",
    layout="centered"
)

# ------------------ HEADER ------------------
st.title("💊 Medication Made Simple")
st.caption("An Explainable AI–based Medication Understanding & Adherence Support System")

st.divider()

# ------------------ CONTEXT ------------------
st.markdown(
    """
    ### 🧠 Why this app exists
    Many patients miss doses **not because they forget**,  
    but because they don’t understand *why timing and consistency matter*.

    This system focuses on:
    - Translating prescriptions into **plain language**
    - Creating a **simple daily routine**
    - Using **behavioral nudges instead of alarms**
    - Highlighting **basic safety awareness**

    👉 **Understanding first. Adherence next.**
    """
)

st.info(
    "This tool supports patients and caregivers by improving understanding. "
    "It does not replace professional medical advice."
)

st.divider()

# ------------------ INPUT ------------------
st.subheader("📄 Enter Prescription")

prescription_text = st.text_area(
    "Paste the prescription text below",
    height=150,
    value=(
        "Paracetamol 500 mg – 1-0-1 – After food – 5 days\n"
        "Amoxicillin 250 mg – 0-1-1 – After food – 7 days"
    )
)

# ------------------ PROCESS ------------------
if st.button("✨ Generate My Medication Plan"):

    medicines = parse_prescription(prescription_text)

    st.subheader("🔍 What the system understood")
    st.json(medicines)

    # -------- Schedule --------
    plan = generate_adherence_plan(medicines)

    st.subheader("🗓️ Your Daily Medication Routine")

    for time, meds in plan.items():
        if meds:
            st.markdown(f"**{time}**")
            for m in meds:
                st.write("•", m)

    # -------- Explainability --------
    st.subheader("🧠 How this plan was created (Explainable AI)")

    st.write(
        """
        - The schedule follows the dosage pattern written in the prescription  
        - For example, **1-0-1** means morning and night  
        - Timing consistency supports routine and reduces missed doses  
        - No medical decisions are made by the system
        """
    )

    # -------- Nudges --------
    st.subheader("💡 Why timing matters (Behavioral Nudges)")

    nudges = generate_nudges(medicines)
    for n in nudges:
        st.info(n)

    # -------- Safety Awareness --------
    warnings = check_basic_contraindications(plan)
    if warnings:
        st.subheader("⚠️ Gentle Safety Awareness")
        for w in warnings:
            st.warning(w)

    st.success(
        "If a dose is missed, continue with the next scheduled time "
        "as advised by your healthcare provider."
    )

    # -------- Daily Motivation --------
    with st.expander("🌱 Your motivation for today"):
        st.success(get_daily_motivation())

    # -------- Ethical AI Note --------
    st.divider()
    st.caption(
        "Ethical AI Notice: This prototype focuses on explanation, routine, "
        "and behavioral support. It intentionally avoids diagnosis, "
        "dose changes, or outcome predictions."
    )   
