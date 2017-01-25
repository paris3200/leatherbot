leatherbot
==========

.. image:: https://img.shields.io/pypi/v/leatherbot.svg
    :target: https://pypi.python.org/pypi/leatherbot
    :alt: Latest PyPI version

.. image:: https://travis-ci.org/borntyping/cookiecutter-pypackage-minimal.png
   :target: https://travis-ci.org/borntyping/cookiecutter-pypackage-minimal
   :alt: Latest Travis CI build status

A simple bot to help moderate a reddit subreddit.

Usage
-----

    $leatherbot

Installation
------------

Configure PRAW:  https://praw.readthedocs.io/en/latest/getting_started/configuration/prawini.html

Configure leatherbot

    Edit leatherbot/leatherbot.py

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



Requirements
^^^^^^^^^^^^

Compatibility
-------------

Licence
-------

Authors
-------

`leatherbot` was written by `Jason Paris <paris3200@gmail.com>`_.
