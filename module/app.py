import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import base64
from io import BytesIO
from datetime import datetime

# ---------------------- Utility functions ----------------------

def fig_to_base64(fig):
    buf = BytesIO()
    fig.savefig(buf, format="png", bbox_inches='tight')
    plt.close(fig)
    buf.seek(0)
    return base64.b64encode(buf.read()).decode("utf-8")

def generate_shannon_gauge(value):
    fig, ax = plt.subplots(figsize=(6, 4), subplot_kw={'projection': 'polar'})
    ax.set_theta_offset(np.pi)
    ax.set_theta_direction(-1)
    ax.set_yticklabels([])
    ax.set_xticks([])
    ax.set_thetamin(0)
    ax.set_thetamax(180)
    ax.set_facecolor('white')

    # Shannon diversity ranges (custom)
    color_ranges = [(0.0, 0.3, '#f44336'), (0.3, 0.7, '#ffeb3b'), (0.7, 1.0, '#4caf50')]
    for start, end, color in color_ranges:
        theta = np.linspace(start * np.pi, end * np.pi, 30)
        ax.plot(theta, [1] * len(theta), color=color, linewidth=10)

    # Normalize based on max 5
    angle = (1 - value / 5) * np.pi
    ax.plot([angle, angle], [0, 1], color='black', linewidth=3)

    fig.subplots_adjust(bottom=0.3)
    fig.text(0.5, 0.1, f"{value:.3f}", ha='center', va='center', fontsize=12)
    fig.text(0.5, 0.05, "Shannon Index", ha='center', va='center', fontsize=11)

    return f'<div style="margin: 30px auto; text-align:center;"><img src="data:image/png;base64,{fig_to_base64(fig)}" style="max-width:350px;"></div>'

def generate_simpson_gauge(value):
    scaled_value = value * 5  # Scale to match 0–5 display
    fig, ax = plt.subplots(figsize=(6, 4), subplot_kw={'projection': 'polar'})
    ax.set_theta_offset(np.pi)
    ax.set_theta_direction(-1)
    ax.set_yticklabels([])
    ax.set_xticks([])
    ax.set_thetamin(0)
    ax.set_thetamax(180)
    ax.set_facecolor('white')

    # Simpson diversity ranges
    color_ranges = [(0.0, 0.3, '#f44336'), (0.3, 0.7, '#ffeb3b'), (0.7, 1.0, '#4caf50')]
    for start, end, color in color_ranges:
        theta = np.linspace(start * np.pi, end * np.pi, 30)
        ax.plot(theta, [1] * len(theta), color=color, linewidth=10)

    angle = (1 - scaled_value / 5) * np.pi
    ax.plot([angle, angle], [0, 1], color='black', linewidth=3)

    fig.subplots_adjust(bottom=0.3)
    fig.text(0.5, 0.1, f"{value:.3f}", ha='center', va='center', fontsize=12)
    fig.text(0.5, 0.05, "Simpson Index", ha='center', va='center', fontsize=11)

    return f'<div style="margin: 30px auto; text-align:center;"><img src="data:image/png;base64,{fig_to_base64(fig)}" style="max-width:350px;"></div>'

def generate_fb_ratio_gauge(value):
    # Scale F/B value for gauge display (we assume 10 as max for scaling)
    scaled_value = min(value / 10, 1.0)  # Normalize to 0–1 range
    fig, ax = plt.subplots(figsize=(6, 4), subplot_kw={'projection': 'polar'})
    ax.set_theta_offset(np.pi)
    ax.set_theta_direction(-1)
    ax.set_yticklabels([])
    ax.set_xticks([])
    ax.set_thetamin(0)
    ax.set_thetamax(180)
    ax.set_facecolor('white')

    # Color-coded ranges (red-yellow-green)
    color_ranges = [(0.0, 0.3, '#f44336'), (0.3, 0.7, '#ffeb3b'), (0.7, 1.0, '#4caf50')]
    for start, end, color in color_ranges:
        theta = np.linspace(start * np.pi, end * np.pi, 30)
        ax.plot(theta, [1] * len(theta), color=color, linewidth=10)

    # Needle
    angle = scaled_value * np.pi  # Full right (good) is π, full left is 0
    ax.plot([angle, angle], [0, 1], color='black', linewidth=3)

    # Text annotations
    fig.subplots_adjust(bottom=0.3)
    fig.text(0.5, 0.1, f"{value:.3f}", ha='center', va='center', fontsize=12)
    fig.text(0.5, 0.05, "F/B Ratio", ha='center', va='center', fontsize=11)

    return f'<div style="margin: 30px auto; text-align:center;"><img src="data:image/png;base64,{fig_to_base64(fig)}" style="max-width:350px;"></div>'



# ---------------------- Parsing functions ----------------------

