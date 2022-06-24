import os
import nextcord
from nextcord.ext import commands
import json
import logging

TESTING_GUILDS = []

class StatusHandler(commands.Cog):

    _default = {
        "lastStatus":None,
        "type":None,
    }

    _data: dict

    _path: str

    _LOG_ERROR: bool

    _config: dict

    def __init__(self,bot: commands.bot,config) -> None:
        self._bot = bot
        self._path = os.getcwd()
        self.__check_data()
        self._LOG_ERROR = bool(config['OPTIONS']['LOG_ERROR'])
        self._config = config
        
    def __check_data(self) -> None:
        if not os.path.isfile(self._path+'\\data.json'):
            with open(self._path+'\\data.json','w') as file:
                json.dump(self._default,file)
        self.__get_data()  

    def __get_data(self) -> None:
        os.chdir(self._path)
        with open(self._path+'\\data.json','r') as file:
                self._data = json.load(file)

    def __update_data(self) -> None:
        os.chdir(self._path)
        with open(self._path+'\\data.json','w') as file:
            json.dump(self._data,file)

    # EVENT LISTENERS

    @commands.Cog.listener()
    async def on_ready(self):
        await self._bot.change_presence(activity=nextcord.Game(self._data['lastStatus']))

    # COMMANDS

    @nextcord.slash_command(
        name='set-status',
        description='Set status of the bot',
        guild_ids= TESTING_GUILDS,
        default_member_permissions=8
    )
    async def status(self,inter: nextcord.Interaction,message: str):
        os.chdir(self._path)

        await self._bot.change_presence(activity=nextcord.Game(message))

        self._data['type'] = 'none'
        self._data['lastStatus'] = message

        logging.info(f"Status changed to '{message}'")
        await inter.send(f"Status succesfully changed to '{message}'",ephemeral=True)

        self.__update_data()

def setup(bot, **kwargs):
    bot.add_cog(StatusHandler(bot,kwargs))
