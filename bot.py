# bot.py
import os
import random
import requests
import json
import urllib
from json import JSONEncoder
import discord
from discord.ext import commands
from dotenv import load_dotenv
from requests.auth import HTTPBasicAuth
import typing
import keep_alive

load_dotenv()
token = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')
couchPotatoURL = os.getenv('CP_URL')
couchPotatoAPIKey = os.getenv('CP_APIKEY')
imdbKey = os.getenv('IMDB_APIKEY')
sonarrAPIKey = os.getenv('SONARR_APIKEY')
sonarrURL = os.getenv('SONARR_URL')

client = discord.Client()
bot = commands.Bot(command_prefix='!')

@bot.event
async def on_ready():
    guild = discord.utils.get(bot.guilds, name=GUILD)
    print(
        f'{bot.user} is connected to the following guild:\n'
        f'{guild.name}(id: {guild.id})'
    )

    members = '\n - '.join([member.name for member in guild.members])
    print(f'Guild Members:\n - {members}')

@bot.event
async def on_member_join(member):
    await member.create_dm()
    await member.dm_channel.send(
        f'Hi {member.name}, welcome to the BHB Discord server! \n Check out the #media channel description!'
    )


@bot.command(name='cp-version', help='Checks version of CouchPotato Server')
@commands.has_role('Media Requester')
async def cp_version(ctx):
    try:
        request = requests.get(couchPotatoURL + '/api/' + couchPotatoAPIKey + '/app.version')
        cpversion = json.loads(request.text)
        await ctx.send(cpversion['version'])
    except: 
	    await ctx.send('Failed to get info')

@bot.command(name='MovieReq', help='Add A Movie. Example: !MovieReq "Deadpool 2" ')
@commands.has_role('Media Requester')
async def movie_req(ctx, mName):
    # Search for IMDB ID from name of 
    try:
        url = 'http://www.omdbapi.com/?t=' + urllib.parse.quote_plus(mName) + '&apikey=' + imdbKey
        print(url)
        request = requests.get(url)
        json_data = json.loads(request.text)
        if json_data['Response'] == "":
            await ctx.send ("Movie not found on IMDB")
            return
        imdbID = json_data['imdbID']
        movieTitle = json_data['Title']
        await ctx.send('Matched your request to ' + movieTitle + ' - ' + imdbID)
    except:
        await ctx.send('Failed IMDB request')
        
    # Add movie to couch potato wanted list
    try:
        request = requests.get(couchPotatoURL + '/api/' + couchPotatoAPIKey + '/movie.add/?identifier=' + imdbID)
        json_data = json.loads(request.text)
        await ctx.send('Added ' + movieTitle + ' to wanted list. \nIt may take some time to acquire.  CouchPotato Bot will take it from here.')
    except:
        await ctx.send('Unable to add ' + movieTitle + 'to wanted list')



