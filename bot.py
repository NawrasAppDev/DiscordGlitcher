import discord
from discord.ext import commands
import asyncio
import logging
import os
from dotenv import load_dotenv
from config import Config
from utils import handle_rate_limit

# Load environment variables from .env file
load_dotenv()

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('bot.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class GlitchBot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True
        super().__init__(command_prefix='!', intents=intents)

    async def setup_hook(self):
        """Called when the bot is starting up"""
        try:
            # Sync slash commands
            synced = await self.tree.sync()
            logger.info(f"Synced {len(synced)} command(s)")
        except Exception as e:
            logger.error(f"Failed to sync commands: {e}")

    async def on_ready(self):
        """Called when the bot is ready"""
        logger.info(f'{self.user} has connected to Discord!')
        logger.info(f'Bot is in {len(self.guilds)} guilds')

    async def on_command_error(self, ctx, error):
        """Handle command errors"""
        logger.error(f"Command error: {error}")

bot = GlitchBot()

@bot.tree.command(name="glitch", description="Spam mentions of @example")
async def glitch_command(interaction: discord.Interaction):
    """
    Slash command that spams mentions of @example
    """
    try:
        # Acknowledge the interaction first
        await interaction.response.defer()
        
        logger.info(f"Glitch command triggered by {interaction.user} in {interaction.channel}")
        
        # Get the channel where the command was used
        channel = interaction.channel
        
        if not channel:
            await interaction.followup.send("❌ Could not access the channel!", ephemeral=True)
            return
            
        # Check if bot has permission to send messages
        if not channel.permissions_for(interaction.guild.me).send_messages:
            await interaction.followup.send("❌ I don't have permission to send messages in this channel!", ephemeral=True)
            return
        
        # Send initial response
        await interaction.followup.send("🔥 **GLITCH ACTIVATED** 🔥\nSpamming @example mentions...")
        
        # Spam the mentions
        spam_count = Config.SPAM_COUNT
        successful_sends = 0
        
        for i in range(spam_count):
            try:
                # Create the mention message
                message = f"@example GLITCH #{i+1} 🔥⚡"
                
                # Send the message with rate limit handling
                await handle_rate_limit(channel.send, message)
                successful_sends += 1
                
                logger.info(f"Sent spam message {i+1}/{spam_count}")
                
                # Small delay between messages to be less aggressive
                await asyncio.sleep(Config.MESSAGE_DELAY)
                
            except discord.HTTPException as e:
                if e.status == 429:  # Rate limited
                    logger.warning(f"Rate limited on message {i+1}, waiting...")
                    retry_after = getattr(e, 'retry_after', Config.RATE_LIMIT_DELAY)
                    await asyncio.sleep(retry_after)
                    
                    # Try to send the message again
                    try:
                        await handle_rate_limit(channel.send, message)
                        successful_sends += 1
                    except Exception as retry_error:
                        logger.error(f"Failed to send message {i+1} even after rate limit wait: {retry_error}")
                else:
                    logger.error(f"HTTP error sending message {i+1}: {e}")
                    
            except discord.Forbidden:
                logger.error("Bot lacks permission to send messages")
                await channel.send("❌ I lost permission to send messages!")
                break
                
            except Exception as e:
                logger.error(f"Unexpected error sending message {i+1}: {e}")
        
        # Send completion message
        try:
            completion_msg = f"✅ **GLITCH COMPLETE** ✅\nSent {successful_sends}/{spam_count} spam messages!"
            await handle_rate_limit(channel.send, completion_msg)
        except Exception as e:
            logger.error(f"Failed to send completion message: {e}")
            
    except discord.NotFound:
        logger.error("Interaction or channel not found")
    except discord.Forbidden:
        logger.error("Bot lacks necessary permissions")
        try:
            await interaction.followup.send("❌ I don't have the necessary permissions!", ephemeral=True)
        except:
            pass
    except Exception as e:
        logger.error(f"Unexpected error in glitch command: {e}")
        try:
            await interaction.followup.send("❌ An unexpected error occurred!", ephemeral=True)
        except:
            pass

@bot.event
async def on_app_command_error(interaction: discord.Interaction, error: Exception):
    """Handle slash command errors"""
    logger.error(f"Slash command error: {error}")
    
    if not interaction.response.is_done():
        try:
            await interaction.response.send_message("❌ An error occurred while processing the command!", ephemeral=True)
        except:
            pass
    else:
        try:
            await interaction.followup.send("❌ An error occurred while processing the command!", ephemeral=True)
        except:
            pass

async def main():
    """Main function to run the bot"""
    token = os.getenv('DISCORD_TOKEN')
    
    if not token:
        logger.error("Discord token not found! Please add DISCORD_TOKEN to your .env file.")
        return
    
    try:
        logger.info("Starting bot...")
        await bot.start(token)
    except discord.LoginFailure:
        logger.error("Invalid Discord token provided!")
    except discord.HTTPException as e:
        logger.error(f"HTTP error occurred: {e}")
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
    finally:
        await bot.close()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Bot stopped by user")
    except Exception as e:
        logger.error(f"Failed to start bot: {e}")
