import json
import pandas as pd
import random

# -----------------------------
# File paths
# -----------------------------
PERSPECTRUM_FILE = "perspectrum_with_answers_v1.0.json"
PERSPECTIVE_POOL_FILE = "perspective_pool_v1.0.json"
OUTPUT_FILE = "hw3_annotation_sample_100.csv"

# Set random seed so your sample is reproducible
RANDOM_SEED = 98

# -----------------------------
# Load JSON files
# -----------------------------
with open(PERSPECTRUM_FILE, "r", encoding="utf-8") as f:
    perspectrum_data = json.load(f)

with open(PERSPECTIVE_POOL_FILE, "r", encoding="utf-8") as f:
    perspective_pool_data = json.load(f)

# -----------------------------
# Build a lookup dictionary:
# pId -> perspective text
# -----------------------------
pid_to_text = {}
for item in perspective_pool_data:
    pid = item["pId"]
    text = item["text"]
    pid_to_text[pid] = text

# -----------------------------
# Expand into claim-perspective pairs
# Each individual pId becomes its own row
# -----------------------------
rows = []

for claim in perspectrum_data:
    cid = claim["cId"]
    claim_text = claim["text"]

    for perspective_group in claim["perspectives"]:
        pids = perspective_group["pids"]

        for pid in pids:
            perspective_text = pid_to_text.get(pid, None)

            # Skip if pid is missing from the perspective pool
            if perspective_text is None:
                continue

            rows.append({
                "cid": cid,
                "claim_text": claim_text,
                "pid": pid,
                "perspective_text": perspective_text
            })

# -----------------------------
# Convert to DataFrame
# -----------------------------
df = pd.DataFrame(rows)

# Optional: remove exact duplicate rows
df = df.drop_duplicates()

# -----------------------------
# Randomly sample 100 instances
# -----------------------------
if len(df) < 100:
    raise ValueError(f"Dataset only has {len(df)} rows, which is fewer than 100.")

sample_df = df.sample(n=100, random_state=RANDOM_SEED).copy()

# Add blank annotation columns for you to fill in
sample_df["stance_annotation"] = ""
sample_df["relevance_annotation"] = ""

# -----------------------------
# Save to CSV
# -----------------------------
sample_df.to_csv(OUTPUT_FILE, index=False, encoding="utf-8")

print(f"Entire file unsampled df contains: {len(df)} rows.")

print(f"Saved {len(sample_df)} rows to {OUTPUT_FILE}")
print(sample_df.head())