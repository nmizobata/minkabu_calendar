# ---
# jupyter:
#   jupytext:
#     formats: ipynb,py:light
#     text_representation:
#       extension: .py
#       format_name: light
#       format_version: '1.5'
#       jupytext_version: 1.16.4
#   kernelspec:
#     display_name: Python 3 (ipykernel)
#     language: python
#     name: python3
# ---

# +
# MT4 Python スクリプト用ライブラリ
# ver1.0 20240706 class Mt4, ChartFileを追加

# +
# このライブラリを使う時はmainに以下を挿入
# import sys
# sys.path.append('..')    # pythonモジュール検索パスに親ディレクトリを追加。(シェル環境では削除)
# #pprint.pprint(sys.path)
# from MT4_common_lib.mt4_lib import get_folderpath,get_currency_timeframe, reset_timeframe

# +
# Mt4クラス
# 【Property】
# Mt4.name:       Alpari MT4, Titan_2 MT4等
# Mt4.TATE:        チャートウィンドウの縦サイズ
# Mt4.YOKO:        チャートウィンドウの横サイズ
# Mt4.datafolder:  Chartsetが保存されているフォルダパス
# Mt4.boxfolder:  6枚チャートのオリジナルが保存されているフォルダパス。(datafolderにはシンボリックリンクが保存されている)
# Mt4.currency_list: サポートされている通貨ペアのリスト
# 【Method】
# get_chartsets(): 対象のMT4が持つChartsetオブジェクトのリストを返す
# get_chartsets_namelist(): 対象のMT4が持つChartsetのフォルダ名のリストを返す
# get_realchartsets(): 対象のMT4が持つ実体チャートファイルのChartsetオブジェクトのリストを返す
class Mt4:
    def __init__(self, name):
        self.name=name
        self.TATE, self.YOKO, self.datafolder, self.boxfolder, self.supported_currency_list = self.__get_profile_from_MT4_info_xlsx(self.name)

    def __get_profile_from_MT4_info_xlsx(self,mt4_name):
        # import pandas as pd
        # mt4=pd.read_excel("\\MT4_common_lib\\mt4_info.xlsx")
        # mt4_TATE = mt4.loc[mt4["MT4_name"]==mt4_name]["MT4_TATE"].iloc[0]
        # mt4_YOKO = mt4.loc[mt4["MT4_name"]==mt4_name]["MT4_YOKO"].iloc[0]
        # mt4_datafolder = mt4.loc[mt4["MT4_name"]==mt4_name]["datafolder"].iloc[0]
        # mt4_boxfolder  = mt4.loc[mt4["MT4_name"]==mt4_name]["boxfolder"].iloc[0]
        # currencies_list=["JPN225","EURGBP","EURAUD","GBPAUD","EURNZD","GBPNZD","AUDNZD","EURUSD","GBPUSD","AUDUSD","NZDUSD",
        #        "EURCAD","GBPCAD","AUDCAD","NZDCAD","USDCAD","EURCHF","GBPCHF","AUDCHF","NZDCHF","USDCHF","CADCHF",
        #        "EURJPY","GBPJPY","AUDJPY","NZDJPY","USDJPY","CADJPY","CHFJPY","XAUUSD"]
        # for currency in currencies_list:
        #     # print("{}: {}".format(currency,mt4.loc[mt4["MT4_name"]==mt4_name][currency].values))
        #     if mt4.loc[mt4["MT4_name"]==mt4_name][currency].values==[0]:  # サポートしていない通貨をリストから削除
        #         # print("Erase!! {}".format(currency))
        #         currencies_list.remove(currency)
        import json
        import os
        with open(os.path.dirname(__file__)+"\\system_info.json","r",encoding="utf-8_sig") as f:
            system_dic = json.load(f)
        mt4_TATE = system_dic["TATE_MAX"]
        mt4_YOKO = system_dic["YOKO_MAX"]
        mt4_datafolder = system_dic[mt4_name]["datafolder"]
        mt4_boxfolder  = system_dic[mt4_name]["boxfolder"]
        currencies_list = system_dic[mt4_name]["supported currencypair"]
        return int(mt4_TATE), int(mt4_YOKO), mt4_datafolder,mt4_boxfolder,currencies_list

    def get_chartsets(self):
        return [ChartSet(self.datafolder+'/'+chartset) for chartset in self.__get_all_folders(self.datafolder)
              if self.__check_chartsettype(self.datafolder+"/"+chartset)!="general folder"]

    def get_chartsets_namelist(self):
        return [chartset for chartset in self.__get_all_folders(self.datafolder)
              if self.__check_chartsettype(self.datafolder+"/"+chartset)!="general folder"]

    def get_realchartsets(self):
        return [ChartSet(self.datafolder+'/'+chartset) for chartset in self.__get_all_folders(self.datafolder)
                if self.__check_chartsettype(self.datafolder+"/"+chartset)=="realfile"]

