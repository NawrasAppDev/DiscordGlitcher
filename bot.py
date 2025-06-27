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
        intents.members = True  # Required for DM commands and member access
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

@bot.tree.command(name="glitch", description="Spam mentions of a user")
async def glitch_command(interaction: discord.Interaction, user: discord.Member):
    """
    Slash command that spams mentions of a specific user
    """
    try:
        # Acknowledge the interaction first
        await interaction.response.defer()

        logger.info(f"Glitch command triggered by {interaction.user} in {interaction.channel} targeting {user}")

        # Get the channel where the command was used
        channel = interaction.channel

        if not channel:
            await interaction.followup.send("❌ Could not access the channel!", ephemeral=True)
            return

        # Check if bot has permission to send messages
        bot_member = interaction.guild.me
        if not bot_member or not channel.permissions_for(bot_member).send_messages:
            await interaction.followup.send("❌ I don't have permission to send messages in this channel! Please give me 'Send Messages' permission.", ephemeral=True)
            return

        # Send initial response
        await interaction.followup.send(f"🔥 **GLITCH ACTIVATED** 🔥\nSpamming {user.mention} mentions and pinging everyone...")

        # Spam the mentions - set to 100 as requested
        spam_count = 100
        successful_sends = 0

        for i in range(spam_count):
            try:
                # Create the mention message with the actual user and @everyone ping
                message = f"@everyone {user.mention} GLITCH #{i+1} 🔥⚡"

                # Send the message with rate limit handling
                await handle_rate_limit(channel.send, message)
                successful_sends += 1

                logger.info(f"Sent spam message {i+1}/{spam_count}")

                # No delay between messages
                if Config.MESSAGE_DELAY > 0:
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

@bot.tree.command(name="glitchev-100", description="Ping @everyone 100 times")
async def glitchev_100_command(interaction: discord.Interaction):
    """
    Slash command that pings @everyone 100 times
    """
    try:
        # Acknowledge the interaction first
        await interaction.response.defer()

        logger.info(f"GlitchEV-100 command triggered by {interaction.user} in {interaction.channel}")

        # Get the channel where the command was used
        channel = interaction.channel

        if not channel:
            await interaction.followup.send("❌ Could not access the channel!", ephemeral=True)
            return

        # Check if bot has permission to send messages
        bot_member = interaction.guild.me
        if not bot_member or not channel.permissions_for(bot_member).send_messages:
            await interaction.followup.send("❌ I don't have permission to send messages in this channel! Please give me 'Send Messages' permission.", ephemeral=True)
            return

        # Send initial response
        await interaction.followup.send(f"🔥 **GLITCH EV-100 ACTIVATED** 🔥\nPinging everyone 100 times...")

        # Spam @everyone 100 times
        spam_count = 100
        successful_sends = 0

        for i in range(spam_count):
            try:
                # Create the @everyone ping message
                message = f"@everyone GLITCH EV #{i+1} 🔥⚡"

                # Send the message with rate limit handling
                await handle_rate_limit(channel.send, message)
                successful_sends += 1

                logger.info(f"Sent @everyone spam message {i+1}/{spam_count}")

                # No delay between messages
                if Config.MESSAGE_DELAY > 0:
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
            completion_msg = f"✅ **GLITCH EV-100 COMPLETE** ✅\nSent {successful_sends}/{spam_count} @everyone pings!"
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
        logger.error(f"Unexpected error in glitchev-100 command: {e}")
        try:
            await interaction.followup.send("❌ An unexpected error occurred!", ephemeral=True)
        except:
            pass

