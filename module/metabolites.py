# save as: ec_to_metabolite.py
import pandas as pd
import sys
import os

# === Hardcoded path to your EC → Metabolite mapping file ===
MAPPING_FILE = "/home/rdadmin/Desktop/ShreyasWGS_Pipeline/WGS_Pipeline/databases/map_ec_name.txt"

def map_ec_to_metabolite(input_file):
    # Generate output filename
    base_name = os.path.splitext(os.path.basename(input_file))[0]
    output_file = f"{base_name}_metabolites.tsv"

    # === Step 1: Load EC data ===
    df = pd.read_csv(input_file, sep="\t", header=None, names=["EC_raw", "Abundance"])

    # Convert Abundance column to float
    df["Abundance"] = pd.to_numeric(df["Abundance"], errors='coerce')
    df = df.dropna(subset=["Abundance"])

    # === Step 2: Clean EC numbers ===
    df["EC"] = df["EC_raw"].str.split("|").str[0]

    # === Step 3: Sum abundance per EC ===
    abundance_df = df.groupby("EC", as_index=False)["Abundance"].sum()

    # === Step 4: Load EC → Metabolite mapping ===
    mapping = pd.read_csv(MAPPING_FILE, sep="\t", header=None, names=["EC", "Metabolite"])
    
    # === Step 5: Map EC to Metabolite ===
    result = pd.merge(abundance_df, mapping, on="EC", how="left")

    # === Step 6: Save output ===
    result.to_csv(output_file, sep="\t", index=False)
    print(f"✅ Output saved as {output_file}")

# === CLI Entry Point ===
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python ec_to_metabolite.py <input_file>")
        sys.exit(1)

    input_file = sys.argv[1]
    map_ec_to_metabolite(input_file)


