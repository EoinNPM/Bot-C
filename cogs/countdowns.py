import asyncio
import discord
from discord import Option
from discord.ext import commands
from guild_manager import CountdownStatus
from math import floor


def format_remaining_time(seconds):
    q, r = divmod(seconds, 60)
    return str(floor(q)) + ':' + ('0' if r < 10 else '') + str(floor(r))


class Countdowns(commands.Cog, name='Countdowns'):
    def __init__(self, bot):
        self.bot = bot

    @discord.slash_command(name='start-countdown', description='Begins a countdown until players are returned to the Town Square.')
    async def start_countdown(self, 
        ctx : discord.ApplicationContext, 
        duration : Option(float, description='The duration of the countdown, in minutes.', min_value=0, max_value=60), 
        delay : Option(int, description='The delay after which players will be moved to the Town Square, in seconds.', required=False, min=0)
    ):
        discussion_category_channel_id = self.bot.guild_manager.get_discussion_category_channel_id(ctx.guild_id)
        townsquare_id = self.bot.guild_manager.get_townsquare_channel_id(ctx.guild_id)

        if discussion_category_channel_id and townsquare_id:
            seconds_remaining = floor(duration * 60)
            self.bot.guild_manager.start_countdown(ctx.guild_id)

            interaction = await ctx.respond(
                content=f'Time until players must return to the Town Square: {format_remaining_time(seconds_remaining)}.'
            )
            
            while (countdown_status := self.bot.guild_manager.countdown_statuses[ctx.guild_id]) != CountdownStatus.STOPPED:
                await asyncio.sleep(1)

                if countdown_status == CountdownStatus.RUNNING:
                    seconds_remaining -= 1

                    await interaction.edit_original_response(
                        content=f'Time until players must return to the Town Square: {format_remaining_time(max(0, seconds_remaining))}.'
                    )

                    if seconds_remaining <= 0:
                        if delay:
                            await ctx.send(f"Time's up! Returning you to the Town Square in {delay} seconds!")
                            await asyncio.sleep(delay)

                            for channel in ctx.guild.get_channel(discussion_category_channel_id).voice_channels:
                                if channel.id != townsquare_id:
                                    for member in channel.members:
                                        if not any(role.id == self.bot.guild_manager.get_storyteller_role_id(ctx.guild_id) for role in member.roles):
                                            await member.move_to(ctx.guild.get_channel(townsquare_id))
                        else:
                            await ctx.send("Time's up! Please return to the Town Square now!")

                        self.bot.guild_manager.stop_countdown(ctx.guild_id)
        else:
            await ctx.respond(
                'Please use `/choose-townsquare` to choose a voice channel to act as the Town Square, ' + \
                    'and please use `/choose-discussion-channels` to choose a category containing voice ' + \
                    'channels to act as discussion rooms during the day phase.'
            )

    @discord.slash_command(name='pause-countdown', description='Pauses an existing countdown.')
    async def pause_countdown(self, ctx : discord.ApplicationContext):
        if (countdown_status := self.bot.guild_manager.countdown_statuses[ctx.guild_id]) == CountdownStatus.RUNNING:
            self.bot.guild_manager.pause_countdown(ctx.guild_id)
            response = 'The countdown has been paused.'
        elif countdown_status == CountdownStatus.PAUSED:
            response = 'The countdown is already paused.'
        else:
            response = 'There is no countdown currently running.'

        await ctx.respond(response)

    @discord.slash_command(name='unpause-countdown', description='Resumes an existing countdown.')
    async def unpause_countdown(self, ctx : discord.ApplicationContext):
        if (countdown_status := self.bot.guild_manager.countdown_statuses[ctx.guild_id]) == CountdownStatus.PAUSED:
            self.bot.guild_manager.start_countdown(ctx.guild_id)
            response = 'The countdown has resumed.'
        elif countdown_status == CountdownStatus.RUNNING:
            response = 'The countdown is not paused.'
        else:
            response = 'There is no countdown currently running.'

        await ctx.respond(response)  

    @discord.slash_command(name='stop-countdown', description='Stops an existing countdown.')
    async def stop_countdown(self, ctx : discord.ApplicationContext):
        if self.bot.guild_manager.countdown_statuses[ctx.guild_id] == CountdownStatus.STOPPED:
            response = 'There is no countdown currently running.'
        else:
            self.bot.guild_manager.stop_countdown(ctx.guild_id)
            response = 'The countdown has been stopped.'

        await ctx.respond(response)


def setup(bot):
    bot.add_cog(Countdowns(bot))
