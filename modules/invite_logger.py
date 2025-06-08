import discord
from discord.ext import commands
import json
import os
from collections import defaultdict
from typing import Dict, Optional

# Global variables for invite tracking
invites = {}
invite_counts = defaultdict(int)
invited_by = {}

def save_invite_counts():
    """Save invite counts to file"""
    os.makedirs("data", exist_ok=True)
    with open("data/invite_counts.json", "w", encoding="utf-8") as f:
        json.dump(dict(invite_counts), f, ensure_ascii=False, indent=4)

def save_invited_by():
    """Save invited by data to file"""
    os.makedirs("data", exist_ok=True)
    with open("data/invited_by.json", "w", encoding="utf-8") as f:
        json.dump(invited_by, f, ensure_ascii=False, indent=4)

def load_invite_data():
    """Load invite data from files"""
    global invite_counts, invited_by
    
    # Load invite counts
    if os.path.exists("data/invite_counts.json"):
        with open("data/invite_counts.json", "r", encoding="utf-8") as f:
            invite_counts = defaultdict(int, json.load(f))
    
    # Load invited by data
    if os.path.exists("data/invited_by.json"):
        with open("data/invited_by.json", "r", encoding="utf-8") as f:
            invited_by = json.load(f)

async def update_inviter_roles(inviter, invite_count, inviter_roles, guild):
    """Update inviter roles based on invite count"""
    try:
        # Check if user should get a new role
        for required_count, role_id in inviter_roles.items():
            if invite_count >= required_count:
                role = guild.get_role(role_id)
                if role and role not in inviter.roles:
                    await inviter.add_roles(role)
                    print(f"✅ Assigned role {role.name} to {inviter.name} for {invite_count} invites")
    except Exception as e:
        print(f"❌ Error updating inviter roles: {e}")

