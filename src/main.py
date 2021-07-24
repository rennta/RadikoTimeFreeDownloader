# -*- coding: utf-8 -*-

##-----------------------------------------------------------------------------------------#
## [ main.py ]
##
##
##------------------------------------------------------------------------------------------#


# [ ライブラリ ]                                                                             # 正規表現
import base64
import sys
import subprocess
import time

# [ メイン関数 ] ----------------------------------------------------------------------------#
# 関数名：def main()
# 機能　：メインの処理を行う
# 引数　：なし
# 戻り値：なし
#-------------------------------------------------------------------------------------------#
def main():

    URL = "https://radiko.jp/#!/ts/IBS/20210721030000"
    URL = "https://radiko.jp/#!/ts/LFR/20210721220000"
    AUTHKEY_VALUE="bcd151073c03b352e1ef2fd66c32209da9ca0afa"
    
    station_id = re.search("[A-Z]+",URL)
    start_time = re.search("[0-9]+",URL)

    radio_schedule = "https://radiko.jp/v3/program/station/weekly/"+station_id.group()+".xml";

    with urllib.request.urlopen(radio_schedule) as response:
        schedule_url = response.read()

    # XML抽出（該当該当ラジオ progデータ）
    schedule_xml = xml.etree.ElementTree.fromstring(schedule_url)
    for data in schedule_xml.iter('prog'):
        finish_time = re.search("\'ft\': \'"+start_time.group()+"\', \'to\': \'[0-9]+\'",str(data.attrib))
        if finish_time != None:
            finish_time = re.search("\'to\': \'[0-9]+\'",finish_time.group())
            finish_time = re.search("[0-9]+",finish_time.group())
            break

    req_header = {
        'X-Radiko-App': 'pc_html5',
        'X-Radiko-App-Version': '0.0.1',
        'X-Radiko-Device': 'pc',
        'X-Radiko-User': 'dummy_user'
    }
    auth1 = urllib.request.Request("https://radiko.jp/v2/api/auth1",headers=req_header)
    with urllib.request.urlopen(auth1) as response:
        print("auth1_ok")
        headers = response.info()
    
    auth_token  = headers["x-radiko-authtoken"];
    key_length  = int(headers["x-radiko-keylength"]);
    key_offset  = int(headers["x-radiko-keyoffset"]);

    replace_auth_key = AUTHKEY_VALUE[key_offset:key_offset+key_length]
    partial_key = str(base64.b64encode(replace_auth_key.encode()).decode())

    send_header = {
        'X-Radiko-AuthToken': auth_token,
        'X-Radiko-PartialKey': partial_key,
        'X-Radiko-User': 'dummy_user',
        'X-Radiko-Device': 'pc'
    }

    auth2  = urllib.request.Request('https://radiko.jp/v2/api/auth2',None,send_header)
    with urllib.request.urlopen(auth2) as response:
        print("auth2_ok")
   
    radio_url = "https://radiko.jp/v2/api/ts/playlist.m3u8?station_id="+station_id.group()+"&l=15&ft="+start_time.group()+"&to="+finish_time.group()   
    cmd = "ffmpeg -loglevel error -fflags +discardcorrupt -headers \"X-Radiko-Authtoken: "+auth_token+"\" -i \""+radio_url+"\" -bsf:a aac_adtstoasc -stats -acodec copy output.m4a"
    #subprocess.run(cmd)
    p=subprocess.run(cmd, stdout=subprocess.PIPE)

    #print("ffmpeg -headers \"X-Radiko-Authtoken: "+auth_token+"\" -i \""+radio_url+"\" -acodec copy ./output.m4a")

    print("station_id     : ",station_id.group())
    print("start_time     : ",start_time.group())
    print("finish_time    : ",finish_time.group())
    print("auth_token     : ",auth_token)
    print("key_length     : ",key_length)
    print("key_offset     : ",key_offset)
    print("partial_key    : ",partial_key)

#--------------------------------------------------------------------------------------------#


# [ 処理実行 ]
main()