import discord
from discord.ext import commands
import asyncio
# configuration files
import configparser
import sys, traceback

# grammar check
import language_check
grammar_en = language_check.LanguageTool('en-US')


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

    matches = grammar_en.check(message.content)
    for match in matches:
        bad_word = message.content[match.offset:match.offset + match.errorlength]
        if(match.ruleId == 'UPPERCASE_SENTENCE_START'):
            await message.channel.send('Wow. I can\'t believe you didn\'t start your sentence with a capital letter.')
        elif(match.ruleId == 'MORFOLOGIK_RULE_EN_US'): # spelling errors
            await message.channel.send('Ugh. The word \'' + bad_word + '\' is not spelled correctly.')
        elif(match.ruleId == 'IT_VBZ'): # this are a problem <- fixes that sort of issue
            await message.channel.send('Subject verb disagreement! Did you mean to use \'' + match.replacements[0] + '\' instead? (hint: you did)')
        elif(match.ruleId in ['IT_IS', 'EN_CONTRACTION_SPELLING']): # its when should be it's and that when should be that's
            await message.channel.send('Missing an apostrophe here: \'' + bad_word + '\'. Fix it.')
        elif(match.ruleId == 'PROGRESSIVE_VERBS'): # ???
            await message.channel.send('This word is not usually used in the progressive form.' +
                'I know you don\'t know what that means. http://lmgtfy.com/?q=progressive+form')
        elif(match.ruleId == 'PERS_PRONOUN_AGREEMENT_SENT_START'): # I are should be I am
            await message.channel.send('really? That verb does not agree with \'' + bad_word + '\'. You clearly meant \'' + match.replacements[0] + '\'')
        else:
            await message.channel.send([match])



# now actually connect the bot
client.run(config.get(section='Configuration', option='connection_token'),
           bot=True, reconnect=True)

