import discord
import random
from discord.ext import commands


class PhaseShifts(commands.Cog, name='Phase Shifts'):
    def __init__(self, bot):
        self.bot = bot

    @discord.slash_command(name='day', description='Progresses the game into the day phase.')
    async def day(self, ctx):
        cabin_category_channel_id = self.bot.guild_manager.get_cabin_category_channel_id(ctx.guild_id)
        townsquare_channel_id = self.bot.guild_manager.get_townsquare_channel_id(ctx.guild_id)

        if cabin_category_channel_id and townsquare_channel_id:
            for channel in ctx.guild.get_channel(cabin_category_channel_id).voice_channels:
                for member in channel.members:
                    if not any(role.id == self.bot.guild_manager.get_storyteller_role_id(ctx.guild_id) for role in member.roles):
                        await member.move_to(ctx.guild.get_channel(townsquare_channel_id))

            response = 'All players have been brought to the Town Square. Good morning, Ravenswood Bluff! ☀️'
        else:
            response = 'Please use `/choose-townsquare` to choose a voice channel to act as the Town Square, ' + \
                'and please use `/choose-cabin-channels` to choose a category containing voice channels to act ' + \
                'as cabins during the night phase.'

        await ctx.respond(response)

    @discord.slash_command(name='night', description='Progresses the game into the night phase.')
    async def night(self, ctx):
        movements = {}

        cabin_category_channel_id = self.bot.guild_manager.get_cabin_category_channel_id(ctx.guild_id)
        townsquare_channel_id = self.bot.guild_manager.get_townsquare_channel_id(ctx.guild_id)

        if cabin_category_channel_id and townsquare_channel_id:
            available_channel_ids = {channel.id for channel in ctx.guild.get_channel(cabin_category_channel_id).voice_channels}
            print(ctx.guild.get_channel(townsquare_channel_id).members)

            town_square_member_ids = {
                member.id for member in ctx.guild.get_channel(townsquare_channel_id).members
            if not any(role.id == self.bot.guild_manager.get_storyteller_role_id(ctx.guild_id) for role in member.roles)}

            if (cabin_ownership_dict := self.bot.guild_manager.get_cabin_ownership_dict(ctx.guild_id)):
                for player_id, channel_id in cabin_ownership_dict.items():
                    if channel_id in available_channel_ids:
                        available_channel_ids.remove(channel_id)

                        if int(player_id) in town_square_member_ids:
                            movements[player_id] = channel_id
                            town_square_member_ids.remove(int(player_id))

            if len(available_channel_ids) >= len(town_square_member_ids):
                available_channel_ids = list(available_channel_ids)
                random.shuffle(available_channel_ids)

                movements.update(dict(zip(town_square_member_ids, available_channel_ids)))

                for player_id, channel_id in movements.items():
                    member = ctx.guild.get_member(player_id)
                    channel = ctx.guild.get_channel(channel_id)

                    await member.move_to(channel)

                response = 'All players successfully moved to their cabins. Goodnight, Ravenswood Bluff! 🌙'
            else:
                response = 'There are too few voice channels in that category to accommodate the current players.'
        else:
            response = 'Please use `/choose-townsquare` to choose a voice channel to act as the Town Square, ' + \
                'and please use `/choose-cabin-channels` to choose a category containing voice channels to act ' + \
                'as cabins during the night phase.'
                        
        await ctx.respond(response)


def setup(bot):
    bot.add_cog(PhaseShifts(bot))
