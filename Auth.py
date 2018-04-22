#!/usr/bin/env python
# -*- coding:utf-8 -*-

# Tweepyライブラリをインポート
import tweepy
import os
import webbrowser

authfile = os.path.exists('data.dat')
authfile2 = os.path.exists('data2.dat')


class TwitterMgr():
    def __init__(self):
        os.makedirs("./data", exist_ok=True)
        os.makedirs("./data/user", exist_ok=True)
        os.makedirs("./data/cache", exist_ok=True)
        
    def init_Auth(self):
        self.auth = tweepy.OAuthHandler(self.CONSUMER_KEY, self.CONSUMER_SECRET)

    def init_Api(self):
        self.api = tweepy.API(self.auth)

    def savedata(data1, data2):  # トークン取得スキップのために保存
        f = open('data.dat', 'w')
        f.write(data1)
        f.close()
        f = open('data2.dat', 'w')
        f.write(data2)
        f.close()


    def get_Authurl(self):
        print("ファイルが存在しないためトークンを取得します")

        # OAuth認証コードを貰いに行くアドレスを取得する
        redirect_url = auth.get_authorization_url()
        # アドレスを表示し、ブラウザでアクセスして認証用コードを取得してくる。
        print('ここにアクセスしてPINを入手してください: ' + redirect_url)
        webbrowser.open(redirect_url)
        # ブラウザから取得してきた認証用コードを対話モードで入力する。
        # strip()はコピペの際に末尾に改行コードとかスペースが入ったのを消すため。
        verifier = input('PIN>> ').strip()

        # Access TokenとAccess Token Secretを取得してそれぞれオブジェクト
        # として格納しておく。
        auth.get_access_token(verifier)
        ACCESS_TOKEN = auth.access_token
        ACCESS_SECRET = auth.access_token_secret
        savedata(ACCESS_TOKEN, ACCESS_SECRET)  # data1にACCESS_TOKEN、data2にACCESS_SECRET
        return 0


    # トークンが保存されているかチェック
    print("ファイルチェック中...")
    if authfile == True:
        if authfile2 == True:
            f = open('data.dat', 'r')
            ACCESS_TOKEN = f.readline()
            f.close()
            f = open('data2.dat', 'r')
            ACCESS_SECRET = f.readline()
            f.close()
            print("ファイルが存在したため認証をスキップしました。")
            auth.access_token = ACCESS_TOKEN
            auth.access_token_secret = ACCESS_SECRET
        else:
            Gettoken()
    else:
        Gettoken()

# APIインスタンスを作成
api = tweepy.API(auth)

# これだけで、Twitter APIをPythonから操作するための準備は完了。
print('Done!')