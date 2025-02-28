import google_credits as secret

class GoogleCalendar:
    def __init__(self):
        self.calendar_id, self.service = self.initialize_googlecalendar()
    
    def initialize_googlecalendar(self):
        import googleapiclient.discovery
        import google.auth
        
        SCOPES = ['https://www.googleapis.com/auth/calendar']
        calendar_id = secret.GoogleCalendarId("経済指標").getURL()
        gapi_creds = google.auth.load_credentials_from_file(secret.GoogleCredential().FilePath, SCOPES)[0]
        service = googleapiclient.discovery.build('calendar', 'v3', credentials=gapi_creds)
        return calendar_id, service
    
    # 経済指標スケジュールデータと、google calendarのデータを比較して差分を返す
    # google calendar timeMinで指定できる時間のフォーマットは厳密。'2024-09-11T06:41:10.580216Z'に合わせること。
    def get_googlecalendar(self):
        import datetime as dt
        import pandas as pd
        
        # google calendar 経済指標データの取り込み
        # now = dt.datetime.utcnow().isoformat() + 'Z'
        previous_days = dt.timedelta(days=0)     # 何日さかのぼってデータを取得するか? 今は0日で処理。
        now = "T".join(str(dt.datetime.now(dt.timezone.utc)-previous_days).split(" "))[:-6]+"Z"
        event_list = self.service.events().list(
            calendarId=self.calendar_id, timeMin=now,
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
    def add_googlecalendar(self,df):
        import datetime
        
        total=len(df['date'])
        for i in range(total):
        #    print(df_over4.iloc[i])
            item=df.iloc[i]
            print('\n{}: ({}){}をカレンダーに追加しています '.format(item['date'],item['currency'],item['event_short']))
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
            event=self.service.events().insert(calendarId=self.calendar_id, body=body).execute()
            print("全{}件中 {}件完了".format(total,i+1))
        return event

    # DataFrameのスケジュール情報をGoogle Calendarから削除(event_idがキーコード)
    def remove_googlecalendar(self,df):
        import time
        
        total=len(df['date'])
        for i in range(len(df)):
            item=df.iloc[i]
            print('{}: {}を削除しています'.format(item['date'],item['event(currency)']))
            print("全{}件中 {}件削除しました".format(total, i+1))
            self.service.events().delete(calendarId=self.calendar_id,eventId=df.iloc[i]['event_id']).execute()
            time.sleep(3)  # サイトに拒否されないようにスリープを入れる
            
if __name__=="__main__":
    gcallendar = GoogleCalendar()
    current_eventdata=gcallendar.get_googlecalendar()
    print(current_eventdata)