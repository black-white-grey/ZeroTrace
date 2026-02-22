"""
UI Components for ZeroTrace
Reusable UI elements for the Streamlit app
"""

import streamlit as st


def render_header():
    """Render ZeroTrace header with logo and offline badge"""
    st.markdown("""
        <div class="zerotrace-header">
            <div class="zerotrace-logo">
                🔒 ZeroTrace
            </div>
            <div class="zerotrace-tagline">
                Vulnerability Intelligence that leaves no trace
            </div>
            <div class="offline-badge">
                🛡️ 100% OFFLINE - No data leaves your device
            </div>
        </div>
    """, unsafe_allow_html=True)


def render_severity_badge(severity: str) -> str:
    """
    Render severity badge HTML
    
    Args:
        severity: Severity level (CRITICAL, HIGH, MEDIUM, LOW)
        
    Returns:
        HTML string for badge
    """
    severity = severity.upper()
    badge_class = f"badge-{severity.lower()}"
    
    return f'<span class="severity-badge {badge_class}">{severity}</span>'


def render_stat_card(label: str, count: int, severity: str):
    """
    Render statistics card
    
    Args:
        label: Card label
        count: Number to display
        severity: Severity type for styling (total, critical, high, medium, low)
    """
    st.markdown(f"""
        <div class="stat-card {severity.lower()}">
            <div class="stat-number">{count}</div>
            <div class="stat-label">{label}</div>
        </div>
    """, unsafe_allow_html=True)


def render_vulnerability_card(vuln_data):
    """
    Render detailed vulnerability card
    
    Args:
        vuln_data: Dictionary or Series with vulnerability information
    """
    # Extract data
    cve_id = vuln_data['cve_id']
    severity = vuln_data['severity']
    software = vuln_data['software']
    version = vuln_data['version']
    description = vuln_data['description']
    cvss_score = vuln_data.get('cvss_score', 'N/A')
    action_plan = vuln_data.get('action_plan', '')
    
    # Build the card HTML
    severity_badge = render_severity_badge(severity)
    
    card_html = f"""
    <div class="vuln-card">
        <div class="vuln-header">
            <div class="vuln-cve-id">{cve_id}</div>
            <div>{severity_badge}</div>
        </div>
        
        <div class="vuln-software">
            <span class="vuln-software-name">{software}</span> version {version}
        </div>
        
        <div class="vuln-cvss">
            CVSS Score: {cvss_score}
        </div>
        
        <div class="vuln-description">
            {description}
        </div>
    """
    
    # Add action plan if available
    if action_plan and not action_plan.startswith('⚠️'):
        card_html += f"""
        <div class="action-plan">
            <div class="action-plan-header">
                🤖 AI-Generated Action Plan
            </div>
            <div class="action-plan-content">
                {action_plan}
            </div>
        </div>
        """
    elif action_plan:
        # Show warning/error message
        card_html += f"""
        <div style="margin-top: 1rem; padding: 1rem; background: #1e293b; border-radius: 0.5rem; color: #eab308;">
            {action_plan}
        </div>
        """
    
    card_html += "</div>"
    
    st.markdown(card_html, unsafe_allow_html=True)


def render_upload_section(title: str, description: str, file_type: str, key: str):
    """
    Render file upload section with custom styling
    
    Args:
        title: Section title
        description: Description text
        file_type: File type to accept
        key: Unique key for uploader
        
    Returns:
        Uploaded file object or None
    """
    st.markdown(f"### {title}")
    st.markdown(f"<p style='color: #94a3b8; margin-bottom: 1rem;'>{description}</p>", 
                unsafe_allow_html=True)
    
    uploaded_file = st.file_uploader(
        f"Choose a {file_type.upper()} file",
        type=[file_type],
        key=key,
        label_visibility="collapsed"
    )
    
    return uploaded_file


def render_no_results():
    """Render no results found message"""
    st.markdown("""
        <div style="
            background: #1e293b;
            border: 2px solid #10b981;
            border-radius: 1rem;
            padding: 3rem;
            text-align: center;
            margin: 2rem 0;
        ">
            <div style="font-size: 3rem; margin-bottom: 1rem;">✅</div>
            <div style="font-size: 1.5rem; font-weight: 700; color: #10b981; margin-bottom: 0.5rem;">
                No Vulnerabilities Detected
            </div>
            <div style="color: #94a3b8;">
                Your assets appear to be secure based on the loaded CVE database.
            </div>
        </div>
    """, unsafe_allow_html=True)


def render_loading_message(message: str):
    """Render custom loading message"""
    st.markdown(f"""
        <div style="
            background: #1e293b;
            border: 2px solid #3b82f6;
            border-radius: 0.75rem;
            padding: 1.5rem;
            text-align: center;
            color: #3b82f6;
        ">
            <div style="font-size: 1.2rem; font-weight: 600;">
                {message}
            </div>
        </div>
    """, unsafe_allow_html=True)
