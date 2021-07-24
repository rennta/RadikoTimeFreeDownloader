##-----------------------------------------------------------------------------------------------------------#
## [ Authentication.py ]
##
## - Radikoの認証処理を行う
##   1. ラジオの終了時間等のデータを取得
##   2. https://radiko.jp/v2/api/auth1 にGETリクエストしてトークンを取得
##   3. https://radiko.jp/v2/api/auth2 にGETリクエストしてトークンを認証
##
## - 参考
##   - https://blog.bluedeer.net/archives/216
##
## - 関数
##   - def getRadioData(self)           # ラジオデータ取得 (戻り値：なし)
##   - def auth1(self)                  # auth1実行 (戻り値：auth1リクエスト結果(header))
##   - def getTokens(self,auth1Header)  # Token抽出 (戻り値：authToken, keyLength, keyOffset,authKey, partialKey) 
##   - def auth2(self,tokens)           # auth2実行 (戻り値：なし)
##
##-----------------------------------------------------------------------------------------------------------#

# [ライブラリ]
import urllib.request                                                                                        # URL利用
import xml.etree.ElementTree                                                                                 # XML解析
import re                                                                                                    # 正規表現
import base64


# [ラジコ認証クラス]
class Authentication:


    #--------------------------------------------------------------------------------------------------------#
    # 関数名 : def __init__(self, a_URL)
    # 機能   : 初期化を行う
    # 引数   : self  インスタンス変数
    #        : a_URL ラジコURL
    # 戻り値 : なし
    #--------------------------------------------------------------------------------------------------------#     
    def __init__(self, a_URL):

        self.URL = a_URL
        self.AUTHKEY_VALUE = "bcd151073c03b352e1ef2fd66c32209da9ca0afa"
        
    #--------------------------------------------------------------------------------------------------------#  


    #--------------------------------------------------------------------------------------------------------#
    # 関数名 : def getRadioData(self):
    # 機能   : ラジオデータを取得する
    # 引数   : self  インスタンス変数
    # 戻り値 : 放送局ID, 開始時間, 終了時間
    #--------------------------------------------------------------------------------------------------------#    
    def getRadioData(self):

        # 放送局ID,開始時刻取得
        stationId = re.search("[A-Z]+",self.URL).group()
        startTime = re.search("[0-9]+",self.URL).group()

        # XMLデータ取得
        radioSchedule = "https://radiko.jp/v3/program/station/weekly/"+stationId+".xml";
        with urllib.request.urlopen(radioSchedule) as response:
            scheduleURL = response.read()

        # XMLデータ抽出
        scheduleXML = xml.etree.ElementTree.fromstring(scheduleURL)

        for data in scheduleXML.iter('prog'):
            finishTime = re.search("\'ft\': \'"+startTime+"\', \'to\': \'[0-9]+\'",str(data.attrib))
            if finishTime != None:
                finishTime = re.search("\'to\': \'[0-9]+\'",finishTime.group())
                finishTime = re.search("[0-9]+",finishTime.group())
                break

        radioData = {
            "stationId" : stationId,
            "startTime" : startTime,
            "finishTime" : finishTime.group()
        }
        return radioData
    
    #--------------------------------------------------------------------------------------------------------# 


    #--------------------------------------------------------------------------------------------------------#
    # 関数名 : def auth1(self)
    # 機能   : auth1処理を行う
    # 引数   : self  インスタンス変数
    # 戻り値 : auth1リクエスト結果(header)
    #--------------------------------------------------------------------------------------------------------#    
    def auth1(self):

        # Auth1 トークン取得処理
        header = {
            'X-Radiko-App': 'pc_html5',
            'X-Radiko-App-Version': '0.0.1',
            'X-Radiko-Device': 'pc',
            'X-Radiko-User': 'dummy_user'
        }
        req_auth1 = urllib.request.Request("https://radiko.jp/v2/api/auth1",headers=header)
        with urllib.request.urlopen(req_auth1) as response:
            print("auth1_ok")
            headers = response.info()

        return headers

    #--------------------------------------------------------------------------------------------------------#


    #--------------------------------------------------------------------------------------------------------#
    # 関数名 : getTokens(self,auth1Header)
    # 機能   : トークンを抽出する
    # 引数   : self         インスタンス変数
    #        : auth1Header  auth1リクエスト結果(header)
    # 戻り値 : authToken, keyLength, keyOffset,authKey, partialKey
    #--------------------------------------------------------------------------------------------------------#  
    def getTokens(self,auth1Header):

        # 要素抽出
        authToken  = auth1Header["x-radiko-authtoken"];
        keyLength  = int(auth1Header["x-radiko-keylength"]);
        keyOffset  = int(auth1Header["x-radiko-keyoffset"]);
        authKey    = self.AUTHKEY_VALUE[keyOffset:keyOffset+keyLength]
        partialKey = str(base64.b64encode(authKey.encode()).decode())

        tokenData = {
            "authToken" : authToken, 
            "keyLength" : keyLength,
            "keyOffset" : keyOffset,
            "authKey" : authKey,
            "partialKey" : partialKey
        }
        return tokenData

    #--------------------------------------------------------------------------------------------------------#


    #--------------------------------------------------------------------------------------------------------#
    # 関数名 : def auth2(self,token)
    # 機能   : auth2処理を行う
    # 引数   : self  インスタンス変数
    # 戻り値 : 開始時間, 終了時間
    #--------------------------------------------------------------------------------------------------------#  
    def auth2(self,tokens):
        header = {
            'X-Radiko-AuthToken': tokens['authToken'],
            'X-Radiko-PartialKey': tokens['partialKey'],
            'X-Radiko-User': 'dummy_user',
            'X-Radiko-Device': 'pc'
        }

        req_auth2  = urllib.request.Request('https://radiko.jp/v2/api/auth2',None,header)
        with urllib.request.urlopen(req_auth2) as response:
            print("auth2_ok")
    
    #--------------------------------------------------------------------------------------------------------#