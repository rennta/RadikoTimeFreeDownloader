##-----------------------------------------------------------------------------------------------------------#
## [ CUI.py ]
##
## - コマンドの入力でアプリケーションの操作を行う
##
## - 関数
##   - def messageInfo(self)        # リファレンスを表示する (戻り値：選択番号)
##   - def getURL(self)             # URLを取得する　(戻り値：ラジオURL,ラジオ情報(名前))
##
##-----------------------------------------------------------------------------------------------------------#


# [ライブラリ] 
from datetime import datetime
from dateutil.relativedelta import relativedelta
import calendar

# [CUIクラス]
class CUI:

    #--------------------------------------------------------------------------------------------------------#
    # 関数名 : def messageInfo(self):
    # 機能   : リファレンスを表示する
    # 引数   : self  インスタンス変数
    # 戻り値 : 選択番号
    #--------------------------------------------------------------------------------------------------------#    
    def messageInfo(self):
        
        # 表示内容
        info = "\n#\n"\
                 "# [ Radiko Time Free Download Script ]\n"\
                 "# \n"\
                 "# - Radio List\n"\
                 "#   - CreepyNutsのオールナイトニッポン0（ZERO）\n"\
                 "#     ---> 1\n"\
                 "# \n"\
                 "# - 有吉弘行のSUNDAY NIGHT DREAMER\n"\
                 "#     ---> 2\n"\
                 "# \n"\
        
        print(info)

        return int(input("[ Please number ] : "))

    #--------------------------------------------------------------------------------------------------------#  


    #--------------------------------------------------------------------------------------------------------#
    # 関数名 : def getURL(self ,count)
    # 機能   : URLを取得する
    # 引数   : self  インスタンス変数
    # 戻り値 : ラジオURL,ラジオ情報(名前)
    #--------------------------------------------------------------------------------------------------------#    
    def getURL(self ,count):

        target_date = datetime.today()

        if(count == 1):
            day       = target_date - relativedelta(weeks=1, weekday=calendar.WEDNESDAY)
            radioURL  = "https://radiko.jp/#!/ts/IBS/"+day.strftime("%Y%m%d")+"030000"
            radioName = "CreepyNutsのオールナイトニッポン0（ZERO）"

        elif(count == 2):
            day    = target_date - relativedelta(weeks=1, weekday=calendar.SUNDAY)
            radioURL  = "https://radiko.jp/#!/ts/FMGIFU/"+day.strftime("%Y%m%d")+"200000"
            radioName = "有吉弘行のSUNDAY_NIGHT_DREAMER"

        print("[   radio URL   ] :",radioURL)

        return radioURL,radioName,day

    #--------------------------------------------------------------------------------------------------------#  