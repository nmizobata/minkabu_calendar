# ---
# jupyter:
#   jupytext:
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.3'
#       jupytext_version: 1.16.2
#   kernelspec:
#     display_name: Python 3 (ipykernel)
#     language: python
#     name: python3
# ---

# このライブラリを使う時はmainに以下を挿入
# import sys
# sys.path.append('..')    # pythonモジュール検索パスに親ディレクトリを追加。(シェル環境では削除)
# #pprint.pprint(sys.path)
# from MT4_common_lib.mt4_lib import get_folderpath,get_currency_timeframe, reset_timeframe

# %%
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

# Boxのチャートデータベースを参照しているチャートセットを除いたMT4データフォルダに登録されている通貨チャートフォルダのリストを得る
def get_currency_folder_list_wo_symboliclink_chart(mt4_name):
    currency_folder_list=get_all_folders(get_folderpath(mt4_name))
    for item in _chartset_list_of_symboliclink():
        if item in currency_folder_list:
            currency_folder_list=currency_folder_list.remove(item)
    return currency_folder_list

def _chartset_list_of_symboliclink():
    return ['21_EURGBP','31_EURAUD','32_GBPAUD','41_EURNZD','42_GBPNZD','43_AUDNZD','51_EURUSD',
             '52_GBPUSD','53_AUDUSD','54_NZDUSD','61_EURCAD','62_GBPCAD','63_AUDCAD','64_NZDCAD',
             '65_USDCAD','71_EURCHF','72_GBPCHF','73_AUDCHF','74_NZDCHF','75_USDCHF','76_CADCHF',
             '81_EURJPY','82_GBPJPY','83_AUDJPY','84_NZDJPY','85_USDJPY','86_CADJPY','87_CHFJPY',
             'a1_EURクロス','a2_GBPクロス','a3_AUDクロス','a4_NZDクロス','a5_USDストレート','a6_CADクロス','a7_CHFクロス','a8_JPYクロス',
             'b1_EURクロス','b2_GBPクロス','b3_AUDクロス','b4_NZDクロス','b5_USDストレート','b6_CADクロス','b7_CHFクロス','b8_JPYクロス',
             '95_XAUUSD','00_JPN225']


# %%
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

# %%
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
