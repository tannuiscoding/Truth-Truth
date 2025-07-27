import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Bot Configuration
BOT_TOKEN = os.getenv('DISCORD_TOKEN')
COMMAND_PREFIX = '!'

# Web Scraping Configuration
REQUEST_TIMEOUT = 10
MAX_QUESTIONS_PER_SOURCE = 50
CACHE_DURATION_HOURS = 1

# User Agent for web scraping
USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'

# Question sources - you can add more sources here
QUESTION_SOURCES = {
    'truth': [
        'https://www.truthordarequestions.net/truth-questions/',
        'https://www.truthordarequestions.net/funny-truth-questions/',
        'https://www.truthordarequestions.net/dirty-truth-questions/',
        'https://www.truthordarequestions.net/embarrassing-truth-questions/'
    ],
    'dare': [
        'https://www.truthordarequestions.net/dare-questions/',
        'https://www.truthordarequestions.net/funny-dare-questions/',
        'https://www.truthordarequestions.net/dirty-dare-questions/',
        'https://www.truthordarequestions.net/embarrassing-dare-questions/'
    ],
    'would_you_rather': [
        'https://www.truthordarequestions.net/would-you-rather-questions/',
        'https://www.truthordarequestions.net/funny-would-you-rather-questions/',
        'https://www.truthordarequestions.net/dirty-would-you-rather-questions/'
    ]
}

# Additional question sources (alternative websites)
ALTERNATIVE_SOURCES = {
    'truth': [
        'https://www.truthordarequestions.net/truth-questions-for-couples/',
        'https://www.truthordarequestions.net/truth-questions-for-teens/'
    ],
    'dare': [
        'https://www.truthordarequestions.net/dare-questions-for-couples/',
        'https://www.truthordarequestions.net/dare-questions-for-teens/'
    ]
}

# Words to filter out when scraping (to avoid ads, navigation, etc.)
FILTER_WORDS = [
    'cookie', 'privacy', 'advertisement', 'menu', 'navigation', 
    'subscribe', 'newsletter', 'ad', 'sponsored', 'click here',
    'terms', 'conditions', 'copyright', 'all rights reserved'
]

# Embed colors for different question types
EMBED_COLORS = {
    'truth': 0x00ff00,      # Green
    'dare': 0xff0000,       # Red
    'would_you_rather': 0x0099ff,  # Blue
    'random': 0x9932cc      # Purple
}

# Bot status messages
STATUS_MESSAGES = [
    "!info for commands",
    "Scraping questions...",
    "Truth or Dare?",
    "Would you rather...",
    "Playing with friends"
] 