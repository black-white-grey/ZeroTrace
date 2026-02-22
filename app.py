"""
ZeroTrace - Vulnerability Intelligence Platform
100% Offline CVE Scanner with AI-Powered Remediation
"""

import streamlit as st
import pandas as pd
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from database import DatabaseManager
from services import load_cves_from_json, match_assets_to_cves, OllamaService
from ui import (
    get_custom_css,
    render_header,
    render_stat_card,
    render_vulnerability_card,
    render_upload_section,
    render_no_results
)


# Page configuration
st.set_page_config(
    page_title="ZeroTrace - Vulnerability Intelligence",
    page_icon="🔒",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Inject custom CSS
st.markdown(get_custom_css(), unsafe_allow_html=True)

# Initialize session state
if 'db_manager' not in st.session_state:
    st.session_state.db_manager = DatabaseManager(
        db_path=os.path.join(os.path.dirname(__file__), "data", "zerotrace.db")
    )
    st.session_state.db_manager.initialize_database()

if 'cve_loaded' not in st.session_state:
    st.session_state.cve_loaded = False
    
if 'cve_count' not in st.session_state:
    st.session_state.cve_count = 0

if 'matches' not in st.session_state:
    st.session_state.matches = None

if 'assets_df' not in st.session_state:
    st.session_state.assets_df = None


# HEADER
render_header()

# MAIN CONTENT
st.markdown("---")

# Two-column layout for upload sections
col1, col2 = st.columns(2)

with col1:
    st.markdown("### 📊 Load CVE Database")
    st.markdown("<p style='color: #94a3b8; margin-bottom: 1rem;'>Upload a JSON file containing CVE data</p>", 
                unsafe_allow_html=True)
    
    uploaded_json = st.file_uploader(
        "Choose a JSON file",
        type=['json'],
        key='cve_json',
        label_visibility="collapsed"
    )
    
    if uploaded_json:
        col_btn1, col_btn2 = st.columns([1, 1])
        
        with col_btn1:
            if st.button("📥 Load CVEs", use_container_width=True):
                with st.spinner("Loading CVEs into database..."):
                    try:
                        success_count, errors = load_cves_from_json(
                            uploaded_json,
                            st.session_state.db_manager
                        )
                        
                        if success_count > 0:
                            st.session_state.cve_loaded = True
                            st.session_state.cve_count = success_count
                            st.success(f"✅ Successfully loaded {success_count} CVEs!")
                            
                            if errors:
                                with st.expander("⚠️ View warnings"):
                                    for error in errors:
                                        st.warning(error)
                        else:
                            st.error("❌ Failed to load CVEs")
                            if errors:
                                for error in errors[:5]:  # Show first 5 errors
                                    st.error(error)
                    except Exception as e:
                        st.error(f"❌ Error: {str(e)}")
        
        with col_btn2:
            if st.button("🗑️ Clear Database", use_container_width=True):
                st.session_state.db_manager.clear_database()
                st.session_state.cve_loaded = False
                st.session_state.cve_count = 0
                st.session_state.matches = None
                st.info("Database cleared")
    
    # Show database status
    if st.session_state.cve_loaded:
        st.markdown(f"""
            <div style="
                background: #1e293b;
                border: 2px solid #10b981;
                border-radius: 0.5rem;
                padding: 1rem;
                margin-top: 1rem;
                text-align: center;
            ">
                <div style="color: #10b981; font-weight: 700; font-size: 1.1rem;">
                    ✓ Database Ready
                </div>
                <div style="color: #94a3b8; font-size: 0.9rem; margin-top: 0.5rem;">
                    {st.session_state.cve_count} CVEs loaded
                </div>
            </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
            <div style="
                background: #1e293b;
                border: 2px dashed #334155;
                border-radius: 0.5rem;
                padding: 1rem;
                margin-top: 1rem;
                text-align: center;
                color: #64748b;
            ">
                No CVE database loaded
            </div>
        """, unsafe_allow_html=True)

with col2:
    st.markdown("### 📤 Upload Asset Inventory")
    st.markdown("<p style='color: #94a3b8; margin-bottom: 1rem;'>Upload a CSV with columns: software, version</p>", 
                unsafe_allow_html=True)
    
    uploaded_csv = st.file_uploader(
        "Choose a CSV file",
        type=['csv'],
        key='asset_csv',
        label_visibility="collapsed"
    )
    
    if uploaded_csv:
        try:
            assets_df = pd.read_csv(uploaded_csv)
            st.session_state.assets_df = assets_df
            
            st.markdown("""
                <div style="margin-top: 1rem; margin-bottom: 0.5rem;">
                    <span style="color: #10b981; font-weight: 600;">✓ Asset Preview:</span>
                </div>
            """, unsafe_allow_html=True)
            
            st.dataframe(
                assets_df.head(10),
                use_container_width=True,
                height=250
            )
            
            if len(assets_df) > 10:
                st.caption(f"Showing 10 of {len(assets_df)} assets")
                
        except Exception as e:
            st.error(f"❌ Error reading CSV: {str(e)}")
            st.session_state.assets_df = None
    else:
        st.markdown("""
            <div style="
                background: #1e293b;
                border: 2px dashed #334155;
                border-radius: 0.5rem;
                padding: 1rem;
                margin-top: 1rem;
                text-align: center;
                color: #64748b;
            ">
                No asset inventory loaded
            </div>
        """, unsafe_allow_html=True)

# SCAN SECTION
st.markdown("---")

if st.session_state.cve_loaded and st.session_state.assets_df is not None:
    col_scan = st.columns([2, 1, 2])[1]
    
    with col_scan:
        if st.button("🔍 SCAN FOR VULNERABILITIES", use_container_width=True, type="primary"):
            # Step 1: Match assets
            with st.spinner("🔍 Matching assets against CVE database..."):
                try:
                    matches = match_assets_to_cves(
                        st.session_state.assets_df,
                        st.session_state.db_manager
                    )
                    
                    st.session_state.matches = matches
                    
                    if len(matches) == 0:
                        st.info("✅ No vulnerabilities found!")
                    else:
                        st.success(f"Found {len(matches)} vulnerabilities!")
                        
                except Exception as e:
                    st.error(f"❌ Scan error: {str(e)}")
                    st.session_state.matches = pd.DataFrame()
            
            # Step 2: Generate action plans with Ollama
            if st.session_state.matches is not None and len(st.session_state.matches) > 0:
                ollama = OllamaService()
                
                if ollama.is_available():
                    st.info("🤖 Generating AI-powered action plans...")
                    
                    progress_bar = st.progress(0)
                    status_text = st.empty()
                    
                    matches = st.session_state.matches
                    
                    for idx, row in matches.iterrows():
                        status_text.text(f"Processing {idx + 1}/{len(matches)}: {row['cve_id']}")
                        
                        action_plan = ollama.generate_action_plan(row.to_dict())
                        matches.at[idx, 'action_plan'] = action_plan
                        
                        progress_bar.progress((idx + 1) / len(matches))
                    
                    st.session_state.matches = matches
                    status_text.empty()
                    progress_bar.empty()
                    st.success("✅ Action plans generated!")
                else:
                    st.warning("⚠️ Ollama service not available. Scan results will be shown without AI action plans.")
                    st.info("To enable AI action plans, install and start Ollama with llama3 model.")

else:
    st.markdown("""
        <div style="
            background: #1e293b;
            border: 2px dashed #334155;
            border-radius: 1rem;
            padding: 2rem;
            text-align: center;
            color: #64748b;
        ">
            <div style="font-size: 1.2rem; margin-bottom: 0.5rem;">
                📋 Ready to Scan
            </div>
            <div style="font-size: 0.9rem;">
                Upload both a CVE database and asset inventory to begin scanning
            </div>
        </div>
    """, unsafe_allow_html=True)

# RESULTS SECTION
if st.session_state.matches is not None and len(st.session_state.matches) > 0:
    st.markdown("---")
    st.markdown("## 📈 Vulnerability Assessment Results")
    st.markdown("")
    
    matches = st.session_state.matches
    
    # STATISTICS CARDS
    severity_counts = matches['severity'].value_counts().to_dict()
    
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        render_stat_card("Total", len(matches), "total")
    with col2:
        render_stat_card("Critical", severity_counts.get('CRITICAL', 0), "critical")
    with col3:
        render_stat_card("High", severity_counts.get('HIGH', 0), "high")
    with col4:
        render_stat_card("Medium", severity_counts.get('MEDIUM', 0), "medium")
    with col5:
        render_stat_card("Low", severity_counts.get('LOW', 0), "low")
    
    st.markdown("")
    st.markdown("---")
    
    # FILTER SECTION
    st.markdown("### 🔍 Filter Results")
    
    col_filter1, col_filter2 = st.columns([3, 1])
    
    with col_filter1:
        severity_filter = st.multiselect(
            "Filter by Severity",
            ['CRITICAL', 'HIGH', 'MEDIUM', 'LOW'],
            default=['CRITICAL', 'HIGH', 'MEDIUM', 'LOW'],
            key='severity_filter'
        )
    
    with col_filter2:
        sort_by = st.selectbox(
            "Sort by",
            ['Severity', 'CVSS Score', 'CVE ID'],
            key='sort_by'
        )
    
    # Apply filters
    filtered_matches = matches[matches['severity'].isin(severity_filter)].copy()
    
    # Apply sorting
    if sort_by == 'CVSS Score':
        filtered_matches = filtered_matches.sort_values('cvss_score', ascending=False)
    elif sort_by == 'CVE ID':
        filtered_matches = filtered_matches.sort_values('cve_id')
    # Default is already sorted by severity
    
    st.markdown(f"### 📊 Showing {len(filtered_matches)} of {len(matches)} Vulnerabilities")
    st.markdown("")
    
    # VULNERABILITY CARDS
    if len(filtered_matches) > 0:
        for _, vuln in filtered_matches.iterrows():
            render_vulnerability_card(vuln)
    else:
        st.info("No vulnerabilities match the current filters")
    
    # EXPORT SECTION
    st.markdown("---")
    st.markdown("### 📥 Export Results")
    
    col_export1, col_export2, col_export3 = st.columns([1, 1, 2])
    
    with col_export1:
        csv = matches.to_csv(index=False)
        st.download_button(
            label="📄 Export as CSV",
            data=csv,
            file_name="zerotrace_vulnerabilities.csv",
            mime="text/csv",
            use_container_width=True
        )
    
    with col_export2:
        # Export with action plans
        csv_with_plans = matches.to_csv(index=False)
        st.download_button(
            label="📄 Export with Action Plans",
            data=csv_with_plans,
            file_name="zerotrace_full_report.csv",
            mime="text/csv",
            use_container_width=True
        )

elif st.session_state.matches is not None and len(st.session_state.matches) == 0:
    st.markdown("---")
    render_no_results()

# FOOTER
st.markdown("---")
st.markdown("""
    <div style="text-align: center; color: #64748b; padding: 2rem 0;">
        <div style="margin-bottom: 0.5rem;">
            🔒 <strong>ZeroTrace</strong> - 100% Offline Vulnerability Intelligence
        </div>
        <div style="font-size: 0.85rem;">
            All data processing happens locally. No telemetry. No cloud. No tracking.
        </div>
    </div>
""", unsafe_allow_html=True)
