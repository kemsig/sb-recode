# Discord Bot Command Documentation

This document describes the usage and behavior of each slash command available in the bot. Commands are categorized into **Admin**, **Default (User)**, and **Manual Admin** functionalities. These commands primarily interact with a local SQLite database, awarding or deducting points from users, and managing moderation workflows.

---

## 📚 Table of Contents
- [🛠 Admin Commands](#-admin-commands)
  - [/setup](#setup)
  - [/confirm](#confirm-numpoints)
  - [/deny](#deny-reason)
- [👤 Default (User) Commands](#-default-user-commands)
  - [/points](#points)
  - [/gacha](#gacha)
- [🔧 Manual Admin Commands](#-manual-admin-commands)
  - [/remuser](#remuser-user_id)
  - [/addpoints](#addpoints-user_idpoints)
  - [/addtotalpoints](#addtotalpoints-user_idpoints)
- [🔐 Permissions & Notes](#-permissions--notes)
- [🚀 Deployment Instructions](#-deployment-instructions)
- [🧭 Moderator Onboarding Guide](#-moderator-onboarding-guide)
  - [Permissions Required](#-permissions-required)
  - [Setting Up the Ticket System](#-setting-up-the-ticket-system)
  - [Approving a Request](#-approving-a-request)
  - [Denying a Request](#-denying-a-request)
  - [Manual Adjustments](#-manual-adjustments)
  - [Logging Guide](#-logging-guide)

---

## 🛠 Admin Commands

These commands are only accessible to moderators (checked via `@is_mod()` decorator).

### `/setup`
- **Purpose:** Deploys the interactive ticket system by placing a persistent button in the current channel.
- **Behavior:**
  - Logs the setup initiation to the configured log channel.
  - Sends a view containing the `TicketCreateButton` to the channel.
  - Requires appropriate channel name configuration.

---

### `/confirm <num_points>`
- **Purpose:** Confirms a user's point request and awards points.
- **Usage:** Run this inside a thread named in the format: `someprefix_<user_id>`
- **Arguments:**
  - `num_points` (int): The number of points to award.
- **Behavior:**
  - Extracts user ID from the thread name.
  - Adds the specified points to the user's current and total in the database.
  - Sends the updated point info to the user via DM.
  - Deletes the thread upon successful operation.

---

### `/deny <reason>`
- **Purpose:** Denies a point request and informs the user.
- **Usage:** Run this inside a thread named in the format: `someprefix_<user_id>`
- **Arguments:**
  - `reason` (str): Explanation shown to the user.
- **Behavior:**
  - Extracts user ID from thread name.
  - Sends a DM to the user with the reason.
  - Logs the denial to the logs channel.
  - Deletes the thread.

---

## 👤 Default (User) Commands

These are available to all users.

### `/points`
- **Purpose:** Displays the user's current and lifetime points.
- **Behavior:**
  - Fetches user info from the local database.
  - Returns the user's current and total points as an ephemeral message.
  - Logs any database failure to the log channel.

---

### `/gacha`
- **Purpose:** Deducts points for a "gacha roll" that yields a prize.
- **Behavior:**
  - Requires a minimum balance (defined in `config.GACHA_MIN_BALANCE`).
  - Deducts points on success.
  - Logs the event to the logs channel and notifies `@everyone`.
  - Sends a placeholder message; actual prize logic can be added later.

---

## 🔧 Manual Admin Commands

Commands for manually modifying the user database.

### `/remuser <user_id>`
- **Purpose:** Removes a user from the database.
- **Arguments:**
  - `user_id` (str): The target user's Discord ID.
- **Behavior:**
  - Tries to remove the user record.
  - Logs the result.
  - Returns success or failure message to the mod.

---

### `/addpoints <user_id>:<points>`
- **Purpose:** Adds points to a user’s current and total.
- **Arguments:**
  - `key` (str): Format should be `user_id:points`
- **Behavior:**
  - Adds the given points to both `points_cur` and `points_total`.
  - Logs success or failure to the logs channel.

---

### `/addtotalpoints <user_id>:<points>`
- **Purpose:** Adds points to a user's total score only.
- **Arguments:**
  - `key` (str): Format should be `user_id:points`
- **Behavior:**
  - If user exists, updates their `points_total` only.
  - If user doesn’t exist, inserts a new row with 0 current points.
  - Logs success or failure to the logs channel.

---

## 🔐 Permissions & Notes

- All admin and manual commands require moderator privileges via the `@is_mod()` check.
- Commands rely on the naming format of threads to extract user IDs (e.g., `request_613425008575905856`).
- SQLite database access is done via `local_db`, which must be properly initialized in `main.py`.
- Logs are sent to the Discord channel defined by `config.LOG_CHANNEL_NAME`.
- Users must have DMs open to receive confirmation/denial messages.

---

## 🚀 Deployment Instructions

You can run the bot in one of the following ways:

### 🐳 Option 1: Pull and Run from Docker Hub
```bash
docker pull kemsig/sasebot
docker run --env-file .env kemsig/sasebot
```

### 🛠 Option 2: Build and Run Locally
```bash
docker build -t sasebot .
docker run --env-file .env sasebot
```

### 🐍 Option 3: Manual Local Setup with pip
```bash
# (Optional) Create virtual environment
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows

# Install dependencies
pip install -r requirements.txt

# Set environment variables (or use .env)
export DISCORD_BOT_SECRET=your_token
python bot.py
```

### 📄 Example `.env`
```env
# client secrets
DISCORD_BOT_SECRET=<your_secret>
NO_MONGO=true
LOCAL_DB_NAME=data/local.db

# Bot settings
GACHA_MIN_BALANCE=14
ADMIN_CHANNEL_NAME=sustain-admin
LOG_CHANNEL_NAME=logs-sustainability
ROLE_NAME=Sustain Mod

# other settings
# MAX_DB_SIZE=
# SETUP_MESSAGE=
# CLAIM_POINTS_MESSAGE=
```

---

## 🧭 Moderator Onboarding Guide

Welcome to the moderation team! Here’s everything you need to know to get started using the bot effectively:

### ✅ Permissions Required
Ensure you have the role specified in `.env` under `ROLE_NAME` (e.g., `Sustain Mod`). This gives you access to all mod commands.

### 🧷 Setting Up the Ticket System
Use `/setup` in the appropriate channel to deploy the ticket button. This is the entry point for user point requests.

### ✅ Approving a Request
1. Navigate to the thread created by a user (format: `request_<user_id>`).
2. Run `/confirm <points>` with the appropriate point amount.
3. The user is notified via DM and the thread is auto-deleted.

### ❌ Denying a Request
1. Navigate to the thread created by a user.
2. Run `/deny <reason>` with a short explanation.
3. The user is DM'd and the thread is removed.

### 🛠 Manual Adjustments
- Use `/addpoints user_id:amount` to add points to both current and total.
- Use `/addtotalpoints user_id:amount` to add points only to lifetime total.
- Use `/remuser user_id` to completely remove a user from the database.

### 📢 Logging Guide
The bot uses a centralized logging system to report actions and errors. Logs are sent to the channel specified by `LOG_CHANNEL_NAME`.

#### 🧾 Types of Logs to Look Out For:
- **✅ Command Success**: Logged when a command completes as expected.
- **⚠️ Warning**: Logged for non-critical issues (e.g., user doesn't meet gacha requirements).
- **❌ Database Failure**: Critical — review immediately. May indicate issues with data integrity.
- **🎉 Gacha Roll Success**: Indicates a user has won a prize. Mods should follow up to deliver it.

#### 📘 Example:
```python
from utils.logger import Logger
log_embed = Logger.command_success("@mod", "Successfully added 10 points to user 123456")
await logs_channel.send(embed=log_embed)
```

If you have any issues, contact the bot maintainer or check the logs for error messages.

---

For any additional features, bug fixes, or to onboard new moderators, consider expanding these docs further or integrating command descriptions directly in Discord via `@app_commands.describe`.

