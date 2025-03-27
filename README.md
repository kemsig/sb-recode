# Discord Bot Command Documentation

This document describes the usage and behavior of each slash command available in the bot. Commands are categorized into **Admin**, **Default (User)**, and **Manual Admin** functionalities. These commands primarily interact with a local SQLite database, awarding or deducting points from users, and managing moderation workflows.

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

For any additional features, bug fixes, or to onboard new moderators, consider expanding these docs further or integrating command descriptions directly in Discord via `@app_commands.describe`.

