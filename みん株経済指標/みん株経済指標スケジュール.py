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
# みん株 経済指標スケジュールをWebスクレイピングしGoogle Calendarに反映する
# https://fx.minkabu.jp/indicators
# googleカレンダーのプログラムに関するメモ https://share.evernote.com/note/9195e429-ef9a-785a-7259-4eec3c5c10b8
# 
# 20230113 ver0.1 みんかぶ株式指標スケジュールからデータを抜き出すエンジン開発
# 20230114 ver1.0 定期実行可能なように、重複の回避、差分のみの追加機能を実装
# 20230315 ver1.1 時間部分に"未定"と記入されている場合のエラー発生を回避
# 20230724 ver1.2 プライオリティのフォーマットが変更されあため対応
# 20240911 ver1.3 バグ修正-UTCフォーマット, 「米国休場」でのエラー他
# 20241224 ver1.4 バグ修正-(def get_googlecalendar()) google calendarから取得データが無い場合に発生するエラーを修正

# +
# #!pip install google-api-python-client google-auth
# #!pip install google-auth-httplib2
# #!pip install google-auth-oauthlib
# #!pip install investpy

# +
# investpyによる経済指標情報の入手

#import investpy
#import pandas as pd
#economic_data = investpy.economic_calendar(time_zone= "GMT +9:00", time_filter='time_only', countries=None,importances=["high"],from_date='01/1/2023', to_date='31/12/2023')
#economic_data = economic_data[economic_data['importance']=='high']
#euro_data = economic_data[economic_data["zone"] == "euro zone"]
#japan_data = economic_data[economic_data["zone"] == "japan"]
#usa_data = economic_data[economic_data["zone"] == "united states"]

# +
# みんかぶの将来データは、翌月末まで。
# みんかぶから経済指標スケジュール情報を明日～翌月末(最長60日間)分を取得。翌々月以降は取得しない。
def get_economiy_indicators_60days():
    import datetime as dt
    import pandas as pd

    date_index = pd.date_range(dt.datetime.now()+dt.timedelta(days=1), periods=60, freq="D")
    thisMonth = dt.datetime.now().month
#    date_index = pd.date_range(dt.datetime.now(), periods=60, freq="D")
    df=pd.DataFrame()
    for date in date_index:
        if date.month > thisMonth+1:
            continue
        print('{}のデータを取り込んでいます'.format(date.strftime('%Y%m%d')))
        df_temp=get_economy_indicators_from_minkabu(date)
        df=pd.concat([df,df_temp])

    # date, country, event_shortが同一のデータを消去
    df.drop_duplicates(subset=['date','country','event_short'],inplace=True)
    df=df.reset_index(drop=True)

    return df


# 特定の日付のみんかぶWebスクレイピングによる経済指標データの入手
# date: 日付(datetime形式)
# 返値: pandas dataframe: date,time,importance,currency,country,event,event_short
# 注意！ みんかぶは日付が存在するデータを超えて日付を指定した場合、エラーではなく最終日のデータを表示。そのためその日付としてデータを取り込むエラーが起きる。修正が必要。
def get_economy_indicators_from_minkabu(date):
    import pandas as pd
    import requests
    import bs4
    import re

    # みんかぶ経済指標スケジュールサイト
    date_text=date.strftime('%Y-%m-%d')
    URL= 'https://fx.minkabu.jp/indicators?date='+date_text

    res = requests.get(URL)
    soup=bs4.BeautifulSoup(res.content,'lxml',from_encoding='utf-8')
    listdata=str(soup.select('body > div > main > section > div > table:nth-child(3)')) 
#    print(listdata)
#    listdataのファイルへの書き出し(デバッグ用)
#    with open(r"C:\Users\blues\Desktop"+"/"+"listdata.txt",mode="w") as f:
#        f.write(listdata)

    # 時刻データ
    re_command=re.compile(r'(?:>)?([\d]+?:[\d]+?|－|未定)(?:<br/>|</span>|</td>)')
    time_data=re_command.findall(listdata)
    time_data=['0:0' if time == "未定" else time for time in time_data]
#    print('time_data:{}'.format(time_data))

    # 日付データ
    date_data=[date.strftime('%Y/%m/%d')]*len(time_data)
