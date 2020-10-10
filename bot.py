import discord
import secrets
import json
import requests
import spotipy
import os
import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors

client_credentials_manager = spotipy.SpotifyClientCredentials(client_id=secrets.spotifyClientID, client_secret=secrets.spotifyClientSecret)
scopes= ["https://www.googleapis.com/auth/youtube.readonly"]

DEVELOPER_KEY = "AIzaSyB9j3xtCHvY_pi2DioKuxfX08jd8oN-ScE"
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"

youtube = googleapiclient.discovery.build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,
    developerKey=DEVELOPER_KEY)

#Spotify object to access API
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager) 

client = discord.Client()

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    if message.content.startswith("https://open.spotify.com/track/"):
        songID = message.content[31:].split('?',1)[0]
        result = sp.track(songID)
        song = {result['name'],result['artists'][0]['name']}
        print(song)
        request = youtube.search().list(
            part="snippet",
            maxResults=1,
            order="relevance",
            q=song
        )
        response = request.execute()

        videoId = response['items'][0]['id']['videoId']

        await message.channel.send('https://www.youtube.com/watch?v=' + str(videoId))

client.run('NzYxMDczNDQ1NTUwODE3MzAx.X3VS4Q.YUor3ZkNPlpSzs5NG4HICVY3Ziw')