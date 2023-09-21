import discord, json, requests, urllib.parse

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
tree = discord.app_commands.CommandTree(bot)

@tree.command(name="search", description="Search for an anime scene")
async def self(interaction: discord.Interaction, url:str):
    # payload = requests.get("https://api.trace.moe/search?url={}".format(urllib.parse.quote_plus(url))).json()
    try:
        payload = requests.get("https://api.trace.moe/search?anilistInfo&url={}".format(urllib.parse.quote_plus(url))).json()
        title = payload["result"][0]["anilist"]["title"]["romaji"]
    except:
        payload = requests.get("https://api.trace.moe/search?url={}".format(urllib.parse.quote_plus(url))).json()
        title = (payload["result"][0]["filename"]).replace('.mp4', '')
    time_stamp, image_link = payload["result"][0]["from"], payload["result"][0]["image"]
    # title, time_stamp, image_link = (payload["result"][0]["filename"]).replace('.mp4', ''), payload["result"][0]["from"], payload["result"][0]["image"]
    # requests.post("https://api.trace.moe/search", data=open("demo.jpg", "rb"),headers={"Content-Type": "image/jpeg"}).json() # Upload version
    
    embed = discord.Embed(title=f"{title}", description=f"{time_stamp}", color=discord.Colour.green())
    embed.set_image(url=image_link)
    
    await interaction.response.reply(embed=embed)