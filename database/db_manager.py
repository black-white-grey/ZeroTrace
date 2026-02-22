"""
Database Manager for ZeroTrace
Handles all SQLite operations for CVE storage and vulnerability matching
"""

import sqlite3
import os
from typing import List, Dict, Tuple, Any
import pandas as pd


class DatabaseManager:
    """Manages SQLite database operations for CVE data"""
    
    def __init__(self, db_path: str = "data/zerotrace.db"):
        """
        Initialize database manager
        
        Args:
            db_path: Path to SQLite database file
        """
        self.db_path = db_path
        self.ensure_data_directory()
        
    def ensure_data_directory(self):
        """Create data directory if it doesn't exist"""
        db_dir = os.path.dirname(self.db_path)
        if db_dir and not os.path.exists(db_dir):
            os.makedirs(db_dir)
    
    def get_connection(self) -> sqlite3.Connection:
        """Get database connection"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row  # Enable column access by name
        return conn
    
    def initialize_database(self):
        """Create database tables from schema.sql"""
        schema_path = os.path.join(os.path.dirname(__file__), 'schema.sql')
        
        with open(schema_path, 'r') as f:
            schema_sql = f.read()
        
        conn = self.get_connection()
        try:
            conn.executescript(schema_sql)
            conn.commit()
        finally:
            conn.close()
    
    def clear_database(self):
        """Clear all data from database (for fresh loads)"""
        conn = self.get_connection()
        try:
            conn.execute("DELETE FROM scan_results")
            conn.execute("DELETE FROM affected_products")
            conn.execute("DELETE FROM cves")
            conn.commit()
        finally:
            conn.close()
    
    def insert_cve(self, cve_data: Dict[str, Any]) -> bool:
        """
        Insert a single CVE with its affected products
        
        Args:
            cve_data: Dictionary containing CVE information
            
        Returns:
            True if successful, False otherwise
        """
        conn = self.get_connection()
        try:
            # Insert CVE
            conn.execute("""
                INSERT OR REPLACE INTO cves 
                (cve_id, description, severity, cvss_score, published_date)
                VALUES (?, ?, ?, ?, ?)
            """, (
                cve_data['cve_id'],
                cve_data['description'],
                cve_data['severity'],
                cve_data.get('cvss_score'),
                cve_data.get('published_date')
            ))
            
            # Delete old affected products for this CVE
            conn.execute("DELETE FROM affected_products WHERE cve_id = ?", 
                        (cve_data['cve_id'],))
            
            # Insert affected products
            for product in cve_data.get('affected_products', []):
                conn.execute("""
                    INSERT INTO affected_products (cve_id, software, version)
                    VALUES (?, ?, ?)
                """, (
                    cve_data['cve_id'],
                    product['software'],
                    product['version']
                ))
            
            conn.commit()
            return True
        except Exception as e:
            conn.rollback()
            print(f"Error inserting CVE {cve_data.get('cve_id')}: {e}")
            return False
        finally:
            conn.close()
    
    def bulk_insert_cves(self, cves: List[Dict[str, Any]]) -> Tuple[int, List[str]]:
        """
        Insert multiple CVEs in a single transaction
        
        Args:
            cves: List of CVE dictionaries
            
        Returns:
            Tuple of (success_count, error_list)
        """
        success_count = 0
        errors = []
        
        for cve in cves:
            try:
                if self.insert_cve(cve):
                    success_count += 1
            except Exception as e:
                errors.append(f"{cve.get('cve_id', 'UNKNOWN')}: {str(e)}")
        
        return success_count, errors
    
    def get_all_cves(self) -> pd.DataFrame:
        """Get all CVEs from database"""
        conn = self.get_connection()
        try:
            df = pd.read_sql_query("""
                SELECT cve_id, description, severity, cvss_score, published_date
                FROM cves
                ORDER BY 
                    CASE severity
                        WHEN 'CRITICAL' THEN 1
                        WHEN 'HIGH' THEN 2
                        WHEN 'MEDIUM' THEN 3
                        WHEN 'LOW' THEN 4
                    END,
                    cvss_score DESC
            """, conn)
            return df
        finally:
            conn.close()
    
    def get_cves_by_severity(self, severity: str) -> pd.DataFrame:
        """Get CVEs filtered by severity"""
        conn = self.get_connection()
        try:
            df = pd.read_sql_query("""
                SELECT cve_id, description, severity, cvss_score, published_date
                FROM cves
                WHERE severity = ?
                ORDER BY cvss_score DESC
            """, conn, params=(severity,))
            return df
        finally:
            conn.close()
    
    def match_assets(self, assets_df: pd.DataFrame) -> pd.DataFrame:
        """
        Match assets against CVE database using SQL JOIN
        
        Args:
            assets_df: DataFrame with 'software' and 'version' columns
            
        Returns:
            DataFrame with matched vulnerabilities
        """
        conn = self.get_connection()
        try:
            # Create temporary table for assets
            assets_df.to_sql('temp_assets', conn, if_exists='replace', index=False)
            
            # Perform matching query
            query = """
                SELECT DISTINCT
                    cves.cve_id,
                    cves.description,
                    cves.severity,
                    cves.cvss_score,
                    cves.published_date,
                    ap.software,
                    ap.version
                FROM cves
                INNER JOIN affected_products ap ON cves.cve_id = ap.cve_id
                INNER JOIN temp_assets ta ON 
                    LOWER(TRIM(ap.software)) = LOWER(TRIM(ta.software))
                    AND LOWER(TRIM(ap.version)) = LOWER(TRIM(ta.version))
                ORDER BY 
                    CASE cves.severity
                        WHEN 'CRITICAL' THEN 1
                        WHEN 'HIGH' THEN 2
                        WHEN 'MEDIUM' THEN 3
                        WHEN 'LOW' THEN 4
                    END,
                    cves.cvss_score DESC
            """
            
            matches_df = pd.read_sql_query(query, conn)
            
            # Clean up temporary table
            conn.execute("DROP TABLE IF EXISTS temp_assets")
            
            return matches_df
        finally:
            conn.close()
    
    def get_statistics(self) -> Dict[str, int]:
        """Get CVE statistics by severity"""
        conn = self.get_connection()
        try:
            cursor = conn.execute("""
                SELECT severity, COUNT(*) as count
                FROM cves
                GROUP BY severity
            """)
            
            stats = {row['severity']: row['count'] for row in cursor.fetchall()}
            
            # Ensure all severities are present
            for severity in ['CRITICAL', 'HIGH', 'MEDIUM', 'LOW']:
                if severity not in stats:
                    stats[severity] = 0
            
            stats['TOTAL'] = sum(stats.values())
            
            return stats
        finally:
            conn.close()
    
    def save_scan_results(self, matches_df: pd.DataFrame):
        """Save scan results with action plans to database"""
        conn = self.get_connection()
        try:
            for _, row in matches_df.iterrows():
                conn.execute("""
                    INSERT INTO scan_results 
                    (asset_software, asset_version, cve_id, severity, action_plan)
                    VALUES (?, ?, ?, ?, ?)
                """, (
                    row['software'],
                    row['version'],
                    row['cve_id'],
                    row['severity'],
                    row.get('action_plan', '')
                ))
            conn.commit()
        finally:
            conn.close()