################### chartset functions ######################

    # ChartsetのChartファイルのタイプを返す。
    # Input
    # chartset_folderpath: Chartsetのフォルダパス
    # Output
    # "realfile": 実体, "symboliclink":シンボリックリンク, "general folder":Chartsetではない通常のフォルダ
    def __check_chartsettype(self,chartset_folderpath):
        import os
        from glob import glob

        filepath_list=glob(chartset_folderpath+'/*.chr')
        if len(filepath_list)==0: return "general folder"
        chartsettype = "realfile"
        for filepath in filepath_list:
            if self.__check_filetype(filepath) == "symboliclink":
                chartsettype = "symboliclink"
        return chartsettype


    # 指定フォルダ以下のすべてのフォルダを取得
    def __get_all_folders(self,path):
        import os

        files = os.listdir(path)
        dir = [f for f in files if os.path.isdir(os.path.join(path, f))]
        return dir

    def __check_filetype(self,path):
        import os
        return "symboliclink" if os.path.islink(path) else "file" if os.path.isfile(path) else "folder"


# +
# Chartsetのクラス
class ChartSet:
    def __init__(self,path):
        import os
        self.path = path
        self.name = os.path.basename(path)
        self.filetype = self.__check_chartsettype(self.path)
        if self.filetype == "general folder": print("!!Error {}はChartsetではありません".format(self.path))
        self.layouttype = self.get_layouttype()

    def get_layouttype(self):
        if self.__is_layouttype_6charts(self.path)==True: return "Layout_6charts"
        if self.__is_layouttype_16watch_charts(self.path)==True: return "Layout_16watch_charts"
        if self.__is_layouttype_07cross_charts(self.path)==True: return "Layout_07cross_charts"
        if self.__is_layouttype_14cross_charts(self.path)==True: return "Layout_14cross_charts"
        if self.__is_layouttype_21cross_charts(self.path)==True: return "Layout_21cross_charts"
        if self.__is_layouttype_28cross_charts(self.path)==True: return "Layout_28cross_charts"
        if self.__is_layouttype_35cross_charts(self.path)==True: return "Layout_35cross_charts"
        return "Layout_notype"

    def __str__(self):
        return "{}( class:ChartSet, layouttype:{}, filetype:{})".format(self.name,self.layouttype,self.filetype)
    # # ChartsetのChartファイルのタイプを返す。
    # # Input
    # # chartset_folderpath: Chartsetのフォルダパス
    # # Output
    # # "realfile": 実体, "symboliclink":シンボリックリンク, "general folder":Chartsetではない通常のフォルダ
    # def _check_chartsettype(self,chartset_folderpath):
    #     import os
    #     from glob import glob

    #     filepath_list=glob(chartset_folderpath+'/*.chr')
    #     if len(filepath_list)==0: return "general folder"
    #     chartsettype = "realfile"
    #     for filepath in filepath_list:
    #         if _check_filetype(filepath) == "symboliclink":
    #             chartsettype = "symboliclink"
    #     return chartsettype

    # def _check_filetype(self,path):
    #     import os
    #     return "symboliclink" if os.path.islink(path) else "file" if os.path.isfile(path) else "folder"