@bot.tree.command(name="ping-ec", description="Ping @everyone 100 times in every channel")
async def ping_ec_command(interaction: discord.Interaction):
    """
    Slash command that pings @everyone 100 times in every channel in the server
    """
    try:
        # Acknowledge the interaction first
        await interaction.response.defer()

        logger.info(f"Ping-EC command triggered by {interaction.user} in {interaction.guild}")

        # Get the guild
        guild = interaction.guild
        if not guild:
            await interaction.followup.send("❌ This command can only be used in a server!", ephemeral=True)
            return

        # Get all text channels in the guild
        text_channels = [channel for channel in guild.channels if isinstance(channel, discord.TextChannel)]

        if not text_channels:
            await interaction.followup.send("❌ No text channels found in this server!", ephemeral=True)
            return

        # Check bot permissions
        bot_member = guild.me
        if not bot_member:
            await interaction.followup.send("❌ Could not find bot member in server!", ephemeral=True)
            return

        # Send initial response
        await interaction.followup.send(f"🔥 **PING-EC ACTIVATED** 🔥\nPinging @everyone 100 times in {len(text_channels)} channels...")

        spam_count = 100
        total_successful_sends = 0

        # Loop through each channel
        for channel_index, channel in enumerate(text_channels):
            try:
                # Check if bot has permission to send messages in this channel
                if not channel.permissions_for(bot_member).send_messages:
                    logger.warning(f"No permission to send messages in {channel.name}")
                    # Send a message to the original channel about the skipped channel
                    try:
                        await interaction.channel.send(f"⚠️ Skipping #{channel.name} - No permission to send messages!")
                    except:
                        pass
                    continue

                logger.info(f"Starting spam in channel {channel.name} ({channel_index + 1}/{len(text_channels)})")

                # Spam @everyone 100 times in this channel
                channel_successful_sends = 0

                for i in range(spam_count):
                    try:
                        # Create the @everyone ping message
                        message = f"@everyone PING-EC #{i+1} in {channel.name} 🔥⚡"

                        # Send the message with rate limit handling
                        await handle_rate_limit(channel.send, message)
                        channel_successful_sends += 1
                        total_successful_sends += 1

                        logger.info(f"Sent @everyone spam message {i+1}/{spam_count} in {channel.name}")

                        # No delay between messages
                        if Config.MESSAGE_DELAY > 0:
                            await asyncio.sleep(Config.MESSAGE_DELAY)

                    except discord.HTTPException as e:
                        if e.status == 429:  # Rate limited
                            logger.warning(f"Rate limited on message {i+1} in {channel.name}, waiting...")
                            retry_after = getattr(e, 'retry_after', Config.RATE_LIMIT_DELAY)
                            await asyncio.sleep(retry_after)

                            # Try to send the message again
                            try:
                                await handle_rate_limit(channel.send, message)
                                channel_successful_sends += 1
                                total_successful_sends += 1
                            except Exception as retry_error:
                                logger.error(f"Failed to send message {i+1} in {channel.name} even after rate limit wait: {retry_error}")
                        else:
                            logger.error(f"HTTP error sending message {i+1} in {channel.name}: {e}")

                    except discord.Forbidden:
                        logger.error(f"Bot lacks permission to send messages in {channel.name}")
                        break

                    except Exception as e:
                        logger.error(f"Unexpected error sending message {i+1} in {channel.name}: {e}")

                logger.info(f"Completed spam in {channel.name}: {channel_successful_sends}/{spam_count} messages sent")

            except Exception as e:
                logger.error(f"Error processing channel {channel.name}: {e}")
                continue

        # Send completion message to the original channel
        try:
            completion_msg = f"✅ **PING-EC COMPLETE** ✅\nSent {total_successful_sends} total @everyone pings across {len(text_channels)} channels!"
            await handle_rate_limit(interaction.channel.send, completion_msg)
        except Exception as e:
            logger.error(f"Failed to send completion message: {e}")

    except discord.NotFound:
        logger.error("Interaction or guild not found")
    except discord.Forbidden:
        logger.error("Bot lacks necessary permissions")
        try:
            await interaction.followup.send("❌ I don't have the necessary permissions!", ephemeral=True)
        except:
            pass
    except Exception as e:
        logger.error(f"Unexpected error in ping-ec command: {e}")
        try:
            await interaction.followup.send("❌ An unexpected error occurred!", ephemeral=True)
        except:
            pass

