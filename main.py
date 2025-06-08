import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
from modules.invite_logger import setup_invite_logger
from modules.config_manager import ConfigManager

# Load environment variables
load_dotenv()

# Initialize bot
intents = discord.Intents.default()
intents.members = True
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)

# Initialize config manager
config_manager = ConfigManager()

@bot.event
async def on_ready():
    print(f'✅ Bot {bot.user} is ready!')
    print(f'📊 Connected to {len(bot.guilds)} servers')
    print(f'🎨 Current style: {config_manager.current_style}')
    
    # Setup invite logger
    await setup_invite_logger(bot, config_manager)

@bot.command(name="setstyle")
@commands.has_permissions(administrator=True)
async def set_style(ctx, style: str):
    """Set bot communication style (admin only)"""
    if config_manager.set_style(style):
        style_info = config_manager.get_current_style_info()
        embed = discord.Embed(
            title="✅ Style Updated",
            description=f"**Style:** {style_info['name']}\n**Language:** {style_info['language']}\n**Tone:** {style_info['tone']}\n**Description:** {style_info['description']}",
            color=discord.Color.green()
        )
        await ctx.send(embed=embed)
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

@bot.command(name="styles")
async def list_styles(ctx):
    """List all available communication styles"""
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

@bot.command(name="reloadconfig")
@commands.has_permissions(administrator=True)
async def reload_config(ctx):
    """Reload configuration files (admin only)"""
    try:
        config_manager.reload_config()
        style_info = config_manager.get_current_style_info()
        embed = discord.Embed(
            title="✅ Configuration Reloaded",
            description=f"All configuration files have been reloaded successfully!\n\n**Current Style:** {style_info['name']}\n**Language:** {style_info['language']}\n**Tone:** {style_info['tone']}",
            color=discord.Color.green()
        )
        await ctx.send(embed=embed)
    except Exception as e:
        embed = discord.Embed(
            title="❌ Reload Failed",
            description=f"Error reloading configuration: {str(e)}",
            color=discord.Color.red()
        )
        await ctx.send(embed=embed)

if __name__ == "__main__":
    TOKEN = os.getenv("DISCORD_TOKEN")
    if not TOKEN:
        print("❌ DISCORD_TOKEN not found in environment variables!")
        exit(1)
    
    bot.run(TOKEN)