#    print('date_data:{}'.format(date_data))
    
    # イベントデータ(フル表示)
    re_command2=re.compile(r'(?:nowrap">|fbd">)(.+?)(?:</p>)')
    title_data=re_command2.findall(listdata)
    title=[]
    title_num=0
    for i in range(len(title_data)):
        # print("title_data:{}".format(title_data[i]))
        if title_data[i][0]=='[':
            title[title_num-1]=title_data[i-1]+' '+title_data[i]
        else:
            if '・' in title_data[i]:
                title_data[i]=title_data[i].split('・',1)[1]
            else:
                continue
            title.append(title_data[i])
            title_num=title_num+1
    
    # イベントデータ(短縮表示)
    short_title=[item.split()[0] for item in title]    
    
    # 国名
#    re_command=re.compile(r'(?:img alt=")(.+?|－)(?:" class="mt3)')
    re_command=re.compile(r'(?:grow fbd">)(.+?|－)(?:・)')
    country_data=re_command.findall(listdata)
    # print("country_data:{}".format(country_data))

    # 関連する通貨名
    currency_dic={  'アメリカ':'USD',
                    'ユーロ':'EUR',
                    'アンドラ':'EUR',
                    'オーストリア':'EUR',
                    'ベルギー':'EUR',
                    'キプロス':'EUR',
                    'ドイツ':'EUR',
                    'スペイン':'EUR',
                    'エストニア':'EUR',
                    'フィンランド':'EUR',
                    'フランス':'EUR',
                    'ギリシャ':'EUR',
                    'クロアチア':'EUR',
                    'アイルランド':'EUR',
                    'イタリア':'EUR',
                    'ラトビア':'EUR',
                    'リトアニア':'EUR',
                    'ルクセンブルク':'EUR',
                    'モナコ':'EUR',
                    'マルタ':'EUR',
                    'オランダ':'EUR',
                    'ポルトガル':'EUR',
                    'サンマリノ':'EUR',
                    'スロバキア':'EUR',
                    'スロベニア':'EUR',
                    'バチカン':'EUR',
                    '英国':'GBP',
                    'オーストラリア':'AUD',
                    'ニュージーランド':'NZD',
                    'カナダ':'CAD',
                    'スイス':'CHF',
                    '日本':'JPY'}
    currency=[]
    for country in country_data:
        if country in currency_dic:
            currency.append(currency_dic[country])
        else:
            currency.append('-')

    # 重要度 i-starの文字列の中のstar-fillの数を数える
#    re_command3=re.compile(r'(?:img alt=")(.+?)(?:" class="i-star")')
    re_command3=re.compile(r'<span><img class="i-star".+.svg"/></span>')
    priority_string_list=re_command3.findall(listdata)
#    print('priority_data:{}'.format(priority_string_list))
    priority=[]
#    for i in range(int(len(priority_data)/5)):
#        priority_level=0
#        for j in range(5):
#            if priority_data[i*5+j]=='Star fill':
#                priority_level=priority_level+1
    for priority_string in priority_string_list:
        priority_level=priority_string.count('star-fill')
        priority.append(priority_level)
#        print('stars:{}'.format(priority_level))

    # DataFrame化
#    print('date:{}, time:{}, inportance:{},currency:{}, country:{}, event:{}, event_short:{}'.format(date_data, time_data, priority, currency, country_data, title,short_title))
    # print("date:{}, {}".format(date_data,len(date_data)))
    # print("time:{},{}".format(time_data,len(time_data)))
    # print("importance:{},{}".format(priority,len(priority)))
    # print("currency:{},{}".format(currency,len(currency)))
    # print("country:{},{}".format(country_data,len(country_data)))
    # print("event:{},{}".format(title,len(title)))
    # print("event_short:{},{}".format(short_title,len(short_title)))

    df = pd.DataFrame({'date':date_data,
                       'time':time_data,
                       'importance':priority,
                       'currency':currency,
                       'country':country_data,
                       'event':title,
                       'event_short':short_title})
    # print(df)
    return df



