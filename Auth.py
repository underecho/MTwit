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

  def init_api(self):
    self.api = tweepy.API(self.auth)

  def set_accesstoken(self, token, secret):  # GUI
    self.ACCESS_TOKEN = token
    self.ACCESS_SECRET = secret
    self.auth.set_access_token(token, secret)

  def open_twitterauth(self):
    try:
      redirect_url = self.auth.get_authorization_url()
    except TweepError:
      
      pass
    webbrowser.open(redirect_url)

  def verify_twitter(self, verifier):  # GUI
    try:
      self.auth.get_access_token(verifier)
    except TweepError:
      return False
    self.ACCESS_TOKEN = self.auth.access_token
    self.ACCESS_SECRET = self.auth.access_token_secret
    return True

class Cryptor:

  def get_uuid(self):
    x = subprocess.check_output('wmic csproduct get UUID')
    x = str(x).split()
    x = x[1].replace("b'", "")\
            .replace("'", "")\
            .replace("-", "")\
            .replace("\\r", "")\
            .replace("\\n", "")
    return(x)

  def doEncryption_data(self, raw_data, key, iv):
    # 前準備
    raw_base64 = base64.b64encode(raw_data)
    while len(raw_base64) % 16 != 0:
      raw_base64 += "_"
    key_32bit = hashlib.sha256(key).digest()
    iv = hashlib.md5(iv).digest()
    # 暗号化とデータの文字列化
    crypt = AES.new(key_32bit, AES.MODE_CBC, iv)
    encrypted_data = crypt.encrypt(raw_base64)
    encrypted_data_base64 = base64.b64encode(encrypted_data)
    return encrypted_data_base64

  def doDecryption_data(self, encrypted_data_base64, key, iv):
    # 前準備
    encrypted_data = base64.b64decode(encrypted_data_base64)
    key_32bit = hashlib.sha256(key).digest()
    iv = hashlib.md5(iv).digest()
    crypt = AES.new(key_32bit, AES.MODE_CBC, iv)
    # 復号と後処理
    decrypted_data = crypt.decrypt(encrypted_data)
    decrypted_data = decrypted_data.split("_")[0]
    raw_data = base64.b64decode(decrypted_data)
    return raw_data

