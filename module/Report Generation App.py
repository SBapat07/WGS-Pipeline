import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import base64
from io import BytesIO
from datetime import datetime
import os
import time

# ---------------------- Utility functions ----------------------

def fig_to_base64(fig):
    buf = BytesIO()
    fig.savefig(buf, format="png", bbox_inches='tight')
    plt.close(fig)
    buf.seek(0)
    return base64.b64encode(buf.read()).decode("utf-8")

def generate_shannon_gauge(value):
    fig, ax = plt.subplots(figsize=(6, 4), subplot_kw={'projection': 'polar'})
    ax.set_theta_offset(np.pi)  # Start at the top (180°)
    ax.set_theta_direction(-1)  # Clockwise direction
    ax.set_yticklabels([])
    ax.set_xticks([])
    ax.set_thetamin(0)
    ax.set_thetamax(180)
    ax.set_facecolor('white')
    ax.text(np.pi * (0.75/5), 1.2, 'Low', ha='center', va='center', fontsize=8, color='red')
    ax.text(np.pi * (2.5/5), 1.2, 'Moderate', ha='center', va='center', fontsize=8, color='orange')
    ax.text(np.pi * (4.25/5), 1.2, 'High', ha='center', va='center', fontsize=8, color='green')
    


    # Correct color sequence: RED -> YELLOW -> GREEN
    color_ranges = [
        (0, 1.5, '#f44336'),   # Red
        (1.5, 3.5, '#ffeb3b'), # Yellow
        (3.5, 5.0, '#4caf50')  # Green
    ]

    for start, end, color in color_ranges:
        theta_start = (start / 5) * np.pi  # LEFT side
        theta_end = (end / 5) * np.pi       # RIGHT side
        theta = np.linspace(theta_start, theta_end, 30)
        ax.plot(theta, [1] * len(theta), color=color, linewidth=10)

    # Draw the needle
    angle = (value / 5) * np.pi
    ax.plot([angle, angle], [0, 1], color='black', linewidth=3)

    fig.subplots_adjust(bottom=0.3)
    fig.text(0.5, 0.1, f"{value:.3f}", ha='center', va='center', fontsize=12)
    fig.text(0.5, 0.05, "Shannon Index", ha='center', va='center', fontsize=11)

    return f'<div style="margin: 30px auto; text-align:center;"><img src="data:image/png;base64,{fig_to_base64(fig)}" style="max-width:350px;"></div>'


def generate_simpson_gauge(value):
    fig, ax = plt.subplots(figsize=(6, 4), subplot_kw={'projection': 'polar'})
    ax.set_theta_offset(np.pi)  # Start at top
    ax.set_theta_direction(-1)  # Clockwise
    ax.set_yticklabels([])
    ax.set_xticks([])
    ax.set_thetamin(0)
    ax.set_thetamax(180)
    ax.set_facecolor('white')

    # Labels for Low / Moderate / High
    ax.text(np.pi * (0.15/1), 1.2, 'Low', ha='center', va='center', fontsize=8, color='red')
    ax.text(np.pi * (0.5/1), 1.2, 'Moderate', ha='center', va='center', fontsize=8, color='orange')
    ax.text(np.pi * (0.85/1), 1.2, 'High', ha='center', va='center', fontsize=8, color='green')

    # Color ranges directly for 0–1
    color_ranges = [
        (0.0, 0.3, '#f44336'),   # Red
        (0.3, 0.7, '#ffeb3b'),   # Yellow
        (0.7, 1.0, '#4caf50')    # Green
    ]

    for start, end, color in color_ranges:
        theta_start = start * np.pi  # start mapped to [0, π]
        theta_end = end * np.pi
        theta = np.linspace(theta_start, theta_end, 30)
        ax.plot(theta, [1] * len(theta), color=color, linewidth=10)

    # Draw the needle
    angle = value * np.pi  # direct mapping
    ax.plot([angle, angle], [0, 1], color='black', linewidth=3)

    fig.subplots_adjust(bottom=0.3)
    fig.text(0.5, 0.1, f"{value:.3f}", ha='center', va='center', fontsize=12)
    fig.text(0.5, 0.05, "Simpson Index", ha='center', va='center', fontsize=11)

    return f'<div style="margin: 30px auto; text-align:center;"><img src="data:image/png;base64,{fig_to_base64(fig)}" style="max-width:350px;"></div>'

