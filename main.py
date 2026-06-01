from discord import app_commands
import csv,discord,os
from datetime import datetime
import requests
import asyncio
from dotenv import load_dotenv

load_dotenv()

# TOKENS/API KEYS
load_dotenv()
discordtoken = os.getenv("discordtoken")
hf_api = os.getenv("hf_api")

if (not discordtoken) or (not hf_api):
    print("MISSING DETAILS -hf_api or discordtoken")
    

# SETTING UP DISCORD
Intents=discord.Intents.default()
Intents.messages = True
Intents.dm_messages = True
Intents.guilds = True
Intents.message_content = True


# filess
acces="files/acces.csv"
logs="files/logs.csv" #incase of misuse/inapropriate useage
togglefiles="files/toggle.csv"# form of serverid,on/off
configfiles="files/config.csv" # serverid,modelname,apikey




#File Functions


#Loads access
def lacces():
    data={}
    try:
        with open(acces,newline="") as f:
            for gid, uid in csv.reader(f):
                gid ,uid= int(gid) ,int(uid)
                if gid not in data: data[gid] = set()

                data[gid].add(uid)
        
    except: pass
    return data





def ltoggle():
    try:
        with open(togglefiles) as f:
            return {int(line.strip()) for line in f if line.strip()}
    except: return set()
    
    
    
    
def stoggle(c):
    with open(togglefiles,"w") as f:
        for gid in c:
            f.write(f"{gid}\n")
            
            
            
            
def lconfig():
    d={}
    try:
        with open(configfiles,newline="") as f:
            for gid,model,key,prompt in csv.reader(f):
                d[int(gid)]={"model":model,"apikey":key,"prompt":prompt}
    except: pass
    return d



def sconfig(gid,model,key,prompt):
    d=lconfig()
    d[gid]={"model":model,"apikey":key,"prompt":prompt}
    
    try:
        with open(configfiles,"w",newline="") as f:
            writer=csv.writer(f)
            for gid,config in d.items():
                writer.writerow([gid,config["model"],config["apikey"],config["prompt"]])
    except: print("error at scofnig")
                
            
    
                      
# De-appreciated Functions
'''

def racces(guild_id, user_id):
    try:
        with open(acces, "a", newline="") as f:
            writer = csv.writer(f)
            writer.writerow([guild_id, user_id])
    except: print("error")
    


def getdcinfo(interaction):
    return{
    "guild_name":interaction.guild.name if interaction.guild else"DM",
    "guild_id":str(interaction.guild.id) if interaction.guild else"DM", 
   '''


#Discord Setup

class RepliyBot(discord.Client): #fun fact name felt more funny this way\
    def __init__(self):
        super().__init__(intents=Intents)
        self.tree = app_commands.CommandTree(self)
    async def setup_hook(self):
         await self.tree.sync()




bot=RepliyBot()



# AI Handling Part
def aiconvo(prompt:str,interaction=None,message=None):
    
    
    # Get info for dc
    guild_name = "DM"
    guild_id = "DM"
    channel_name = "DM"
    channel_id = "DM"
    user_name = "Null"
    try:
        if interaction:
            user_name=str(interaction.user)
            if interaction.guild:
                guild_name=interaction.guild.name
                guild_id=str(interaction.guild.id)
                channel_name=interaction.channel.name
                channel_id=str(interaction.channel.id)
            else:
                channel_name="DM"
                channel_id=str(interaction.channel_id)
        elif message:
            user_name = str(message.author)
            if message.guild:
                guild_name = message.guild.name
                guild_id = str(message.guild.id)
                channel_name = message.channel.name
                channel_id = str(message.channel.id)
            else:
                channel_name = "DM"
                channel_id = str(message.channel.id)

    except Exception:
        pass   
    logit(prompt,hf(),"qwen",guild_name,guild_id,channel_name,channel_id,user_name)

#   





