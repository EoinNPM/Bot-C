import json
from enum import Enum


class CabinAlreadyAssignedException(Exception):
    def __init__(self, member_id):
        self.member_id = member_id


class CountdownStatus(Enum):
    STOPPED = 1
    PAUSED = 2
    RUNNING = 3


class GuildManager:
    def __init__(self, config_file_path):
        self.config_file_path = config_file_path
        self.countdown_statuses = {}

        try:
            with open(self.config_file_path) as f:
                self.guild_settings = json.load(f)
        except FileNotFoundError:
            self.guild_settings = {}

    def write_guild_settings(self):
        with open(self.config_file_path, 'w') as f:
            json.dump(self.guild_settings, f)

    def register_guild(self, guild_id):
        self.guild_settings[str(guild_id)] = {}
        self.write_guild_settings()

    def unregister_guild(self, guild_id):
        try:
            del self.guild_settings[str(guild_id)]
            self.write_guild_settings()
        except KeyError:
            pass

    def set_storyteller_role_id(self, guild_id, role_id):
        self.guild_settings[str(guild_id)]['Storyteller'] = role_id
        self.write_guild_settings()

    def get_storyteller_role_id(self, guild_id):
        try:
            return self.guild_settings[str(guild_id)]['Storyteller']
        except KeyError:
            pass

    def set_townsquare_channel_id(self, guild_id, channel_id):
        self.guild_settings[str(guild_id)]['Town Square'] = channel_id
        self.write_guild_settings()

    def get_townsquare_channel_id(self, guild_id):
        try:
            return self.guild_settings[str(guild_id)]['Town Square']
        except KeyError:
            pass

    def set_cabin_category_channel_id(self, guild_id, channel_id):
        self.guild_settings[str(guild_id)]['Cabin Category'] = channel_id
        self.write_guild_settings()

    def get_cabin_category_channel_id(self, guild_id):
        try:
            return self.guild_settings[str(guild_id)]['Cabin Category']
        except KeyError:
            pass
    
    def set_member_as_cabin_owner(self, guild_id, member_id, channel_id):
        guild_id_str = str(guild_id)
        member_id_str = str(member_id)

        if 'Cabin Ownership' not in self.guild_settings[str(guild_id)].keys():
            self.guild_settings[guild_id_str]['Cabin Ownership'] = {}

        for k, v in self.guild_settings[guild_id_str]['Cabin Ownership'].items():
            if v == channel_id:
                raise CabinAlreadyAssignedException(k)
        
        self.guild_settings[guild_id_str]['Cabin Ownership'][member_id_str] = channel_id
        self.write_guild_settings()

    def get_cabin_ownership_dict(self, guild_id):
        try:
            return self.guild_settings[str(guild_id)]['Cabin Ownership']
        except KeyError:
            pass

    def set_discussion_category_channel_id(self, guild_id, channel_id):
        self.guild_settings[str(guild_id)]['Discussion Category'] = channel_id
        self.write_guild_settings()

    def get_discussion_category_channel_id(self, guild_id):
        try:
            return self.guild_settings[str(guild_id)]['Discussion Category']
        except KeyError:
            pass

    def start_countdown(self, guild_id):
        try:
            self.countdown_statuses[guild_id] = CountdownStatus.RUNNING
        except KeyError:
            pass

    def pause_countdown(self, guild_id):
        try:
            self.countdown_statuses[guild_id] = CountdownStatus.PAUSED
        except KeyError:
            pass

    def stop_countdown(self, guild_id):
        try:
            self.countdown_statuses[guild_id] = CountdownStatus.STOPPED
        except KeyError:
            pass
