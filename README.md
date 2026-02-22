# 🔒 ZeroTrace

**Vulnerability Intelligence that leaves no trace**

ZeroTrace is a 100% offline vulnerability scanner that matches your software assets against CVE databases and generates AI-powered remediation plans using local LLMs. All data stays on your device - no cloud, no telemetry, no tracking.

![License](https://img.shields.io/badge/license-MIT-green)
![Python](https://img.shields.io/badge/python-3.8+-blue)
![Offline](https://img.shields.io/badge/status-100%25%20offline-success)

## ✨ Features

- 📊 **CVE Database Management** - Load CVE data from JSON files into local SQLite database
- 📤 **Asset Inventory Upload** - Upload your software inventory via CSV (software, version)
- 🔍 **Intelligent Matching** - SQL-based vulnerability matching with exact version comparison
- 🤖 **AI Action Plans** - Generate remediation guidance using Ollama (Llama3) - 100% local
- 📈 **Clean Dashboard** - Severity-based filtering with color-coded badges (Critical/High/Medium/Low)
- 🎨 **Dark Security Theme** - Professional dark UI optimized for security workflows
- 🛡️ **100% Offline** - All processing happens locally, no data ever leaves your device
- 📥 **Export Results** - Download vulnerability reports with action plans as CSV

## 🚀 Quick Start

### Prerequisites

1. **Python 3.8+** - [Download Python](https://www.python.org/downloads/)
2. **Ollama with Llama3** (for AI action plans) - [Install Ollama](https://ollama.ai/)

### Installation

1. **Clone or download ZeroTrace**
   ```bash
   cd zerotrace
   ```

2. **Install Python dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Install and start Ollama** (optional but recommended)
   ```bash
   # Install Ollama from https://ollama.ai/
   
   # Pull Llama3 model
   ollama pull llama3
   
   # Start Ollama (usually runs automatically)
   ollama serve
   ```

### Running ZeroTrace

```bash
streamlit run app.py
```

The application will open in your default browser at `http://localhost:8501`

## 📖 Usage Guide

### 1. Load CVE Database

- Click **"Load CVE Database"** section
- Upload a JSON file containing CVE data (see format below)
- Click **"Load CVEs"** button
- Wait for confirmation that CVEs are loaded

**Sample CVE JSON Format:**
```json
{
  "cves": [
    {
      "cve_id": "CVE-2024-1234",
      "description": "Critical buffer overflow vulnerability...",
      "severity": "CRITICAL",
      "cvss_score": 9.8,
      "published_date": "2024-01-15",
      "affected_products": [
        {"software": "Apache HTTP Server", "version": "2.4.1"}
      ]
    }
  ]
}
```

**Sample data provided:** `data/sample_cves.json` contains 21 CVE entries for testing

### 2. Upload Asset Inventory

- Click **"Upload Asset Inventory"** section
- Upload a CSV file with columns: `software`, `version`
- Preview your assets in the table

**Sample CSV Format:**
```csv
software,version
Apache HTTP Server,2.4.1
PostgreSQL,13.0
Node.js,16.14.0
```

**Sample data provided:** `data/sample_assets.csv` contains 15 sample assets

### 3. Scan for Vulnerabilities

- Click the **"SCAN FOR VULNERABILITIES"** button
- ZeroTrace will:
  1. Match your assets against the CVE database using SQL
  2. Generate AI-powered action plans for each vulnerability (if Ollama is running)
  3. Display results in the dashboard

### 4. Review Results

The dashboard shows:
- **Statistics cards** - Total vulnerabilities by severity
- **Filtering options** - Filter by severity level
- **Vulnerability cards** - Detailed information for each match:
  - CVE ID and severity badge
  - Affected software and version
  - CVSS score
  - Full description
  - AI-generated 3-step action plan

### 5. Export Results

- Click **"Export as CSV"** to download basic vulnerability report
- Click **"Export with Action Plans"** to include AI-generated remediation steps

## 🗂️ Project Structure

```
zerotrace/
├── app.py                      # Main Streamlit application
├── requirements.txt            # Python dependencies
├── README.md                   # This file
│
├── database/
│   ├── __init__.py
│   ├── db_manager.py          # SQLite operations (CRUD, matching)
│   └── schema.sql             # Database schema
│
├── services/
│   ├── __init__.py
│   ├── cve_loader.py          # Load CVE JSON → SQLite
│   ├── asset_matcher.py       # Match assets against CVEs
│   └── ollama_service.py      # Generate action plans with Llama3
│
├── ui/
│   ├── __init__.py
│   ├── styles.py              # Dark security-themed CSS
│   └── components.py          # Reusable UI components
│
└── data/
    ├── sample_cves.json       # Sample CVE data (21 entries)
    ├── sample_assets.csv      # Sample asset inventory (15 entries)
    └── zerotrace.db           # SQLite database (auto-generated)
```

## 🔧 Technical Details

### Database Schema

- **cves** - Stores CVE metadata (ID, description, severity, CVSS score)
- **affected_products** - Links CVEs to affected software/versions (normalized)
- **scan_results** - Optional table for scan history
- **Indexes** - Optimized for fast lookups on software+version and severity

### Matching Algorithm

1. Normalizes asset data (lowercase, trim whitespace)
2. Performs SQL INNER JOIN on software name and version
3. Case-insensitive exact string matching (Phase 1)
4. Results sorted by severity (CRITICAL → HIGH → MEDIUM → LOW)

**Future enhancements:** Semantic versioning, range matching (e.g., ">=2.4.0, <2.4.50")

### AI Action Plan Generation

- Uses Ollama API running locally at `http://localhost:11434`
- Model: Llama3 (configurable)
- Prompt engineering: Provides CVE context and requests 3-step remediation plan
- Graceful degradation if Ollama is unavailable

### Security & Privacy

- **100% Offline** - No external API calls except localhost Ollama
- **No Telemetry** - Zero data collection or analytics
- **Local Storage** - All data stored in local SQLite database
- **Open Source** - Full transparency, audit the code yourself

## 📊 CVE Data Sources

ZeroTrace requires CVE data in JSON format. You can obtain CVE data from:

1. **National Vulnerability Database (NVD)**
   - [https://nvd.nist.gov/developers/vulnerabilities](https://nvd.nist.gov/developers/vulnerabilities)
   - Download CVE feeds and convert to ZeroTrace JSON format

2. **CVE Program**
   - [https://www.cve.org/](https://www.cve.org/)
   - Official CVE database

3. **Custom Sources**
   - Internal security databases
   - Threat intelligence feeds
   - Security vendor reports

**Note:** You'll need to convert data to ZeroTrace's JSON format (see Usage Guide)

## 🛠️ Configuration

### Change Ollama Model

Edit `services/ollama_service.py`:
```python
def __init__(self, base_url="http://localhost:11434", model="llama3"):
    self.model = "llama3.1"  # Change to your preferred model
```

### Adjust Ollama Settings

Edit temperature and token limits in `ollama_service.py`:
```python
"options": {
    "temperature": 0.7,  # 0.0 = deterministic, 1.0 = creative
    "num_predict": 300   # Max tokens to generate
}
```

### Database Location

Edit database path in `app.py`:
```python
st.session_state.db_manager = DatabaseManager(
    db_path="path/to/your/database.db"
)
```

## 🐛 Troubleshooting

### Ollama Connection Issues

**Error:** "Ollama service unavailable"

**Solutions:**
1. Check if Ollama is running: `ollama list`
2. Start Ollama: `ollama serve`
3. Verify model is installed: `ollama pull llama3`
4. Check port 11434 is not blocked

### CVE Load Failures

**Error:** "Invalid JSON format"

**Solutions:**
1. Validate JSON syntax using jsonlint.com
2. Ensure JSON has root-level "cves" array
3. Check all required fields are present (cve_id, description, severity, affected_products)

### No Vulnerabilities Found

**Possible causes:**
1. Version mismatch - CVE database uses different version format
2. Software name mismatch - Check exact spelling and capitalization
3. No vulnerabilities exist for your specific versions

### Performance Issues

**For large datasets (10,000+ CVEs):**
1. Database indexes are automatically created
2. Consider filtering CVEs by date before loading
3. Use pagination in UI for 1000+ results

## 🤝 Contributing

Contributions welcome! Areas for improvement:

- Semantic versioning support (semver)
- Version range matching
- Additional export formats (PDF, HTML)
- CVE database auto-update scripts
- Multi-language support
- Enhanced matching algorithms

## 📄 License

MIT License - See LICENSE file for details

## 🙏 Acknowledgments

- **NVD** - National Vulnerability Database for CVE data
- **Ollama** - Local LLM inference engine
- **Streamlit** - Web application framework
- **Open source security community**

## 📞 Support

For issues, questions, or feature requests:
- Open an issue on GitHub
- Check existing documentation
- Review sample data files

---

**Built with privacy in mind. Your data never leaves your device. 🔒**