# +
# 経済指標スケジュールデータと、google calendarのデータを比較して差分を返す
# google calendar timeMinで指定できる時間のフォーマットは厳密。'2024-09-11T06:41:10.580216Z'に合わせること。
def get_googlecalendar(calendar_id,service):
    import datetime as dt
    import pandas as pd
    
    # google calendar 経済指標データの取り込み
    # now = dt.datetime.utcnow().isoformat() + 'Z'
    previous_days = dt.timedelta(days=0)     # 何日さかのぼってデータを取得するか? 今は0日で処理。
    now = "T".join(str(dt.datetime.now(dt.UTC)-previous_days).split(" "))[:-6]+"Z"
    event_list = service.events().list(
         calendarId=calendar_id, timeMin=now,
         #maxResults=3, 
         singleEvents=True,
         orderBy='startTime').execute()

    events = event_list.get('items', [])
    # print(events)
    formatted_events = [
        {
        'start':event['start'].get('dateTime', event['start'].get('date')), # start time or day
        'end':event['end'].get('dateTime', event['end'].get('date')), # end time or day
        'event(currency)':event['summary'],
        'event_id':event['id']} 
                        for event in events]
    # print(formatted_events)
    df_googlecalendar=pd.DataFrame(formatted_events,columns=["start","end","event(currency)","event_id"])
    # print(df_googlecalendar)
    df_googlecalendar['len_date']=[len(df_googlecalendar.iloc[i]['start']) for i in range(len(df_googlecalendar))]
    df_googlecalendar=df_googlecalendar[df_googlecalendar['len_date']==25]
    df_googlecalendar['date']=[datetime_str[:4]+'/'+datetime_str[5:7]+'/'+datetime_str[8:10] for datetime_str in df_googlecalendar['start']]
    df_googlecalendar['time']=[datetime_str[11:16] for datetime_str in df_googlecalendar['start']]
    df_googlecalendar=df_googlecalendar.reindex(columns=['date','time','event(currency)','event_id'])
    return df_googlecalendar

# DataFrameのスケジュール情報をGoogle Calendarに追加
def add_googlecalendar(calendar_id,service,df):
    import datetime
    
    total=len(df['date'])
    for i in range(total):
    #    print(df_over4.iloc[i])
        item=df.iloc[i]
        print('全{}件中{}件完了\n{}:({}){}をカレンダーに追加しています '.format(total,i,item['date'],item['currency'],item['event_short']))
        body = {
            'summary': '('+item['currency']+')'+item['event_short'],
            'start': {
                'dateTime':datetime.datetime.strptime(item['date']+' '+item['time'],'%Y/%m/%d %H:%M').isoformat(),
                'timeZone':'Japan'
            },
            'end':{
                'dateTime':(datetime.datetime.strptime(item['date']+' '+item['time'],'%Y/%m/%d %H:%M')+datetime.timedelta(minutes=5)).isoformat(),
                'timeZone':'Japan'
            }
        }
        event=service.events().insert(calendarId=calendar_id, body=body).execute()

# DataFrameのスケジュール情報をGoogle Calendarから削除
def remove_googlecalendar(calendar_id,service,df):
    import datetime
    import time
    
    total=len(df['date'])
    for i in range(len(df)):
        item=df.iloc[i]
        print('全{}件中{}件完了\n{}:{}を削除しています'.format(total,i,item['date'],item['event_short']))
        service.events().delete(calendarId=calendar_id,eventId=df.iloc[i]['event_id']).execute()
        time.sleep(3)  # サイトに拒否されないようにスリープを入れる
        
def initialize_googlecalendar():
    import googleapiclient.discovery
    import google.auth
    SCOPES = ['https://www.googleapis.com/auth/calendar']
    calendar_id = 'pk3dm4n2tmlqvr6t9h0ipeears@group.calendar.google.com'
    gapi_creds = google.auth.load_credentials_from_file(r'D:\FX\★FX_chartfile\MT4バッチツール\googlecalendar\mycalendarproject-374505-ded433e45278.json', SCOPES)[0]
    service = googleapiclient.discovery.build('calendar', 'v3', credentials=gapi_creds)
    return calendar_id, service


# +
# Googleカレンダーのイベント取得
# import datetime
# import googleapiclient.discovery
# import google.auth

