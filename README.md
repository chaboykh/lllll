
<div align="center">

# 🎯 Discord Invite Tracker Bot

*A powerful Discord bot for tracking invitations with customizable communication styles*

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://python.org)
[![Discord.py](https://img.shields.io/badge/discord.py-2.3.0+-blue.svg)](https://github.com/Rapptz/discord.py)
[![License](https://github.com/MrFolium/discord-invite-tracker-bot/blob/main/LICENSE)](LICENSE)



[Features](#-features) • [Installation](#-installation) • [Commands](#-commands) • [Configuration](#-configuration) • [Logging](#-logging)

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
- 📝 **Comprehensive logging**

</td>
<td width="50%">

### 🎨 **Customization**
- 🌍 **Multi-language support**
- 🎭 **Communication styles**
- ⚙️ **Flexible configuration**
- 🔄 **Hot-reload settings**
- 🚀 **Background operation**

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
# ZIP: Click "Code" → "Download ZIP"
# OR Git:
git clone https://github.com/MrFolium/discord-invite-tracker-bot.git
cd discord-invite-tracker-bot

# 2. Setup environment
cp .env.example .env
# Edit .env with your bot token and server ID

# 3. Run bot
# Windows: double-click start.bat
# Linux/Mac: ./start.sh
```

### 📋 Requirements
- **Python 3.8+**
- **Discord Bot Token** ([Get one here](https://discord.com/developers/applications))
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
<summary><b>⚙️ Administration (Admin Only)</b></summary>

| Command | Description | Usage |
|---------|-------------|-------|
| `!resetinvites` | Reset user invite count | `!resetinvites @user` |
| `!resetall` | Reset all invite counts | `!resetall` |
| `!reloadconfig` | Reload configuration | `!reloadconfig` |

</details>

---

## 📝 Logging

The bot includes comprehensive logging system:

- **📁 Automatic log directory creation**
- **📝 All events logged to `logs/bot.log`**
- **🚀 Startup and shutdown logging**
- **❌ Error tracking and debugging**
- **👥 User activity monitoring**

### Log File Location
```
logs/
└── bot.log    # All bot activity and errors
```

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
├── 🚀 start.bat               # Windows startup script
├── 🚀 start.sh                # Linux/Mac startup script
├── 📋 requirements.txt        # Python dependencies
├── 📄 .env.example           # Environment template
├── 💾 data/                   # Bot data (auto-created)
├── 📝 logs/                   # Bot logs (auto-created)
│   └── bot.log               # Application logs
└── 🔧 .env                    # Environment variables
```

### 🔧 Environment Configuration

Edit `.env` file:

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

# Switch to friendly Russian
!setstyle casual_ru

# Switch to professional English
!setstyle formal_en
```

### 📊 Tracking Invites
```bash
# Check your invites
!invites

# Check someone else's invites
!invites @username

# View top 10 inviters
!leaderboard 10

# Find who invited a user
!whoinvited @newmember
```

### 🔧 Administration
```bash
# Reset specific user's invites
!resetinvites @user

# Reset all invite statistics
!resetall

# Reload bot configuration
!reloadconfig
```

---

## 🎭 Style Preview

> **Casual Russian Style:**
> 
> *🎉 Привет, @newuser! Добро пожаловать в наше сообщество!*  
> *👤 Пригласил: @inviter*  
> *📊 У него теперь 5 приглашений!*

> **Formal English Style:**
> 
> *🎉 Welcome to the server, @newuser.*  
> *👤 Invited by: @inviter*  
> *📊 Current invitation count: 5*

---

## 🛠️ Troubleshooting

<div align="center">

**Common Issues:**

1. ✅ **Bot not responding?** Check your `.env` configuration
2. 🔐 **Permission errors?** Ensure bot has Administrator permissions
3. 📋 **Startup issues?** Check `logs/bot.log` for errors
4. 🔄 **Commands not working?** Try `!reloadconfig`

**Still need help?** [Create an issue](https://github.com/MrFolium/discord-invite-tracker-bot/issues)

</div>

---

<div align="center">

## 📄 License

This project is licensed under the **MIT License**

*Made with ❤️ for Discord communities*

**[⭐ Star this repo](https://github.com/MrFolium/discord-invite-tracker-bot)** • **[🍴 Fork it](https://github.com/MrFolium/discord-invite-tracker-bot/fork)** • **[📝 Report Issues](https://github.com/MrFolium/discord-invite-tracker-bot/issues)**

</div>