def parse_krona_abundance(file):
    df = pd.read_csv(file, sep="\t", comment='#', header=None,
                     names=["clade_name", "relative_abundance", "coverage", "genome_length", "reads"])
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

    df["Taxon"], df["Level"] = zip(*df["clade_name"].map(extract_taxon))

    proportions = df["reads"] / df["reads"].sum()
    shannon = -np.sum(proportions * np.log(proportions))
    simpson = 1 - np.sum((proportions) ** 2)

    def get_phylum_abundance(phylum):
        match = df[df["clade_name"].str.contains(f"p__{phylum}")]
        return match["relative_abundance"].sum()

    firm = get_phylum_abundance("Firmicutes")
    bact = get_phylum_abundance("Bacteroidetes")
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

def parse_prokka(file):
    try:
        df = pd.read_csv(file, sep="\t", comment="#")
        if "product" not in df.columns:
            return "<p><b>Prokka Error:</b> 'product' column missing.</p>"

        df_all = df[df["product"].notna()]
        df_clean = df_all[~df_all["product"].str.contains("hypothetical protein", case=False)]
        prod_counts = df_clean["product"].value_counts().reset_index()
        prod_counts.columns = ["Product", "Count"]
        prod_counts["Rank"] = np.arange(1, len(prod_counts)+1)

        fig, ax = plt.subplots(figsize=(10, 6))
        ax.barh(prod_counts["Product"].head(10), prod_counts["Count"].head(10), color="#ab47bc")
        ax.set_title("Top Functional Products (Prokka)", fontsize=16, color='#333')
        fig.tight_layout()
        img_html = f"<img src='data:image/png;base64,{fig_to_base64(fig)}' style='max-width:100%; margin:0 auto;'>"

        table = df_all['product'].value_counts().reset_index()
        table.columns = ["Product", "Count"]
        table["Rank"] = table.index + 1
        table = table[["Rank", "Product", "Count"]].to_html(index=False, header=True)

        return f"{table}{img_html}"


    except Exception as e:
        return f"<p>Error parsing Prokka: {e}</p>"
        


# Date and Time
date = datetime.now().strftime("%B %d, %Y %H:%M:%S")  # Current date and time in the format: Month Day, Year Hour:Minute:Second

# File path for the logo
logo_path = "/home/ghadmin/Downloads/company_logo.png"  # Update with your actual path

# Base64 encode the image
with open(logo_path, "rb") as img_file:
    encoded_logo = base64.b64encode(img_file.read()).decode("utf-8")

# Create img tag with base64 encoded logo
img_tag = f'<img src="data:image/png;base64,{encoded_logo}" alt="Company Logo" class="logo">'

# Add date and time
date_time_tag = f'<div class="date-time">{date}</div>'

# ---------------------- Streamlit UI ----------------------

st.set_page_config(page_title="Microbiome HTML Report Generator", layout="wide")
st.title("🧬 Microbiome Report Generator")

metaphlan_file = st.file_uploader("Upload MetaPhlAn File", type=["txt", "tsv"])
prokka_file = st.file_uploader("Upload Prokka TSV File", type=["tsv"])
krona_file = st.file_uploader("Upload Krona Plot HTML File", type=["html"])
sample_name = st.text_input("Enter Sample Name", value="Sample_1")

if not (krona_file and metaphlan_file and prokka_file):
    st.warning("Please upload all three files (MetaPhlAn, Prokka, Krona).")
else:
    st.success("✅ Files uploaded successfully!")

    # Continue with the rest of the code only if all files are uploaded
    diversity_html, tax_df = parse_krona_abundance(metaphlan_file)
    taxonomy_html = taxonomic_tables(tax_df)
    prokka_html = parse_prokka(prokka_file)

    krona_embed = ""
    if krona_file:
        krona_html = krona_file.getvalue().decode("utf-8")
        krona_embed = f"""
        <h2 id="krona">🌀 Krona Plot</h2>
        <div style="width: 100%; height: 600px; border: 1px solid #ccc; overflow: hidden;">
            <iframe srcdoc="{krona_html.replace('"', '&quot;')}" 
                    width="100%" height="600px" style="border:none;"></iframe>
        </div>
        """
    else:
        krona_embed = "<h2 id='krona'>🌀 Krona Plot</h2><p style='text-align:center;'>No Krona file uploaded.</p>"


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
<img src="company_logo.png" alt="Company Logo" class="logo">

<div class='toc'>
    <h3>🧭 Table of Contents</h3>
    <p>
        <a href="#diversity">🔬 Diversity Indices & Ratios</a> |
        <a href="#taxonomy">🧫 Taxonomic Classification</a> |
        <a href="#krona">🌀 Krona Plot</a> |
        <a href="#functional">🧪 Functional Annotation (Prokka)</a>
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
    <h2>🧪 Functional Annotation (Prokka)</h2>
    {prokka_html}
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
file_name = f"{sample_name}_metagenomic_report.html"

# Download button
st.download_button(
    label="📥 Download Full Report",
    data=buffer,
    file_name=file_name,
    mime="text/html"
)



