import pandas as pd
import json
import os

# ---------- Paths ----------
RAW_PATH = r"D:\Advanced_AI\medical_chatbot\data\raw"
OUTPUT_PATH = r"D:\Advanced_AI\medical_chatbot\data\processed"

SYMPTOMS_FILE = "DiseaseAndSymptoms.csv"
PRECAUTION_FILE = "Disease precaution.csv"

# ---------- Create output folder ----------
os.makedirs(OUTPUT_PATH, exist_ok=True)

# ---------- Load datasets ----------
symptoms_df = pd.read_csv(os.path.join(RAW_PATH, SYMPTOMS_FILE))
precautions_df = pd.read_csv(os.path.join(RAW_PATH, PRECAUTION_FILE))

# ---------- Basic cleaning ----------
symptoms_df.fillna("", inplace=True)
precautions_df.fillna("", inplace=True)

symptoms_df["Disease"] = symptoms_df["Disease"].str.lower()
precautions_df["Disease"] = precautions_df["Disease"].str.lower()

# ---------- Merge datasets ----------
merged_df = pd.merge(symptoms_df, precautions_df, on="Disease")

# ---------- Identify columns ----------
symptom_cols = [col for col in merged_df.columns if "symptom" in col.lower()]
precaution_cols = [col for col in merged_df.columns if "precaution" in col.lower()]

# ---------- Convert rows to chatbot-friendly JSON ----------
final_data = []

for _, row in merged_df.iterrows():
    entry = {
        "disease": row["Disease"].title(),
        "symptoms": [row[col] for col in symptom_cols if row[col] != ""],
        "prevention": [row[col] for col in precaution_cols if row[col] != ""],
        "common_solutions": [row[col] for col in precaution_cols if row[col] != ""],
        "disclaimer": "This information is for general awareness only and not medical advice."
    }
    final_data.append(entry)

# ---------- Save outputs ----------
os.makedirs(OUTPUT_PATH, exist_ok=True)
merged_df.to_csv(os.path.join(OUTPUT_PATH, "merged_dataset.csv"), index=False)

with open(os.path.join(OUTPUT_PATH, "medical_chatbot_dataset.json"), "w") as f:
    json.dump(final_data, f, indent=4)

print("✅ Data cleaned and merged successfully.")
