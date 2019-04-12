#!/usr/bin/env py -3-32
# -*- coding:utf-8 -*-

# Tweepyライブラリをインポート
import os
import webbrowser
import subprocess
import hashlib
import base64
import tweepy
from Crypto.Cipher import AES
from tweepy.error import TweepError

"""Tweepy Settings Class"""
class TwitterMgr:
  """Auth, User Token Manager"""
  def __init__(self, CK = None, CS = None):
    """Required CK CS"""
    
    os.makedirs("./data", exist_ok=True)
    os.makedirs("./data/user", exist_ok=True)
    os.makedirs("./data/cache", exist_ok=True)
    self.ACCESS_TOKEN = None
    self.ACCESS_SECRET = None
    if CS and CK:
      self.CONSUMER_KEY = CK
      self.CONSUMER_SECRET = CS
      self.auth = tweepy.OAuthHandler(self.CONSUMER_KEY, self.CONSUMER_SECRET)
      self.api = tweepy.API(self.auth)
    else:
      print("Failed make auth instance")
      self.auth = None
      self.api = None

  """
  def set_accesstoken(self, token, secret):  # GUI
    self.ACCESS_TOKEN = token
    self.ACCESS_SECRET = secret
    self.auth.set_access_token(token, secret)
  """

  def open_twitterauth(self):
    try:
      redirect_url = self.auth.get_authorization_url()
    except TweepError:
      pass
    webbrowser.open(redirect_url) # webブラウザを開き認証コードを入手する

  def verify_twitter(self, verifier):  # GUI
    try:
      self.auth.get_access_token(verifier)
    except TweepError:
      return False
    self.ACCESS_TOKEN = self.auth.access_token
    self.ACCESS_SECRET = self.auth.access_token_secret
    return True