################### chartset functions ######################
    def __get_chartsets(self):
        # chartsets_temp = []
        # for item in get_all_folders(self.datafolder):
        #     chartsetfolderpath = self.datafolder+"/"+item
        #     if _check_chartsettype(chartsetfolderpath)!="general folder":
        #         chartsets_temp.append(item)
        return [chartset for chartset in self.__get_all_folders(self.datafolder)
              if self.__check_chartsettype(self.datafolder+"/"+chartset)!="general folder"]

    def __get_realchartsets(self):
        return [chartset for chartset in self.__get_all_folders(self.datafolder)
                if self.__check_chartsettype(self.datafolder+"/"+chartset)=="realfile"]

    # ChartsetのChartファイルのタイプを返す。
    # Input
    # chartset_folderpath: Chartsetのフォルダパス
    # Output
    # "realfile": 実体, "symboliclink":シンボリックリンク, "general folder":Chartsetではない通常のフォルダ
    def __check_chartsettype(self,chartset_folderpath):
        import os
        from glob import glob

        filepath_list=glob(chartset_folderpath+'/*.chr')
        if len(filepath_list)==0: return "general folder"
        chartsettype = "realfile"
        for filepath in filepath_list:
            if self.__check_filetype(filepath) == "symboliclink":
                chartsettype = "symboliclink"
        return chartsettype

    # 指定フォルダ以下のすべてのフォルダを取得
    def __get_all_folders(self,path):
        import os

        files = os.listdir(path)
        dir = [f for f in files if os.path.isdir(os.path.join(path, f))]
        return dir

    def __check_filetype(self,path):
        import os
        return "symboliclink" if os.path.islink(path) else "file" if os.path.isfile(path) else "folder"

    # Layout typeが6枚チャートか判定
    # 現時点はチャートの数＝6であるか、で判定
    def __is_layouttype_6charts(self,chartset_folderpath):
        from glob import glob

        chart_list = glob(chartset_folderpath + '/*.chr')
        if len(chart_list) != 6: return False
        return True

    # Layout typeが16枚監視チャートか判定
    # 現時点はチャートの数＝16または17であるか、で判定
    def __is_layouttype_16watch_charts(self,chartset_folderpath):
        from glob import glob

        chart_list = glob(chartset_folderpath + '/*.chr')
        if (len(chart_list) != 17)&(len(chart_list) !=16): return False
        return True

    # Layout typeが07枚クロスチャートか判定
    # 現時点はチャートの数＝7であるか、で判定
    def __is_layouttype_07cross_charts(self,chartset_folderpath):
        from glob import glob

        chart_list = glob(chartset_folderpath + '/*.chr')
        if len(chart_list) != 7: return False
        return True

    # Layout typeが14枚クロスチャートか判定
    # 現時点はチャートの数＝14であるか、で判定
    def __is_layouttype_14cross_charts(self,chartset_folderpath):
        from glob import glob

        chart_list = glob(chartset_folderpath + '/*.chr')
        if len(chart_list) != 14: return False
        return True

    # Layout typeが21枚クロスチャートか判定
    # 現時点はチャートの数＝21であるか、で判定
    def __is_layouttype_21cross_charts(self,chartset_folderpath):
        from glob import glob

        chart_list = glob(chartset_folderpath + '/*.chr')
        if len(chart_list) != 21: return False
        return True

    # Layout typeが28枚クロスチャートか判定
    # 現時点はチャートの数＝28であるか、で判定
    def __is_layouttype_28cross_charts(self,chartset_folderpath):
        from glob import glob

        chart_list = glob(chartset_folderpath + '/*.chr')
        if len(chart_list) != 28: return False
        return True

    # Layout typeが35枚クロスチャートか判定
    # 現時点はチャートの数＝35であるか、で判定
    def __is_layouttype_35cross_charts(self,chartset_folderpath):
        from glob import glob

        chart_list = glob(chartset_folderpath + '/*.chr')
        if len(chart_list) != 35: return False
        return True


# -

