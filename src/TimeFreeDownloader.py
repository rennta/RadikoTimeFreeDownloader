##-----------------------------------------------------------------------------------------------------------#
## [ TimeFreeDownloader.py ]
##
## - ffmpegを利用して該当ラジオのタイムフリーをダウンロード
##
## - 関数
##   - def setup(self, auth1Header, tokens) # ダウンロードに必要なデータの準備を行う(戻り値:なし)   
##   - def download(self, saveURL)          # タイムフリーのダウンロードを行う(戻り値:なし)
##
##-----------------------------------------------------------------------------------------------------------#

# [ライブラリ]
import subprocess
from Authentication import Authentication

# [ラジコタイムフリーダウンロードクラス]
class TimeFreeDownloader:


    #--------------------------------------------------------------------------------------------------------#
    # 関数名 : def __init__(self, a_URL)
    # 機能   : 初期化する
    # 引数   : self  インスタンス変数
    # 戻り値 : なし
    #--------------------------------------------------------------------------------------------------------#     
    def __init__(self):

        self.stationId  = ""
        self.startTime  = ""
        self.finishTime = ""
        self.authToken  = ""
        
    #--------------------------------------------------------------------------------------------------------#  


    #--------------------------------------------------------------------------------------------------------#
    # 関数名 : setup(self, auth1Header, tokens)
    # 機能   : ダウンロードに必要なデータの準備を行う
    # 引数   : self        インスタンス変数
    #        : auth1Header auth1リクエスト結果(header)
    #        : tokens      (authToken, keyLength, keyOffset,authKey, partialKey)
    # 戻り値 : なし
    #--------------------------------------------------------------------------------------------------------#  
    def setup(self, radioData, tokens):

        tokenData       = list(tokens.values())
        radioInfoData   = list(radioData.values())
        self.stationId  = radioInfoData[0]
        self.startTime  = radioInfoData[1]
        self.finishTime = radioInfoData[2]
        self.authToken  = tokenData[0]

        print("self.stationId:"+self.stationId)
        print("self.startTime:"+self.startTime)
        print("self.finishTime:"+self.finishTime)
        print("self.authToken:"+self.authToken)
    
    #--------------------------------------------------------------------------------------------------------#  


    #--------------------------------------------------------------------------------------------------------#
    # 関数名 : def download(self, saveURL)
    # 機能   : タイムフリーのダウンロードを行う
    # 引数   : self    インスタンス変数
    #        : saveURL 保存先ファイル
    # 戻り値 : なし
    #--------------------------------------------------------------------------------------------------------#     
    def download(self, saveURL):

        radioURL = "https://radiko.jp/v2/api/ts/playlist.m3u8?station_id="\
                    +self.stationId+"&l=15&ft="\
                    +self.startTime+"&to="\
                    +self.finishTime

        print(radioURL)
        ffmpegOption = " -loglevel error"\
                       " -fflags +discardcorrupt"\
                       " -headers \"X-Radiko-Authtoken: "+self.authToken+"\""\
                       " -i \""+radioURL+"\""\
                       " -bsf:a aac_adtstoasc"\
                       " -stats"\
                       " -acodec copy "+saveURL

        cmd = "ffmpeg"+ffmpegOption
        subprocess.run(cmd, stdout=subprocess.PIPE)

    #--------------------------------------------------------------------------------------------------------# 

Authentication = Authentication("https://radiko.jp/#!/ts/IBS/20210721030000")
radioData = Authentication.getRadioData()
auth1Header = Authentication.auth1()
tokens = Authentication.getTokens(auth1Header)
Authentication.auth2(tokens)
TimeFreeDownloader = TimeFreeDownloader()
TimeFreeDownloader.setup(radioData,tokens)
TimeFreeDownloader.download("./output.m4a")