def parse_prescription(text):
    medicines = []

    lines = text.split("\n")
    for line in lines:
        parts = [p.strip() for p in line.split("–")]

        if len(parts) < 4:
            continue

        name_dose = parts[0].split()
        name = name_dose[0]
        dose = name_dose[1] + " " + name_dose[2]

        frequency = parts[1]
        instruction = parts[2]
        duration = parts[3]

        timing = []
        if frequency == "1-0-1":
            timing = ["Morning", "Night"]
        elif frequency == "0-1-1":
            timing = ["Afternoon", "Night"]
        elif frequency == "1-1-1":
            timing = ["Morning", "Afternoon", "Night"]

        medicines.append({
            "name": name,
            "dose": dose,
            "frequency": frequency,
            "timing": timing,
            "instruction": instruction,
            "duration": duration
        })

    return medicines


def generate_adherence_plan(medicines):
    plan = {
        "Morning": [],
        "Afternoon": [],
        "Night": []
    }

    for med in medicines:
        for time in med["timing"]:
            plan[time].append(
                f"{med['name']} {med['dose']} ({med['instruction']})"
            )

    return plan


def generate_nudges(medicines):
    nudges = []

    for med in medicines:
        if med["name"].lower() in ["amoxicillin", "azithromycin"]:
            nudges.append(
                "Completing the full antibiotic course helps prevent resistance."
            )

    nudges.append(
        "Taking medicines at the same time every day improves recovery."
    )

    return nudges


def check_basic_contraindications(plan):
    warnings = []

    if len(plan["Night"]) > 1:
        warnings.append(
            "Multiple medicines are scheduled at night. Take them after food to avoid stomach irritation."
        )

    return warnings

