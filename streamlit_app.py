import streamlit as st
from PIL import Image

# Optional OCR import (safe for prototype)
try:
    import pytesseract
    OCR_AVAILABLE = True
except:
    OCR_AVAILABLE = False

from logic import (
    parse_prescription,
    generate_adherence_plan,
    generate_nudges,
    check_basic_contraindications,
    get_daily_motivation
)

# ─────────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────────
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

    input_mode = st.radio(
        "Choose input type",
        ["Text", "Image"],
        horizontal=True
    )

    prescription_text = ""

    if input_mode == "Text":
        prescription_text = st.text_area(
            "Paste the prescription text below",
            height=150,
            value=(
                "Paracetamol 500 mg – 1-0-1 – After food – 5 days\n"
                "Amoxicillin 250 mg – 0-1-1 – After food – 7 days"
            )
        )

    else:
        uploaded_image = st.file_uploader(
            "Upload prescription image",
            type=["png", "jpg", "jpeg"]
        )

        if uploaded_image:
            image = Image.open(uploaded_image)
            st.image(image, caption="Uploaded Prescription", use_column_width=True)

            if OCR_AVAILABLE:
                with st.spinner("Extracting text from image..."):
                    extracted_text = pytesseract.image_to_string(image)
            else:
                extracted_text = ""

            prescription_text = st.text_area(
                "Extracted text (you can edit before proceeding)",
                value=extracted_text,
                height=150
            )

    generate = st.button("🔍 Generate Medication Plan")

# ─────────────────────────────────────────────
# OUTPUT SECTION
# ─────────────────────────────────────────────
if generate and prescription_text.strip():

    medicines = parse_prescription(prescription_text)

    with st.container():
        st.subheader("🔍 Extracted Information")
        st.json(medicines)

    plan = generate_adherence_plan(medicines)

    st.divider()

    # Schedule + Explanation
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
            "The schedule is created directly from the prescription pattern "
            "(for example, 1-0-1 means morning and night doses). "
            "Consistent timing helps medicines work effectively and safely."
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

    # Daily motivation (one per day)
    with st.expander("🌱 A Gentle Nudge for Today"):
        st.success(get_daily_motivation())

    st.divider()

    st.caption(
        "Disclaimer: This prototype is for informational purposes only "
        "and does not replace professional medical advice."
    )
