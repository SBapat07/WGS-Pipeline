import streamlit as st
import os
import base64
from streamlit_extras.switch_page_button import switch_page


# ---- PAGE CONFIGURATION ----
st.set_page_config(page_title="ISHA Pipeline Dashboard", layout="wide")

# ---- CSS for Styling ----
st.markdown("""
    <style>
    .center-text {
        text-align: center;
    }
    div.stButton > button {
        height: 160px;
        width: 230px;
        border-radius: 18px;
        font-size: 22px;
        font-weight: bold;
        margin: 12px;
        background: linear-gradient(135deg, #6e8efb, #a777e3);
        color: #f5f5f5;
        border: none;
        transition: 0.4s;
        box-shadow: 0 6px 15px rgba(0,0,0,0.3);
    }
    div.stButton > button:hover {
        background: linear-gradient(135deg, #a777e3, #6e8efb);
        color: black;
        font-weight: 900;
        box-shadow: 0 12px 24px rgba(0,0,0,0.4);
        transform: scale(1.08);
        cursor: pointer;
    }
    </style>
""", unsafe_allow_html=True)


# ---- STATE MANAGEMENT ----
if 'page' not in st.session_state:
    st.session_state.page = 'main'

# ---- PATH TO MAIN MULTIQC FOLDER ----
MULTIQC_MAIN_FOLDER = "/home/rdadmin/Desktop/ShreyasWGS_Pipeline/WGS_Pipeline/Results/MultiQC_result" 

KRONA_MAIN_FOLDER = "/home/rdadmin/Desktop/ShreyasWGS_Pipeline/WGS_Pipeline/Results/Krona_result" 

# ---- FUNCTIONS ----

def multiqc_page():
    st.markdown("<h2 class='center-text'>MultiQC Report Viewer</h2>", unsafe_allow_html=True)
    st.markdown("### Select a sample ID to display the MultiQC report")

    # Get list of sample folders
    sample_folders = sorted([
        folder for folder in os.listdir(MULTIQC_MAIN_FOLDER)
        if os.path.isdir(os.path.join(MULTIQC_MAIN_FOLDER, folder))
    ])

    # Add default dropdown option
    sample_options = ["Select a sample ID to display report"] + sample_folders
    selected_sample = st.selectbox("Sample ID", sample_options)

    if selected_sample != "Select a sample ID to display report":
        sample_folder = os.path.join(MULTIQC_MAIN_FOLDER, selected_sample)
        html_files = [
            f for f in os.listdir(sample_folder)
            if f.endswith(".html") and "multiqc" in f.lower()
        ]

        if html_files:
            found_html = os.path.join(sample_folder, html_files[0])

            with st.spinner('Loading MultiQC report...'):
                progress_text = "Fetching and rendering the report..."
                my_bar = st.progress(0, text=progress_text)

                import time
                for percent_complete in range(0, 101, 10):
                    time.sleep(0.05)
                    my_bar.progress(percent_complete, text=progress_text)

                # Change text just before clearing the progress bar
                my_bar.progress(100, text="✅ Report fully loaded!")
                time.sleep(0.5)  # Brief pause to show success message
                my_bar.empty()  # Clear the bar

            st.success(f"MultiQC report loaded for Sample ID: {selected_sample}")
            st.warning("⚠️ **Please do not click on sections in the MultiQC report.** Instead, scroll to the desired content to view the information.")

            with open(found_html, 'r', encoding='utf-8') as f:
                html_content = f.read()
            st.components.v1.html(html_content, height=900, scrolling=True)
        else:
            st.error(f"No MultiQC report found in folder for Sample ID: {selected_sample}")

    if st.button("⬅️ Back to Dashboard"):
        st.session_state.page = 'main'
        st.rerun()

