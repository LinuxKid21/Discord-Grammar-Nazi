import discord
from discord.ext import commands
import asyncio
# configuration files
import configparser
import sys, traceback

# grammar check
import language_check
grammar_en = language_check.LanguageTool('en-US')

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


def handle_grammar(message):
    matches = grammar_en.check(message.content)
    sentences = []
    for match in matches:
        bad_word = message.content[match.offset:match.offset + match.errorlength]
        if(match.ruleId == 'UPPERCASE_SENTENCE_START'):
            sentences.append('Wow. I can\'t believe you didn\'t start your sentence with a capital letter.')
        elif(match.ruleId == 'MORFOLOGIK_RULE_EN_US'): # spelling errors
            sentences.append('Ugh. The word \'' + bad_word + '\' is not spelled correctly.')
        elif(match.ruleId == 'IT_VBZ'): # this are a problem <- fixes that sort of issue
            sentences.append('Subject verb disagreement! Did you mean to use \'' + match.replacements[0] + '\' instead? (hint: you did)')
        elif(match.ruleId in ['IT_IS', 'EN_CONTRACTION_SPELLING']): # its when should be it's and that when should be that's
            sentences.append('Missing an apostrophe here: \'' + bad_word + '\'. Fix it.')
        elif(match.ruleId == 'PROGRESSIVE_VERBS'): # ???
            sentences.append('This word is not usually used in the progressive form.' +
                'I know you don\'t know what that means. http://lmgtfy.com/?q=progressive+form')
        elif(match.ruleId == 'PERS_PRONOUN_AGREEMENT_SENT_START'): # I are should be I am
            sentences.append('really? That verb does not agree with \'' + bad_word + '\'. You clearly meant \'' + match.replacements[0] + '\'')
        else:
            sentences.append([match])
    return sentences

 
@client.event
async def on_message(message):
    if(message.author.bot):
        return

    sentences = handle_grammar(message)
    for sentence in sentences:
        await message.channel.send(sentence)


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
