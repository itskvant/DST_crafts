import discord
from discord import Message
from discord.ext import commands
from discord.ext.commands import context, Context
import logging
import requests
from bs4 import BeautifulSoup

# Настройка бота
client = commands.Bot(command_prefix='!')

# Настройка логгера
logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

# Ивент, вызывающийся каждый раз когда бот (клиент) запущен
@client.event
async def on_ready():
    print(f"[LOG] Logged in as {client.user}")
    logger.debug(f"[LOG] Logged in as {client.user}")

# Основная функция с крафтами
@client.command(aliases=['get_craft', 'get_recipe', 'recipe', 'gc', 'gr'])
async def craft(ctx: Context, *, item):
    item = item[0].upper() + item[1:].strip().replace(' ', '_')
    soup = BeautifulSoup(requests.get(f"https://dont-starve.fandom.com/ru/wiki/{item}").content, 'lxml')
    divs = soup.find_all("div", class_="pi-data-value pi-font")
    if divs:
        craft_div = divs[0]
        a_tags = craft_div.find_all("a")
        msg = f"Для создания \"{item}\" нужно:\n"
        for resource, count in zip([a_tags[i]["title"] for i in range(len(a_tags))], craft_div.getText().split()):
            msg += ' '.join([resource, count]) + '\n'
        await ctx.reply(msg)
    else:
        await ctx.reply("Я не нашел такой крафт...")

if __name__ == '__main__':
    client.run("ODk0OTMwMDY5MzI2Mjc0NTYx.YVxKkw.hUqyasDYoyyU8z5Jzw4QuM2reng")