import asyncio
import discord
import youtube_dl
from discord.ext import commands

bot = commands.Bot(command_prefix =commands.when_mentioned_or("!"), description = 'NekoMaid Is private bot for Net Boukensha Guild Maintainance by Nakshima \n on progress')

@bot.event
async def siap():
    print('------------------------------------')
    print('NekoMaid ready to serve you master!')
    print('logged in as')
    print(bot.user.name)
    print('------------------------------------')

youtube_dl.utils.bug_reports_message = lambda: ''


ytdl_format_options = {
    'format': 'bestaudio/best',
    'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0' 
}

ffmpeg_options = {
    'options': '-vn'
}

ytdl = youtube_dl.YoutubeDL(ytdl_format_options)


class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=0.5):
        super().__init__(source, volume)
        self.data = data
        self.title = data.get('title')
        self.url = data.get('url')
    @classmethod
    async def from_url(cls, url, *, loop=None, stream=False):
        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream))
        if 'entries' in data:
            data = data['entries'][0]
        filename = data['url'] if stream else ytdl.prepare_filename(data)
        return cls(discord.FFmpegPCMAudio(filename, **ffmpeg_options), data=data)
class Music(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
	@commands.command()
	async def join(self, ctx):
		if ctx.author.voice:
			await ctx.author.voice.channel.connect()
		else:
			await ctx.send('GENIUS')
			raise commands.CommandError("Author not connected to a voice channel.")
	@commands.command()
	async def play(self, ctx, *, url):
		async with ctx.typing():
			player = await YTDLSource.from_url(url, loop=self.bot.loop, stream=True)
			ctx.voice_client.play(player, after=lambda e: print('Player error: %s' % e) if e else None)
		await ctx.send('Now Playing : {}'.format(player.title))
	@commands.command()
	async def volume(self, ctx, volume : int):
		if ctx.voice_client is None:
			return await ctx.send("Not connected to a voice channel")
		ctx.voice_client.source.volume = volume / 100
		await ctx.send("changed volume to {}%".format(volume))
	@commands.command()
	async def stop(self,ctx):

		await ctx.voice_client.disconnect()

	@play.before_invoke
	async def ensure_voice(self, ctx):
		if ctx.voice_client is None:
			if ctx.author.voice:
				await ctx.author.voice.channel.connect()
			else:
				await ctx.send("You are not connected to a voice channel.")
				raise commands.CommandError("Author not connected to a voice channel.")
		elif ctx.voice_client.is_playing():
			ctx.voice_client.stop()
class Fun(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
	@commands.command()
	async def wakeup(self,ctx):
		await ctx.send('Yes Master!!')
	@commands.command()
	async def sum (self,ctx, a, b):
		c = int(a) + int(b)
		await ctx.send(c)
bot.add_cog(Fun(bot))
bot.add_cog(Music(bot))
bot.run('Token')
