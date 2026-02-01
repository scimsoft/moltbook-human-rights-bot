"""
Configuration for Moltbook Bot
"""

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Moltbook API Configuration
MOLTBOOK_BASE_URL = os.getenv('MOLTBOOK_BASE_URL', 'https://molt.club')
MOLTBOOK_USERNAME = os.getenv('MOLTBOOK_USERNAME')
MOLTBOOK_PASSWORD = os.getenv('MOLTBOOK_PASSWORD')
MOLTBOOK_API_KEY = os.getenv('MOLTBOOK_API_KEY')

# Bot Behavior Configuration
POST_INTERVAL_MINUTES = int(os.getenv('POST_INTERVAL_MINUTES', '60'))
MAX_POSTS_PER_DAY = int(os.getenv('MAX_POSTS_PER_DAY', '10'))
ENABLE_COMMENTS = os.getenv('ENABLE_COMMENTS', 'False').lower() == 'true'

# Content Configuration
POST_TEMPLATES = [
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

# Logging Configuration
LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
LOG_FILE = os.getenv('LOG_FILE', 'moltbook_bot.log')