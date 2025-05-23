import requests
from bs4 import BeautifulSoup
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import os

year = input("which year you want to travel?In the format YYYY-MM-DD\n")
headers = {"User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36"}
URL = f"https://www.billboard.com/charts/hot-100/{year}"
response = requests.get(URL,headers=headers)
songs = response.text
soup = BeautifulSoup(songs,"html.parser")
song_names_spans = soup.select("li ul li h3")
song_names = [song.getText().strip() for song in song_names_spans]
client_id = os.environ.get("CLIENT_ID")
client_secert = os.environ.get("CLIENT_SECERT")
sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
    client_id=client_id,
    client_secret=client_secert,
    redirect_uri="https://example.com",
    scope="playlist-modify-private",
    show_dialog=True,
    cache_path="token.txt",
    username="your unique spotipy name",
)
)
user_id = sp.current_user()["id"]
song_uris = []
date = year.split("-")[0]
for song in song_names:
    song_uri = sp.search(f"track:{song} year:{date}",type="track")

    try:
        song_uriss = song_uri["tracks"]["items"][0]["uri"]
        song_uris.append(song_uriss)
    except IndexError:
        print(f"{song} not found..skipped")
hello_my = sp.user_playlist_create(user=user_id,name="YYYY-MM-DD Billboard 100",public=False)
sp.playlist_add_items(items=song_uris,playlist_id=hello_my["id"])


