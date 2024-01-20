import discord
from discord import Option
from discord.ext import commands


class Misc(commands.Cog, name='Miscellaneous'):
    def __init__(self, bot):
        self.bot = bot

    @discord.slash_command(name='al-hadikhia', description='Announces which players have been chosen by the Al-Hadikhia.')
    async def al_hadikhia(self, 
        ctx : discord.ApplicationContext,
        player1 : Option(discord.Member, description='Please select the first player.'),
        player2 : Option(discord.Member, description='Please select the second player.'),
        player3 : Option(discord.Member, description='Please select the last player.')
    ):
        await ctx.respond(f"The Al-Hadikhia has chosen {player1.mention}, {player2.mention} and {player3.mention} as tonight's victims.")

    @discord.slash_command(name='fearmonger', description='Announces that the Fearmonger has chosen a new player.')
    async def fearmonger(self, ctx : discord.ApplicationContext):
        await ctx.respond('The Fearmonger has chosen a new victim. 💀 Be careful who you execute!')

    @discord.slash_command(name='gather', description='Gathers all players in the Town Square.')
    async def gather(self, ctx : discord.ApplicationContext):
        discussion_category_channel_id = self.bot.guild_manager.get_discussion_category_channel_id(ctx.guild_id)
        townsquare_id = self.bot.guild_manager.get_townsquare_channel_id(ctx.guild_id)

        if discussion_category_channel_id and townsquare_id:
            for channel in ctx.guild.get_channel(discussion_category_channel_id).voice_channels:
                if channel.id != townsquare_id:
                    for member in channel.members:
                        if not any(role.id == self.bot.guild_manager.get_storyteller_role_id(ctx.guild_id) for role in member.roles):
                            await member.move_to(ctx.guild.get_channel(townsquare_id))

            response = 'Moving all players back to the Town Square now!'
        else:
            response = 'Please use `/choose-townsquare` to choose a voice channel to act as the Town Square, ' + \
                'and please use `/choose-discussion-channels` to choose a category containing voice channels ' + \
                'to act as discussion rooms during the day phase.'
            
        ctx.respond(response)

    @discord.slash_command(name='help', description='Displays this help message.')
    async def help(self, ctx : discord.ApplicationContext):
        response = '```'

        for cog_name, cog in self.bot.cogs.items():
            response += f'{cog_name}:\n'

            for command in cog.walk_commands():
                response += f'\t{command.name}\t{command.description}\n'

        response += '```'
        await ctx.respond(response)


def setup(bot):
    bot.add_cog(Misc(bot))
