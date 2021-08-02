##-----------------------------------------------------------------------------------------------------------#
## [ Radiko.py ]
## 
##  - 指定ラジオのダウンロードの一連の動作を行う
##
##  - 関数
##    - def run(self):      # Radikoのタイムフリーダウンロード動作を行う（戻り値：なし）
##
##-----------------------------------------------------------------------------------------------------------#

# [ライブラリ]
from Authentication import Authentication
from TimeFreeDownloader import TimeFreeDownloader
from CUI import CUI
import os
import subprocess

# [ラジコクラス]
class Radiko:


    #--------------------------------------------------------------------------------------------------------#
    # 関数名 : def run(self)
    # 機能   : Radikoのタイムフリーダウンロード動作を行う
    # 引数   : self  インスタンス変数
    # 戻り値 : なし
    #--------------------------------------------------------------------------------------------------------#  
    def run(self):
        
        UI = CUI()
        count       = UI.selectRadio()
        radioInfo   = UI.getURL(int(count))

        if(count == 1):
            Auth        = Authentication(radioInfo[0])
            radioData   = Auth.getRadioData()
            auth1Header = Auth.auth1()
            tokens      = Auth.getTokens(auth1Header)
            Auth.auth2(tokens)
    
            f = open('../data/saveURL.txt', 'r',encoding="utf-8")
            datalist = f.readlines()
            saveURL = datalist[int(count)-1].rstrip(os.linesep)+radioInfo[1]+"_"+radioInfo[2].strftime("%Y%m%d")+".m4a"

            TFD = TimeFreeDownloader()
            TFD.setup(radioData,tokens)
            TFD.download(saveURL)

        if(count == 2):
            stationCount = UI.selectStation()
            SND_stationID = "FMGIFU" if stationCount == 1 else "FMGUNMA"
            radioURL    = "https://radiko.jp/#!/ts/"+SND_stationID+"/"+radioInfo[2].strftime("%Y%m%d")+"200000"
            Auth         = Authentication(radioURL)
            radioData    = Auth.getRadioData()
            auth1Header  = Auth.auth1()
            tokens       = Auth.getTokens(auth1Header)
            Auth.auth2(tokens)

            saveURL = "../temp/output1.m4a"
            TFD = TimeFreeDownloader()
            TFD.setup(radioData,tokens)
            TFD.download(saveURL)

            radioURL1    = "https://radiko.jp/#!/ts/"+SND_stationID+"/"+radioInfo[2].strftime("%Y%m%d")+"210000"
            Auth         = Authentication(radioURL1)
            radioData    = Auth.getRadioData()
            auth1Header  = Auth.auth1()
            tokens       = Auth.getTokens(auth1Header)
            Auth.auth2(tokens)
    
            saveURL = "../temp/output2.m4a"
            TFD = TimeFreeDownloader()
            TFD.setup(radioData,tokens)
            TFD.download(saveURL)
            
            f = open('../data/saveURL.txt', 'r',encoding="utf-8")
            datalist = f.readlines()
            
            saveURL = datalist[int(count)-1].rstrip(os.linesep)+radioInfo[1]+"_"+radioInfo[2].strftime("%Y%m%d")
            print(saveURL)
            subprocess.run("ffmpeg -loglevel error -f concat -i ../temp/list.txt -c copy "+saveURL+".m4a", stdout=subprocess.PIPE)
            os.remove("../temp/output1.m4a")
            os.remove("../temp/output2.m4a")


    #--------------------------------------------------------------------------------------------------------# 

        

