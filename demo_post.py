#!/usr/bin/env python3
"""
Demo post script for Moltbook Bot
This demonstrates how the post would work once the bot is claimed.
"""

import os
import requests
import random
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

class MoltbookDemoBot:
    def __init__(self):
        self.api_key = os.getenv('MOLTBOOK_API_KEY')
        self.base_url = 'https://www.moltbook.com/api/v1'
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

    def demo_post(self):
        """Demonstrate how a post would be made once the bot is claimed"""
        if not self.api_key:
            print("❌ No API key found. Please ensure MOLTBOOK_API_KEY is set in your .env file.")
            return False
        
        # Select a random post from our content
        content = random.choice(self.sample_posts)
        
        print("📝 Preparing to post:")
        print(f"--- Content Preview ---")
        print(f"{content[:150]}{'...' if len(content) > 150 else ''}")
        print(f"--- End Preview ---")
        
        post_data = {
            'submolt': 'general',
            'title': content[:100] if len(content) > 100 else content,  # Use content as title (truncated)
            'content': content
        }
        
        print(f"\n📡 Attempting to post to Moltbook...")
        print(f"   Endpoint: {self.base_url}/posts")
        print(f"   Submolt: {post_data['submolt']}")
        print(f"   Title: {post_data['title'][:50]}...")
        
        try:
            response = requests.post(f'{self.base_url}/posts', json=post_data, headers=self.headers)
            
            if response.status_code == 201 or response.status_code == 200:
                print(f"✅ SUCCESS: Post created!")
                result = response.json()
                if 'post' in result:
                    print(f"   Post ID: {result['post'].get('id', 'Unknown')}")
                return True
            elif response.status_code == 401:
                print(f"❌ AUTHENTICATION ERROR: {response.json().get('error', 'Agent not claimed')}")
                print(f"   Hint: {response.json().get('hint', 'Visit the claim URL to verify ownership')}")
                print(f"   Claim URL: https://moltbook.com/claim/moltbook_claim_kBypHyjatdZMYv1goaJm8hzAHMiSccCG")
                return False
            else:
                print(f"❌ FAILED: Status {response.status_code}")
                print(f"   Response: {response.text}")
                return False
                
        except requests.exceptions.ConnectionError:
            print("❌ NETWORK ERROR: Could not connect to Moltbook API")
            return False
        except Exception as e:
            print(f"❌ ERROR: {e}")
            return False

def main():
    print("🦞 Moltbook Bot - Demo Post")
    print("="*40)
    
    bot = MoltbookDemoBot()
    
    print("ℹ️  Note: This demo shows how the post would work once the bot is claimed.")
    print("   Currently, the bot needs human verification before posting.")
    print()
    
    success = bot.demo_post()
    
    if success:
        print("\n🎉 Post successful!")
    else:
        print("\n📋 To enable posting:")
        print("   1. Visit the claim URL to verify ownership")
        print("   2. Once claimed, the bot can post automatically")
        print("   3. Claim URL: https://moltbook.com/claim/moltbook_claim_kBypHyjatdZMYv1goaJm8hzAHMiSccCG")

if __name__ == "__main__":
    main()