import os
from subprocess import Popen
import warnings

from dotenv import dotenv_values
import spotipy
from spotipy.oauth2 import SpotifyOAuth

# Override sample with non-sample file-based env variables,
# and override both with actual env variables
config = {**dotenv_values("sample.env"), **dotenv_values(".env"), **os.environ}

# Authenticate
scopes = ["playlist-read-private", "playlist-modify-private"]
auth_manager = SpotifyOAuth(
    scope=scopes,
    client_id=config["CLIENT_ID"],
    client_secret=config["CLIENT_SECRET"],
    redirect_uri=config["REDIRECT_URI"],
)

url = auth_manager.get_authorize_url()

redirect_server = None
# Start up a server at the redirct uri so that the browser has somewhere to go.
if "localhost" in config["REDIRECT_URI"]:
    port = config["REDIRECT_URI"].rstrip("/").split(":")[-1]
    redirect_server = Popen(["python", "-m", "http.server", port])


print(f"1. Open the following link in your browser:\n\n{url}\n")
print("2. Accept the Spotify authorization.")

redirect_url = input(
    "3. Enter the URL that you got redirected to after accepting the authorization\n"
)
response_code = auth_manager.parse_response_code(redirect_url)
with warnings.catch_warnings():
    warnings.filterwarnings("ignore")
    access_token = auth_manager.get_access_token(response_code)

print(f"Your refresh token is:\n\n{access_token['refresh_token']}\n")
print(f"Store this as the REFRESH_TOKEN in your environment variables")

if redirect_server is not None:
    redirect_server.terminate()
