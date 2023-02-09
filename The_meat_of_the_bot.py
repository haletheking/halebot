import datetime

import discord
import time
import requests
import queue
import re
import math
from discord.utils import get
global tester
tester=0
#https://discordapp.com/oauth2/authorize?client_id=483812776570126346&scope=bot&permissions=8

client = discord.Client()
client.tester=tester


headers = {
    'Authorization': 'Bearer 5n1543t6wswcg5lqdld356u4gfmnyl',
    'Client-Id': '0lgiwe50wrgbj5r2952i3mvxtabqz3',
}

params = {
    'login': 'thelgx',
}

response = requests.get('https://api.twitch.tv/helix/users', params=params, headers=headers)

responsejs=response.json()
id=responsejs["data"][0]['id']
print(id)


vidparams = {
    'user_id': id,
    'type': 'archive',
}


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))
    #await client.change_presence(status=discord.Status.invisible)


@client.event
async def on_message_delete(message):
    #print('FOUND DELETE')
    pass


@client.event
async def on_message(message):
    if message.author == client.user:
        #await message.add_reaction('👀')
        pass


    elif message.content.startswith('[print'):
        pass

    elif message.content.startswith('[startday'):
        print('gotmessage')
        vidresponse = requests.get('https://api.twitch.tv/helix/videos', params=vidparams, headers=headers)

        vidresponsejs = vidresponse.json()
        print(vidresponsejs)

        pub_at_formated=time.strptime((vidresponsejs['data'][0]['published_at']), "%Y-%m-%dT%H:%M:%SZ")
        print(pub_at_formated)
        outputmsg="**theLGX Stream Recap: "+str(pub_at_formated.tm_mon)+"/"+str(pub_at_formated.tm_mday)+"/"+str(pub_at_formated.tm_year)+" || "+vidresponsejs['data'][0]['title']+"**"
        await message.channel.send(outputmsg)

    elif message.content.startswith('[tldrnow'):
        print('gotmessage')
        vidresponse = requests.get('https://api.twitch.tv/helix/videos', params=vidparams, headers=headers)

        vidresponsejs = vidresponse.json()
        durations = list()
        for i in range(10):
            response2 = requests.get('https://api.twitch.tv/helix/videos', params=vidparams, headers=headers)
            responsejs2 = response2.json()
            duration = responsejs2['data'][0]['duration']
            #print(duration)
            durationsplit = time.strptime(duration, "%Hh%Mm%Ss")
            durinsecs = durationsplit.tm_hour * 60 * 60 + durationsplit.tm_min * 60 + durationsplit.tm_sec
            #print(durinsecs)
            durations.append(durinsecs)
        averagedur = math.floor((sum(durations) / len(durations)))
        averagedurhr = math.floor(averagedur / 3600)
        averagedurmin = math.floor((averagedur % 3600) / 60)
        averagedursec = math.floor(averagedur % 60)
        timestamp=str(averagedurhr).zfill(2) + ":" + str(averagedurmin).zfill(2) + ":" + str(averagedursec).zfill(2)


        url = vidresponsejs['data'][0]['url'] + "?t=" + str(averagedur) + "s"
        print(url)

        input=message.content[8:]
        if len(input)>0:
            if input[0]==' ':
                input=input[1:]
        outputmsg="- <"+url+"> **"+timestamp+"** - "+input
        await message.channel.send(outputmsg)

    elif message.content.startswith('[tldrtime'):
        print('gotmessage')
        vidresponse = requests.get('https://api.twitch.tv/helix/videos', params=vidparams, headers=headers)

        vidresponsejs = vidresponse.json()

        input = message.content[8:]
        if len(input) > 0:
            if input[0] == ' ':
                input = input[1:]
        try:
            inputtime=(input.split("[")[1])[:8]
            properinput=(input.split("[")[1])[8:]

            durationsplit = time.strptime(inputtime, "%H:%M:%S")
            durinsecs = durationsplit.tm_hour * 60 * 60 + durationsplit.tm_min * 60 + durationsplit.tm_sec
            averagedur = math.floor(durinsecs)
            averagedurhr = math.floor(averagedur / 3600)
            averagedurmin = math.floor((averagedur % 3600) / 60)
            averagedursec = math.floor(averagedur % 60)
            timestamp = str(averagedurhr).zfill(2) + ":" + str(averagedurmin).zfill(2) + ":" + str(averagedursec).zfill(2)

            url = vidresponsejs['data'][0]['url'] + "?t=" + str(averagedur) + "s"
            print(url)


            outputmsg = "- <" + url + "> **" + timestamp + "** - " + properinput
            await message.channel.send(outputmsg)
        except:
            await message.channel.send("improper formating")


    elif message.content.startswith('[inc'):
        client.tester=client.tester+1
        #await client.send_message(message.author,str('a message was found that you track      tracked word: '+str(client.tester)+'      in: '+str(message.server)+' , <#'+str(message.channel.id)+'> \n'+str(message.content)))
    elif message.content.startswith('[init'):
        pass
        #await message.channel.send(str('p!help'))
    else:
        pass
        print (str(message.channel)+' : '+str(message.author)+' : '+str(message.channel.id)+' : '+str(message.content))
@client.event
async def on_reaction_add(reaction,user):
   pass

@client.event
async def on_reaction_remove(reaction, user):
    pass
@client.event
async def on_message_edit(before, after):
    pass
with open("token.txt") as file:
    token = file.readlines()[0]
client.run(token)