def krona_page():
    st.markdown("<h2 class='center-text'>Krona Plot Viewer</h2>", unsafe_allow_html=True)
    st.markdown("### Select a sample ID to display the Krona plot")


    # Get list of sample folders based on strict filtering
    sample_folders = sorted([
        folder for folder in os.listdir(KRONA_MAIN_FOLDER)
        if os.path.isdir(os.path.join(KRONA_MAIN_FOLDER, folder))
        and folder.lower().endswith("abundance")  # Ends with abundance
    ])

    # Add default dropdown option
    sample_options = ["Select a sample ID to display plot"] + sample_folders
    selected_sample = st.selectbox("Sample ID", sample_options)

    if selected_sample != "Select a sample ID to display plot":
        sample_folder = os.path.join(KRONA_MAIN_FOLDER, selected_sample)
        html_files = [
            f for f in os.listdir(sample_folder)
            if f.endswith(".html") and "krona" in f.lower()
        ]

        if html_files:
            found_html = os.path.join(sample_folder, html_files[0])

            with st.spinner('Loading Krona plot...'):
                progress_text = "Fetching and rendering the plot..."
                my_bar = st.progress(0, text=progress_text)

                import time
                for percent_complete in range(0, 101, 10):
                    time.sleep(0.05)
                    my_bar.progress(percent_complete, text=progress_text)

                # Before removing bar
                my_bar.progress(100, text="✅ Plot fully loaded!")
                time.sleep(0.5)
                my_bar.empty()

            st.success(f"Krona plot loaded for Sample ID: {selected_sample}")
            st.warning("⚠️ **Krona plots are interactive.** You can click to zoom into taxonomic levels.")

            with open(found_html, 'r', encoding='utf-8') as f:
                html_content = f.read()

            # Add white background
            html_content = f"""
            <style>
                body {{
                    background-color: white !important;
                }}
            </style>
            {html_content}
            """

            st.components.v1.html(html_content, height=900, scrolling=True)

        else:
            st.error(f"No Krona plot found in folder for Sample ID: {selected_sample}")

    if st.button("⬅️ Back to Dashboard"):
        st.session_state.page = 'main'
        st.rerun()
        
def about_page():
    st.markdown("<h2 class='center-text'>About the Pipeline</h2>", unsafe_allow_html=True)
    
    about_text = """
    ### 🔬 Purpose:
    This pipeline is designed for analyzing Whole Genome Shotgun (WGS) metagenomic sequencing data, particularly from human gut microbiota. It performs quality control, taxonomic profiling, functional annotation, and metabolic pathway prediction.

    ### 🧰 Tools & Modules Included:
    - **FASTQC** – Quality check of raw reads  
    - **Fastp** – Read trimming and filtering  
    - **MultiQC** – Aggregated QC reports  
    - **BWA** – Host genome alignment and filtering  
    - **MetaPhlAn** – Taxonomic profiling  
    - **Krona** – Interactive taxonomic visualization  
    - **HUMAnN** – Functional profiling and pathway prediction    

    ### 📦 Output Highlights:
    - Quality control reports  
    - Abundance tables (taxonomic and functional)  
    - Interactive charts (bar graphs, pie charts, Krona plots)  
    - Predicted metabolic pathways and associated metabolites  
    - Final HTML report with all integrated outputs  

    ### 📁 Technologies Used:
    - Nextflow DSL2  
    - Docker & Conda for reproducibility  
    - Python (Streamlit UI + Reporting)  

    **Created by:** Shreyas S. Bapat  
    **Version:** 1.0  
    """
    
    st.markdown(about_text)
    
    if st.button("⬅️ Back to Dashboard"):
        st.session_state.page = 'main'
        st.rerun()

def main_dashboard():
    st.markdown("<h1 class='center-text'>ISHA Pipeline Dashboard</h1>", unsafe_allow_html=True)
    st.markdown("<h4 class='center-text'>Welcome to ISHA (Integrated Suite for Human microbiome Analysis pipeline) – a complete pipeline for analyzing human gut metagenomic data.</h4>", unsafe_allow_html=True)
    st.markdown("---")

    # 4 Columns for buttons
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        if st.button("MultiQC"):
            st.session_state.page = 'multiqc'
            st.rerun()

    with col2:
    	if st.button("Krona Plot"):
    		st.session_state.page = 'krona'
    		st.rerun()

    with col3:
        if st.button("Report Generation"):
        	st.write("This feture is available in another app. This app will be found in the left side tab. Click on 'Report Generator App' to generate the report.")
        	

    with col4:
        if st.button("About"):
        	st.session_state.page = 'about'
        	st.rerun()

# ---- PAGE ROUTER ----
if st.session_state.page == 'main':
    main_dashboard()
elif st.session_state.page == 'multiqc':
    multiqc_page()
elif st.session_state.page == 'krona':
    krona_page()
elif st.session_state.page == 'about':
    about_page()

