import os
import re
from discord import app_commands
import discord
import random
import csv,json,os
from datetime import datetime
import google.generativeai

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

# AI Handling Part
def aiconvo():
    return ""

def gemini():
    return ""
def hf(prompt:str,system_prompt:str,interaction=None,message=None):
    
    if not hf_api: return None
    
    url = "https://router.huggingface.co/v1/chat/completions"
   
    headers={
        "Authorization": f"Bearer {hf_api}",
        "Content-Type": "application/json"
    }
    
    modelname="meta-llama/Meta-Llama-3-8B-Instruct"
    

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
        