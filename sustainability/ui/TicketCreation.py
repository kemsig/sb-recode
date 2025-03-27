import discord
from datetime import datetime as dt
from discord import ui
from ui.TicketSubmission import TicketSubmitButtons

class TicketCreateButton(ui.View):
        def __init__(self):
            super().__init__(timeout=None)
            self.value = None

        @discord.ui.button(label='Claim your points!', style=discord.ButtonStyle.blurple, disabled= False, custom_id="create_ticket")
        async def confirm(self, interaction: discord.Interaction, button: discord.ui.Button):
            # get the user's mention and id
            user_mention = interaction.user.mention
            user_id = interaction.user.id

            # get current time
            cur_time = dt.now()

            # create a thread for the ticket
            thread = await interaction.channel.create_thread(name=f'{cur_time}_{user_id}', invitable=False )

            # create ticket submission button
            sub_button = TicketSubmitButtons()
            # mention the user so that they can join and send the info
            await thread.send(f'Hello! {user_mention}', view=sub_button)