async def hf(a,systemp,prompt,modelname="google/gemma-4-31B-it",apikey=hf_api):

    if not hf_api: return None
    
    url = "https://router.huggingface.co/v1/chat/completions"
   
    headers={
        "Authorization": f"Bearer {apikey}",
        "Content-Type": "application/json"
    }
    
    
    payload={
        
        
    "model":modelname,
    "messages":[
        {"role":"system","content":a},
                {"role":"user","content":prompt}],
    "temperature": 0.7,
    "max_tokens": 1020,
    "stream": False
    }
    req = await asyncio.to_thread(
    requests.post,
    url,
    headers=headers,
    json=payload,
    timeout=90
    )
    if req.status_code != 200:

        return "error"

    return req.json()["choices"][0]["message"]["content"]
   
   
   
  #Logging 
    
def logit(prompt:str,output:str,model:str,guild_name: str = "DM",guild_id: str = "DM",channel_name: str = "DM",channel_id: str = "DM",user: str = "Unknown"):
    with open(logs,"a",newline="") as f:
        writer=csv.writer(f)
        if not os.path.isfile(logs): writer.writerow([
                "timestamp","model","server_name","server_id","channel_name","channel_id","user","prompt","final_output"])

        writer.writerow([
            datetime.now().isoformat(),
            model,
            guild_name,
            guild_id,
            channel_name,
            channel_id,
            user,
            prompt,
            output
        ])
@bot.event
async def on_message(message):

    
    #print("hi")
    if message.author.bot:
        return

    guid=message.guild.id
    configes=lconfig()
    
    configer=configes.get(guid)
    if configer:
        modelc = configer.get("model") 
        apikeyc = configer.get("apikey") 

    else:
        modelc = "google/gemma-4-31B-it" #wasted 20 mins doing ts man
        apikeyc = hf_api

    uid=message.author.id
    allowed = lacces()
    enabled = ltoggle()
    if  not bot.user.mentioned_in(message): return

    if message.guild.id not in enabled: return
    if message.author.guild_permissions.administrator: pass

    elif uid not in allowed.get(guid, set()): return
    sysprompt=f"You are a helpful ai made by chaitanya,U are Not apart of any meta/nvidia/any company.You Are to act as a chill Knowledable person kind of like a PHD holder,Your answers should be cool,chill and knowledgable and fitting in rather then robotic.Also Discord info ur in server {message.guild.name} in channel of{message.channel.name}  talking to user and user is {message.author.name} dont be  repetetive also man speak in discord format and anything to be in discord  ui/uxway only also max 1000 characters only try to be concise and more discordy dont always say tteir name also" 

    #print("hiii")
    history = []

    current = message

    while current.reference:
        try:
            parent = await current.channel.fetch_message(
                current.reference.message_id
            )

            history.append(
                f"{parent.author}: {parent.content}"
            )

            current = parent

        except Exception:
            break

    history.reverse()
    history.append( f"{message.author}: {message.content}" # tells context
)

    prompt = "\n".join(history)

    async with message.channel.typing():
        try:
            if configer:
                response = await  hf(
                    sysprompt,"",
                    prompt,
                    modelname=modelc,
                    apikey=apikeyc
                )
            else:
                response = await  hf(
                sysprompt,"",
                prompt
            )

            if not response:response = "erorr with response"

            if len(response) > 1000: response = response[:1000] + "ask me for more"

            await message.reply(response)

        except:
            await message.reply("error ")
            
            
# Discord Commands

@bot.tree.command(name="giveacc",description="gives acces")
@app_commands.checks.has_permissions(administrator=True)
async def giveacc(interaction: discord.Interaction, user: discord.User):
    with open(acces,"a",newline="") as f:
        csv.writer(f).writerow([interaction.guild.id,user.id])
        await interaction.response.send_message(f"gave access to {user.name}")
        
        
@bot.tree.context_menu(name="Give ACCES")
@app_commands.checks.has_permissions(administrator=True)
async def giveacc(interaction: discord.Interaction, user: discord.User):
    with open(acces,"a",newline="") as f:
        csv.writer(f).writerow([interaction.guild.id,user.id])
        await interaction.response.send_message(f"gave access to {user.name}")
        
      
        
