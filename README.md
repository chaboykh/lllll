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
| 🇺🇸 **business_en** | English | Corporate | Professional business communication |
| 🇺🇸 **friendly_en** | English | Casual | Warm and welcoming style |

</div>

---

## 🚀 Installation

### Quick Start

```bash
# 1. Clone the repository
git clone https://github.com/yourusername/discord-invite-bot.git
cd discord-invite-bot

# 2. Install dependencies
pip install -r requirements.txt

# 3. Configure environment
cp .env.example .env
# Edit .env with your bot token

# 4. Run the bot
python main.py
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
│       ├── business_en.json  # 🇺🇸 Business English
│       └── friendly_en.json  # 🇺🇸 Friendly English
├── 💾 data/                   # Bot data (auto-created)
└── 🔧 .env                    # Environment variables
```

### 🎛️ Main Configuration

```json
{
    "current_style": "casual_ru",
    "features": {
        "welcome_messages": true,
        "leave_messages": true,
        "invite_tracking": true,
        "auto_role_assignment": true
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
        "🎉 Welcome {user}! Invited by {inviter} ({count} invites)"
    ],
    "messages": {
        "invite_count_message": "📊 {user} has **{count}** invites"
    }
}
```

---

## 💡 Usage Examples

### 🎨 Style Management
```bash
# View all available styles
!styles

# Switch to business English
!setstyle business_en
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

> **Casual Russian Style:**
> 
> *🎉 Привет, @newuser! Добро пожаловать к нам!*  
> *👤 Тебя пригласил: @inviter*  
> *📊 У него уже 5 приглашений!*

---

## 🤝 Support

<div align="center">

**Need help?** Check these steps:

1. ✅ Verify your `.env` configuration
2. 🔐 Ensure bot has proper server permissions
3. 📋 Check console logs for errors
4. 📖 Review the documentation

**Found a bug?** [Create an issue](https://github.com/yourusername/discord-invite-bot/issues)

</div>

---

<div align="center">

## 📄 License

This project is licensed under the **MIT License**

*Made with ❤️ for Discord communities*

**[⭐ Star this repo](https://github.com/yourusername/discord-invite-bot)** • **[🍴 Fork it](https://github.com/yourusername/discord-invite-bot/fork)** • **[📝 Contribute](CONTRIBUTING.md)**

</div>
