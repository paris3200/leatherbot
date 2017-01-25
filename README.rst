# leatherbot


A simple bot to help moderate a reddit subreddit.

## Usage
    

    $leatherbot

## Installation

Leatherbot makes use of PRAW.  In order for leatherbot to work you must configure PRAW.  

Configure PRAW:  https://praw.readthedocs.io/en/latest/getting_started/configuration/prawini.html

## Configure leatherbot 

The config settings can be found in leatherbot/leatherbot.py

### Edit leatherbot/leatherbot.py ###

    """
    Config Settings
    sub: The subreddit being moded.
    bot: Name of the bot user
    grace_period: Time in minutes to delete post that don't follow the rules
    """
    sub = "leathertesting"
    bot = "leathercraft_mod"
    grace_period = 60

Run Setup

    $python setup.py