async def setup_invite_logger(bot, config_manager):
    """Setup invite logger functionality"""
    if bot is None:
        print("❌ Error: bot object is None in setup_invite_logger")
        return
    
    # Load existing invite data
    load_invite_data()
    
    # Get environment variables
    WELCOME_CHANNEL_ID = int(os.getenv("WELCOME_CHANNEL_ID", 0))
    MEMBER_ROLE_ID = int(os.getenv("MEMBER_ROLE_ID", 0))
    
    # Parse inviter roles from environment
    INVITER_ROLES = {}
    if os.getenv("INVITER_ROLES"):
        for role_info in os.getenv("INVITER_ROLES").split(','):
            try:
                count, role_id = role_info.split(':')
                INVITER_ROLES[int(count)] = int(role_id)
            except ValueError:
                print(f"⚠️ Invalid INVITER_ROLES format: {role_info}")
    
    @bot.event
    async def on_ready():
        """Load invite cache when bot is ready"""
        print("🔄 Loading invite cache...")
        for guild in bot.guilds:
            try:
                invites[guild.id] = await guild.invites()
                print(f"✅ Invite cache loaded for server {guild.name}")
            except Exception as e:
                print(f"❌ Error loading invites for server {guild.name}: {e}")
        print("✅ Bot is ready!")
    
    @bot.event
    async def on_invite_create(invite):
        """Update invite cache when new invite is created"""
        guild = invite.guild
        try:
            invites[guild.id] = await guild.invites()
            print(f"✅ Invite cache updated after new invite creation on server {guild.name}")
        except Exception as e:
            print(f"❌ Error updating invite cache: {e}")
    
    @bot.event
    async def on_member_join(member):
        """Handle member join events"""
        if member.bot:
            return
        
        guild = member.guild
        welcome_channel = bot.get_channel(WELCOME_CHANNEL_ID)
        
        # Assign member role if configured
        if MEMBER_ROLE_ID and config_manager.get_feature_enabled("auto_role_assignment"):
            try:
                member_role = guild.get_role(MEMBER_ROLE_ID)
                if member_role:
                    await member.add_roles(member_role)
                    print(f"✅ Assigned role {member_role.name} to user {member.name}")
                else:
                    print(f"❌ Role with ID {MEMBER_ROLE_ID} not found on server")
            except Exception as e:
                print(f"❌ Error assigning role: {e}")
        
        if not welcome_channel or not config_manager.get_feature_enabled("welcome_messages"):
            return
        
        # Get current invites
        try:
            current_invites = await guild.invites()
            print(f"📋 Retrieved {len(current_invites)} current invites")
        except Exception as e:
            print(f"❌ Error getting current invites: {e}")
            current_invites = []
        
        # Find used invite
        inviter = None
        invite_code = None
        
        if guild.id in invites and config_manager.get_feature_enabled("invite_tracking"):
            old_invites = invites[guild.id]
            
            print(f"🔍 Searching for used invite for {member.name}...")
            print(f"📊 Old invites: {len(old_invites)}, New invites: {len(current_invites)}")
            
            # Create dictionary for quick lookup
            old_invites_dict = {invite.code: invite.uses for invite in old_invites}
            
            # Compare old and new invites
            for invite in current_invites:
                if invite.code in old_invites_dict:
                    old_uses = old_invites_dict[invite.code]
                    if invite.uses > old_uses:
                        inviter = invite.inviter
                        invite_code = invite.code
                        print(f"✅ Found used invite: {invite_code} by {inviter.name}")
                        print(f"   Uses: {old_uses} -> {invite.uses}")
                        break
            
            # Check for one-time invites that disappeared
            if not inviter:
                print("🔍 Checking for one-time invites...")
                for old_invite in old_invites:
                    if not any(inv.code == old_invite.code for inv in current_invites):
                        print(f"🔎 Found disappeared invite: {old_invite.code}")
                        inviter = old_invite.inviter
                        invite_code = old_invite.code
                        print(f"✅ Probably used one-time invite: {invite_code} by {inviter.name}")
                        break
        
        # Update invite cache
        invites[guild.id] = current_invites
        print(f"✅ Invite cache updated after {member.name} joined")
        
        # Process inviter if found
        if inviter:
            # Increment invite count
            invite_counts[str(inviter.id)] += 1
            current_invites_count = invite_counts[str(inviter.id)]
            save_invite_counts()
            
            # Save who invited whom
            invited_by[str(member.id)] = str(inviter.id)
            save_invited_by()
            print(f"📝 Saved invite info: {member.name} was invited by {inviter.name}")
            
            # Check if inviter should get a role
            await update_inviter_roles(inviter, current_invites_count, INVITER_ROLES, guild)
            
            # Send welcome message with inviter info
            greeting = config_manager.get_random_greeting()
            formatted_greeting = greeting.format(
                user=member.mention,
                inviter=inviter.mention,
                count=current_invites_count
            )
            
            embed = discord.Embed(
                title=config_manager.get_embed_title("new_member_title"),
                description=formatted_greeting,
                color=discord.Color.green()
            )
            embed.set_thumbnail(url=member.display_avatar.url)
            embed.timestamp = discord.utils.utcnow()
            await welcome_channel.send(embed=embed)
        else:
            print(f"⚠️ Could not determine who invited {member.name}")
            # Send default welcome message
            default_greeting = config_manager.lang_config.get("default_greeting", "Welcome {user}!")
            formatted_greeting = default_greeting.format(user=member.mention)
            
            embed = discord.Embed(
                title=config_manager.get_embed_title("new_member_title"),
                description=formatted_greeting,
                color=discord.Color.green()
            )
            embed.set_thumbnail(url=member.display_avatar.url)
            embed.timestamp = discord.utils.utcnow()
            await welcome_channel.send(embed=embed)
    
    @bot.event
    async def on_member_remove(member):
        """Handle member leave events"""
        if member.bot:
            return
        
        guild = member.guild
        welcome_channel = bot.get_channel(WELCOME_CHANNEL_ID)
        
        if not welcome_channel or not config_manager.get_feature_enabled("leave_messages"):
            return
        
        # Check if we know who invited this member
        member_id = str(member.id)
        inviter_id = invited_by.get(member_id)
        
        if inviter_id and config_manager.get_feature_enabled("invite_tracking"):
            # Decrease inviter's count
            invite_counts[inviter_id] = max(0, invite_counts[inviter_id] - 1)
            save_invite_counts()
            
            # Remove from invited_by tracking
            del invited_by[member_id]
            save_invited_by()
            
            # Get inviter info
            try:
                inviter = await bot.fetch_user(int(inviter_id))
                inviter_mention = inviter.mention
                current_count = invite_counts[inviter_id]
                print(f"📉 Decreased invite count for {inviter.name}: {current_count + 1} -> {current_count}")
            except:
                inviter_mention = "Unknown User"
                current_count = invite_counts[inviter_id]
            
            # Send leave message with inviter info
            leave_message = config_manager.get_random_leave_message()
            formatted_message = leave_message.format(
                user=member.name,
                inviter=inviter_mention,
                count=current_count
            )
        else:
            # Send default leave message
            default_leave = config_manager.lang_config.get("default_leave_message", "Goodbye {user}!")
            formatted_message = default_leave.format(user=member.name)
        
        embed = discord.Embed(
            title=config_manager.get_embed_title("member_left_title"),
            description=formatted_message,
            color=discord.Color.red()
        )
        embed.set_thumbnail(url=member.display_avatar.url)
        embed.timestamp = discord.utils.utcnow()
        await welcome_channel.send(embed=embed)
    
    # Add invite-related commands
    @bot.command(name="invites")
    async def check_invites(ctx, user: discord.Member = None):
        """Check invite count for a user"""
        if not config_manager.get_feature_enabled("invite_tracking"):
            await ctx.send(config_manager.get_message("feature_disabled"))
            return
        
        target_user = user or ctx.author
        user_invites = invite_counts.get(str(target_user.id), 0)
        
        embed = discord.Embed(
            title=config_manager.get_embed_title("invite_count_title"),
            description=config_manager.get_message("invite_count_message").format(
                user=target_user.mention,
                count=user_invites
            ),
            color=discord.Color.blue()
        )
        embed.set_thumbnail(url=target_user.display_avatar.url)
        await ctx.send(embed=embed)
    
    @bot.command(name="leaderboard", aliases=["lb", "top"])
    async def invite_leaderboard(ctx, limit: int = 10):
        """Show invite leaderboard"""
        if not config_manager.get_feature_enabled("invite_tracking"):
            await ctx.send(config_manager.get_message("feature_disabled"))
            return
        
        if limit > 20:
            limit = 20
        
        # Sort users by invite count
        sorted_invites = sorted(invite_counts.items(), key=lambda x: x[1], reverse=True)
        
        if not sorted_invites:
            embed = discord.Embed(
                title=config_manager.get_embed_title("leaderboard_title"),
                description=config_manager.get_message("no_invites_yet"),
                color=discord.Color.blue()
            )
            await ctx.send(embed=embed)
            return
        
        leaderboard_text = ""
        for i, (user_id, count) in enumerate(sorted_invites[:limit], 1):
            try:
                user = await bot.fetch_user(int(user_id))
                username = user.name
            except:
                username = "Unknown User"
            
            medal = "🥇" if i == 1 else "🥈" if i == 2 else "🥉" if i == 3 else f"{i}."
            leaderboard_text += f"{medal} **{username}** - {count} invites\n"
        
        embed = discord.Embed(
            title=config_manager.get_embed_title("leaderboard_title"),
            description=leaderboard_text,
            color=discord.Color.gold()
        )
        embed.set_footer(text=f"Top {min(limit, len(sorted_invites))} inviters")
        await ctx.send(embed=embed)
    
    @bot.command(name="whoinvited")
    async def who_invited(ctx, user: discord.Member = None):
        """Check who invited a specific user"""
        if not config_manager.get_feature_enabled("invite_tracking"):
            await ctx.send(config_manager.get_message("feature_disabled"))
            return
        
        target_user = user or ctx.author
        inviter_id = invited_by.get(str(target_user.id))
        
        if not inviter_id:
            embed = discord.Embed(
                title=config_manager.get_embed_title("who_invited_title"),
                description=config_manager.get_message("inviter_unknown").format(user=target_user.mention),
                color=discord.Color.orange()
            )
        else:
            try:
                inviter = await bot.fetch_user(int(inviter_id))
                embed = discord.Embed(
                    title=config_manager.get_embed_title("who_invited_title"),
                    description=config_manager.get_message("invited_by_message").format(
                        user=target_user.mention,
                        inviter=inviter.mention
                    ),
                    color=discord.Color.green()
                )
                embed.set_thumbnail(url=inviter.display_avatar.url)
            except:
                embed = discord.Embed(
                    title=config_manager.get_embed_title("who_invited_title"),
                    description=config_manager.get_message("inviter_not_found").format(user=target_user.mention),
                    color=discord.Color.red()
                )
        
        await ctx.send(embed=embed)
    
    @bot.command(name="resetinvites")
    @commands.has_permissions(administrator=True)
    async def reset_invites(ctx, user: discord.Member = None):
        """Reset invite count for a user or all users (admin only)"""
        if not config_manager.get_feature_enabled("invite_tracking"):
            await ctx.send(config_manager.get_message("feature_disabled"))
            return
        
        if user:
            # Reset specific user
            user_id = str(user.id)
            old_count = invite_counts.get(user_id, 0)
            invite_counts[user_id] = 0
            save_invite_counts()
            
            embed = discord.Embed(
                title=config_manager.get_embed_title("reset_invites_title"),
                description=config_manager.get_message("user_invites_reset").format(
                    user=user.mention,
                    count=old_count
                ),
                color=discord.Color.green()
            )
        else:
            # Reset all invites
            total_users = len(invite_counts)
            invite_counts.clear()
            invited_by.clear()
            save_invite_counts()
            save_invited_by()
            
            embed = discord.Embed(
                title=config_manager.get_embed_title("reset_invites_title"),
                description=config_manager.get_message("all_invites_reset").format(count=total_users),
                color=discord.Color.green()
            )
        
        await ctx.send(embed=embed)
    
    print("✅ Invite logger setup completed")
