# RadikoTimeFreeDownloader

Radikoのタイムフリーをダウンロードするためのプログラムです。

## 概要
    1. ラジオの選択（現在はCUI）
    2. Radikoの認証を行う
        ・ラジオの終了時間等のデータを取得
        ・https://radiko.jp/v2/api/auth1 にGETリクエストしてトークンを取得
        ・https://radiko.jp/v2/api/auth2 にGETリクエストしてトークンを認証

    3. ffmpegで音声を変換保存


## 使用ライブラリ，ソフト
    =============================================
    Pythonライブラリ
    =============================================
    ・datetime
    ・dateutil.relativedelta
    ・relativedelta
    ・calendar
    ・base64
    ・urllib.request
    ・xml.etree.ElementTree
    ・re
    ・subprocess
    ・os


    =============================================
    必須ソフト
    =============================================
    ffmpeg

     =============================================
    あると便利ソフト
    ==============================================
    SoftEther VPN

## 環境
    Windows 10 Home 20H2
    Python 3.7.0

## 参考
https://blog.bluedeer.net/archives/216


