#!/usr/bin/env py -3-32
# -*- coding:utf-8 -*-

# Tweepyライブラリをインポート
import os
import webbrowser
import subprocess
import hashlib
import base64
import tweepy
from mTwit.Error import *
from Crypto.Cipher import AES
from tweepy.error import TweepError

"""Tweepy Settings Class"""
class TwitterMgr:
  """Test"""
  def __init__(self):
    os.makedirs("./data", exist_ok=True)
    os.makedirs("./data/user", exist_ok=True)
    os.makedirs("./data/cache", exist_ok=True)
    self.ACCESS_TOKEN = None
    self.ACCESS_SECRET = None
    self.CONSUMER_KEY = None
    self.CONSUMER_SECRET = None

  def init_auth(self, consumer_key, consumer_secret):  # GUI
    self.CONSUMER_KEY = consumer_key
    self.CONSUMER_SECRET = consumer_secret
    self.auth = tweepy.OAuthHandler(self.CONSUMER_KEY, self.CONSUMER_SECRET)
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
      self.CONSUMER_KEY = None
      self.CONSUMER_SECRET = None
      return False
    if not redirect_url:
      self.CONSUMER_KEY = None
      self.CONSUMER_SECRET = None
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