# ChartFile(.chrファイル)のクラス
# <Property>
# ChartFile.path:         .chrのパス(ファイル名を含む)
# ChartFile.currencyname: .chrの通貨ペア名
# ChartFile.symbol:       .chrのシンボル名(通貨ペア名+取引会社固有のサフィックス)
# ChartFile.timeframe:    .chrの時間枠
# CharFile.filetype:      "symboliclink" or "file" or "folder"
# <method>
# ChartFile.copy(コピー先フォルダのパス): .chrファイルをコピー。ファイル名はもとのファイル名を使用。コピー先のChartFileクラスを返す
# ChartFile.linkcopy(コピー先フォルダのパス): .chrファイルをシンボリックリンクコピー。ファイル名は元のファイル名を使用。コピー先のChartFileクラスを返す
# ChartFile.move(移動先フォルダのパス): .chrファイルを移動。移動先のChartFileクラスを返す
# ChartFile.rename(新ファイル名): .chrファイルの名前を変更。パスは含めないこと
# ChartFile.remove(): .chrファイルを削除。ChartFileインスタンス変数は削除されないので、別途delコマンドでインスタンスを削除のこと
class ChartFile:
    def __init__(self,path):
        import os
        self.path = path
        self.currencyname, self.symbol, self.timeframe = self.__get_currency_symbol_timeframe(self.path)
        self.filetype = "symboliclink" if os.path.islink(path) else "file" if os.path.isfile(path) else "folder"

    def __get_currency_symbol_timeframe(self,path):
        # pathが不適でファイルオープンエラーが発生した場合の処理を後日追加
        f = open(path,'r',encoding='shift_jis')
        datalist = f.readlines()
        timeframe_name_dict = {'15':'M30','30':'M30','60':'H1','240':'H4','1440':'D1','10080':'W1','43200':'MN'}
        lines = 0
        for data in datalist:
            lines=lines+1
            if data[:7]=='symbol=':
                currency=data[7:13].rstrip('\n')
                symbol  =data[7:].rstrip('\n')
            if (data[:7]=='period=') & (lines<10):
                timeframe = timeframe_name_dict[data[7:].rstrip('\n')]
        f.close()
        return currency,symbol,timeframe

    def __str__(self):
        return "ChartFile:{} - {}, FileType:{}, Path:{}".format(self.currencyname,self.timeframe,self.filetype,self.path)

    def copy(self,dst_path):
        import shutil
        import os
        if self.__check_path(dst_path)==False: return False

        dst_path = dst_path+'\\'+os.path.basename(self.path)
        shutil.copy2(self.path,dst_path)
        return ChartFile(dst_path)

    def linkcopy(self,dst_path):
        import shutil
        import os
        if self.__check_path(dst_path)==False: return False

        dst_path = dst_path+'\\'+os.path.basename(self.path)
        os.symlink(self.path,dst_path)
        return ChartFile(dst_path)

    def move(self,dst_path):
        import os
        import shutil
        if self.__check_path(dst_path)==False: return False

        dst_path = dst_path+'\\'+os.path.basename(self.path)
        shutil.move(self.path,dst_path)
        self.path = dst_path
        return dst_path

    def rename(self,new_name):
        import os
        if '\\' in new_name:
            print("ERROR: パスは含めないでください")
        new_path_name = os.path.dirname(self.path)+'\\'+new_name
        os.rename(self.path, new_path_name)
        self.path = new_path_name
        return new_path_name

    def remove(self):
        # ファイルは削除されるがChartFileインスタンスは削除されないため注意。(外部でdel インスタンスを行う必要がある)
        import os
        os.remove(self.path)

    def __check_path(self,_path):
        import os
        if os.path.isdir(_path)==False:
            print("ERROR: コピー先のフォルダが無いか、ファイル名が入っています")
            return False
        if os.path.isfile(_path+'\\'+os.path.basename(self.path)):
            print("ERROR: すでに同名のファイルが存在します")
            return False
        return True


# +
# MT4 データフォルダのパス
# mt4_name: Boxデータ: FXTF/FXTF_2/Alpari/Alpari_2 in Box, MT4profile: FXTF/FXTF_2/Alpari/Alpari_2 MT4
def get_folderpath(mt4_name):
    import os
#    print('mt4_name in get_folderpath:{}'.format(mt4_name))
    folderpath = 'None'

    # FXTF MT4の中に[test]名で作られたチャートセット
    if mt4_name=='test':
        folderpath = r'C:\Users\blues\AppData\Roaming\MetaQuotes\Terminal\F1DD1D6E7C4A311D1B1CA0D34E33291D\profiles'
        currency_folder_list=['test']

    if mt4_name=='Alpari in Box':
