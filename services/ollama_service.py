"""
Ollama Service
Generate AI-powered action plans using Llama3
"""

import requests
from typing import Dict, Optional, Callable
import time


class OllamaService:
    """Service for generating action plans using Ollama/Llama3"""
    
    def __init__(self, base_url: str = "http://localhost:11434", model: str = "llama3"):
        """
        Initialize Ollama service
        
        Args:
            base_url: Ollama API base URL
            model: Model name to use (default: llama3)
        """
        self.base_url = base_url
        self.model = model
        self.timeout = 30  # seconds
    
    def is_available(self) -> bool:
        """
        Check if Ollama service is available
        
        Returns:
            True if Ollama is running, False otherwise
        """
        try:
            response = requests.get(f"{self.base_url}/api/tags", timeout=5)
            return response.status_code == 200
        except:
            return False
    
    def _create_prompt(self, cve_data: Dict) -> str:
        """
        Create prompt for action plan generation
        
        Args:
            cve_data: Dictionary with CVE information
            
        Returns:
            Formatted prompt string
        """
        prompt = f"""You are a cybersecurity analyst. A vulnerability has been identified in a software asset:

CVE ID: {cve_data['cve_id']}
Affected Software: {cve_data['software']} version {cve_data['version']}
Severity: {cve_data['severity']} (CVSS Score: {cve_data.get('cvss_score', 'N/A')})
Description: {cve_data['description']}

Provide a concise 3-step remediation action plan. Be specific, actionable, and prioritize security. Format your response as:
1. [First action]
2. [Second action]
3. [Third action]

Action Plan:"""
        
        return prompt
    
    def generate_action_plan(self, cve_data: Dict, retry: bool = True) -> str:
        """
        Generate action plan for a CVE
        
        Args:
            cve_data: Dictionary with CVE information
            retry: Whether to retry on failure
            
        Returns:
            Action plan text
        """
        if not self.is_available():
            return "⚠️ Ollama service unavailable. Please start Ollama to generate AI action plans."
        
        prompt = self._create_prompt(cve_data)
        
        try:
            response = requests.post(
                f"{self.base_url}/api/generate",
                json={
                    "model": self.model,
                    "prompt": prompt,
                    "stream": False,
                    "options": {
                        "temperature": 0.7,
                        "num_predict": 300
                    }
                },
                timeout=self.timeout
            )
            
            if response.status_code == 200:
                result = response.json()
                action_plan = result.get('response', '').strip()
                
                # Clean up the response
                if action_plan:
                    return action_plan
                else:
                    return "⚠️ No action plan generated. Please try again."
            else:
                if retry:
                    time.sleep(1)
                    return self.generate_action_plan(cve_data, retry=False)
                return f"⚠️ Error generating action plan: HTTP {response.status_code}"
        
        except requests.exceptions.Timeout:
            return "⚠️ Request timed out. Ollama may be busy processing another request."
        except Exception as e:
            return f"⚠️ Error: {str(e)}"
    
    def batch_generate(self, 
                      matches_list: list, 
                      progress_callback: Optional[Callable[[int, int], None]] = None) -> list:
        """
        Generate action plans for multiple CVEs
        
        Args:
            matches_list: List of CVE dictionaries
            progress_callback: Optional callback function(current, total)
            
        Returns:
            List of action plans
        """
        action_plans = []
        total = len(matches_list)
        
        for idx, cve_data in enumerate(matches_list):
            action_plan = self.generate_action_plan(cve_data)
            action_plans.append(action_plan)
            
            if progress_callback:
                progress_callback(idx + 1, total)
        
        return action_plans