@bot.tree.command(name="removeacc",description="removes acces")
@app_commands.checks.has_permissions(administrator=True)
async def removeacc(interaction: discord.Interaction, user: discord.User):
    a=False
    r=[]
    with open(acces,newline="") as f:
        for gid,uid in csv.reader(f):
            if not (int(gid) == interaction.guild.id and int(uid) == user.id):
                r.append([gid,uid])
            else:
                a=True
    with open(acces,"w",newline="") as f:
        csv.writer(f).writerows(r)
    
    await interaction.response.send_message(f"remove access from {user.name}"if not a else "didnt have anw")
    
    
@bot.tree.context_menu(name="Remove Access")
@app_commands.checks.has_permissions(administrator=True)
async def removeacc(interaction: discord.Interaction, user: discord.User):
    r=[]
    a=False
    with open(acces,newline="") as f:
        for gid,uid in csv.reader(f):
            if not (int(gid) == interaction.guild.id and int(uid) == user.id):
                r.append([gid,uid])
            else:
                a=True
    with open(acces,"w",newline="") as f:
        csv.writer(f).writerows(r)
    
    await interaction.response.send_message(f"remove access from {user.name}" if not a else "didnt have anw")
    
  

@bot.tree.command(name="toggle", description="Toggle bot on/off")
@app_commands.checks.has_permissions(administrator=True)
async def toggle(interaction: discord.Interaction):
    enabled = ltoggle()
    gid = interaction.guild.id
    if gid in enabled:
        enabled.remove(gid)
        s = "off"
    else:
        enabled.add(gid)
        s= "on"
    stoggle(enabled)
    await interaction.response.send_message(f"its now {s}")







#custom config

@bot.tree.command(name="configcustom",description="Setup configuration for custom response")
@app_commands.checks.has_permissions(administrator=True)
async def configcustom(interaction:discord.Interaction,model:str,apikey:str):
    if not model: 
        await interaction.response.send_message("No model chosne")
        return
    if not apikey:  
        await interaction.response.send_message("no api key given")
        return
    sconfig(interaction.guild.id,model,apikey,"")
    await interaction.response.send_message(f"{model} chosen")
    
    
#default config
    
@bot.tree.command(name="configdefault",description="Setup configuration to be default")
@app_commands.checks.has_permissions(administrator=True)
async def configdefault(interaction:discord.Interaction):

    sconfig( interaction.guild.id,"google/gemma-4-31B-it",hf_api,"")
    await interaction.response.send_message(f"default chosen")

   
@bot.tree.command(name="help",description="Helps Provide u with Information to use the bot")      
async def help(interaction:discord.Interaction):
    embed = discord.Embed(
    title="Help",
    description=        '''
        # Commands 
        /help -This command
        /configcustom -Setups up a configuration for specific ai model -requires hugginface api key and modelname
        /configdefault- Makes server go back to default configuration
        /giveacc- Gives acces in server to let sm1 Talk to ai
        /removeacc -Removes Acesss
        /Toggle -Toggles ai on and off
        /add - Gives link to add to server invite for bot
        #Also
        U can right click on people to give and remove access with apps
        
        
        
        
        ''',
    timestamp=datetime.now()
)
    await interaction.response.send_message(embed=embed)
    
@bot.tree.command(name="add",description='Get bot adding linkws')
async def add(interaction:discord.Interaction):
    await interaction.response.send_message(
        f"Server Invite link- https://discord.com/api/oauth2/authorize?client_id={bot.user.id}&permissions=448824200272&scope=bot%20applications.commands",ephemeral=True
        
    )


@bot.event
async def on_ready():
    print(f"Server Invite link- https://discord.com/api/oauth2/authorize?client_id={bot.user.id}&permissions=448824200272&scope=bot%20applications.commands")     
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name="Lets Talk it"))
   

    
    

        
bot.run(discordtoken)   
        
      