#         folderpath = r'C:\Users\blues\Box\Documents\★FX\Alpari_MT4'
        folderpath = r'D:\FX\★FX_chartfile\Alpari_MT4'

    if mt4_name=='Alpari_2 in Box':
#         folderpath = r'C:\Users\blues\Box\Documents\★FX\Alpari_MT4_2'
        folderpath = r'D:\FX\★FX_chartfile\Alpari_MT4_2'

    if mt4_name=='FXTF in Box':
#         folderpath = r'C:\Users\blues\Box\Documents\★FX\FXTF_MT4'
        folderpath = r'D:\FX\★FX_chartfile\FXTF_MT4'

    if mt4_name=='FXTF_2 in Box':
#         folderpath = r'C:\Users\blues\Box\Documents\★FX\FXTF_MT4_2'
        folderpath = r'D:\FX\★FX_chartfile\FXTF_MT4_2'

    if mt4_name=='Titan in Box':
#         folderpath = r'C:\Users\blues\Box\Documents\★FX\Titan_MT4'
        folderpath = r'D:\FX\★FX_chartfile\Titan_MT4'

    if mt4_name=='Titan_2 in Box':
#         folderpath = r'C:\Users\blues\Box\Documents\★FX\Titan_MT4_2'
        folderpath = r'D:\FX\★FX_chartfile\Titan_MT4_2'

    if mt4_name=='Alpari MT4':
        folderpath = r'C:\Users\blues\AppData\Roaming\MetaQuotes\Terminal\287469DEA9630EA94D0715D755974F1B\profiles'

    if mt4_name=='Alpari_2 MT4':
        folderpath = r'C:\Users\blues\AppData\Roaming\MetaQuotes\Terminal\38EF02A5905678051D158DB441089AC0\profiles'

    if mt4_name=='FXTF MT4':
        folderpath = r'C:\Users\blues\AppData\Roaming\MetaQuotes\Terminal\F1DD1D6E7C4A311D1B1CA0D34E33291D\profiles'

    if mt4_name=='FXTF_1 MT4':
        folderpath = r'C:\Users\blues\AppData\Roaming\MetaQuotes\Terminal\2BCD94FB82029A7F5E4FB4BC1A1F4D83\profiles'

    if mt4_name=='FXTF_2 MT4':
        folderpath = r'C:\Users\blues\AppData\Roaming\MetaQuotes\Terminal\0A4685E8FFF330A4CFC9174E6FE966FD\profiles'

    if mt4_name=='Titan MT4':
        folderpath = r'C:\Users\blues\AppData\Roaming\MetaQuotes\Terminal\EC3CF66DAC6B4F7210364B8A2584852D\profiles'

    if mt4_name=='Titan_1 MT4':
        folderpath = r'C:\Users\blues\AppData\Roaming\MetaQuotes\Terminal\449BB6B768FDC0170D4FEC86F084DADE\profiles'

    if mt4_name=='Titan_2 MT4':
        folderpath = r'C:\Users\blues\AppData\Roaming\MetaQuotes\Terminal\0BC0B991B0227E1C66B83051763B592F\profiles'

    return folderpath

# 指定フォルダ以下のすべてのフォルダを取得
def get_all_folders(path):
    import os

    files = os.listdir(path)
    dir = [f for f in files if os.path.isdir(os.path.join(path, f))]
    return dir

# _chartset_list_of_symboliclink以外のフォルダのリストを返す(このリストは実体ファイルと想定)
# def get_currency_folder_list_wo_symboliclink_chart_old(mt4_name):
#     currency_folder_list=[item for item in get_all_folders(get_folderpath(mt4_name))
#                           if item not in _chartset_list_of_symboliclink()]
#     return currency_folder_list

