import os
import discord
import requests 
import json 
import random 
from replit import db 
from keep_alive import keep_alive

client = discord.Client()

sad_words = ["sad", "depressed", "lonely", "angry", "bad", "loser", "stressed"]

starter_encouragements = ["Be Happy!", "Cheer Up!", "Don't Cry!"]

def get_quote(): 
  response = requests.get("https://zenquotes.io/api/random")
  json_data = json.loads(response.text)
  quote = json_data[0]['q'] # get random quote from response
  return quote

def update_encouragements(encourage_message):
  if "encouragements" in db.keys(): 
    encouragements = db["encouragements"] 
    encouragements.append(encourage_message)
    db["encouragements"] = encouragements
  else:
    db["encouragements"] = [encourage_message]

def delete_encouragement(index): 
  encouragements = db["encouragements"] 
  if len(encouragements) > index: 
    del encouragements[index]
    db["encouragements"] = encouragements

@client.event  
async def on_ready(): # when the bot is ready to be used
  print("We have logged in as {0.user}".format(client))


@client.event
async def on_message(message): # when a user writes a message
  if message.author == client.user: 
    return 
  
  if message.content.startswith("$hello"): # $ sign used to communicate with bot
    await message.channel.send("Hello")

  if message.content.startswith("$inspire"): # $ sign used to communicate with bot
    await message.channel.send(get_quote())

  options = starter_encouragements
  if "encouragements" in db.keys() and db["encouragements"] == []: 
      for word in starter_encouragements: 
        db["encouragements"].append(word)


  if any(word in message.content for word in sad_words): 
    await message.channel.send(random.choice(options))


  if message.content.startswith("$new"):
    encourage_message = message.content.split("$new ",1)[1]
    update_encouragements(encourage_message)
    await message.channel.send("Encouraging message added!")

  if message.content.startswith("delAll"):
    db["encouragements"] = []
    encouragements = db["encouragements"]
    await message.channel.send(encouragements) 

  if message.content.startswith("$show"): 
    encouragements = [] 
    if "encouragements" in db.keys(): 
      encouragements = db["encouragements"]
      await message.channel.send(encouragements)

  if message.content.startswith("$responding"): 
    value = message.content.split("$responding ", 1)[1]

    if value.lower() == "true": 
      db["responding"] = True 
      await message.channel.send("Responding is on.")
    else: 
      db["responding"] = False 
      await message.channel.send("Responding is off.")
 
keep_alive() 
client.run(os.environ['TOKEN']) # run the bot
