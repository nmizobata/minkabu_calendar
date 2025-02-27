import pandas as pd
import googlecalendar_lib as googlecalendar
import minkabu as minkabu_df


if __name__=="__main__":
    minkabu = minkabu_df.Minkabu_EconomicIndicators()
    df=minkabu.get_economiy_indicators_60days()
    # df.to_excel("event.xlsx")
    
    keyevent = minkabu_df.KeyEvents(df)
    df_keyevents = keyevent.extract()
    df_keyevents['event(currency)']=['('+df_keyevents.iloc[i]['currency']+')'+df_keyevents.iloc[i]['event_short'] for i in range(len(df_keyevents))]

    # 現在のGoogleCalendarの情報を取得
    gcaledar = googlecalendar.GoogleCalendar()
    current_event=gcaledar.get_googlecalendar()
    
    # みんかぶの情報と現在のGoogle Calendarとの差分を抽出
    diff_df=pd.concat([current_event,df_keyevents])
    diff_df.drop_duplicates(subset=['date','time','event(currency)'],keep=False,inplace=True)
   
    # そのうち、未登録の情報を追加
    add_df=diff_df[diff_df['event_id'].isnull()]
    gcaledar.add_googlecalendar(add_df)

    # そのうち、google calendarのみに存在する情報を消去
    del_df=diff_df[~diff_df['event_id'].isnull()]
    gcaledar.remove_googlecalendar(del_df)