# # 認証情報の設定
# SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']
# SERVICE_ACCOUNT_FILE = r'D:\FX\★FX_chartfile\MT4バッチツール\googlecalendar\mycalendarproject-374505-ded433e45278.json'

# # 認証情報を読み込む
# credentials = google.auth.load_credentials_from_file(SERVICE_ACCOUNT_FILE, SCOPES)[0]

# # APIサービスを構築
# service = googleapiclient.discovery.build('calendar', 'v3', credentials=credentials)

# # 現在時刻を取得
# #now = datetime.datetime.utcnow().isoformat() + 'Z'
# now = "T".join(str(datetime.datetime.now(datetime.UTC)).split(" "))[:-6]+"Z"

# # イベントを取得
# events_result = service.events().list(
#     calendarId='primary', timeMin=now,
#     maxResults=50, singleEvents=True,
#     orderBy='startTime').execute()
# events = events_result.get('items', [])

# # イベント情報を表示
# if not events:
#     print('No upcoming events found.')
# for event in events:
#     start = event['start'].get('dateTime', event['start'].get('date'))
#     print(start, event['summary'])

# +
# google calendarに登録
import datetime
import googleapiclient.discovery
import google.auth
import pandas as pd

# 重要なイベントだけ抽出
df=get_economiy_indicators_60days()
# df_over4=df[df['importance']>=4][df['currency']!='-']
df_over4=df.loc[(df['importance']>=4)&(df['currency']!='-')]
df_over4=pd.concat([df_over4,df.loc[(df['currency']=='CAD')&(df['event_short']=='中銀政策金利')]])
df_over4['event(currency)']=['('+df_over4.iloc[i]['currency']+')'+df_over4.iloc[i]['event_short'] for i in range(len(df_over4))]

# 現在のGoogleCalendarの情報を取得
calendar_id,service=initialize_googlecalendar()
googlecalendar=get_googlecalendar(calendar_id,service)

# みんかぶの情報と現在のGoogle Calendarとの差分を抽出
diff_df=pd.concat([googlecalendar,df_over4])
diff_df.drop_duplicates(subset=['date','time','event(currency)'],keep=False,inplace=True)

# そのうち、未登録の情報を追加
add_df=diff_df[diff_df['event_id'].isnull()]
add_googlecalendar(calendar_id,service,add_df)

# そのうち、google calendarのみに存在する情報を消去
del_df=diff_df[~diff_df['event_id'].isnull()]
remove_googlecalendar(calendar_id,service,del_df)


# +
# 現時点のGoogle Calendarの登録内容を今日以降の登録内容をチェックし、重複しているイベントを削除
def remove_duplicates_from_googlecalendar(calendar_id,service):
    import datetime
    import pandas as pd
    import time

#    now = (datetime.datetime.utcnow()-datetime.timedelta(days=5)).isoformat() + 'Z'  utcnow()が未推奨となったため変更
    now = (datetime.datetime.now(datetime.UTC)-datetime.timedelta(days=5)).isoformat()[:-6] + "Z"

    event_list = service.events().list(
         calendarId=calendar_id, timeMin=now,
    #     maxResults=3, 
         singleEvents=True,
         orderBy='startTime').execute()

    events = event_list.get('items', [])
    formatted_events = [{'start':event['start'].get('dateTime', event['start'].get('date')), # start time or day
         'end':event['end'].get('dateTime', event['end'].get('date')), # end time or day
         'event':event['summary'],
         'event_id':event['id']} for event in events]
    df_googlecalendar=pd.DataFrame(formatted_events)
    df_googlecalendar['duplicated']=df_googlecalendar.duplicated(subset=['start','end','event'])

    j=0
    for i in range(len(df_googlecalendar)):
        if df_googlecalendar.iloc[i]['duplicated']==True:
            j=j+1
            item=df_googlecalendar.iloc[i]
            print('{}:{}を削除しています'.format(item['start'],item['event']))
            ret=service.events().delete(calendarId=calendar_id,eventId=item['event_id']).execute()
            time.sleep(3)  # サイトに拒否されないようにスリープを入れる
    print('{}件削除しました'.format(j))


# -

calendar_id,service=initialize_googlecalendar()
remove_duplicates_from_googlecalendar(calendar_id,service)


