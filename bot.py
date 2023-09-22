import discord, json, requests, asyncio
from discord import app_commands

with open('config.json', 'r') as f:
    data = json.load(f)
    
TOKEN = data['TOKEN']

class pre_bot(discord.Client):
    def __init__(self):
        super().__init__(intents=discord.Intents.all())
        self.synced = False

    async def on_ready(self):
        await tree.sync(guild=discord.Object(id=1121639089897230516)) # ! Test Server
        self.synced = True
        print("Bot Online")
        
bot = pre_bot()
tree = app_commands.CommandTree(bot)

@tree.command(name="search", description="Search for an anime scene", guild=discord.Object(id=1121639089897230516)) # ! Test server
async def self(interaction: discord.Interaction, url:str):
    try:
        payload = requests.get(f"https://api.trace.moe/search?anilistInfo&url={url}").json()
        title = payload["result"][0]["anilist"]["title"]["romaji"]
    except:
        payload = requests.get(f"https://api.trace.moe/search?url={url}").json()
        title = (payload["result"][0]["filename"]).replace('.mp4', '')
    time_stamp, image_link = payload["result"][0]["from"], payload["result"][0]["image"]
    
    time_minutes, time_seconds = int(time_stamp / 60), int(time_stamp % 60)
    
    embed = discord.Embed(title=f"{title}", description=f"{time_minutes}:{time_seconds}", color=discord.Colour.green())
    embed.set_image(url=image_link)
    
    await interaction.response.defer()
    await asyncio.sleep(15) 
    await interaction.followup.send(embed=embed, ephemeral=True)

if __name__ == '__main__':
    bot.run(TOKEN)