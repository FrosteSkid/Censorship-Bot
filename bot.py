import discord
from asyncio import sleep
from discord.ext import bridge
import json

intents = discord.Intents.all()
intents.message_content = True
bot = bridge.Bot(command_prefix=".", intents=intents)
config = json.load(open('config.json'))
allowed = config['allowed']
TOKEN = config['token']

@bot.event
async def on_ready():
    print(f"{bot.user} is ready and online in to censor!")

@bot.slash_command(name="1984", description="censors a user")
async def censor(ctx, user: discord.User):
    if ctx.author.id in allowed:
        if user.id != bot.user.id:
            print(f'{ctx.author.name} censored {user.name}')

            json_data = json.load(open('censored.json'))
            censored = json_data['censored']

            if user.id not in censored:
                censored.append(user.id)


                dump = {'censored':censored}
                dumps = json.dumps(dump, indent=4)
                with open('censored.json', 'w') as outfile:
                    outfile.write(dumps)
                await ctx.respond(f'Censored ``{user.name}`` <:iamspreadingmisinformationatanal:1021414041744330804>')
                await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=f"Censoring {len(censored)} people"))
            else:
                await ctx.respond(f'``{user.name}`` is already censored')
        else:
            await ctx.respond(f'You cant censor me <:iamspreadingmisinformationatanal:1021414041744330804>')
    else:
        await ctx.respond(f'You cannot censor <:iamspreadingmisinformationatanal:1021414041744330804>')

@bot.slash_command(name="1985", description="uncensors a user")
async def uncensor(ctx, user: discord.User):
    if ctx.author.id in allowed:
        if user.id != bot.user.id:
            print(f'{ctx.author.name} uncensored {user.name}')

            json_data = json.load(open('censored.json'))
            censored = json_data['censored']

            if user.id in censored:
                censored.remove(user.id)


                dump = {'censored':censored}
                dumps = json.dumps(dump, indent=4)
                with open('censored.json', 'w') as outfile:
                    outfile.write(dumps)
                await ctx.respond(f'Uncensored ``{user.name}`` <:iamspreadingmisinformationatanal:1021414041744330804>')
                await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=f"Censoring {len(censored)} people"))
            else:
                await ctx.respond(f'``{user.name}`` is already uncensored')
        else:
            await ctx.respond(f'You cant uncensor me <:iamspreadingmisinformationatanal:1021414041744330804>')
    else:
        await ctx.respond(f'You cannot uncensor <:iamspreadingmisinformationatanal:1021414041744330804>')

@bot.event
async def on_message(message):
    json_data = json.load(open('censored.json'))
    censored = json_data['censored']
    if message.author.id in censored:
        await message.delete()
        msgstoptalking = await message.channel.send(f'<@{message.author.id}> stop sending messages you noob <a:bombk:1071682724068347914>')
        await sleep(3)
        await msgstoptalking.delete()

bot.run(TOKEN)
