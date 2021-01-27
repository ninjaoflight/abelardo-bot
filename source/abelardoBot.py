import discord
from discord.ext import commands
from discord.ext.commands.errors import MissingRequiredArgument


class AbelardoBot(commands.Bot):
    def __init__(self, command_prefix, **kwargs):
        super().__init__(command_prefix, **kwargs)
        self.verbose_level = kwargs.get('verbose_level', 0)

    async def on_ready(self):
        print(f'{self.user} esta listo para la accion!')
        for guild in self.guilds:
            if (self.verbose_level > 5):
                print(f'conectado en el servidor {guild.name}(id: {guild.id})')
                miembros = '\n - '.join([member.name for member in guild.members])
                print(f'Miembros del servidor:\n - {miembros}')

    async def procesar_member_join(self, member):
        await member.create_dm()
        await member.dm_channel.send(f'Hola {member.name}, Bienvenido al servidor!')

    async def procesar_mensaje(self, mensaje):
        # no procesar los mensajes del bot
        if mensaje.author == self.user:
            return
        if mensaje.content == 'mesero':
            await mensaje.channel.send('digame señor')
        if mensaje.content == 'yarou':
            await mensaje.channel.send('**DIO**')
        elif mensaje.content == '!raise-exception':
            await mensaje.channel.send('_choca_ **fuertemente**')
            raise discord.DiscordException

    async def procesar_error(self, event, *args, **kwargs):
        with open('err.log', 'a') as f:
            if event == 'on_message':
                f.write(f'Unhandled message: {args[0]}\n')
            elif event == 'on_command_error':
                for error in args:
                    if isinstance(error, MissingRequiredArgument):
                        f.write(f'argumentos faltantes: {error}')

            else:
                raise Exception

    async def procesar_command_error(ctx, error):
        if isinstance(error, commands.errors.CheckFailure):
            await ctx.send('No tienes los permisos necesarios para ejecutar este comando.')