def generate_fb_ratio_gauge(value):
    # Scale F/B value for gauge display (use 10 as reference max)
    scaled_value = min(value / 10, 1.0)  # Normalize to 0–1 range
    fig, ax = plt.subplots(figsize=(6, 4), subplot_kw={'projection': 'polar'})
    ax.set_theta_offset(np.pi)  # Start from top
    ax.set_theta_direction(-1)  # Clockwise
    ax.set_yticklabels([])
    ax.set_xticks([])
    ax.set_thetamin(0)
    ax.set_thetamax(180)
    ax.set_facecolor('white')

    # Add labels
    ax.text(np.pi * (0.15/1), 1.2, 'Low', ha='center', va='center', fontsize=8, color='red')
    ax.text(np.pi * (0.5/1), 1.2, 'Normal', ha='center', va='center', fontsize=8, color='orange')
    ax.text(np.pi * (0.85/1), 1.2, 'High', ha='center', va='center', fontsize=8, color='green')

    # Color-coded ranges (red-yellow-green)
    color_ranges = [
        (0.0, 0.3, '#f44336'),   # Red (Low F/B ratio)
        (0.3, 0.7, '#ffeb3b'),   # Yellow (Normal)
        (0.7, 1.0, '#4caf50')    # Green (High or Very High)
    ]
    for start, end, color in color_ranges:
        theta = np.linspace(start * np.pi, end * np.pi, 30)
        ax.plot(theta, [1] * len(theta), color=color, linewidth=10)

    # Draw the needle
    angle = scaled_value * np.pi
    ax.plot([angle, angle], [0, 1], color='black', linewidth=3)

    # Display exact F/B ratio value
    fig.subplots_adjust(bottom=0.3)
    fig.text(0.5, 0.1, f"{value:.3f}", ha='center', va='center', fontsize=12)
    fig.text(0.5, 0.05, "F/B Ratio", ha='center', va='center', fontsize=11)

    return f'<div style="margin: 30px auto; text-align:center;"><img src="data:image/png;base64,{fig_to_base64(fig)}" style="max-width:350px;"></div>'




# ---------------------- Parsing functions ----------------------

def parse_krona_abundance(file):
    import pandas as pd
    import numpy as np

    df = pd.read_csv(file, sep="\t", comment='#', header=None,
                     names=["clade_name", "NCBI_tax_id", "relative_abundance", "additional_species"])

    df["relative_abundance"] = pd.to_numeric(df["relative_abundance"], errors="coerce")
    df = df[df["relative_abundance"] > 0].copy()

    def extract_taxon(taxon_str):
        levels = taxon_str.strip().split('|')
        taxon_dict = {}
        for part in levels:
            if '__' in part:
                prefix, name = part.split('__')
                taxon_dict[prefix] = name.replace('_', ' ').strip()
        if 's' in taxon_dict and taxon_dict['s'].lower() != 'unclassified':
            return taxon_dict['s'], 'Species'
        elif 'g' in taxon_dict and taxon_dict['g'].lower() != 'unclassified':
            return taxon_dict['g'], 'Genus'
        elif 'f' in taxon_dict and taxon_dict['f'].lower() != 'unclassified':
            return taxon_dict['f'], 'Family'
        elif 'p' in taxon_dict and taxon_dict['p'].lower() != 'unclassified':
            return taxon_dict['p'], 'Phylum'
        elif 'k' in taxon_dict and taxon_dict['k'].lower() != 'unclassified':
            return taxon_dict['k'], 'Kingdom'
        else:
            return 'Unclassified', 'Unclassified'

    if df.empty:
        return "<p>No valid abundance data found.</p>", pd.DataFrame(columns=["clade_name", "relative_abundance", "Taxon", "Level"])

    df["Taxon"], df["Level"] = zip(*df["clade_name"].map(extract_taxon))

    # Add relative abundance percentage column formatted as string with 2 decimals
    df['relative_abundance_percent'] = df['relative_abundance'].apply(lambda x: f"{x * 100:.2f}%")

    proportions = df["relative_abundance"] / df["relative_abundance"].sum()
    shannon = -np.sum(proportions * np.log(proportions))
    simpson = 1 - np.sum(proportions ** 2)

    def get_phylum_abundance(phylum):
        match = df[df["clade_name"].str.contains(f"p__{phylum}")]
        return match["relative_abundance"].sum()

    firm = get_phylum_abundance("Firmicutes")
    bact = get_phylum_abundance("Bacteroidota")
    fb_ratio = firm / bact if bact > 0 else 0

    gauges = "".join([
        generate_shannon_gauge(shannon),
        generate_simpson_gauge(simpson),
        generate_fb_ratio_gauge(fb_ratio)
    ])

    html = f"{gauges}"
    return html, df

