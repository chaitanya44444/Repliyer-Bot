import os
from discord import app_commands
import discord
import random
import csv,json,os
from datetime import datetime
import google.generativeai
import requests
import asyncio
from dotenv import load_dotenv
load_dotenv()

# TOKENS/API KEYS
load_dotenv()
discordtoken = os.getenv("discordtoken")
hf_api = os.getenv("hf_api")




# SETTING UP DISCORD
Intents=discord.Intents.default()
Intents.messages = True
Intents.dm_messages = True
Intents.guilds = True
Intents.message_content = True


# Files
acces="acces.csv"
logs="logs.csv" #incase of misuse/inapropriate useage
toggle="toggle.csv"# form of serverid,on/off
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
#Realised this would cause issues later with message/interaction diff



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

#   hf("You are a helpful ai made by chaitanya,U are Not apart of any meta/nvidia/any company.You Are to act as a chill Knowledable person kind of like a PHD holder,Your answers should be cool,chill and knowledgable and fitting in rather then robotic.Also Discord info ur in server {guild_name} in channel of{channel_name}  talking to user and user is {user_name}")

def gemini():
    return ""



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
        print(req.text)
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
    print("hi")
    if message.author.bot:
        return

    guid=message.guild.id
    uid=message.author.id
    allowed = lacces()
    if message.author.guild_permissions.administrator: pass

    elif uid not in allowed[guid] or guid not in allowed:
        return
    print("hiii")
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
            response = await  hf(
                "You are a helpful AI made by Chaitanya.You are to act knowledgable and funny and know about memes and cultural references.You woll reply in less then 500 charascters and in discord foramat","",
                prompt
            )

            if not response:
                response = "erorr with response"

            if len(response) > 2000:
                response = response[:1990] + "..."

            await message.reply(response)

        except Exception as e:
            await message.reply(f"Error: {e}")

bot.run(discordtoken)   
        
      