# def _chartset_list_of_symboliclink():
#     return ['21_EURGBP','31_EURAUD','32_GBPAUD','41_EURNZD','42_GBPNZD','43_AUDNZD','51_EURUSD',
#              '52_GBPUSD','53_AUDUSD','54_NZDUSD','61_EURCAD','62_GBPCAD','63_AUDCAD','64_NZDCAD',
#              '65_USDCAD','71_EURCHF','72_GBPCHF','73_AUDCHF','74_NZDCHF','75_USDCHF','76_CADCHF',
#              '81_EURJPY','82_GBPJPY','83_AUDJPY','84_NZDJPY','85_USDJPY','86_CADJPY','87_CHFJPY',
#              'a1_EURクロス','a2_GBPクロス','a3_AUDクロス','a4_NZDクロス','a5_USDストレート','a6_CADクロス','a7_CHFクロス','a8_JPYクロス',
#              'b1_EURクロス','b2_GBPクロス','b3_AUDクロス','b4_NZDクロス','b5_USDストレート','b6_CADクロス','b7_CHFクロス','b8_JPYクロス',
#              ]

# 実体のChartsetのリストを返す
# Input
# mt4_name: MT4名
# Output
# Chartsetのリスト
def get_currency_folder_list_wo_symboliclink_chart(mt4_name):
    datafolderpath = get_folderpath(mt4_name)
    currency_folder_list = get_all_folders(datafolderpath)
    currency_folder_list_realfile = [ item for item in currency_folder_list
                                     if _check_chartsettype(datafolderpath+"/"+item)=="realfile" ]
    # currency_folder_list_realfile = []
    # for item in currency_folder_list:
    #     if _check_chartsettype(datafolderpath+"/"+item)=="realfile":
    #         currency_folder_list_realfile.append(item)
    return currency_folder_list_realfile

# ChartsetのChartファイルのタイプを返す。
# Input
# chartset_folderpath: Chartsetのフォルダパス
# Output
# "realfile": 実体, "symboliclink":シンボリックリンク, "general folder":Chartsetではない通常のフォルダ
def _check_chartsettype(chartset_folderpath):
    import os
    from glob import glob

    filepath_list=glob(chartset_folderpath+'/*.chr')
    if len(filepath_list)==0: return "general folder"
    chartsettype = "realfile"
    for filepath in filepath_list:
        if _check_filetype(filepath) == "symboliclink":
            chartsettype = "symboliclink"
    return chartsettype

def _check_filetype(path):
    import os
    return "symboliclink" if os.path.islink(path) else "file" if os.path.isfile(path) else "folder"


# +
# .chrファイルから通貨名、時間足名を取得する
# .chrファイルパス → 通貨名('JPYUSD'等), 時間足名('M30'等)
def get_currency_timeframe(filepath:str):

    f = open(filepath, 'r', encoding='shift_jis')

    datalist = f.readlines()
    timeframe_namelist={'15':'M30','30':'M30','60':'H1','240':'H4','1440':'D1','10080':'W1','43200':'MN'}
    lines=0
    for data in datalist:
        lines=lines+1
        if data[:7]=='symbol=':
            symbol=data[7:13].rstrip('\n')
        if (data[:7]=='period=') & (lines<10):  # Moving Averageインジケータがperiod=を使っているため
#            print('period={}'.format(data[7:]))
            timeframe_name=timeframe_namelist[data[7:].rstrip('\n')]

#    print(symbol+'_'+timeframe_name)
    f.close()
    return symbol,timeframe_name

# .chrファイルからシンボル名(通貨名+サフィックス)、時間足名を取得する
# .chrファイルパス → シンボル名('JPYUSD-cd'等), 時間足名('M30'等)
def get_symbol_timeframe(filepath):

    f = open(filepath, 'r', encoding='shift_jis')

    datalist = f.readlines()
    timeframe_namelist={'15':'M30','30':'M30','60':'H1','240':'H4','1440':'D1','10080':'W1','43200':'MN'}
    lines=0
    for data in datalist:
        lines=lines+1
        if data[:7]=='symbol=':
            symbol=data[7:].rstrip('\n')
        if (data[:7]=='period=') & (lines<10):  # Moving Averageインジケータがperiod=を使っているため
#            print('period={}'.format(data[7:]))
            timeframe_name=timeframe_namelist[data[7:].rstrip('\n')]

#    print(symbol+'_'+timeframe_name)
    f.close()
    return symbol,timeframe_name