def generate_bar(df, level):
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.barh(df['Taxon'], df['relative_abundance'], color="#42a5f5")
    ax.set_title(f"Top {level} Level Taxa", fontsize=16, color='#333')
    fig.tight_layout()
    return fig_to_base64(fig)

def generate_pie(df, level):
    fig, ax = plt.subplots(figsize=(8, 8))
    ax.pie(df["relative_abundance"], labels=df["Taxon"], autopct='%1.1f%%',
           startangle=140, textprops={'fontsize': 8}, wedgeprops={'linewidth': 1, 'edgecolor': 'white'})
    ax.set_title(f"{level} Distribution", fontsize=16, color='#333')
    return fig_to_base64(fig)

def taxonomic_tables(df):
    html_blocks = []
    for level in ["Species", "Genus", "Family", "Phylum", "Kingdom", "Unclassified"]:
        sub = df[df["Level"] == level][["Taxon", "relative_abundance"]].copy()
        if sub.empty:
            continue
        sub = sub.groupby("Taxon", as_index=False).sum().sort_values(by="relative_abundance", ascending=False)
        sub["Rank"] = np.arange(1, len(sub)+1)
        table = sub[["Rank", "Taxon", "relative_abundance"]].to_html(index=False, escape=False, header=True)
        plot = generate_bar(sub.head(10), level) if level in ["Species", "Genus", "Family"] else generate_pie(sub.head(10), level)

        html_blocks.append(f"{table}")
        html_blocks.append(f"<img src='data:image/png;base64,{plot}' style='max-width:90%; display:block; margin:0 auto;'>")

    return "\n".join(html_blocks)


