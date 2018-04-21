#!/usr/bin/env python
# -*- coding:utf-8 -*-

# Tweepyライブラリをインポート
import tweepy
import os
import webbrowser

# 各種キーをセット
CONSUMER_KEY = '52vTKp6AIVKyBESMyxO0p0y0V'
CONSUMER_SECRET = '57vn9D85XVYIOwzEmyP9JUObNbWjxg06UOGUltqyFpKkiWqeso'
auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)

authfile = os.path.exists('data.dat')
authfile2 = os.path.exists('data2.dat')


class tokenMgr():


    def savedata(data1, data2):  # トークン取得スキップのために保存
        f = open('data.dat', 'w')
        f.write(data1)
        f.close()
        f = open('data2.dat', 'w')
        f.write(data2)
        f.close()


    def Gettoken():
        print("ファイルが存在しないためトークンを取得します")
        # 念のためトークンファイルを削除
        if authfile == True:
            os.remove(data.dat)
        if authfile2 == True:
            os.remove(data2.dat)

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