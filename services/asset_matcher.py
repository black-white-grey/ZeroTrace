"""
Asset Matcher Service
Matches uploaded assets against CVE database
"""

import pandas as pd
from typing import Dict


def validate_assets_csv(df: pd.DataFrame) -> tuple[bool, str]:
    """
    Validate asset CSV structure
    
    Args:
        df: DataFrame from CSV
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    required_columns = ['software', 'version']
    
    for col in required_columns:
        if col not in df.columns:
            return False, f"Missing required column: '{col}'. CSV must have columns: software, version"
    
    if len(df) == 0:
        return False, "CSV file is empty"
    
    # Check for empty values
    if df['software'].isna().any() or df['version'].isna().any():
        return False, "CSV contains empty values in software or version columns"
    
    return True, ""


def normalize_assets(df: pd.DataFrame) -> pd.DataFrame:
    """
    Normalize asset data for matching
    
    Args:
        df: Raw assets DataFrame
        
    Returns:
        Normalized DataFrame
    """
    df = df.copy()
    
    # Convert to string and normalize
    df['software'] = df['software'].astype(str).str.strip()
    df['version'] = df['version'].astype(str).str.strip()
    
    # Remove duplicates
    df = df.drop_duplicates(subset=['software', 'version'])
    
    return df


def match_assets_to_cves(assets_df: pd.DataFrame, db_manager) -> pd.DataFrame:
    """
    Match assets against CVE database
    
    Args:
        assets_df: DataFrame with software and version columns
        db_manager: DatabaseManager instance
        
    Returns:
        DataFrame with vulnerability matches
    """
    # Validate CSV structure
    is_valid, error_msg = validate_assets_csv(assets_df)
    if not is_valid:
        raise ValueError(error_msg)
    
    # Normalize asset data
    normalized_assets = normalize_assets(assets_df)
    
    # Perform SQL-based matching
    matches_df = db_manager.match_assets(normalized_assets)
    
    # Add empty action_plan column for later population
    if len(matches_df) > 0:
        matches_df['action_plan'] = ''
    
    return matches_df


def calculate_risk_summary(matches_df: pd.DataFrame) -> Dict[str, int]:
    """
    Calculate risk statistics from matches
    
    Args:
        matches_df: DataFrame with vulnerability matches
        
    Returns:
        Dictionary with severity counts
    """
    if len(matches_df) == 0:
        return {
            'TOTAL': 0,
            'CRITICAL': 0,
            'HIGH': 0,
            'MEDIUM': 0,
            'LOW': 0
        }
    
    severity_counts = matches_df['severity'].value_counts().to_dict()
    
    summary = {
        'TOTAL': len(matches_df),
        'CRITICAL': severity_counts.get('CRITICAL', 0),
        'HIGH': severity_counts.get('HIGH', 0),
        'MEDIUM': severity_counts.get('MEDIUM', 0),
        'LOW': severity_counts.get('LOW', 0)
    }
    
    return summary