def parse_metabolite(abundance_file, coverage_file):
    try:
        # Read abundance file
        df_abundance = pd.read_csv(abundance_file, sep="\t", comment="#", header=None, names=["Pathway", "Abundance"])
        df_abundance = df_abundance[df_abundance["Pathway"].str.contains(":", na=False)]

        def extract_pathway_name(pathway):
            if ':' in pathway:
                return pathway.split(":", 1)[1].split("|")[0].strip()
            return None

        df_abundance["Pathway Name"] = df_abundance["Pathway"].apply(extract_pathway_name)
        df_abundance = df_abundance.dropna(subset=["Pathway Name", "Abundance"])
        df_abundance["Abundance"] = pd.to_numeric(df_abundance["Abundance"], errors="coerce")
        df_abundance = df_abundance.dropna(subset=["Abundance"])

        # Read coverage file
        df_coverage = pd.read_csv(coverage_file, sep="\t", comment="#", header=None, names=["Pathway", "Coverage"])
        df_coverage = df_coverage[~df_coverage["Pathway"].isin(["UNMAPPED", "UNINTEGRATED"])]

        df_coverage["Pathway Name"] = df_coverage["Pathway"].apply(extract_pathway_name)
        df_coverage = df_coverage.dropna(subset=["Pathway Name", "Coverage"])
        df_coverage["Coverage"] = pd.to_numeric(df_coverage["Coverage"], errors="coerce")
        df_coverage = df_coverage.dropna(subset=["Coverage"])

        # Merge abundance and coverage on pathway name
        df_merged = pd.merge(
            df_abundance[["Pathway Name", "Abundance"]],
            df_coverage[["Pathway Name", "Coverage"]],
            on="Pathway Name",
            how="inner"
        )

        # Remove duplicates based on Pathway Name, keep first occurrence
        df_merged = df_merged.drop_duplicates(subset=["Pathway Name"])

        # Sort by abundance descending and add serial numbers
        df_merged = df_merged.sort_values(by="Abundance", ascending=False).reset_index(drop=True)
        df_merged["Sr. No."] = df_merged.index + 1

        # Rearrange columns
        df_merged = df_merged[["Sr. No.", "Pathway Name", "Abundance", "Coverage"]]

        # Generate bar plot for top 10 pathways by abundance
        top10 = df_merged.head(10)
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.barh(top10['Pathway Name'], top10['Abundance'], color="#42a5f5")
        ax.set_title("Top Pathways by Abundance", fontsize=16, color='#333')
        ax.set_xlabel("Abundance")
        ax.invert_yaxis()  # Highest abundance on top
        fig.tight_layout()
        img_html = f"<img src='data:image/png;base64,{fig_to_base64(fig)}' style='max-width:100%; margin:0 auto;'>"

        # Generate HTML table
        table_html = df_merged.to_html(index=False)

        return f"{table_html}{img_html}"

    except Exception as e:
        return f"<p><b>Metabolite Parsing Error:</b> {e}</p>"
        

# Date and Time
date = datetime.now().strftime("%B %d, %Y %H:%M:%S")  # Current date and time in the format: Month Day, Year Hour:Minute:Second

# File path for the logo
logo_path = "/home/rdadmin/Desktop/ShreyasWGS_Pipeline/WGS_Pipeline/company_logo.png"  # Update with your actual path

# Base64 encode the image
with open(logo_path, "rb") as img_file:
    encoded_logo = base64.b64encode(img_file.read()).decode("utf-8")

# Create img tag with base64 encoded logo
img_tag = f'<img src="data:image/png;base64,{encoded_logo}" alt="Company Logo" class="logo">'

# Add date and time
date_time_tag = f'<div class="date-time">{date}</div>'

# ---------------------- Streamlit UI ----------------------

# Set up Streamlit page
st.set_page_config(page_title="Microbiome Analysis HTML Report Generator", layout="wide")
st.title("🧬 Microbiome Analysis Report Generator")

# Define directories
data_folder = "/home/rdadmin/Desktop/ShreyasWGS_Pipeline/WGS_Pipeline/Data"
metaphlan_base = "/home/rdadmin/Desktop/ShreyasWGS_Pipeline/WGS_Pipeline/Results/Metaphlan4_results"
krona_base = "/home/rdadmin/Desktop/ShreyasWGS_Pipeline/WGS_Pipeline/Results/Krona_result"
humann_base = "/home/rdadmin/Desktop/ShreyasWGS_Pipeline/WGS_Pipeline/Results/Humann_result"
humann_base1 = "/home/rdadmin/Desktop/ShreyasWGS_Pipeline/WGS_Pipeline/Results/Humann_result"

# Initialize sections
diversity_html = ""
taxonomy_html = ""
humann_html = ""
krona_embed = ""

# Step 1: Sample ID selection
fastq_files = sorted([f for f in os.listdir(data_folder) if f.endswith(".fastq")])
sample_ids = [os.path.splitext(f)[0] for f in fastq_files]

