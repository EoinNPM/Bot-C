import discord
from discord import Option
from discord.ext import commands
from guild_manager import CabinAlreadyAssignedException


class ServerSettings(commands.Cog, name='Server Settings'):
    def __init__(self, bot):
        self.bot = bot

    @discord.slash_command(name='choose-storyteller', description='Determines which role designates the Storyteller.')
    async def choose_storyteller(self, 
        ctx : discord.ApplicationContext, 
        role : Option(discord.Role, description='Please select a role.')
    ):
        self.bot.guild_manager.set_storyteller_role_id(ctx.guild_id, role.id)
        await ctx.respond(f'Members with the `{role.name}` role are now considered Storytellers.')

    @discord.slash_command(name='choose-townsquare', description='Determines which voice channel is the Town Square.')
    async def choose_townsquare(self, 
        ctx : discord.ApplicationContext, 
        voice_channel : Option(discord.VoiceChannel, description='Please select a voice channel.')
    ):
        self.bot.guild_manager.set_townsquare_channel_id(ctx.guild_id, voice_channel.id)
        await ctx.respond(f'The `{voice_channel.name}` channel is now the Town Square.')

    @discord.slash_command(name='choose-cabin-channels', description='Selects the voice channel category containing cabins for the night phase.')
    async def choose_cabin_channels(self, 
        ctx : discord.ApplicationContext, 
        category : Option(discord.CategoryChannel, description='Please select a category containing voice channels.')
    ):
        self.bot.guild_manager.set_cabin_category_channel_id(ctx.guild_id, category.id)
        await ctx.respond(f'The channels in the `{category.name}` category will now house the players during the night phase.')

    @discord.slash_command(name='choose-player-cabin', description="Sets a voice channel as a player's permanent cabin for the night phase.")
    async def choose_player_cabin(self, 
        ctx : discord.ApplicationContext, 
        player : Option(discord.Member, description='Please select a player.'), 
        channel : Option(discord.VoiceChannel, description='Please select a voice channel')
    ):
        if channel in ctx.guild.get_channel(self.bot.get_cabin_category_channel_id(ctx.guild_id)).channels:
            try:
                self.bot.set_member_as_cabin_owner(player.id, channel.id)
                response = f"`{channel.name}` has been set as {player.nick}'s permanent cabin for the night phase."
            except CabinAlreadyAssignedException as e:
                if e.member_id == player.id:
                    response = "That channel is already set as that player's permanent cabin."
                else:
                    response = "That channel is already set as another player's permanent cabin."
        else:
            response = 'That channel is not one of the voice channels set as a cabin for the night phase.'

        await ctx.respond(response)

    @discord.slash_command(name='choose-discussion-channels', description='Selects the voice channel category containing discussion rooms in the day phase.')
    async def choose_discussion_channels(self, 
        ctx : discord.ApplicationContext, 
        category : Option(discord.CategoryChannel, description='Please select a category containing voice channels.')
    ):
        self.bot.guild_manager.set_discussion_category_channel_id(ctx.guild_id, category.id)
        await ctx.respond(f'Public discussion will take place in the channels in the `{category.name}` category during the day phase.')


def setup(bot):
    bot.add_cog(ServerSettings(bot))
