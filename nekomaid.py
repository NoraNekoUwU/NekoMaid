import discord
from discord.ext import commands

bot = commands.Bot(command_prefix='!', description="NekoMaid Is private bot for Net Boukensha Guild Maintainance by Nakshima \n on progress")

@bot.event
async def on_ready():
    print('------------------------------------')
    print('NekoMaid ready to serve you master!')
    print('logged in as')
    print(bot.user.name)
    print('------------------------------------')
@bot.command()
async def wakeup(ctx):
    await ctx.send('Yes Master!')
@bot.command()
async def ping(ctx):
    await ctx.send('pong')
@bot.command()
async def sum(ctx,a,b):
	c = int(a) + int(b)
	await ctx.send(c)
@bot.command()
async def auto_roles(member):
	role = discord.uttils.get(member.guild.roles, name="Wanderer ¦ 冒険者")
	await member.add_roles(roles)
bot.run('Nzg5MDQ1OTM3NzU4MjczNTU3.X9sWSw.Gx3Cswps3m2jJISf91YmkbAmSJo')