if not sample_ids:
    st.warning("⚠️ No FASTQ files found.")
    st.stop()

# Add default placeholder to the list
options = ['Select Sample ID to display the report'] + sample_ids
selected_sample = st.selectbox("🧬 Select Sample ID", options)

# Stop execution if default option is selected
if selected_sample == '--select the sample id--':
    st.warning("⚠️ Please select a valid Sample ID to proceed.")
    st.stop()

# Step 2: Auto-locate result directories for selected sample
def find_sample_subfolder(base_dir, sample_id):
    for folder in os.listdir(base_dir):
        path = os.path.join(base_dir, folder)
        if os.path.isdir(path) and sample_id in folder:
            return path
    return None

metaphlan_path = find_sample_subfolder(metaphlan_base, selected_sample)
krona_path = find_sample_subfolder(krona_base, selected_sample)
humann_path = find_sample_subfolder(humann_base, selected_sample)
humann_path1 = find_sample_subfolder(humann_base, selected_sample)

# Step 3: Validate and list available files
if not all([metaphlan_path, krona_path, humann_path]):
    st.warning(f"⚠️ Missing results for sample: `{selected_sample}`.")
    st.stop()

abundance_files = sorted([f for f in os.listdir(metaphlan_path) if f.endswith(".txt")])
krona_files = sorted([f for f in os.listdir(krona_path) if f.endswith(".html") and "abundance" in f])
humann_files = sorted([f for f in os.listdir(humann_path) if f.endswith(".tsv") and "pathabundance" in f])
humann_files1 = sorted([f for f in os.listdir(humann_path) if f.endswith(".tsv") and "pathcoverage" in f])

if not abundance_files:
    st.warning("⚠️ No MetaPhlAn abundance files found.")
    st.stop()

if not krona_files:
    st.warning("⚠️ No Krona plot files found.")
    st.stop()

if not humann_files:
    st.warning("⚠️ No HUMAnN Pathway Abundance files found.")
    st.stop()
    
if not humann_files1:
    st.warning("⚠️ No HUMAnN Pathway Coverage files found.")
    st.stop()

# Step 4: Dropdowns for each file type
selected_abundance = st.selectbox("📄 Select MetaPhlAn File", abundance_files)
selected_krona = st.selectbox("🌐 Select Krona HTML Plot", krona_files)
selected_humann = st.selectbox("🧪 Select HUMAnN Pathway Abundance File", humann_files)
selected_humann1 = st.selectbox("🧪 Select HUMAnN Pathway Coverage File", humann_files1)

# Step 5: Construct file paths
metaphlan_file_path = os.path.join(metaphlan_path, selected_abundance)
krona_file_path = os.path.join(krona_path, selected_krona)
humann_file_path = os.path.join(humann_path, selected_humann)
humann_file_path1 = os.path.join(humann_path1, selected_humann1)

# Step 6: Read and parse content with spinner and timer
start_time = time.time()

with st.spinner("🔄 Generating report..."):
    with open(metaphlan_file_path, "r") as mfile:
        diversity_html, tax_df = parse_krona_abundance(mfile)

    taxonomy_html = taxonomic_tables(tax_df)

    with open(humann_file_path, "r") as abundance_file, open(humann_file_path1, "r") as coverage_file:
    	humann_html = parse_metabolite(abundance_file, coverage_file)


    with open(krona_file_path, "r") as kfile:
        krona_html = kfile.read()

    krona_embed = f"""
    <h2 id="krona">🌀 Krona Plot</h2>
    <div style="width: 100%; height: 600px; border: 1px solid #ccc; overflow: hidden;">
        <iframe srcdoc="{krona_html.replace('"', '&quot;')}" 
                width="100%" height="600px" style="border:none;"></iframe>
    </div>
    """

end_time = time.time()
duration = round(end_time - start_time, 2)

