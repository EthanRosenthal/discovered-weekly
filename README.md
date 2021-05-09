# discovered-weekly

Archive each week's Discover Weekly

This repo allows you to automatically archive your Discover Weekly playlist each week in two ways:

1. Your Discover Weekly get stored to a unique playlist called "Discovered Weekly YYYY-MM-DD".
1. Your Discover Weekly gets appended to a single playlist containing all archived Discover Weeklies.

This project uses the Spotify API to get and create the playlists. GitHub Actions are used to automate the workflow.

I should note that a cursory search on GitHub for "discover weekly" will show that there are many other projects that do a similar thing to this project. I reinvented the wheel because:

1. I wanted to figure this out for myself.
1. I wanted to archive to both individual playlists and a single playlist of all time.
1. I wanted to make the workflow idempotent. I was worried about ending up with duplicate tracks and playlists if I ran the workflow twice in the same week.


## Setup

Due to the need to provide authorization for this code to read and write playlists to your account, there are a couple steps to get started. The first step, though, is to clone the repo and install the python dependencies using poetry:

```commandline
git clone git@github.com:EthanRosenthal/discovered-weekly.git && cd discovered-weekly
poetry install
```

Next, create a file called `.env`. You will use this file to store environment variables for running some code locally. See `sample.env` for an example of how to define the environment variables.

### Developer Account

1. Go to https://developer.spotify.com/dashboard/ and log in to your Spotify account.
1. Click "CREATE AN APP" and create one.
1. Record the `CLIENT_ID` and `CLIENT_SECRET` from the main page of your app in `.env`.
1. Click EDIT SETTINGS and add a redirect URI. If you're familiar with OAuth, then you may know what this is and what you would like to fill in here. Otherwise, I would recommend filling in http://localhost:$PORT where $PORT is some port on your machine that's not being used (e.g. not 8888 if you're running jupyter).
1. Add the `REDIRECT_URI` to `.env`.

### Refresh Token

You now need to authorize your Spotify app to be able to read and write private playlists to your Spotify account:

1. Record your `USERNAME` in `.env`.
1. Run `python get_refresh_token.py` and follow the instructions in the terminal. This will walk you through the authentication flow.
1. The final step is to copy the `REFRESH_TOKEN` from the terminal and place this in `.env`. This will make it so that you do not have to do the authentication flow again in the future.

### Playlist IDs

The final environment variables you need are the unique IDs for your Discover Weekly playlist and for the playlist that you will use for storing your Discover Weeklies from all time. You can identify the playlist ID by right-clicking the playlist, then clicking Share -> Copy link to playlist. The link will look like http://open.spotify.com/playlist/$PLAYLIST_ID?x=abc. The playlist ID is evertyhing after `/playlist/` and before `?`. Record both your `DISCOVER_WEEKLY_PLAYLIST_ID` and `ALL_DISCOVERED_PLAYLIST_ID` in `.env`.

## Local Usage

```commandline
python discovered_weekly.py
```

## Automated Usage

Fork this repo. From your fork's page on GitHub, click Settings->Secrets. Fill in all of your environment variables from your `.env` file. The code will run via GitHub Actions every Tuesday at 0 UTC. You can also manually trigger a run by clicking Actions, going to the `discovered-weekly` workflow, and clicking `Run workflow`.