# +
# 指定の.chrファイルのタイムフレームを通貨_時間足.chrのファイル名に合わせてリセットする。
def reset_timeframe(filepath:str):
    import os

    pathname, basename=os.path.split(filepath)
    basenamewoext,ext = os.path.splitext(basename)
    change_flg=False
    if len(basenamewoext)>8:
        currency_fn=basenamewoext[:6]
        timeframe_fn=basenamewoext[7:]
#        print('currency_fn={}, timeframe_fn={}'.format(currency_fn,timeframe_fn))
        currency, timeframe=get_currency_timeframe(filepath)
#        print('currency   ={}, timeframe   ={}'.format(currency, timeframe))
        if timeframe_fn!=timeframe:
            # TFを変更する処理
            temp_filepath=pathname+'\\'+basenamewoext+'_'+ext
            timeframe_numberlist={'M30':'30','H1':'60','H4':'240','D1':'1440','W1':'10080','MN':'43200'}
            with open(filepath) as reader, open(temp_filepath, 'w') as writer:
                lines=0
                for line in reader:
                    lines=lines+1
                    if line[:7]=='period=' and lines<=40:
                        line='period={}\n'.format(timeframe_numberlist[timeframe_fn])
                    writer.write(line)
            os.remove(filepath)
            os.rename(temp_filepath,filepath)
            change_flg=True
    return change_flg

# 指定のフォルダが存在するかチェックし、存在する場合は新たに作れるまで'_数値'を増やす
# make_wachcrrency_folderから使用
def check_and_make_folder_suffix(foldername):
    import os
    if os.path.isdir(foldername)==False:
        return ''
    else:
        num=1
        while os.path.isdir(foldername+'_'+str(num)):
            num=num+1
        return '_'+str(num)

def make_backup_under_the_folder(folderpath):
    import os
    import shutil
    from glob import glob

    filepath_list=glob(folderpath+'/*.chr')
    backup_folderpath=folderpath+'/backup'
    if os.path.isdir(backup_folderpath):
        shutil.rmtree(backup_folderpath)
    os.mkdir(backup_folderpath)
    for filepath in filepath_list:
        shutil.copy2(filepath,backup_folderpath)
    return backup_folderpath

# 通貨ペアのID番号(2桁)を返す
def currencypair_id(currencypair):
    return _currencypair_dic()[currencypair]


def _currencypair_dic():
    return {'EURGBP':'21','EURAUD':'31','EURNZD':'41','EURUSD':'51','EURCAD':'61','EURJPY':'81','EURCHF':'71',
                           'GBPAUD':'32','GBPNZD':'42','GBPUSD':'52','GBPCAD':'62','GBPJPY':'82','GBPCHF':'72',
                                         'AUDNZD':'43','AUDUSD':'53','AUDCAD':'63','AUDJPY':'83','AUDCHF':'73',
                                                       'NZDUSD':'54','NZDCAD':'64','NZDJPY':'84','NZDCHF':'74',
                                                                     'USDCAD':'65','USDJPY':'85','USDCHF':'75',
                                                                                   'CADJPY':'86','CADCHF':'76',
                                                                                   'CHFJPY':'87',
                                                                                                 'JPN225':'00',
                                                                                                 'XAUUSD':'95',
            'EURクロス':'01',       'GBPクロス':'02',   'AUDクロス':'03',   'NZDクロス':'04',
            'USDストレート':'05',   'CADクロス':'06',   'CHFクロス':'07',   'JPYクロス':'08'
            }


