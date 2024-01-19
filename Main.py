"""
Author: Braden Huang
Version: 1.0

"""

import base64
import requests
import datetime
import json
import webbrowser
from secret import secrets
from urllib.parse import urlencode
from getcode import get_auth_code
from gettoken import get_token
from getliked import get_liked
from songfeatures import get_song_features
from playlistoperations import *


client_id = secrets['client_id']
client_secret = secrets['client_secret']


credentials = f"{client_id}:{client_secret}"
creds_b64 = base64.b64encode(credentials.encode())


def get_userid(token):
    url = "https://api.spotify.com/v1/me"
    header = {"Authorization" : "Bearer " + token}
    r = requests.get(url, headers=header)
    response = r.json()
    id = response['id']
    print(response)


def main():
    songs = []
    playlists = []
    get_auth_code()
    code = str(input("Enter the code from the URL of the webpage: "))
    token = get_token(code)
    playlists = get_playlists(token, playlists)
    
    while True:
        print("Select playlist to import songs from: \n1. Liked Songs")
        if len(playlists) > 0:
            for index, playlist in enumerate(playlists, start=1):
                print(f"{index+1}. {playlist['name']}")
        choice = int(input("Please enter number of playlist of choice shown above. Enter 0 to quit. Once you are done adding songs enter 999: "))

        if choice == 1: 
            songs = get_liked(token,songs)
        if choice == 0:
            break
        if choice not in [1, 0, 999]:
            pchoice = playlists[choice - 2]
            songs = get_playlist_songs(pchoice, token, songs)
        if choice == 999:
            get_song_features(songs, token)

            """
            with open("output.txt", "w", encoding='utf-8') as file:
                for song in songs:
                    song_json = json.dumps(song, ensure_ascii=False)
                    file.write(song_json + "\n")
                print('All unique songs with audio features added to file')
                """
            break
        



             
    #song = get_liked(token,songs)
    #get_song_features(songs, token)
    #print(playlists)
    #pchoice = playlist_select(playlists)
    #get_playlist_songs_all(playlists,token,songs)

if __name__ == "__main__":
    main()


    