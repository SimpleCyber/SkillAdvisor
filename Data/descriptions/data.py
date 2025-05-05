import json

# Full form map for test types
test_type_mapping = {
    "A": "Ability & Aptitude",
    "B": "Biodata & Situational Judgement",
    "C": "Competencies",
    "D": "Development & 360",
    "E": "Assessment Exercises",
    "K": "Knowledge & Skills",
    "P": "Personality & Behavior",
    "S": "Simulations"
}

def transform_entry(entry, solution_type):
    entry["solution"] = solution_type
    entry["test_types"] = [test_type_mapping.get(code, code) for code in entry.get("test_types", [])]
    return entry

# Load individual2.json
with open("individual2.json", "r") as f:
    individual_data = json.load(f)

# Load prepackage2.json
with open("prepackage2.json", "r") as f:
    prepackage_data = json.load(f)

# Transform each entry with solution type and test type full form
individual_data = [transform_entry(item, "Individual Job Solutions") for item in individual_data]
prepackage_data = [transform_entry(item, "Pre-packaged Job Solutions") for item in prepackage_data]

# Combine both datasets
combined_data = individual_data + prepackage_data

# Save to data.json
with open("data.json", "w") as f:
    json.dump(combined_data, f, indent=4)

print("Data merged and saved to data.json.")
