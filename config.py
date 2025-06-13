"""
Configuration settings for the Discord bot
"""

class Config:
    # Number of spam messages to send (kept reasonable to avoid severe rate limiting)
    SPAM_COUNT = 100
    
    # Delay between messages in seconds (helps avoid rate limits)
    MESSAGE_DELAY = 0.2
    
    # Delay when rate limited (seconds)
    RATE_LIMIT_DELAY = 2.0
    
    # Maximum retries for failed messages
    MAX_RETRIES = 3
    
    # Bot settings
    COMMAND_PREFIX = "!"
    
    # Logging settings
    LOG_LEVEL = "INFO"
    LOG_FILE = "bot.log"