def currencypair_list_dic(mt4):
    return {'FXTF':['EURGBP',
                  'EURAUD','GBPAUD',
                  'EURNZD','GBPNZD','AUDNZD',
                  'EURUSD','GBPUSD','AUDUSD','NZDUSD',
                  'EURCAD','GBPCAD','AUDCAD','NZDCAD','USDCAD',
                  'EURCHF','GBPCHF','AUDCHF','NZDCHF','USDCHF',
                  'EURJPY','GBPJPY','AUDJPY','NZDJPY','USDJPY','CADJPY','CHFJPY',
                  'JPN225','XAUUSD'],
           'Alpari':['EURGBP',
                     'EURAUD','GBPAUD',
                     'EURNZD','GBPNZD','AUDNZD',
                     'EURUSD','GBPUSD','AUDUSD','NZDUSD',
                     'EURCAD','GBPCAD','AUDCAD','NZDCAD','USDCAD',
                     'EURCHF','GBPCHF','AUDCHF','NZDCHF','USDCHF','CADCHF',
                     'EURJPY','GBPJPY','AUDJPY','NZDJPY','USDJPY','CADJPY','CHFJPY'],
           'Titan':['EURGBP',
                     'EURAUD','GBPAUD',
                     'EURNZD','GBPNZD','AUDNZD',
                     'EURUSD','GBPUSD','AUDUSD','NZDUSD',
                     'EURCAD','GBPCAD','AUDCAD','NZDCAD','USDCAD',
                     'EURCHF','GBPCHF','AUDCHF','NZDCHF','USDCHF','CADCHF',
                     'EURJPY','GBPJPY','AUDJPY','NZDJPY','USDJPY','CADJPY','CHFJPY']
            }[mt4]

# 通貨ペアのID番号(2桁)から通貨ペア名を返す
# 注: 通貨以外の銘柄(ID番号0や9)はエラーになるために注意。
def currencypair_id_inverse(currencypair_id):
    CurrencyNo={'1':'EUR','2':'GBP','3':'AUD','4':'NZD','5':'USD','6':'CAD','7':'CHF','8':'JPY'}
    if type(currencypair_id)==int:
        currencypair_id=str(currencypair_id)
    currency2=CurrencyNo[currencypair_id[0]]
    currency1=CurrencyNo[currencypair_id[1]]
    return currency1+currency2

# 文字列の中に含まれる通貨ペア文字列を確認する
def find_currencypair(txt):
    for currencypair in ['EURGBP','EURAUD','GBPAUD','EURNZD','GBPNZD','AUDNZD','EURUSD',
                'GBPUSD','AUDUSD','NZDUSD','EURCAD','GBPCAD','AUDCAD','NZDCAD',
                'USDCAD','EURCHF','GBPCHF','AUDCHF','NZDCHF','USDCHF','CADCHF',
                'EURJPY','GBPJPY','AUDJPY','NZDJPY','USDJPY','CADJPY','CHFJPY']:
        if currencypair in txt:
            return currencypair
    else:
        return False

# Pandas DataFrameに辞書型の変数を追加する
# df.append(dic)が使えなくなったための代替策
def add_dic_to_dataframe(df,dic):
    import pandas as pd
    df_add = pd.DataFrame(dic,index=[0])
    df = pd.concat([df, df_add], ignore_index=True)
    return df

# ユーザーのデスクトップのパス
def user_desktop_path():
    import os
    return os.getenv("HOMEDRIVE") + os.getenv("HOMEPATH") + "\\Desktop"

# MT4オブジェクトを時間足で表示/非表示をしているためのパラメータ
# MT4オブジェクトのパラメータperiod_flagsで使用
def object_display_timeframe_dic():
    return {'M30':'8', 'H1':'16', 'H4':'32', 'D1':'64', 'W1':'128', 'MN':'256',
             'M30+':'504', 'H1+':'496', 'H4+':'480', 'D1+':'448', 'W1+':'384','MN+':'256',
             'M30-':'8', 'H1-':'31', 'H4-':'63', 'D1-':'127', 'W1-':'255', 'MN-':'511',
             'ALL':'0'}

# VT_Chart内部仕様の日付パラメータを返す
# date_and_time: 日付型
def get_VTchart_date_parameter(date_and_time):
    import datetime
    base_date_time=datetime.datetime.strptime('202002100700','%Y%m%d%H%M')
#    (year=2020,month=2,day=10,hour=7)
    parameter=1581292740+(date_and_time-base_date_time).total_seconds()
    return str(int(parameter))




# オブジェクト名の中にオブジェクト辞書に登録されている文字列があるかどうかを確認し、あればその文字列を返す。
# なければ''を返す。
def check_object_name(object_fullname,object_parameter_dic):
    object_name=''
    for name in object_parameter_dic:
        if name in object_fullname:
            object_name=name
    return object_name
