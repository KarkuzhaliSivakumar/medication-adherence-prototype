import random

# ------------------ PRESCRIPTION PARSER ------------------
def parse_prescription(text):
    """
    Converts raw prescription text into structured information.
    This is a simple rule-based prototype for hackathon use.
    """

    medicines = []
    lines = text.strip().split("\n")

    for line in lines:
        parts = line.split("–")
        if len(parts) >= 2:
            medicine = {
                "name": parts[0].strip(),
                "dosage_pattern": parts[1].strip(),
                "instructions": parts[2].strip() if len(parts) > 2 else ""
            }
            medicines.append(medicine)

    return medicines


# ------------------ ADHERENCE PLAN GENERATOR ------------------
def generate_adherence_plan(medicines):
    """
    Creates a daily routine based on dosage patterns like 1-0-1.
    Focuses on routine, not medical optimization.
    """

    plan = {
        "🌅 Morning": [],
        "🌞 Afternoon": [],
        "🌙 Night": []
    }

    for med in medicines:
        pattern = med["dosage_pattern"]

        if pattern.startswith("1"):
            plan["🌅 Morning"].append(med["name"])

        if len(pattern) > 2 and pattern[2] == "1":
            plan["🌞 Afternoon"].append(med["name"])

        if pattern.endswith("1"):
            plan["🌙 Night"].append(med["name"])

    return plan


# ------------------ NUDGE THEORY ENGINE ------------------
def generate_nudges(medicines):
    """
    Generates behavioral nudges that explain WHY adherence matters.
    These are non-clinical, motivational, and ethical.
    """

    nudges = [
        "Taking medicine at the same time daily helps build a habit, making doses easier to remember.",
        "Consistent timing supports a steady routine, which many patients find less stressful.",
        "Completing the full course is important even if you start feeling better.",
        "Understanding your medication schedule can reduce confusion and missed doses.",
        "Small daily habits often lead to better long-term health routines."
    ]

    # Limit nudges to avoid overload (behavioral science principle)
    return random.sample(nudges, min(2, len(nudges)))


# ------------------ BASIC SAFETY AWARENESS ------------------
def check_basic_contraindications(plan):
    """
    Performs simple, non-clinical checks.
    Avoids medical diagnosis or drug interaction claims.
    """

    warnings = []

    total_doses = sum(len(meds) for meds in plan.values())

    if total_doses >= 5:
        warnings.append(
            "Multiple medicines are scheduled in a single day. "
            "Using reminders or caregiver support may help maintain routine."
        )

    if plan["🌙 Night"] and plan["🌅 Morning"]:
        warnings.append(
            "Medicines are scheduled at different times of day. "
            "Maintaining consistent timing helps avoid missed doses."
        )

    return warnings


# ------------------ DAILY MOTIVATION ------------------
def get_daily_motivation():
    """
    Returns one gentle motivational message per day.
    Prevents cognitive overload.
    """

    motivations = [
        "Today’s small steps support tomorrow’s well-being.",
        "Understanding your routine is a powerful first step.",
        "Consistency is more important than perfection.",
        "Every completed dose is a positive action for yourself.",
        "Good habits are built one day at a time."
    ]

    return random.choice(motivations)
