import json
import requests
from typing import Dict, List, Optional

def extract_entities(text: str) -> Dict[str, any]:
    """Uses local DeepSeek-R1 (1.5B) via Ollama to extract project entities."""
    
    url = "http://localhost:11434/api/generate"
    
    prompt = f"""
    Extract the following entities from the project text below and return them ONLY as a JSON object.
    Be thorough and capture detailed descriptions for background and scope.
    
    Format:
    {{
        "project_name": "string",
        "client_name": "string",
        "effective_date": "string",
        "type": "string",
        "scope_timeline": ["list of strings"],
        "background": "detailed background paragraph",
        "scope_description": "detailed scope of service summary",
        "phases": {{
            "phase_1": "details of phase 1",
            "phase_2": "details of phase 2"
        }},
        "tech_stack": ["list of technologies mentioned"],
        "client_contact": "name or email if found"
    }}

    Text:
    {text}
    """
    
    payload = {
        "model": "deepseek-r1:1.5b",
        "prompt": prompt,
        "stream": False,
        "format": "json"
    }

    try:
        response = requests.post(url, json=payload, timeout=120)
        response.raise_for_status()
        result = response.json()
        
        # Parse the JSON response from the model
        raw_response = result.get("response", "{}")
        
        if "{" in raw_response and "}" in raw_response:
            json_str = raw_response[raw_response.find("{"):raw_response.rfind("}")+1]
        else:
            json_str = raw_response

        try:
            entities = json.loads(json_str)
        except json.JSONDecodeError:
            print(f"Failed to parse JSON from response: {raw_response}")
            entities = {}
        
        # Ensure all keys are present
        defaults = {
            "project_name": "Project Name",
            "client_name": "Client Name",
            "effective_date": "TBD",
            "type": "TBD",
            "scope_timeline": [],
            "background": "N/A",
            "scope_description": "N/A",
            "phases": {},
            "tech_stack": [],
            "client_contact": "N/A"
        }
        
        # Merge with defaults
        final_entities = {}
        for key, val in defaults.items():
            final_entities[key] = entities.get(key, val)
        
        return final_entities

    except Exception as e:
        print(f"Error calling Ollama: {e}")
        # Return empty structure on failure
        return {
            "project_name": "Error",
            "client_name": "Error",
            "effective_date": "N/A",
            "type": "N/A",
            "scope_timeline": []
        }

if __name__ == "__main__":
    # Test text
    sample_text = """
    Project Name 
    BOCE Advanced Information Portal   
    Name of Client  
    Alexion Pharmaceuticals, Inc. 
    Effective Date 
    25th May 2024 
    Type 
    Fixed Bid 
    Scope & Timeline 
    Development, Launch and Hypercare of the Application (25th Apr’24 - 31st July’24)  
    Operational Support of the Application as detailed in Section 16 (1st Aug’24 - 31st Dec’24) 
    """
    
    print(json.dumps(extract_entities(sample_text), indent=4))
