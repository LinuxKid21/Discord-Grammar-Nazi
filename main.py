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

import re

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
            if(bad_word[0] == '@'):
                continue # don't over react when the @mention someone!
            sentences.append('Ugh. The word \'' + bad_word + '\' is not spelled correctly.')
        elif(match.ruleId == 'IT_VBZ'): # this are a problem <- fixes that sort of issue
            sentences.append('Subject verb disagreement! Did you mean to use \'' + match.replacements[0] + '\' instead? (hint: you did)')
        elif(match.ruleId in ['IT_IS', 'EN_CONTRACTION_SPELLING']): # its when should be it's and that when should be that's
            sentences.append('Missing an apostrophe here: \'' + bad_word + '\'. Fix it.')
        elif(match.ruleId == 'PROGRESSIVE_VERBS'): # ???
            sentences.append('This usage is not usually used in the progressive form.' +
                'I know you don\'t know what that means so here it is: http://lmgtfy.com/?q=progressive+form')
        elif(match.ruleId == 'PERS_PRONOUN_AGREEMENT_SENT_START'): # I are should be I am
            sentences.append('really? That verb does not agree with \'' + bad_word + '\'. You clearly meant \'' + match.replacements[0] + '\'')
        else:
            sentences.append([match])

    #punctuation = ['.', '!', '?']

    ## looks like the following:
    ##   ['This is a sentence' '.' 'Okay' '?' '']
    ## except the last one is cut out 'cause we don't want it
    #split = re.split('(\.|\!|\?)', message.content)


    #if(split[-1] not in punctuation):
    #    sentences.append('!?!?!?!?!? NO PUNCTUATION? Look at where you missed it! ' + split[-1] + '(here)')

    return sentences

def handle_thesaurus(message):

    my_string_1 = message.content.split("Thesaurus ", 1)[1]

    end = my_string_1.find(" ")
    my_string_2 = my_string_1

    if end != -1:
        my_string_2 = my_string_1[0:end]

    if my_string_2 == "":
        my_string_2 = "nothing"

    # get thesaurus definitions:
    synonyms = []

    for syn in wordnet.synsets(my_string_2):
        for l in syn.lemmas():
            if l.name() != my_string_2:
                synonyms.append(l.name())

    if len(synonyms) == 0:
        ret_string = my_string_2 + " isn't a word i know, which probably means you're wrong. Goof."
        return retstring

    synonyms_2 = ', '.join(synonyms)

    my_string_3 = "Here, dummy:\n\n\'" + my_string_2 + "\' synonyms: "

    for i in synonyms_2:
        my_string_3 = my_string_3 + i
        
    return my_string_3

 
@client.event
async def on_message(message):

    if(message.author.bot):
        return

    if "Thesaurus " in message.content:
        my_string = handle_thesaurus(message)
        await message.channel.send(my_string)
    else:
        sentences = handle_grammar(message)
        for sentence in sentences:
            await message.channel.send(sentence)

# now actually connect the bot
client.run(config.get(section='Configuration', option='connection_token'),
           bot=True, reconnect=True)

