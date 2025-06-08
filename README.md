<div align="center">

# 🎯 Discord Invite Tracker Bot

*A powerful Discord bot for tracking invitations with customizable communication styles*

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://python.org)
[![Discord.py](https://img.shields.io/badge/discord.py-2.3.0+-blue.svg)](https://github.com/Rapptz/discord.py)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

[Features](#-features) • [Installation](#-installation) • [Commands](#-commands) • [Configuration](#-configuration)

</div>

---

## ✨ Features

<table>
<tr>
<td width="50%">

### 🎯 **Core Features**
- 📊 **Real-time invite tracking**
- 🎉 **Custom welcome messages**
- 👋 **Goodbye notifications**
- 🏆 **Interactive leaderboards**

</td>
<td width="50%">

### 🎨 **Customization**
- 🌍 **Multi-language support**
- 🎭 **Communication styles**
- ⚙️ **Flexible configuration**
- 🔄 **Hot-reload settings**

</td>
</tr>
</table>

---

## 🎨 Communication Styles

<div align="center">

| Style | Language | Tone | Description |
|-------|----------|------|-------------|
| 🇷🇺 **casual_ru** | Russian | Friendly | Неформальный дружелюбный стиль |
| 🇷🇺 **formal_ru** | Russian | Professional | Официальный деловой стиль |
| 🇬🇧 **casual_en** | English | Casual | Warm and welcoming style |
| 🇬🇧 **formal_en** | English | Professional | Official formal communication |

</div>

---

## 🚀 Installation

### Quick Start

```bash
# 1. Download project
# ZIP: https://github.com/MrFolium/discord-invite-tracker-bot → Download ZIP
# OR Git:
git clone https://github.com/MrFolium/discord-invite-tracker-bot.git

# 2. Setup .env file
# Edit .env with your bot token and server ID

# 3. Run
# Windows: start.bat
# Linux: start.sh
```

### 📋 Requirements
- **Python 3.8+**
- **Discord Bot Token**
- **Server Administrator Permissions**

---

## 🎮 Commands

<details>
<summary><b>📊 Basic Commands</b></summary>

| Command | Description | Usage |
|---------|-------------|-------|
| `!invites` | Check invitation count | `!invites @user` |
| `!leaderboard` | Show top inviters | `!leaderboard 10` |
| `!whoinvited` | Find who invited user | `!whoinvited @user` |

</details>

<details>
<summary><b>🎨 Style Management</b></summary>

| Command | Description | Usage |
|---------|-------------|-------|
| `!styles` | List available styles | `!styles` |
| `!setstyle` | Change bot style | `!setstyle casual_ru` |

</details>

<details>
<summary><b>⚙️ Administration</b></summary>

| Command | Description | Usage |
|---------|-------------|-------|
| `!resetinvites` | Reset invite counts | `!resetinvites @user` |
| `!reloadconfig` | Reload configuration | `!reloadconfig` |

</details>

---

## ⚙️ Configuration

### 📁 Project Structure

```
discord-invite-bot/
├── 🤖 main.py                 # Main bot file
├── 📦 modules/                # Bot modules
│   ├── config_manager.py      # Configuration manager
│   └── invite_logger.py       # Invitation tracking
├── ⚙️ config/                 # Configuration files
│   ├── config.json           # Main settings
│   └── styles/               # Communication styles
│       ├── casual_ru.json    # 🇷🇺 Casual Russian
│       ├── formal_ru.json    # 🇷🇺 Formal Russian
│       ├── casual_en.json    # 🇬🇧 Casual English
│       └── formal_en.json    # 🇬🇧 Formal English
├── 💾 data/                   # Bot data (auto-created)
└── 🔧 .env                    # Environment variables
```

### 🎛️ Main Configuration

`config/config.json`:

```json
{
    "current_style": "casual_en",
    "features": {
        "welcome_messages": true,
        "leave_messages": true,
        "invite_tracking": true,
        "auto_role_assignment": true
    },
    "bot_settings": {
        "activity_type": "watching",
        "activity_text": "for new members",
        "status": "online"
    }
}
```

### 🎨 Custom Style Creation

Create `config/styles/my_style.json`:

```json
{
    "style_info": {
        "name": "My Custom Style",
        "description": "Personalized communication style",
        "language": "English",
        "tone": "Friendly"
    },
    "greetings": [
        "🎉 Welcome {user}! Invited by {inviter} ({count} invites)",
        "🌟 Hey {user}! Thanks to {inviter} for bringing you! Total: {count}"
    ],
    "leave_messages": [
        "👋 Goodbye {user}! They were invited by {inviter} ({count} invites)",
        "😢 {user} left us... Originally brought by {inviter} (Count: {count})"
    ],
    "default_greeting": "🎉 Welcome {user}!",
    "default_leave_message": "👋 Goodbye {user}!",
    "embeds": {
        "new_member_title": "🎉 New Member",
        "member_left_title": "👋 Member Left",
        "invite_count_title": "📊 Invite Statistics",
        "leaderboard_title": "🏆 Top Inviters",
        "who_invited_title": "🔍 Invitation Info",
        "reset_invites_title": "🔄 Reset Statistics"
    },
    "messages": {
        "feature_disabled": "❌ This feature is disabled",
        "invite_count_message": "📊 {user} has **{count}** invites",
        "no_invites_yet": "📭 No invitations recorded yet",
        "inviter_unknown": "❓ Unknown who invited {user}",
        "invited_by_message": "👤 {user} was invited by {inviter}",
        "inviter_not_found": "❌ Cannot find who invited {user}",
        "user_invites_reset": "✅ Reset {count} invites for {user}",
        "all_invites_reset": "✅ Reset statistics for {count} users"
    }
}
```

### 🔧 Environment Configuration

Edite `.env` file:

```env
# Discord Bot Configuration
DISCORD_TOKEN=your_bot_token_here
GUILD_ID=your_server_id_here

# Optional Settings
DEBUG=false
LOG_LEVEL=INFO
```

---

## 💡 Usage Examples

### 🎨 Style Management
```bash
# View all available styles
!styles

# Switch to friendly English
!setstyle casual_en
```

### 📊 Tracking Invites
```bash
# Check your invites
!invites

# Check someone else's invites
!invites @username

# View leaderboard
!leaderboard 5
```

---

## 🎭 Style Preview

> **Casual English Style:**
> 
> *🎉 Hey there, @newuser! Welcome to our awesome community!*  
> *👤 Invited by our friend: @inviter*  
> *📊 They've got 5 invites now!*

---

## 🤝 Support

<div align="center">

**Need help?** Check these steps:

1. ✅ Verify your `.env` configuration
2. 🔐 Ensure bot has proper server permissions
3. 📋 Check console logs for errors
4. 📖 Review the documentation

**Found a bug?** [Create an issue](https://github.com/mrfolium/discord-invite-bot/issues)

</div>

---

<div align="center">

## 📄 License

This project is licensed under the **MIT License**

*Made with ❤️ for Discord communities*

**[⭐ Star this repo](https://github.com/mrfolium/discord-invite-bot)** • **[🍴 Fork it](https://github.com/mrfolium/discord-invite-bot/fork)** • **[📝 Contribute](CONTRIBUTING.md)**

</div>
