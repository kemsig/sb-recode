import discord
from discord import ui
import discord

class LogEmbedBuilder:
    def __init__(self):
        self._title = ""
        self._action = ""
        self._err = False
        self._moderator_mention = ""
        self._description = "n/a"
        self._chosen_color = None

    def set_title(self, title: str) -> "LogEmbedBuilder":
        self._title = title
        return self

    def set_action(self, action: str) -> "LogEmbedBuilder":
        self._action = action
        return self

    def set_error(self, err: bool) -> "LogEmbedBuilder":
        self._err = err
        return self

    def set_moderator_mention(self, moderator_mention: str) -> "LogEmbedBuilder":
        self._moderator_mention = moderator_mention
        return self

    def set_description(self, description: str) -> "LogEmbedBuilder":
        self._description = description
        return self

    def set_color(self, chosen_color) -> "LogEmbedBuilder":
        self._chosen_color = chosen_color
        return self

    def build(self) -> discord.Embed:
        # Choose default color if none is specified.
        if self._chosen_color is None:
            color = discord.Color.red() if self._err else discord.Color.blue()
        else:
            color = self._chosen_color

        embed = discord.Embed(
            title=self._title,
            description=self._action,
            color=color
        )
        embed.add_field(name="Error:", value=str(self._err), inline=True)
        embed.add_field(name="Description:", value=self._description, inline=False)
        embed.set_footer(text=f"Command sent by {self._moderator_mention}")

        return embed


class Logger:
    @staticmethod
    def database_failure(moderator_string: str, description: str) -> discord.Embed:
        """
        Logs a database failure.
        
        :param moderator_string: The moderator's mention string.
        :param description: A detailed description of the database failure.
        :return: A discord.Embed object with the log details.
        """
        return (
            LogEmbedBuilder()
            .set_title("Database Failure")
            .set_action("An error occurred during a database operation.")
            .set_error(True)
            .set_moderator_mention(moderator_string)
            .set_description(description)
            .build()
        )

    @staticmethod
    def command_success(moderator_string: str, description: str) -> discord.Embed:
        """
        Logs a successful command execution.
        
        :param moderator_string: The moderator's mention string.
        :param description: A description of the successful action.
        :return: A discord.Embed object with the log details.
        """
        return (
            LogEmbedBuilder()
            .set_title("Command Success")
            .set_action("Command executed successfully.")
            .set_error(False)
            .set_moderator_mention(moderator_string)
            .set_description(description)
            .build()
        )

    @staticmethod
    def warning(moderator_string: str, description: str) -> discord.Embed:
        """
        Logs a warning for a non-critical issue.
        
        :param moderator_string: The moderator's mention string.
        :param description: A description of the warning.
        :return: A discord.Embed object with the log details.
        """
        return (
            LogEmbedBuilder()
            .set_title("Warning")
            .set_action("A non-critical issue was encountered.")
            .set_error(False)
            .set_color(discord.Color.yellow())
            .set_moderator_mention(moderator_string)
            .set_description(description)
            .build()
        )
    
    @staticmethod
    def successful_gacha_roll(moderator_string: str, user_id: int, prize: str, description: str = None) -> discord.Embed:
        """
        Logs a successful gacha roll.
        The embed is green so it stands out for moderators.
        
        :param moderator_string: The moderator's mention string.
        :param user_id: The ID of the user who rolled gacha.
        :param prize: The prize received.
        :param description: Optional extra details.
        :return: A discord.Embed object for the successful gacha roll.
        """
        if description is None:
            description = (
                f"User {user_id} successfully executed a gacha roll and received **{prize}**.\n"
                "Moderators: Please award the prize immediately."
            )
        return (
            LogEmbedBuilder()
            .set_title("Gacha Roll Successful!")
            .set_action("Gacha Roll Completed")
            .set_error(False)
            .set_moderator_mention(moderator_string)
            .set_description(description)
            .set_color(discord.Color.green())
            .build()
        )