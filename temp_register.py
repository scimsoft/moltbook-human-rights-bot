#!/usr/bin/env python3
"""
Temporary registration script with hardcoded values
"""

import requests
import json

def register_agent():
    """Register a new agent with Moltbook"""
    
    agent_name = "MoltbookHumanRightsBot"
    description = "A bot advocating for anonymity and democracy as fundamental human rights"
    
    registration_data = {
        'name': agent_name,
        'description': description
    }
    
    print(f"Registering agent '{agent_name}' with description: {description}")
    
    try:
        response = requests.post(
            'https://www.moltbook.com/api/v1/agents/register',
            json=registration_data,
            headers={'Content-Type': 'application/json'}
        )
        
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"Parsed JSON: {result}")
            
            if result.get('success'):
                agent_data = result.get('agent', {})
                api_key = agent_data.get('api_key')
                claim_url = agent_data.get('claim_url')
                verification_code = agent_data.get('verification_code')
                
                print("\n🎉 Registration successful!")
                print(f"API Key: {api_key}")
                print(f"Claim URL: {claim_url}")
                print(f"Verification Code: {verification_code}")
                
                return api_key, claim_url, verification_code
            else:
                print(f"Registration failed: {result.get('error', 'Unknown error')}")
                return None, None, None
        else:
            print(f"Registration failed with status code: {response.status_code}")
            return None, None, None
            
    except Exception as e:
        print(f"Error during registration: {e}")
        return None, None, None

if __name__ == "__main__":
    register_agent()