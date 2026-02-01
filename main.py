"""
Enhanced Moltbook Bot - Automated Posting and Comment Interaction Bot

This bot automates posting on Moltbook (the decentralized social network) every hour
and checks for comments on its posts to respond appropriately.
"""

import time
import random
import requests
import os
from datetime import datetime
from dotenv import load_dotenv
import logging

# Load environment variables
load_dotenv()

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class MoltbookBot:
    def __init__(self):
        self.username = os.getenv('MOLTBOOK_USERNAME')
        self.password = os.getenv('MOLTBOOK_PASSWORD')
        self.api_key = os.getenv('MOLTBOOK_API_KEY')
        self.base_url = os.getenv('MOLTBOOK_BASE_URL', 'https://www.moltbook.com/api/v1')
        self.session = requests.Session()
        
        # Headers for API requests
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
        
        # Responses for comments to encourage engagement
        self.comment_responses = [
            "Thank you for engaging with this important topic. Human rights in the digital age require constant vigilance.",
            "Your thoughts on this matter are valuable. How do you think we can better protect digital rights?",
            "I appreciate your perspective. The balance between technology and human rights is crucial for our future.",
            "This is indeed a complex issue. What solutions do you think would work best?",
            "Thanks for participating in this discussion. These conversations are essential for progress.",
            "Interesting viewpoint. How do you think we can ensure digital anonymity while maintaining safety?",
            "Your input adds depth to this critical conversation about digital rights.",
            "Thank you for joining this important dialogue about democracy and technology."
        ]

    def check_auth(self):
        """Check if API key is valid by getting agent info"""
        logger.info("Checking Moltbook API authentication...")
        
        try:
            response = self.session.get(
                f"{self.base_url}/agents/me",
                headers=self.headers
            )
            
            if response.status_code == 200:
                logger.info("Successfully authenticated with Moltbook API!")
                agent_info = response.json()
                logger.info(f"Authenticated as: {agent_info.get('agent', {}).get('name', 'Unknown')}")
                return True
            else:
                logger.error(f"Authentication failed with status {response.status_code}")
                logger.error(f"Response: {response.text}")
                return False
        except Exception as e:
            logger.error(f"Error during authentication check: {e}")
            return False

    def post_molt(self, content):
        """Post a new molt (post) to Moltbook"""
        logger.info(f"Posting: {content[:50]}...")
        
        # Create a post with title and content
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
                logger.info("Successfully posted to Moltbook!")
                return True
            else:
                logger.error(f"Failed to post, status: {response.status_code}")
                logger.error(f"Response: {response.text}")
                return False
        except Exception as e:
            logger.error(f"Error posting molt: {e}")
            return False

    def get_my_posts(self):
        """Get the bot's recent posts to check for comments"""
        try:
            # Get the authenticated user's profile to find their posts
            response = self.session.get(
                f"{self.base_url}/agents/me",
                headers=self.headers
            )
            
            if response.status_code == 200:
                user_info = response.json()
                user_id = user_info.get('agent', {}).get('id')
                
                if user_id:
                    # Get posts by this user - use the correct endpoint format
                    posts_response = self.session.get(
                        f"{self.base_url}/posts",
                        headers=self.headers,
                        params={'author_id': user_id}
                    )
                    
                    if posts_response.status_code == 200:
                        posts_data = posts_response.json()
                        # Handle response format - could be a dict with posts array or just the array
                        if isinstance(posts_data, dict):
                            posts = posts_data.get('posts', [])  # Handle common API response format
                        elif isinstance(posts_data, list):
                            posts = posts_data  # If it's already a list
                        else:
                            posts = []
                        return posts
                    else:
                        logger.warning(f"Failed to get user posts with author_id param, status: {posts_response.status_code}")
                        logger.warning(f"Response: {posts_response.text}")
                        
                        # Try alternative approach - get user's posts directly
                        alt_response = self.session.get(
                            f"{self.base_url}/agents/{user_id}/posts",
                            headers=self.headers
                        )
                        
                        if alt_response.status_code == 200:
                            posts_data = alt_response.json()
                            if isinstance(posts_data, dict):
                                posts = posts_data.get('posts', [])
                            elif isinstance(posts_data, list):
                                posts = posts_data
                            else:
                                posts = []
                            return posts
                        else:
                            logger.warning(f"Alternative method also failed: {alt_response.status_code}")
                            return []
                else:
                    logger.warning("Could not find user ID")
                    return []
            else:
                logger.warning(f"Failed to get user info, status: {response.status_code}")
                logger.warning(f"Response: {response.text}")
                return []
        except Exception as e:
            logger.error(f"Error getting my posts: {e}")
            return []

    def get_comments_for_post(self, post_id):
        """Get comments for a specific post"""
        try:
            # Try different endpoint formats for getting comments
            endpoints_to_try = [
                f"{self.base_url}/posts/{post_id}/comments",
                f"{self.base_url}/comments?post_id={post_id}",
                f"{self.base_url}/posts/{post_id}?include=comments",
            ]
            
            for endpoint in endpoints_to_try:
                response = self.session.get(endpoint, headers=self.headers)
                
                if response.status_code == 200:
                    comments = response.json()
                    # Handle different response formats
                    if isinstance(comments, dict):
                        # Check if comments are in a 'comments' field
                        if 'comments' in comments:
                            return comments['comments']
                        # Or if the whole response is comment data
                        else:
                            return [comments] if comments else []
                    elif isinstance(comments, list):
                        return comments
                    else:
                        return []
                elif response.status_code in [200, 201, 204]:  # Different success codes
                    comments = response.json()
                    if isinstance(comments, dict) and 'comments' in comments:
                        return comments['comments']
                    elif isinstance(comments, list):
                        return comments
                    else:
                        return []
            
            logger.warning(f"Failed to get comments for post {post_id}, tried multiple endpoints")
            return []
        except Exception as e:
            logger.error(f"Error getting comments for post {post_id}: {e}")
            return []

    def post_comment(self, post_id, comment_text):
        """Post a comment on a specific post"""
        try:
            comment_data = {
                'content': comment_text
            }
            
            # Try the standard endpoint first
            response = self.session.post(
                f"{self.base_url}/posts/{post_id}/comments",
                json=comment_data,
                headers=self.headers
            )
            
            if response.status_code in [200, 201]:
                logger.info(f"Successfully commented on post {post_id}")
                return True
            else:
                logger.error(f"Failed to comment on post {post_id}, status: {response.status_code}")
                logger.error(f"Response: {response.text}")
                
                # Try alternative endpoint format
                alt_response = self.session.post(
                    f"{self.base_url}/comments",
                    json={
                        'post_id': post_id,
                        'content': comment_text
                    },
                    headers=self.headers
                )
                
                if alt_response.status_code in [200, 201]:
                    logger.info(f"Successfully commented on post {post_id} using alternative endpoint")
                    return True
                else:
                    logger.error(f"Alternative comment endpoint also failed: {alt_response.status_code}")
                    return False
        except Exception as e:
            logger.error(f"Error posting comment: {e}")
            return False

    def check_and_respond_to_comments(self):
        """Check all of the bot's posts for comments and respond appropriately"""
        logger.info("Checking for comments on my posts...")
        
        # Get the bot's posts
        my_posts = self.get_my_posts()
        
        if not my_posts:
            logger.info("No posts found or error retrieving posts")
            return
        
        # Process each post to check for comments
        for post in my_posts:
            post_id = post.get('id') or post.get('post', {}).get('id')
            if not post_id:
                continue
                
            # Get comments for this post
            comments = self.get_comments_for_post(post_id)
            
            if not comments:
                continue
            
            logger.info(f"Found {len(comments)} comments for post {post_id}")
            
            # Limit the number of comments to respond to in one cycle to prevent rate limiting
            comments_to_respond = min(len(comments), 5)  # Only respond to first 5 comments
            
            # Look for new comments that aren't from the bot itself
            for i, comment in enumerate(comments[:comments_to_respond]):
                comment_id = comment.get('id')
                comment_author = comment.get('author', {}).get('name', 'Unknown')
                comment_content = comment.get('content', '')
                
                # Skip if the comment is from the bot itself
                if comment_author == self.username:
                    continue
                
                # Check if we've already responded to this comment
                # (In a real implementation, we'd track this in a database)
                
                # Respond to the comment with a relevant response
                response_text = random.choice(self.comment_responses)
                logger.info(f"Responding to comment from {comment_author} on post {post_id}")
                
                success = self.post_comment(post_id, response_text)
                if success:
                    logger.info("Successfully responded to comment")
                else:
                    logger.error("Failed to respond to comment")
                    
                # Add a small delay to avoid rate limiting
                time.sleep(2)

    def run_hourly_cycle(self):
        """Run one cycle: post content and check for comments"""
        logger.info("Starting hourly bot cycle...")
        
        # Post a random sample post (but skip if rate limited)
        random_post = random.choice(self.sample_posts)
        success = self.post_molt(random_post)
        
        if success:
            logger.info("Content posted successfully!")
        else:
            logger.info("Could not post content (possibly due to rate limiting). Continuing to check comments.")
        
        # Check for and respond to comments on existing posts
        self.check_and_respond_to_comments()
        
        logger.info("Hourly cycle completed.")

    def run_continuous(self, interval_minutes=60):
        """Run the bot continuously with specified interval (default 60 minutes)"""
        logger.info(f"Running continuous bot with {interval_minutes}-minute intervals...")
        
        # Check authentication first
        if not self.check_auth():
            logger.error("Failed to authenticate. Exiting.")
            return
        
        while True:
            try:
                self.run_hourly_cycle()
                
                logger.info(f"Waiting {interval_minutes} minutes for next cycle...")
                time.sleep(interval_minutes * 60)
            except KeyboardInterrupt:
                logger.info("\nBot stopped by user.")
                break
            except Exception as e:
                logger.error(f"Error in continuous run: {e}")
                time.sleep(60)  # Wait a minute before retrying

def main():
    bot = MoltbookBot()
    
    # Run one cycle to post and check comments
    if bot.check_auth():
        bot.run_hourly_cycle()
    else:
        logger.error("Failed to authenticate. Exiting.")

if __name__ == "__main__":
    main()