# ZeroTrace Quick Start Guide

## Installation

### Windows
```cmd
cd zerotrace
setup.bat
```

### Linux/Mac
```bash
cd zerotrace
chmod +x setup.sh
./setup.sh
```

### Manual Installation
```bash
pip install -r requirements.txt
```

## Running ZeroTrace

```bash
streamlit run app.py
```

The app will open at: http://localhost:8501

## Step-by-Step Usage

### Step 1: Load CVE Database

1. In the left section "📊 Load CVE Database"
2. Click "Browse files" and select `data/sample_cves.json`
3. Click "📥 Load CVEs" button
4. Wait for confirmation: "✅ Successfully loaded X CVEs!"

### Step 2: Upload Asset Inventory

1. In the right section "📤 Upload Asset Inventory"
2. Click "Browse files" and select `data/sample_assets.csv`
3. Preview your assets in the table

### Step 3: Scan for Vulnerabilities

1. Click the big "🔍 SCAN FOR VULNERABILITIES" button
2. ZeroTrace will:
   - Match your assets against CVEs (instant)
   - Generate AI action plans (30-60 seconds per CVE if Ollama is running)
3. View results in the dashboard

### Step 4: Review and Export

1. Browse vulnerability cards with:
   - CVE details
   - Severity badges
   - AI-generated remediation steps
2. Filter by severity
3. Export results as CSV

## Sample Data

The included sample data will find **8-10 vulnerabilities**:

**Vulnerable Assets (will match):**
- Apache HTTP Server 2.4.1 → CVE-2024-1234 (CRITICAL)
- OpenSSL 1.1.1k → CVE-2024-5678 (CRITICAL)
- Node.js 16.14.0 → CVE-2024-9012 (CRITICAL)
- PostgreSQL 13.0 → CVE-2024-3456 (HIGH)
- nginx 1.18.0 → CVE-2024-7890 (HIGH)
- MySQL 8.0.25 → CVE-2024-2345 (HIGH)
- Redis 6.2.0 → CVE-2024-6789 (HIGH)
- MongoDB 5.0.0 → CVE-2024-4567 (HIGH)
- Python 3.9.0 → CVE-2024-8901 (MEDIUM)
- Docker 20.10.7 → CVE-2024-1357 (MEDIUM)

**Safe Assets (no matches):**
- Apache HTTP Server 2.4.50
- PostgreSQL 15.0
- Node.js 18.0.0
- OpenSSL 3.0.0

## Using Your Own Data

### CVE JSON Format

Create a JSON file with this structure:

```json
{
  "cves": [
    {
      "cve_id": "CVE-2024-XXXX",
      "description": "Description of the vulnerability",
      "severity": "CRITICAL",
      "cvss_score": 9.8,
      "published_date": "2024-01-01",
      "affected_products": [
        {
          "software": "Software Name",
          "version": "1.2.3"
        }
      ]
    }
  ]
}
```

**Field Requirements:**
- `severity` must be: CRITICAL, HIGH, MEDIUM, or LOW
- `cvss_score` is optional (0-10)
- `affected_products` must have at least one entry
- Each product needs `software` and `version`

### Asset CSV Format

Create a CSV file with exactly these columns:

```csv
software,version
Apache HTTP Server,2.4.1
PostgreSQL,13.0
```

**Tips:**
- Use exact software names (case-insensitive matching)
- Version must be exact match (1.0.0 ≠ 1.0)
- No extra columns needed
- Remove duplicates

## Troubleshooting

### "Ollama service unavailable"

**Fix:**
```bash
# Check if Ollama is running
ollama list

# Start Ollama
ollama serve

# Pull llama3 if needed
ollama pull llama3
```

### "No vulnerabilities detected"

**Reasons:**
- Version mismatch (exact match required)
- Software name mismatch
- CVE database doesn't cover your versions

**Debug:**
1. Check spelling of software names
2. Verify version format matches CVE data
3. Try loading sample data first to confirm app works

### Import Errors

```bash
# Reinstall dependencies
pip install --upgrade -r requirements.txt
```

### Database Locked

- Close any other instances of ZeroTrace
- Delete `data/zerotrace.db` and restart

## Tips for Best Results

1. **Consistent Naming:** Use official software names (e.g., "PostgreSQL" not "Postgres")
2. **Version Format:** Match the format in CVE data exactly
3. **Regular Updates:** Reload CVE database weekly/monthly
4. **Action Plans:** Let Ollama finish generating all plans for complete reports
5. **Export Early:** Download results before scanning again

## Advanced Usage

### Custom Ollama Model

Edit `services/ollama_service.py`:
```python
def __init__(self, base_url="http://localhost:11434", model="llama3.1"):
```

### Adjust Temperature

For more creative/conservative action plans, edit:
```python
"temperature": 0.7,  # Lower = more conservative, Higher = more creative
```

### Clear Database

Click "🗑️ Clear Database" to wipe CVE data and start fresh

## Next Steps

1. **Get Real CVE Data:**
   - Download from https://nvd.nist.gov/
   - Convert to ZeroTrace JSON format
   - Load thousands of CVEs

2. **Automate Scanning:**
   - Export your asset inventory regularly
   - Schedule scans (cron/Task Scheduler)
   - Track vulnerability trends

3. **Integrate with CMDB:**
   - Export asset lists from your CMDB
   - Convert to CSV format
   - Scan automatically

## Support

- Read the full README.md
- Check sample data files
- Review error messages in the UI
- Verify JSON/CSV format

---

**Remember: All data stays on your device. No internet required (except Ollama setup).**
