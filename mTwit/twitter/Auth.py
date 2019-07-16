#!/usr/bin/env py -3-32
# -*- coding:utf-8 -*-

# Tweepyライブラリをインポート
import webbrowser
import tweepy
import pathlib
from mTwit.exceptions.twitter import *
from tweepy.error import TweepError

DATA_DIRECTORY = pathlib.Path("./data")

"""Tweepy Settings Class"""


class AppGateway:

    def __init__(self, consumer_key, consumer_secret):
        self._auth = tweepy.OAuthHandler(consumer_key, consumer_secret)

    @property
    def consumer_key(self) -> str:
        return self._auth.consumer_key

    @property
    def consumer_secret(self) -> str:
        return self._auth.consumer_secret

    @property
    def auth_handler(self) -> tweepy.AppAuthHandler:
        return self._auth

    @property
    def authorization_url(self) -> str:
        # signin_with_twitter=True for oauth/authenticate (require app settings)
        # signin_with_twitter=False for oauth/authorize (for desktop apps)
        return self._auth.get_authorization_url()

    def open_auth_page(self) -> bool:
        """
        DEPRECATED. This feature will be moved to UI module.

        Open authorization page in default web browser.
        If succeeded, returns True, else False.
        """
        auth_url = self.authorization_url

        if not auth_url:
            return False

        webbrowser.open(auth_url)
        return True

    def verify(self, verifier: str) -> tweepy.API:
        tokens = self._auth.get_access_token(verifier)
        return self.login(tokens[0], tokens[1])

    def login(self, access_token: str, access_token_secret: str) -> tweepy.API:
        auth_handler = self._auth
        auth_handler.set_access_token(access_token, access_token_secret)
        return tweepy.API(auth_handler)
