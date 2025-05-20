import os
from dotenv import load_dotenv
import spotipy
from spotipy.oauth2 import SpotifyOAuth

# Load and set credentials from .env
load_dotenv()
SPOTIFY_CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
SPOTIFY_CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")
SPOTIFY_REDIRECT_URI = os.getenv("SPOTIFY_REDIRECT_URI")

# Set up Spotify API client
scope = "playlist-modify-private playlist-modify-public"
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id=SPOTIFY_CLIENT_ID,
    client_secret=SPOTIFY_CLIENT_SECRET,
    redirect_uri=SPOTIFY_REDIRECT_URI,
    scope=scope
))

def find_artist_id(artist_name):
    results = sp.search(q=f"artist:{artist_name}", type="artist", limit=1)
    items = results['artists']['items']
    if not items:
        raise Exception(f"Artist '{artist_name}' not found.")
    return items[0]['id'], items[0]['name']

def get_all_albums(artist_id):
    albums = []
    seen_names = set()

    results = sp.artist_albums(artist_id, album_type='album,single', limit=50)
    albums.extend(results['items'])

    while results['next']:
        results = sp.next(results)
        albums.extend(results['items'])

    # Deduplicate by album name
    unique_albums = []
    for album in albums:
        if album['name'].lower() not in seen_names:
            seen_names.add(album['name'].lower())
            unique_albums.append(album)

    return unique_albums

def get_all_track_ids(album_list):
    track_ids = []
    for album in album_list:
        tracks = sp.album_tracks(album['id'])
        for track in tracks['items']:
            track_ids.append(track['id'])
    return track_ids

def create_playlist(user_id, playlist_name):
    playlist = sp.user_playlist_create(user_id, playlist_name, public=False)
    return playlist['id']

def add_tracks_to_playlist(playlist_id, track_ids):
    # Add in batches of 100
    for i in range(0, len(track_ids), 100):
        sp.playlist_add_items(playlist_id, track_ids[i:i+100])

def main():
    artist_input = input("Enter artist name: ").strip()
    artist_id, canonical_name = find_artist_id(artist_input)
    print(f"Found artist: {canonical_name}")

    print("Fetching albums...")
    albums = get_all_albums(artist_id)
    print(f"Found {len(albums)} unique albums/singles.")

    print("Fetching tracks...")
    track_ids = get_all_track_ids(albums)
    print(f"Found {len(track_ids)} tracks.")

    user_id = sp.me()['id']
    playlist_name = f"{canonical_name} Discography"
    playlist_id = create_playlist(user_id, playlist_name)
    print(f"Created playlist: {playlist_name}")

    print("Adding tracks to playlist...")
    add_tracks_to_playlist(playlist_id, track_ids)
    print("Done!")

if __name__ == "__main__":
    main()