# Display success and time taken
st.success(f"✅ Report loaded successfully in {duration} seconds!")


    # ---------------------- Sectioned HTML ----------------------

report_html = f"""
<html><head><style>
body {{
    font-family: Arial, sans-serif;
    margin: 30px;
    padding: 0;
}}

h1, h2, h3 {{
    text-align: center;
    color: #4CAF50;
    margin-bottom: 20px;
}}

h2 {{
    background-color: #FA8BFF;
    background-image: linear-gradient(45deg, #FA8BFF 0%, #2BD2FF 52%, #2BFF88 90%);


    color: white;  /* White text color for contrast */
    padding: 10px;
    border-radius: 5px;
    margin-bottom: 20px;
}}

table {{
    margin: 20px auto;
    border-collapse: collapse;
    width: 95%;
}}

th, td {{
    border: 1px solid #ddd;
    padding: 10px;
    text-align: center;
}}

tr:nth-child(even) {{ background-color: #f9f9f9; }}
tr:hover {{ background-color: #eee; }}
th {{ background-color: #4CAF50; color: white; }}

img {{
    display: block;
    margin: 30px auto;
    max-width: 95%;
}}

.section {{
    margin: 60px 0;
}}

iframe {{
    display: block;
    margin: 0 auto;
    border: none;
}}

a {{
    text-decoration: none;
    color: #1976d2;
}}

.toc {{
    margin: 30px auto;
    text-align: center;
}}

.toc a {{
    margin: 0 10px;
    font-weight: bold;
}}

.logo {{
    position: fixed;  /* Fixes the logo's position relative to the viewport */
    top: 0;           /* Aligns the logo at the top */
    left: 0;          /* Aligns the logo to the left */
    margin: 10px;     /* Optional: Adds spacing from the edges */
    width: 150px;     /* Adjust the width of the logo */
    height: auto;     /* Maintains the aspect ratio */
    z-index: 10;      /* Ensures logo is visible above other elements */
}}

.date-time {{
    position: fixed;
    top: 20px;  /* Adjusted to avoid overlap with the logo */
    right: 10px;
    font-size: 14px;  /* Increased font size for visibility */
    color: black;
    z-index: 10;  /* Ensure it appears on top */
}}
</style></head><body>

<h1>📄 Microbiome Analysis Report</h1>

<div class="date-time">{date}</div>  <!-- Display Date Here -->

<!-- Company Logo -->
{img_tag}

<div class='toc'>
    <h3>🧭 Table of Contents</h3>
    <p>
        <a href="#diversity">🔬 Diversity Indices & Ratios</a> |
        <a href="#taxonomy">🧫 Taxonomic Classification</a> |
        <a href="#krona">🌀 Krona Plot</a> |
        <a href="#functional">🧪 Functional Annotation (HUMAnN)</a>
    </p>
</div>

<div class='section' id='diversity'>
    <h2>🔬 Diversity Indices and Key Ratios</h2>
    {diversity_html}
</div>

<hr style="margin: 50px 0;">

<div class='section' id='taxonomy'>
    <h2>🧫 Taxonomic Classification</h2>
    {taxonomy_html}
</div>

<hr style="margin: 50px 0;">

<div class='section' id='krona'>
    {krona_embed}
</div>

<hr style="margin: 50px 0;">

<div class='section' id='functional'>
    <h2>🧪 Functional Annotation (HUMAnN)</h2>
    {humann_html}
</div>

</body></html>
"""
# Display inside Streamlit
st.components.v1.html(report_html, height=2500, scrolling=True)

# Save HTML to buffer
buffer = BytesIO()
buffer.write(report_html.encode('utf-8'))  # or html_content if that's your variable
buffer.seek(0)

# Construct file name with sample tag
file_name = f"{selected_sample}_report.html"


# Download button
st.download_button(
    label="📥 Download Full Report",
    data=buffer,
    file_name=file_name,
    mime="text/html"
)
