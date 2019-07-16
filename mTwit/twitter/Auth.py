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


class TwitterMgr:
    """
    DEPRECATED.

    TwitterMgr class provides stateful APIs for auth(oriz|enticat)ing application.
    For usability, use AppGateway class.
    """
    """Test"""

    def __init__(self):
        """
        os.makedirs("./data", exist_ok=True)
        os.makedirs("./data/user", exist_ok=True)
        os.makedirs("./data/cache", exist_ok=True)
        """

        [x.mkdir(exist_ok=True) for x in [DATA_DIRECTORY,
                                          DATA_DIRECTORY / "user", DATA_DIRECTORY / "cache"]]

        self.ACCESS_TOKEN: str = ""
        self.ACCESS_SECRET: str = ""
        self.CONSUMER_KEY: str = ""
        self.CONSUMER_SECRET: str = ""

    def init_auth(self, consumer_key: str, consumer_secret: str):  # GUI
        self.CONSUMER_KEY = consumer_key
        self.CONSUMER_SECRET = consumer_secret
        self.auth = tweepy.OAuthHandler(
            self.CONSUMER_KEY, self.CONSUMER_SECRET)
        return self.auth

    def init_api(self):
        self.api = tweepy.API(self.auth)
        return self.api

    def set_accesstoken(self, token, secret):  # GUI
        self.ACCESS_TOKEN = token
        self.ACCESS_SECRET = secret
        self.auth.set_access_token(token, secret)

    def open_twitterauth(self):
        try:
            redirect_url = self.auth.get_authorization_url()
        except TweepError:
            self.CONSUMER_KEY = ""
            self.CONSUMER_SECRET = ""
            return False
        if not redirect_url:
            self.CONSUMER_KEY = ""
            self.CONSUMER_SECRET = ""
            return False
        else:
            webbrowser.open(redirect_url)
            return True

    def verify_twitter(self, verifier):  # GUI
        try:
            self.auth.get_access_token(verifier)
        except TweepError:
            raise VerifyError

        self.ACCESS_TOKEN = self.auth.access_token
        self.ACCESS_SECRET = self.auth.access_token_secret
        return True