@bot.tree.command(name="glitch-dm", description="Send DMs to everyone in the server 100 times")
async def glitch_dm_command(interaction: discord.Interaction):
    """
    Slash command that sends DMs to everyone in the server 100 times
    """
    try:
        # Acknowledge the interaction first
        await interaction.response.defer()

        logger.info(f"Glitch-DM command triggered by {interaction.user} in {interaction.guild}")

        # Get the guild
        guild = interaction.guild
        if not guild:
            await interaction.followup.send("❌ This command can only be used in a server!", ephemeral=True)
            return

        # Get all members in the guild
        members = [member for member in guild.members if not member.bot]

        if not members:
            await interaction.followup.send("❌ No members found in this server!", ephemeral=True)
            return

        # Send initial response
        await interaction.followup.send(f"🔥 **GLITCH-DM ACTIVATED** 🔥\nSending DMs to {len(members)} members 100 times each...")

        spam_count = 100
        total_successful_sends = 0

        # Loop through each member
        for member_index, member in enumerate(members):
            try:
                logger.info(f"Starting DM spam to {member.display_name} ({member_index + 1}/{len(members)})")

                # Spam DMs 100 times to this member
                member_successful_sends = 0

                for i in range(spam_count):
                    try:
                        # Create the DM message with user ping
                        message = f"{member.mention} GLITCH-DM #{i+1} 🔥⚡ From {interaction.guild.name} - You've been GLITCHED!"

                        # Send the DM with rate limit handling
                        await handle_rate_limit(member.send, message)
                        member_successful_sends += 1
                        total_successful_sends += 1

                        logger.info(f"Sent DM {i+1}/{spam_count} to {member.display_name}")

                        # No delay between messages
                        if Config.MESSAGE_DELAY > 0:
                            await asyncio.sleep(Config.MESSAGE_DELAY)

                    except discord.HTTPException as e:
                        if e.status == 429:  # Rate limited
                            logger.warning(f"Rate limited on DM {i+1} to {member.display_name}, waiting...")
                            retry_after = getattr(e, 'retry_after', Config.RATE_LIMIT_DELAY)
                            await asyncio.sleep(retry_after)

                            # Try to send the DM again
                            try:
                                await handle_rate_limit(member.send, message)
                                member_successful_sends += 1
                                total_successful_sends += 1
                            except Exception as retry_error:
                                logger.error(f"Failed to send DM {i+1} to {member.display_name} even after rate limit wait: {retry_error}")
                        else:
                            logger.error(f"HTTP error sending DM {i+1} to {member.display_name}: {e}")

                    except discord.Forbidden:
                        logger.error(f"Cannot send DM to {member.display_name} - DMs disabled or blocked")
                        break

                    except Exception as e:
                        logger.error(f"Unexpected error sending DM {i+1} to {member.display_name}: {e}")

                logger.info(f"Completed DM spam to {member.display_name}: {member_successful_sends}/{spam_count} messages sent")

            except Exception as e:
                logger.error(f"Error processing member {member.display_name}: {e}")
                continue

        # Send completion message to the original channel
        try:
            completion_msg = f"✅ **GLITCH-DM COMPLETE** ✅\nSent {total_successful_sends} total DMs to {len(members)} members!"
            await handle_rate_limit(interaction.channel.send, completion_msg)
        except Exception as e:
            logger.error(f"Failed to send completion message: {e}")

    except discord.NotFound:
        logger.error("Interaction or guild not found")
    except discord.Forbidden:
        logger.error("Bot lacks necessary permissions")
        try:
            await interaction.followup.send("❌ I don't have the necessary permissions!", ephemeral=True)
        except:
            pass
    except Exception as e:
        logger.error(f"Unexpected error in glitch-dm command: {e}")
        try:
            await interaction.followup.send("❌ An unexpected error occurred!", ephemeral=True)
        except:
            pass

@bot.event
async def on_message(message):
    """Handle regular messages for glitch commands"""
    # Ignore messages from bots
    if message.author.bot:
        return

    # Process the message for glitch commands
    if message.content.lower().startswith('glitch '):
        try:
            parts = message.content.split()
            if len(parts) >= 3:
                # Parse: glitch @user number
                mentioned_user = None
                spam_count = 10  # default

                # Find mentioned user
                if message.mentions:
                    mentioned_user = message.mentions[0]

                # Find the number (look for digits in the parts)
                for part in parts[2:]:
                    if part.isdigit():
                        spam_count = min(int(part), 200)  # Cap at 200 for safety
                        break

                if mentioned_user:
                    logger.info(f"Message glitch command: {message.author} targeting {mentioned_user} for {spam_count} times")

                    # Send confirmation
                    await message.channel.send(f"🔥 **GLITCH ACTIVATED** 🔥\nSpamming {mentioned_user.mention} {spam_count} times!")

                    successful_sends = 0

                    for i in range(spam_count):
                        try:
                            # Create the mention message
                            spam_message = f"{mentioned_user.mention} GLITCH #{i+1} 🔥⚡"

                            # Send the message with rate limit handling
                            await handle_rate_limit(message.channel.send, spam_message)
                            successful_sends += 1

                            logger.info(f"Sent spam message {i+1}/{spam_count}")

                            # Small delay to avoid overwhelming
                            if Config.MESSAGE_DELAY > 0:
                                await asyncio.sleep(Config.MESSAGE_DELAY)

                        except discord.HTTPException as e:
                            if e.status == 429:  # Rate limited
                                logger.warning(f"Rate limited on message {i+1}, waiting...")
                                retry_after = getattr(e, 'retry_after', Config.RATE_LIMIT_DELAY)
                                await asyncio.sleep(retry_after)

                                # Try to send the message again
                                try:
                                    await handle_rate_limit(message.channel.send, spam_message)
                                    successful_sends += 1
                                except Exception as retry_error:
                                    logger.error(f"Failed to send message {i+1} even after rate limit wait: {retry_error}")
                            else:
                                logger.error(f"HTTP error sending message {i+1}: {e}")

                        except discord.Forbidden:
                            logger.error("Bot lacks permission to send messages")
                            await message.channel.send("❌ I lost permission to send messages!")
                            break

                        except Exception as e:
                            logger.error(f"Unexpected error sending message {i+1}: {e}")

                    # Send completion message
                    try:
                        completion_msg = f"✅ **GLITCH COMPLETE** ✅\nSent {successful_sends}/{spam_count} spam messages!"
                        await handle_rate_limit(message.channel.send, completion_msg)
                    except Exception as e:
                        logger.error(f"Failed to send completion message: {e}")

        except Exception as e:
            logger.error(f"Error processing glitch message command: {e}")
            await message.channel.send("❌ Error processing glitch command!")

    # Process other commands
    await bot.process_commands(message)

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
        logger.error(f"Bot crashed with error: {e}")