@bot.command(name='ShowLookup', help='!ShowLookup "Watchmen"')
@commands.has_role('Media Requester')
async def show_look(ctx, sName):
    # Perform a Search for shows
    
    cvtName = sName.replace(" ", "%20")
    url = sonarrURL + '/api/series/lookup?term=' + cvtName + '&apikey=' + sonarrAPIKey
    getR = requests.get(url)
    # Manual get and post the top result

    r = getR.json()
    length = len(r)
    if length == 1:
        a = r[0]
        ayear = str(a['year'])
        if "imdbId" not in a:
            aImdbId = "Null"
        else:
            aImdbId = a['imdbId']
        await ctx.send("Series 0: " + a['title'] + " - " + ayear + "     IMDB = " + aImdbId)
    if length == 2:
        a,b = (r[0], r[1])
        ayear = str(a['year'])
        if "imdbId" not in a:
            aImdbId = "Null"
        else:
            aImdbId = a['imdbId']
        await ctx.send("Series 0: " + a['title'] + " - " + ayear + "     IMDB = " + aImdbId)
        byear = str(b['year'])
        if "imdbId" not in b:
            bImdbId = "Null"
        else:
            bImdbId = b['imdbId']
        await ctx.send("Series 1: " + b['title'] + " - " + byear + "     IMDB = " + bImdbId)

    if length == 3:
        a,b,c = (r[0],r[1],r[2])
        ayear = str(a['year'])
        if "imdbId" not in a:
            aImdbId = "Null"
        else:
            aImdbId = a['imdbId']
        await ctx.send("Series 0: " + a['title'] + " - " + ayear + "     IMDB = " + aImdbId)
        byear = str(b['year'])
        if "imdbId" not in b:
            bImdbId = "Null"
        else:
            bImdbId = b['imdbId']
        await ctx.send("Series 1: " + b['title'] + " - " + byear + "     IMDB = " + bImdbId)
        cyear = str(c['year'])
        if "imdbId" not in c:
            cImdbId = "Null"
        else:
            cImdbId = c['imdbId']
        await ctx.send("Series 2: " + c['title'] + " - " + cyear + "     IMDB = " + cImdbId)

    if length == 4:
        a,b,c,d = (r[0],r[1],r[2],r[3])
        ayear = str(a['year'])
        if "imdbId" not in a:
            aImdbId = "Null"
        else:
            aImdbId = a['imdbId']
        await ctx.send("Series 0: " + a['title'] + " - " + ayear + "     IMDB = " + aImdbId)
        byear = str(b['year'])
        if "imdbId" not in b:
            bImdbId = "Null"
        else:
            bImdbId = b['imdbId']
        await ctx.send("Series 1: " + b['title'] + " - " + byear + "     IMDB = " + bImdbId)
        cyear = str(c['year'])
        if "imdbId" not in c:
            cImdbId = "Null"
        else:
            cImdbId = c['imdbId']
        await ctx.send("Series 2: " + c['title'] + " - " + cyear + "     IMDB = " + cImdbId)
        dyear = str(d['year'])
        if "imdbId" not in d:
            dImdbId = "Null"
        else:
            dImdbId = d['imdbId']
        await ctx.send("Series 3: " + d['title'] + " - " + dyear + "     IMDB = " + dImdbId)

    if length >= 5:
        a,b,c,d,e = (r[0],r[1],r[2],r[3],r[4])
        ayear = str(a['year'])
        if "imdbId" not in a:
            aImdbId = "Null"
        else:
            aImdbId = a['imdbId']
        await ctx.send("Series 0: " + a['title'] + " - " + ayear + "     IMDB = " + aImdbId)
        byear = str(b['year'])
        if "imdbId" not in b:
            bImdbId = "Null"
        else:
            bImdbId = b['imdbId']
        await ctx.send("Series 1: " + b['title'] + " - " + byear + "     IMDB = " + bImdbId)
        cyear = str(c['year'])
        if "imdbId" not in c:
            cImdbId = "Null"
        else:
            cImdbId = c['imdbId']
        await ctx.send("Series 2: " + c['title'] + " - " + cyear + "     IMDB = " + cImdbId)
        dyear = str(d['year'])
        if "imdbId" not in d:
            dImdbId = "Null"
        else:
            dImdbId = d['imdbId']
        await ctx.send("Series 3: " + d['title'] + " - " + dyear + "     IMDB = " + dImdbId)
        eyear = str(e['year'])
        if "imdbId" not in e:
            eImdbId = "Null"
        else:
            eImdbId = e['imdbId']
        await ctx.send("Series 4: " + e['title'] + " - " + eyear + "     IMDB = " + eImdbId)

@bot.command(name='ShowReq', help='Add a show. Ex: !ShowReq "Watchmen" or !ShowReq "Watchman", 1')
@commands.has_role('Media Requester')
async def show_req(ctx, sName, sNum: typing.Optional[int] = 0):
    # Check if Series already exists
    #sNum = int(sNum)
    #cvtName = sName.replace(" ", "%20")
    #url = sonarrURL + '/api/series/lookup?term=' + cvtName + '&apikey=' + sonarrAPIKey    
    #lookR = requests.get(url)
    #lookTvdbID = lookR[sNum]
    #gurl = sonarrURL + '/api/series?apikey=' + sonarrAPIKey
    #checkR = requests.get(gurl)
    #checkTvdbID = checkR[sNum]
    #if lookTvdbID == checkTvdbID:
    #    print("Your series is already in plex.")
    #    exit()

    # Add Series into Sonarr
    await ctx.send("Series found and passing info to Sonarr.")
    sNum = int(sNum)
    cvtName = sName.replace(" ", "%20")
    url = sonarrURL + '/api/series/lookup?term=' + cvtName + '&apikey=' + sonarrAPIKey  
    purl = sonarrURL + '/api/series?apikey=' + sonarrAPIKey
    getR = requests.get(url)
    r = getR.json()
    payload={
        "title": r[sNum]['title'], 
        "images": r[sNum]['images'],
        "seasons": r[sNum]['seasons'],
        "path": "/volume1/Media/TV/" + r[sNum]['title'],
        "profileId": 6,
        "seasonFolder": True,
        "monitored": True,
        "tvdbId": r[sNum]['tvdbId'],
        "tvRageId": r[sNum]['tvRageId'],
        "titleSlug": r[sNum]['titleSlug'],
        "addOptions":
        {
            "ignoreEpisodesWithFiles": True,
            "ignoreEpisodesWithoutFiles": False,
            "searchForMissingEpisodes": True
        }
    }
    vPayload = json.dumps(payload, indent=4)
    post = requests.post(purl, data=vPayload)
    await ctx.send("My work is complete, letting Sonarr Bot take it from here.")


# Add show to sonarr schedule / monitoring


# Functions


keep_alive.keep_alive()
bot.run(token)