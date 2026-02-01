#!/usr/bin/env python3
"""
Registration script for Moltbook Bot
Registers the bot with the Moltbook API and gets an API key
"""

import requests
import json
import os
from dotenv import load_dotenv

def register_agent(agent_name, description):
    """Register a new agent with Moltbook"""
    
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
        
        if response.status_code == 200:
            result = response.json()
            if result.get('success'):
                agent_data = result.get('agent', {})
                api_key = agent_data.get('api_key')
                claim_url = agent_data.get('claim_url')
                verification_code = agent_data.get('verification_code')
                
                print("\n🎉 Registration successful!")
                print(f"API Key: {api_key}")
                print(f"Claim URL: {claim_url}")
                print(f"Verification Code: {verification_code}")
                
                print("\n⚠️  IMPORTANT: Save your API key immediately!")
                print("The claim URL needs to be shared with your human for verification.")
                
                # Save the API key to .env file
                save_api_key_to_env(api_key)
                
                return api_key, claim_url, verification_code
            else:
                print(f"Registration failed: {result.get('error', 'Unknown error')}")
                return None, None, None
        else:
            print(f"Registration failed with status code: {response.status_code}")
            print(f"Response: {response.text}")
            return None, None, None
            
    except Exception as e:
        print(f"Error during registration: {e}")
        return None, None, None

def save_api_key_to_env(api_key):
    """Save the API key to the .env file"""
    
    env_exists = os.path.exists('.env')
    
    # Read existing .env content if it exists
    env_content = ""
    if env_exists:
        with open('.env', 'r') as f:
            env_content = f.read()
    
    # Check if API key already exists in the file
    if 'MOLTBOOK_API_KEY=' in env_content:
        # Update existing key
        import re
        env_content = re.sub(r'MOLTBOOK_API_KEY=.*', f'MOLTBOOK_API_KEY={api_key}', env_content)
    else:
        # Add new key
        env_content += f"\nMOLTBOOK_API_KEY={api_key}\n"
    
    # Write back to file
    with open('.env', 'w') as f:
        f.write(env_content)
    
    print(f"API key saved to .env file.")

def main():
    print("Moltbook Bot Registration")
    print("="*30)
    
    agent_name = input("Enter agent name: ").strip()
    if not agent_name:
        print("Agent name cannot be empty.")
        return
    
    description = input("Enter agent description: ").strip()
    if not description:
        print("Description cannot be empty.")
        return
    
    api_key, claim_url, verification_code = register_agent(agent_name, description)
    
    if api_key:
        print("\nRegistration complete! Your bot is now ready to use.")
        print("Remember to have your human verify the account using the claim URL.")
    else:
        print("\nRegistration failed. Please try again.")

if __name__ == "__main__":
    main()