"""
CVE Loader Service
Loads CVE data from JSON files into SQLite database
"""

import json
from typing import Tuple, List, Dict, Any


def validate_cve_data(cve: Dict[str, Any]) -> Tuple[bool, str]:
    """
    Validate CVE data structure
    
    Args:
        cve: CVE dictionary
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    required_fields = ['cve_id', 'description', 'severity']
    
    for field in required_fields:
        if field not in cve:
            return False, f"Missing required field: {field}"
    
    # Validate severity
    valid_severities = ['CRITICAL', 'HIGH', 'MEDIUM', 'LOW']
    if cve['severity'] not in valid_severities:
        return False, f"Invalid severity: {cve['severity']}. Must be one of {valid_severities}"
    
    # Validate CVSS score if present
    if 'cvss_score' in cve:
        try:
            score = float(cve['cvss_score'])
            if score < 0 or score > 10:
                return False, f"CVSS score must be between 0 and 10, got {score}"
        except (ValueError, TypeError):
            return False, f"Invalid CVSS score: {cve['cvss_score']}"
    
    # Validate affected products
    if 'affected_products' not in cve or not cve['affected_products']:
        return False, "Missing or empty affected_products"
    
    for product in cve['affected_products']:
        if 'software' not in product or 'version' not in product:
            return False, "Each affected_product must have 'software' and 'version'"
    
    return True, ""


def load_cves_from_json(json_file, db_manager) -> Tuple[int, List[str]]:
    """
    Load CVEs from JSON file into database
    
    Args:
        json_file: File object or path to JSON file
        db_manager: DatabaseManager instance
        
    Returns:
        Tuple of (success_count, error_list)
    """
    errors = []
    
    try:
        # Read JSON data
        if hasattr(json_file, 'read'):
            # File object from Streamlit uploader
            content = json_file.read()
            if isinstance(content, bytes):
                content = content.decode('utf-8')
            data = json.loads(content)
        else:
            # File path
            with open(json_file, 'r') as f:
                data = json.load(f)
        
        # Validate JSON structure
        if 'cves' not in data:
            return 0, ["JSON must have a 'cves' array at the root level"]
        
        cves = data['cves']
        
        if not isinstance(cves, list):
            return 0, ["'cves' must be an array"]
        
        if len(cves) == 0:
            return 0, ["No CVEs found in JSON file"]
        
        # Validate and prepare CVEs
        valid_cves = []
        for idx, cve in enumerate(cves):
            is_valid, error_msg = validate_cve_data(cve)
            if is_valid:
                valid_cves.append(cve)
            else:
                errors.append(f"CVE #{idx + 1} ({cve.get('cve_id', 'UNKNOWN')}): {error_msg}")
        
        # Insert valid CVEs into database
        if valid_cves:
            success_count, insert_errors = db_manager.bulk_insert_cves(valid_cves)
            errors.extend(insert_errors)
            return success_count, errors
        else:
            return 0, errors
    
    except json.JSONDecodeError as e:
        return 0, [f"Invalid JSON format: {str(e)}"]
    except Exception as e:
        return 0, [f"Error loading CVEs: {str(e)}"]
