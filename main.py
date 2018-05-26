import discord
from discord.ext import commands
import asyncio
# configuration files
import configparser
import sys, traceback

# https://www.geeksforgeeks.org/get-synonymsantonyms-nltk-wordnet-python/
import nltk
from nltk.corpus import wordnet

# load configuration to get around hard coded tokens
config = configparser.ConfigParser()
with open('config.ini') as config_file:
    config.read_file(config_file)

# startup stuff for debugging
print('using discordpy version', discord.__version__)

client = discord.Client()

@client.event
async def on_ready():
    # print some stuff when the bot goes online
    print('Logged in ' + str(client.user.name) + ' - ' +
          str(client.user.id) + '\n' + 'Version ' + str(discord.__version__))

 
@client.event
async def on_message(message):
    if(message.author.bot):
        return

    #print (message.content)

    if "thesaurus " in message.content:
        my_string_1 = message.content.split("thesaurus ", 1)[1]

        end = my_string_1.find(" ")
        my_string_2 = my_string_1

        if end != -1:
            my_string_2 = my_string_1[0:end]

        if my_string_2 != "":

            # get thesaurus definitions:
            synonyms = []
            antonyms = []

            for syn in wordnet.synsets(my_string_2):
                for l in syn.lemmas():
                    if l.name() != my_string_2:
                        synonyms.append(l.name())
                    
                    if l.antonyms() and l.name() != my_string_2:
                        antonyms.append(l.antonyms()[0].name())

            if len(synonyms) == 0:
                await message.channel.send(my_string_2 + " isn't a word i know, which probably means you're wrong. Goof.")
                return

            synonyms_2 = ', '.join(synonyms)
            antonyms_2 = ', '.join(antonyms)

            my_string_3 = "Here, dummy:\n\nsynonyms: "

            for i in synonyms_2:
                my_string_3 = my_string_3 + i

            my_string_3 = my_string_3 + "\n\nantonyms: "

            for i in antonyms_2:
                my_string_3 = my_string_3 + i
                
            await message.channel.send(my_string_3)

# now actually connect the bot
client.run(config.get(section='Configuration', option='connection_token'),
           bot=True, reconnect=True)
