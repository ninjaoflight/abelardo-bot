import os

from dotenv import load_dotenv

from abelardoBot import AbelardoBot
import discord
import random
from discord.ext import commands

load_dotenv()
TOKEN = os.getenv('DISCORD_BOT_TOKEN')
VERBOSE_LEVEL = os.getenv('VERBOSE_LEVEL')

bot = AbelardoBot(command_prefix='!',
                  verbose_level=0 if VERBOSE_LEVEL is None else VERBOSE_LEVEL)


@bot.event
async def on_member_join(member):
    await bot.procesar_member_join(member)


#@bot.event
#async def on_message(message):
#    if not message.content.startswith(bot.command_prefix):
#        await bot.procesar_mensaje(message)
#    else:
#        await bot.super().on_message()


@bot.event
async def on_error(event, *args, **kwargs):
    await bot.procesar_error(event, *args, **kwargs)


@bot.command(name='raise-exception', help='Lanza una excepcion de prueba')
async def nine_nine(ctx):
    await ctx.send('_choca_ **fuertemente**')
    raise discord.DiscordException


@bot.command(name='dados', help='Simula el lanzamiento de un dado.')
async def roll(ctx, numero_dado: int, numero_caras: int):
    dado = [
        str(random.choice(range(1, numero_caras + 1)))
        for _ in range(numero_dado)
    ]
    await ctx.send(f'resultados: {", ".join(dado)}')


@bot.command(name='soy-admin', help='te reconoce como administrador')
@commands.has_role('admin')
async def que_soy(ctx):
    await ctx.send(f'{ctx.message.author.name} eres admin')


@bot.event
async def on_command_error(ctx, error):
    await bot.procesar_command_error(ctx, error)


if __name__ == "__main__":
    print("inicializando el bot")
    bot.run(TOKEN)
