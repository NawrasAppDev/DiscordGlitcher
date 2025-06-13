"""
Utility functions for the Discord bot
"""

import asyncio
import logging
import discord
from config import Config

logger = logging.getLogger(__name__)

async def handle_rate_limit(coro_func, *args, **kwargs):
    """
    Handle rate limiting for Discord API calls with optimized retry logic
    """
    max_attempts = 10  # Increased for spam scenarios
    
    for attempt in range(max_attempts):
        try:
            return await coro_func(*args, **kwargs)
            
        except discord.HTTPException as e:
            if e.status == 429:  # Rate limited
                # Use Discord's exact retry time or minimum 1 second
                retry_after = max(getattr(e, 'retry_after', 1.0), 0.5)
                logger.warning(f"Rate limited, waiting {retry_after:.1f}s")
                await asyncio.sleep(retry_after)
            else:
                # Re-raise non-rate-limit HTTP exceptions
                raise
                
        except Exception as e:
            # Re-raise unexpected exceptions
            raise
    
    # If all attempts failed
    raise Exception(f"Failed after {max_attempts} attempts due to persistent rate limiting")

def format_error_message(error):
    """
    Format error messages for user display
    
    Args:
        error: The exception object
    
    Returns:
        str: A formatted error message
    """
    if isinstance(error, discord.Forbidden):
        return "❌ I don't have permission to perform this action!"
    elif isinstance(error, discord.NotFound):
        return "❌ The requested resource was not found!"
    elif isinstance(error, discord.HTTPException):
        if error.status == 429:
            return "❌ I'm being rate limited! Please try again later."
        else:
            return f"❌ Discord API error: {error.text}"
    else:
        return "❌ An unexpected error occurred!"

def validate_permissions(channel, required_permissions):
    """
    Check if the bot has required permissions in a channel
    
    Args:
        channel: The Discord channel object
        required_permissions: List of permission names to check
    
    Returns:
        tuple: (bool, list) - (has_all_permissions, missing_permissions)
    """
    if not hasattr(channel, 'permissions_for'):
        return False, ["Cannot check permissions for this channel type"]
    
    bot_permissions = channel.permissions_for(channel.guild.me)
    missing_permissions = []
    
    for perm in required_permissions:
        if not getattr(bot_permissions, perm, False):
            missing_permissions.append(perm)
    
    return len(missing_permissions) == 0, missing_permissions

async def safe_send_message(channel, content, **kwargs):
    """
    Safely send a message with error handling
    
    Args:
        channel: The Discord channel to send to
        content: The message content
        **kwargs: Additional arguments for send()
    
    Returns:
        discord.Message or None: The sent message, or None if failed
    """
    try:
        return await handle_rate_limit(channel.send, content, **kwargs)
    except discord.Forbidden:
        logger.error(f"No permission to send message in {channel}")
        return None
    except discord.HTTPException as e:
        logger.error(f"HTTP error sending message: {e}")
        return None
    except Exception as e:
        logger.error(f"Unexpected error sending message: {e}")
        return None

def get_user_display_name(user):
    """
    Get the display name for a user
    
    Args:
        user: Discord user object
    
    Returns:
        str: The user's display name
    """
    if hasattr(user, 'display_name'):
        return user.display_name
    elif hasattr(user, 'global_name') and user.global_name:
        return user.global_name
    else:
        return user.name
