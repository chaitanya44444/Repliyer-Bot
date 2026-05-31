import os
import re
from discord import app_commands
import discord
import random
import csv,json,os
from datetime import datetime
import google.generativeai
import requests

# TOKENS/API KEYS
gpai=""
discordtoken=""
hf_api=""
geminiapi=""

# SETTING UP DISCORD
Intents=discord.Intents.default()
Intents.messages = True
Intents.dm_messages = True
Intents.guilds = True
Intents.message_content = True
# Files
acces="acces.csv"
logs="" #incase of misuse/inapropriate useage

#File Functions
def lacces():
    try:
        with open(acces,newline="") as f:
            return {int(r[0]) for r in csv.reader(f)}
    except: return set()

def racces(user_id):
    try:
        with open(acces,"w",newline="") as f:
            writer=csv.writer(f)
            writer.writerow([user_id])
    except: print("hi")

# Discord Setup
class RepliyBot(discord.Client): #fun fact name felt more funny this way\
    def __init__(self):
        super().__init__(intents=Intents)
        self.tree = app_commands.CommandTree(self)
    async def setup_hook(self):
         await self.tree.sync()

bot=RepliyBot()
#Realised this would cause issues later with message/interaction diff

'''

def getdcinfo(interaction):
    return{
    "guild_name":interaction.guild.name if interaction.guild else"DM",
    "guild_id":str(interaction.guild.id) if interaction.guild else"DM", 
   '''

# AI Handling Part
def aiconvo():
    return ""

def gemini():
    return ""

def hf(prompt:str,interaction=None,message=None):
    
    
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
    if not hf_api: return None
    
    url = "https://router.huggingface.co/v1/chat/completions"
   
    headers={
        "Authorization": f"Bearer {hf_api}",
        "Content-Type": "application/json"
    }
    
    modelname="google/gemma-4-31B-it"
    
    payload={
        
        
    "model":modelname,
    "messages":[
        {"role":"system","content":"You are a helpful ai made by chaitanya,U are Not apart of any meta/nvidia/any company.You Are to act as a chill Knowledable person kind of like a PHD holder,Your answers should be cool,chill and knowledgable and fitting in rather then robotic.Also Discord info ur in server {guild_name} in channel of{channel_name}  talking to user and user is {user_name}"},
                {"role":"user","content":prompt}],
    "temperature": 0.7,
    "max_tokens": 1020,
    "stream": False
    }
    req = requests.post(
    url,
    headers=headers,
    json=payload
)
    
    response=req.json()["choices"][0]["message"]["content"]
    logit(prompt,response,modelname,guild_name,guild_id,channel_name,channel_id,user_name)
    return response
    
def logit(prompt:str,output:str,model:str,guild_name: str = "DM",guild_id: str = "DM",channel_name: str = "DM",channel_id: str = "DM",user: str = "Unknown"):
    with open(logs,"a",newline="") as f:
        writer=csv.writer(f)
        if not os.path.isfile(logs): writer.writerow([
                "timestamp","model","server_name","server_id","channel_name","channel_id","user","prompt","final_output"])

        writer.writerow([
            datetime.isoformat(),
            model,
            guild_name,
            guild_id,
            channel_name,
            channel_id,
            user,
            prompt,
            output
        ])
        