-- ZeroTrace Database Schema
-- SQLite database for storing CVE data and vulnerability matches

-- Main CVE table
CREATE TABLE IF NOT EXISTS cves (
    cve_id TEXT PRIMARY KEY,
    description TEXT NOT NULL,
    severity TEXT NOT NULL CHECK(severity IN ('CRITICAL', 'HIGH', 'MEDIUM', 'LOW')),
    cvss_score REAL,
    published_date TEXT,
    last_modified TEXT DEFAULT CURRENT_TIMESTAMP
);

-- Affected products (normalized for flexible querying)
CREATE TABLE IF NOT EXISTS affected_products (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    cve_id TEXT NOT NULL,
    software TEXT NOT NULL,
    version TEXT NOT NULL,
    FOREIGN KEY (cve_id) REFERENCES cves(cve_id) ON DELETE CASCADE
);

-- Performance indexes
CREATE INDEX IF NOT EXISTS idx_software_version 
    ON affected_products(software, version);
    
CREATE INDEX IF NOT EXISTS idx_severity 
    ON cves(severity);
    
CREATE INDEX IF NOT EXISTS idx_cvss 
    ON cves(cvss_score DESC);

-- Store scan results with action plans
CREATE TABLE IF NOT EXISTS scan_results (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    asset_software TEXT NOT NULL,
    asset_version TEXT NOT NULL,
    cve_id TEXT NOT NULL,
    severity TEXT NOT NULL,
    action_plan TEXT,
    scanned_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (cve_id) REFERENCES cves(cve_id)
);
