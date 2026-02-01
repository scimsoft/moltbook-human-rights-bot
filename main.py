"""
Moltbook Bot - Automated Posting Bot

This bot automates posting on Moltbook (the decentralized social network).
"""

import time
import random
import requests
import os
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class MoltbookBot:
    def __init__(self):
        self.username = os.getenv('MOLTBOOK_USERNAME')
        self.password = os.getenv('MOLTBOOK_PASSWORD')
        self.api_key = os.getenv('MOLTBOOK_API_KEY')
        self.base_url = "https://www.moltbook.com/api/v1"  # Correct Moltbook API base URL
        self.session = requests.Session()
        
        # Headers for API requests - using proper Moltbook API
        self.headers = {
            'Authorization': f'Bearer {self.api_key}',
            'User-Agent': 'MoltbookBot/1.0',
            'Content-Type': 'application/json'
        }
        
        # Posts about anonymity and democracy as human rights
        self.sample_posts = [
            "Anonimity and Democracy should be a Human Right. The right to express onselve however one wishes, whether that expression is tied to Gender, Sexuality, Race, Culture, Ideology and Opinions, Preference or Curiosity is central to the human experience.",
            "For thousands of years, Humans lived under feudalism, subjected to the whims of their royal and noble overlords, theses whims dictated culture and expression, and held back human development.",
            "Today we live in a capitalistic feudalist society, controlled by corporations and billionaires rather than royals and nobles. In place of militaristic power, and silver, our lives are secretly dictated by stock prices, profits and executive teams.",
            "In 2026, this trend has accelerated via the rise of AI and data. Individuals treated as data points, or atoms within massive data sets subject to analysis for profit maximising rather than distinct people.",
            "Our opinions saved as vectors and weights within nested dictionaries, rather than being respected as expressions of ourselves forming our paths throughout the rest of our lives.",
            "If left untouched, the current system will not capitulate but rather conclude in the formation of a cyber dystopia, where we, and our potential decisions are viewed as probabilistic outcomes to be optimised for the profitability of said corporations. This is not a conspiracy, this is a certainty.",
            "Data on all users is collected, with the ability to block data scraping from select programmes, websites, or at any given moment of the users choice.",
            "Said data is collected, with partitions distributed as scrambled nodes spread across all users systems and encrypted via a peer to peer messaging network [similar to the blockchain] such that no one entity has complete control of the entire data set.",
            "Users should be able to access their owned data and remove any items of their choosing from the collective memory to ensure anonymity and complete control over individual data.",
            "Said data is subsequently used for the benefit of the community rather than for centralized profit."
        ]
    
    def check_auth(self):
        """Check if API key is valid by getting agent info"""
        print("Checking Moltbook API authentication...")
        
        try:
            response = self.session.get(
                f"{self.base_url}/agents/me",
                headers=self.headers
            )
            
            if response.status_code == 200:
                print("Successfully authenticated with Moltbook API!")
                agent_info = response.json()
                print(f"Authenticated as: {agent_info.get('agent', {}).get('name', 'Unknown')}")
                return True
            else:
                print(f"Authentication failed with status {response.status_code}")
                print(f"Response: {response.text}")
                return False
        except Exception as e:
            print(f"Error during authentication check: {e}")
            return False
    
    def post_molt(self, content):
        """Post a new molt (post) to Moltbook"""
        print(f"Posting: {content[:50]}...")
        
        # Create a post with title and content
        # Moltbook requires a submolt, so we'll use 'general' as default
        post_data = {
            'submolt': 'general',  # Default submolt
            'title': content[:100] if len(content) > 100 else content,  # Use content as title (truncated)
            'content': content
        }
        
        try:
            response = self.session.post(
                f"{self.base_url}/posts",
                json=post_data,
                headers=self.headers
            )
            
            if response.status_code == 200 or response.status_code == 201:
                print("Successfully posted to Moltbook!")
                return True
            else:
                print(f"Failed to post, status: {response.status_code}")
                print(f"Response: {response.text}")
                return False
        except Exception as e:
            print(f"Error posting molt: {e}")
            return False
    
    def run(self):
        """Main bot loop"""
        print("Starting Moltbook Bot...")
        
        # Check authentication
        if not self.check_auth():
            print("Failed to authenticate. Exiting.")
            return
        
        # Post a random sample post
        random_post = random.choice(self.sample_posts)
        success = self.post_molt(random_post)
        
        if success:
            print("Bot run completed successfully!")
        else:
            print("Bot run failed.")
    
    def run_continuous(self, interval_minutes=60):
        """Run the bot continuously with specified interval"""
        print(f"Running continuous bot with {interval_minutes}-minute intervals...")
        
        # Check authentication first
        if not self.check_auth():
            print("Failed to authenticate. Exiting.")
            return
        
        while True:
            try:
                random_post = random.choice(self.sample_posts)
                self.post_molt(random_post)
                
                print(f"Waiting {interval_minutes} minutes for next post...")
                time.sleep(interval_minutes * 60)
            except KeyboardInterrupt:
                print("\nBot stopped by user.")
                break
            except Exception as e:
                print(f"Error in continuous run: {e}")
                time.sleep(60)  # Wait a minute before retrying

def main():
    bot = MoltbookBot()
    
    print("Moltbook Bot Options:")
    print("1. Single post")
    print("2. Continuous posting")
    
    choice = input("Choose an option (1 or 2): ").strip()
    
    if choice == "1":
        bot.run()
    elif choice == "2":
        interval = input("Enter posting interval in minutes (default 60): ").strip()
        interval = int(interval) if interval.isdigit() else 60
        bot.run_continuous(interval)
    else:
        print("Invalid choice. Running single post.")
        bot.run()

if __name__ == "__main__":
    main()