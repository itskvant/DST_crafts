import discord
from discord import Message
from discord.ext import commands
from discord.ext.commands import context, Context
import logging
import requests
from bs4 import BeautifulSoup
from configparser import ConfigParser

config = ConfigParser()
config.read('config.ini')
lang = int(config["Bot"]["lang"])
print(lang)

client = commands.Bot(command_prefix=config["Bot"]["prefix"])

logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

@client.event
async def on_ready():
    print(f"[LOG] Logged in as {client.user}")
    logger.debug(f"[LOG] Logged in as {client.user}")

@client.command()
async def switchlang(ctx: Context):
    global lang
    lang = not lang


@client.command(aliases=['get_craft', 'get_recipe', 'recipe', 'gc', 'gr'])
async def craft(ctx: Context, *, msg):
    if len(msg.split()) > 1:
        item, cnt = ' '.join(msg.split()[:-1]), int(msg.split()[-1])
    else:
        item, cnt = msg, 1
    print(item)
    if not item:
        return await ctx.reply("Укажи предмет!")
    item = item[0].upper() + item[1:].strip().replace(' ', '_')
    soup = BeautifulSoup(requests.get((f"https://dontstarve.fandom.com/wiki/{item}", f"https://dont-starve.fandom.com/ru/wiki/{item}")[lang]).content, 'lxml')
    divs = soup.find_all("div", class_="pi-data-value pi-font")
    if divs:
        craft_div = divs[not lang] # In the Russian fandom it has to be 0, in the English fandom - 1
        a_tags = craft_div.find_all("a")
        msg = (f"The resources you'll need to craft \"{item}\" are:\n", f"Для создания \"{item}\" нужно:\n")[lang]
        for resource, count in zip([a_tags[i]["title"] for i in range(len(a_tags))], craft_div.getText().split()):
            msg += ' '.join([resource, "×" + str(int(count[1:]) * cnt)]) + '\n'
        await ctx.reply(msg)
    else:
        await ctx.reply(("I couldn't find this recipe", "Я не нашел такой крафт...")[lang])


if __name__ == '__main__':
    client.run(config["Bot"]["token"])