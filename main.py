import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
from modules.invite_logger import setup_invite_logger
from modules.config_manager import ConfigManager
from datetime import datetime
import sys

# Load environment variables
load_dotenv()

# === FIXED LOGGING SYSTEM ===
def log(message, log_type="INFO"):
    """Simple logging function with forced file write"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_message = f"[{timestamp}] [{log_type}] {message}"
    
    # Print to console
    emoji = "❌" if log_type == "ERROR" else "ℹ️"
    print(f"{emoji} {message}")
    
    # Write to file with immediate flush
    try:
        # Ensure logs directory exists
        if not os.path.exists("logs"):
            os.makedirs("logs")
            
        # Write to file and force immediate save
        with open("logs/bot.log", "a", encoding="utf-8") as f:
            f.write(log_message + "\n")
            f.flush()  # Force write to disk
            os.fsync(f.fileno())  # Force OS to write to disk
            
    except Exception as e:
        print(f"❌ Failed to write log: {e}")

# Log startup immediately when script starts
log("=== DISCORD BOT STARTUP ===")
log("Loading environment variables...")

# Initialize bot
intents = discord.Intents.default()
intents.members = True
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

log("Bot instance created successfully")

# Initialize config manager
try:
    config_manager = ConfigManager()
    log("Configuration manager initialized")
except Exception as e:
    log(f"Failed to initialize config manager: {str(e)}", "ERROR")
    sys.exit(1)

@bot.event
async def on_ready():
    """Bot ready event - logs when bot successfully connects"""
    log(f'Bot {bot.user} is now online and ready!')
    log(f'Connected to {len(bot.guilds)} Discord servers')
    log(f'Current communication style: {config_manager.current_style}')
    
    # Also print to console for immediate feedback
    print(f'✅ Bot {bot.user} is ready!')
    print(f'📊 Connected to {len(bot.guilds)} servers')
    print(f'🎨 Current style: {config_manager.current_style}')
        
    # Setup invite tracking system
    try:
        await setup_invite_logger(bot, config_manager)
        log("Invite tracking system initialized successfully")
    except Exception as e:
        log(f"Failed to setup invite tracking: {str(e)}", "ERROR")

@bot.event
async def on_error(event, *args, **kwargs):
    """Global error handler for bot events"""
    import traceback
    error_msg = f"Error in event '{event}': {traceback.format_exc()}"
    log(error_msg, "ERROR")

@bot.event
async def on_guild_join(guild):
    """Log when bot joins a new server"""
    log(f"Bot joined new server: {guild.name} (ID: {guild.id}, Members: {guild.member_count})")

@bot.event
async def on_guild_remove(guild):
    """Log when bot leaves a server"""
    log(f"Bot left server: {guild.name} (ID: {guild.id})")

@bot.command(name="setstyle")
@commands.has_permissions(administrator=True)
async def set_style(ctx, style: str):
    """Set bot communication style (admin only)"""
    try:
        log(f"Style change requested by {ctx.author} in {ctx.guild.name}: {style}")
        
        if config_manager.set_style(style):
            style_info = config_manager.get_current_style_info()
            embed = discord.Embed(
                title="✅ Style Updated",
                description=f"**Style:** {style_info['name']}\n**Language:** {style_info['language']}\n**Tone:** {style_info['tone']}\n**Description:** {style_info['description']}",
                color=discord.Color.green()
            )
            await ctx.send(embed=embed)
            log(f"Communication style successfully changed to: {style}")
        else:
            available_styles = config_manager.get_available_styles()
            styles_info = []
            for style_name in available_styles:
                info = config_manager.get_style_info(style_name)
                styles_info.append(f"**{style_name}** - {info['name']} ({info['language']}, {info['tone']})")
                    
            embed = discord.Embed(
                title="❌ Invalid Style",
                description="**Available styles:**\n" + "\n".join(styles_info),
                color=discord.Color.red()
            )
            await ctx.send(embed=embed)
            log(f"Invalid style requested: {style}", "ERROR")
            
    except Exception as e:
        log(f"Error in setstyle command: {str(e)}", "ERROR")
        await ctx.send("❌ An error occurred while changing style.")

@bot.command(name="styles")
async def list_styles(ctx):
    """List all available communication styles"""
    try:
        log(f"Style list requested by {ctx.author} in {ctx.guild.name}")
        
        available_styles = config_manager.get_available_styles()
        current_style = config_manager.current_style
            
        styles_info = []
        for style_name in available_styles:
            info = config_manager.get_style_info(style_name)
            marker = "🔸" if style_name == current_style else "▫️"
            styles_info.append(f"{marker} **{style_name}** - {info['name']}\n   📝 {info['description']}\n   🌍 {info['language']} | 🎭 {info['tone']}")
            
        embed = discord.Embed(
            title="🎨 Available Communication Styles",
            description="\n\n".join(styles_info),
            color=discord.Color.blue()
        )
        embed.set_footer(text="🔸 = Current style | Use !setstyle <name> to change")
        await ctx.send(embed=embed)
        
    except Exception as e:
        log(f"Error in styles command: {str(e)}", "ERROR")
        await ctx.send("❌ An error occurred while listing styles.")

@bot.command(name="reloadconfig")
@commands.has_permissions(administrator=True)
async def reload_config(ctx):
    """Reload configuration files (admin only)"""
    try:
        log(f"Configuration reload requested by {ctx.author} in {ctx.guild.name}")
        
        config_manager.reload_config()
        style_info = config_manager.get_current_style_info()
        embed = discord.Embed(
            title="✅ Configuration Reloaded",
            description=f"All configuration files have been reloaded successfully!\n\n**Current Style:** {style_info['name']}\n**Language:** {style_info['language']}\n**Tone:** {style_info['tone']}",
            color=discord.Color.green()
        )
        await ctx.send(embed=embed)
        log("Configuration files reloaded successfully")
        
    except Exception as e:
        log(f"Error reloading configuration: {str(e)}", "ERROR")
        embed = discord.Embed(
            title="❌ Reload Failed",
            description=f"Error reloading configuration: {str(e)}",
            color=discord.Color.red()
        )
        await ctx.send(embed=embed)

if __name__ == "__main__":
    log("Checking for Discord bot token...")
    TOKEN = os.getenv("DISCORD_TOKEN")
    if not TOKEN:
        log("DISCORD_TOKEN not found in environment variables!", "ERROR")
        print("❌ DISCORD_TOKEN not found in environment variables!")
        print("Please check your .env file and make sure DISCORD_TOKEN is set.")
        sys.exit(1)
    
    log("Discord token found successfully")
    log("Attempting to connect to Discord...")
    
    try:
        # Start the bot
        bot.run(TOKEN)
    except KeyboardInterrupt:
        log("Bot shutdown requested by user (Ctrl+C)")
    except Exception as e:
        log(f"Critical error starting bot: {str(e)}", "ERROR")
        print(f"❌ Failed to start bot: {str(e)}")
    finally:
        log("=== DISCORD BOT SHUTDOWN ===")
