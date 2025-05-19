from dotenv import load_dotenv
import os

load_dotenv()  # Loads from .env file

client_id = os.getenv("SPOTIFY_CLIENT_ID")
client_secret = os.getenv("SPOTIFY_CLIENT_SECRET")
redirect_uri = os.getenv("SPOTIFY_REDIRECT_URI")

print("Client ID:", client_id)
print("Client Secret:", client_secret)
print("Redirect URI:", redirect_uri)