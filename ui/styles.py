"""
Custom CSS Styles for ZeroTrace
Dark security-themed UI
"""


def get_custom_css() -> str:
    """
    Returns custom CSS for dark security theme
    
    Returns:
        CSS string to inject into Streamlit app
    """
    return """
    <style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&family=JetBrains+Mono&display=swap');
    
    /* Global theme overrides */
    .stApp {
        background-color: #0f172a;
        color: #f1f5f9;
        font-family: 'Inter', sans-serif;
    }
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Headers */
    h1, h2, h3, h4, h5, h6 {
        color: #f1f5f9 !important;
        font-weight: 700 !important;
    }
    
    /* ZeroTrace header */
    .zerotrace-header {
        background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%);
        padding: 2rem;
        border-radius: 1rem;
        margin-bottom: 2rem;
        border: 2px solid #334155;
        text-align: center;
    }
    
    .zerotrace-logo {
        font-size: 3rem;
        font-weight: 700;
        color: #10b981;
        margin-bottom: 0.5rem;
        text-shadow: 0 0 20px rgba(16, 185, 129, 0.3);
    }
    
    .zerotrace-tagline {
        font-size: 1.2rem;
        color: #94a3b8;
        margin-bottom: 1rem;
        font-style: italic;
    }
    
    /* Offline badge */
    .offline-badge {
        background: linear-gradient(135deg, #10b981 0%, #059669 100%);
        color: #0f172a;
        padding: 0.6rem 1.5rem;
        border-radius: 2rem;
        font-weight: 700;
        display: inline-block;
        box-shadow: 0 4px 15px rgba(16, 185, 129, 0.3);
        font-size: 0.9rem;
        letter-spacing: 0.5px;
    }
    
    /* Severity badges */
    .severity-badge {
        display: inline-block;
        padding: 0.4rem 1rem;
        border-radius: 0.5rem;
        font-weight: 700;
        font-size: 0.85rem;
        text-transform: uppercase;
        letter-spacing: 1px;
        color: #ffffff;
    }
    
    .badge-critical {
        background: linear-gradient(135deg, #dc2626 0%, #991b1b 100%);
        box-shadow: 0 2px 10px rgba(220, 38, 38, 0.4);
    }
    
    .badge-high {
        background: linear-gradient(135deg, #ea580c 0%, #c2410c 100%);
        box-shadow: 0 2px 10px rgba(234, 88, 12, 0.4);
    }
    
    .badge-medium {
        background: linear-gradient(135deg, #eab308 0%, #a16207 100%);
        box-shadow: 0 2px 10px rgba(234, 179, 8, 0.4);
    }
    
    .badge-low {
        background: linear-gradient(135deg, #3b82f6 0%, #1d4ed8 100%);
        box-shadow: 0 2px 10px rgba(59, 130, 246, 0.4);
    }
    
    /* Statistics cards */
    .stat-card {
        background: #1e293b;
        border-radius: 0.75rem;
        padding: 1.5rem;
        text-align: center;
        border-left: 5px solid;
        transition: transform 0.2s, box-shadow 0.2s;
    }
    
    .stat-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.4);
    }
    
    .stat-card.total {
        border-left-color: #10b981;
    }
    
    .stat-card.critical {
        border-left-color: #dc2626;
    }
    
    .stat-card.high {
        border-left-color: #ea580c;
    }
    
    .stat-card.medium {
        border-left-color: #eab308;
    }
    
    .stat-card.low {
        border-left-color: #3b82f6;
    }
    
    .stat-number {
        font-size: 2.5rem;
        font-weight: 700;
        color: #f1f5f9;
        margin-bottom: 0.5rem;
    }
    
    .stat-label {
        font-size: 0.9rem;
        color: #94a3b8;
        text-transform: uppercase;
        letter-spacing: 1px;
        font-weight: 600;
    }
    
    /* Vulnerability cards */
    .vuln-card {
        background: #1e293b;
        border: 2px solid #334155;
        border-radius: 1rem;
        padding: 1.5rem;
        margin-bottom: 1.5rem;
        transition: all 0.3s;
    }
    
    .vuln-card:hover {
        transform: translateY(-2px);
        border-color: #10b981;
        box-shadow: 0 8px 25px rgba(16, 185, 129, 0.2);
    }
    
    .vuln-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 1rem;
    }
    
    .vuln-cve-id {
        font-size: 1.2rem;
        font-weight: 700;
        color: #10b981;
        font-family: 'JetBrains Mono', monospace;
    }
    
    .vuln-software {
        font-size: 1rem;
        color: #cbd5e1;
        margin-bottom: 0.5rem;
    }
    
    .vuln-software-name {
        font-weight: 600;
        color: #f1f5f9;
    }
    
    .vuln-description {
        color: #94a3b8;
        line-height: 1.6;
        margin: 1rem 0;
        padding: 1rem;
        background: #0f172a;
        border-radius: 0.5rem;
        border-left: 3px solid #334155;
    }
    
    .vuln-cvss {
        display: inline-block;
        padding: 0.3rem 0.8rem;
        background: #334155;
        border-radius: 0.5rem;
        font-size: 0.85rem;
        color: #cbd5e1;
        font-family: 'JetBrains Mono', monospace;
    }
    
    /* Action plan section */
    .action-plan {
        background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%);
        border: 2px solid #10b981;
        border-radius: 0.75rem;
        padding: 1.5rem;
        margin-top: 1rem;
    }
    
    .action-plan-header {
        font-size: 1rem;
        font-weight: 700;
        color: #10b981;
        margin-bottom: 1rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    
    .action-plan-content {
        color: #e2e8f0;
        line-height: 1.8;
        white-space: pre-wrap;
    }
    
    /* File uploader styling */
    .stFileUploader {
        background: #1e293b;
        border: 2px dashed #334155;
        border-radius: 0.75rem;
        padding: 1rem;
    }
    
    .stFileUploader:hover {
        border-color: #10b981;
    }
    
    /* Buttons */
    .stButton > button {
        background: linear-gradient(135deg, #10b981 0%, #059669 100%);
        color: #ffffff;
        font-weight: 700;
        border: none;
        border-radius: 0.5rem;
        padding: 0.75rem 2rem;
        transition: all 0.3s;
        box-shadow: 0 4px 15px rgba(16, 185, 129, 0.3);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(16, 185, 129, 0.4);
    }
    
    /* Data frames */
    .stDataFrame {
        background: #1e293b;
        border-radius: 0.5rem;
    }
    
    /* Expander */
    .streamlit-expanderHeader {
        background: #1e293b;
        color: #f1f5f9;
        border-radius: 0.5rem;
    }
    
    /* Progress bar */
    .stProgress > div > div > div {
        background: linear-gradient(90deg, #10b981 0%, #059669 100%);
    }
    
    /* Multiselect */
    .stMultiSelect {
        background: #1e293b;
        border-radius: 0.5rem;
    }
    
    /* Success/Warning/Error messages */
    .stSuccess {
        background: #1e293b;
        border-left: 4px solid #10b981;
        color: #10b981;
    }
    
    .stWarning {
        background: #1e293b;
        border-left: 4px solid #eab308;
        color: #eab308;
    }
    
    .stError {
        background: #1e293b;
        border-left: 4px solid #dc2626;
        color: #dc2626;
    }
    
    /* Section dividers */
    hr {
        border-color: #334155;
        margin: 2rem 0;
    }
    </style>
    """
