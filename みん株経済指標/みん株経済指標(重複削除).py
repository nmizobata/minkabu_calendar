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
# みん株 経済指標スケジュール、Google Calendarに重複登録されているアイテムを削除
# https://fx.minkabu.jp/indicators
# googleカレンダーのプログラムに関するメモ https://share.evernote.com/note/9195e429-ef9a-785a-7259-4eec3c5c10b8
# 20241224 ver1.0 みん株 経済指標スケジュール ver1.4よりモジュールを分離
# -

def initialize_googlecalendar():
    import googleapiclient.discovery
    import google.auth
    
    SCOPES = ['https://www.googleapis.com/auth/calendar']
    calendar_id = 'pk3dm4n2tmlqvr6t9h0ipeears@group.calendar.google.com'
    gapi_creds = google.auth.load_credentials_from_file(r'D:\FX\★FX_chartfile\MT4バッチツール\googlecalendar\mycalendarproject-374505-ded433e45278.json', SCOPES)[0]
    service = googleapiclient.discovery.build('calendar', 'v3', credentials=gapi_creds)
    return calendar_id, service


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


