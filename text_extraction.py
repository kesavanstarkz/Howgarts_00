import json
import requests
from typing import Dict, List, Optional

def extract_entities(text: str) -> Dict[str, any]:
    """Uses local DeepSeek-R1 (1.5B) via Ollama to extract project entities."""
    
    url = "http://localhost:11434/api/generate"
    
    prompt = f"""
    Extract the following entities from the project text below and return them ONLY as a JSON object.
    Do not include any reasoning, preambles, or explanations. 
    
    Format:
    {{
        "project_name": "string",
        "client_name": "string",
        "effective_date": "string",
        "type": "string",
        "scope_timeline": ["list of strings"]
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
        response = requests.post(url, json=payload, timeout=60)
        response.raise_for_status()
        result = response.json()
        
        # Parse the JSON response from the model
        entities = json.loads(result.get("response", "{}"))
        
        # Ensure all keys are present
        defaults = {
            "project_name": None,
            "client_name": None,
            "effective_date": None,
            "type": None,
            "scope_timeline": []
        }
        
        # Merge with defaults
        for key, val in defaults.items():
            if key not in entities:
                entities[key] = val
        
        return entities

    except Exception as e:
        print(f"Error calling Ollama: {e}")
        # Return empty structure on failure
        return {
            "project_name": None,
            "client_name": None,
            "effective_date": None,
            "type": None,
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
