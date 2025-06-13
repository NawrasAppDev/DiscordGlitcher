"""
Configuration settings for the Discord bot
"""

class Config:
    # Number of spam messages to send (kept reasonable to avoid severe rate limiting)
    SPAM_COUNT = 8
    
    # Delay between messages in seconds (helps avoid rate limits)
    MESSAGE_DELAY = 0.5
    
    # Delay when rate limited (seconds)
    RATE_LIMIT_DELAY = 2.0
    
    # Maximum retries for failed messages
    MAX_RETRIES = 3
    
    # Bot settings
    COMMAND_PREFIX = "!"
    
    # Logging settings
    LOG_LEVEL = "INFO"
    LOG_FILE = "bot.log"
