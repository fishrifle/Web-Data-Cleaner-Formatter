import csv
import re
from datetime import datetime

# ---------------------------
# Cleaning helper functions
# ---------------------------

def clean_email(email):
    if not email:
        return ""
    email = email.strip().lower()
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return email if re.match(pattern, email) else ""

def clean_name(name):
    if not name:
        return ""
    return name.strip().title()

def clean_date(date_str):
    if not date_str:
        return ""
    try:
        parsed = datetime.strptime(date_str.strip(), "%m/%d/%Y")
        return parsed.strftime("%Y-%m-%d")
    except:
        return ""


# ---------------------------
# Fix duplicate logic
# ---------------------------

def remove_duplicates(data):
    unique = []
    seen = set()

    for entry in data:
        email = entry["email"].strip().lower()
        name = entry["name"].strip().title()

        # Skip invalid emails
        if email == "":
            continue

        key = (email, name)
        if key not in seen:
            seen.add(key)
            entry["email"] = email
            entry["name"] = name
            unique.append(entry)

    return unique


# ---------------------------
# Main CSV processing function
# ---------------------------

def clean_csv(input_file, output_file):
    temp_data = []

    # Read CSV (with utf-8-sig for Windows BOM support)
    with open(input_file, mode="r", newline="", encoding="utf-8-sig") as file:
        reader = csv.DictReader(file)

        for row in reader:
            cleaned = {
                "name": clean_name(row.get("name")),
                "email": clean_email(row.get("email")),
                "signup_date": clean_date(row.get("signup_date"))
            }
            temp_data.append(cleaned)

    # Clean duplicates AFTER cleaning rows
    cleaned_data = remove_duplicates(temp_data)

    # Write cleaned data
    with open(output_file, "w+", newline="", encoding="utf-8") as file:
        fieldnames = ["name", "email", "signup_date"]
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(cleaned_data)

    print(f"✔ Cleaning complete! {len(cleaned_data)} rows saved to {output_file}")


# ---------------------------
# Script entry point
# ---------------------------

if __name__ == "__main__":
    clean_csv("data/raw_data.csv", "data/cleaned_data.csv")
