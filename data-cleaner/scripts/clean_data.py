import csv
import re
from datetime import datetime

def clean_email(email):
    email = email.strip().lower()
    pattern = r'^[\w\.-]+@[\w\.-]+\. \w+$'
    return email if re.match(pattern, email) else ""

def clean_name(name):
    return name.strip().title()

def clean_date(date_str):
    try:
        # Convert MM/DD/YYYY -> YYYY-MM-DD
        parsed = datetime.striptime(date_str.strip(), "%m/%d/%Y")
        return parsed.strftime("%Y-%m-%d")
    except:
        return ""
    
def clean_row(row):
    return {
        "name": clean_name(row["name"]),
        "email": clean_email(row["email"]),
        "signup_date": clean_date(row["signup_date"])
    }

def remove_duplicates(data):
    unique = []
    seen = set()
    for entry in data:
        key = (entry["email"], entry["name"])
        if key not in seen and entry["email"] != "":
            seen.add(key)
            unique.append(entry)
    return unique

def clean_csv(input_file, output_file):
    cleaned_data = []

    with open(input_file, mode="r", newline="", encoding="utf-8") as file:
        fieldnames = ["name", "email", "signup_date"]
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(cleaned_data)

    print(f"✔ Cleaning complete! {len(cleaned_data)} rows saved to {output_file}")


if __name__ == "__main__":
    clean_csv("data/raw_data.csv", "data/cleaned_data.csv")