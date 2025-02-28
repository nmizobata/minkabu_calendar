class Minkabu_EconomicIndicators:
    
    # みんかぶの将来データは、翌月末まで。
    # みんかぶから経済指標スケジュール情報を明日～翌月末(最長60日間)分を取得。翌々月以降は取得しない。
    def get_economiy_indicators_60days(self):
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
            df_temp=self.get_economy_indicators_from_minkabu(date)
            df=pd.concat([df,df_temp])

        # date, country, event_shortが同一のデータを消去
        df.drop_duplicates(subset=['date','country','event_short'],inplace=True)
        df=df.reset_index(drop=True)

        return df
    
    # 特定の日付のみんかぶWebスクレイピングによる経済指標データの入手
    # date: 日付(datetime形式)
    # 返値: pandas dataframe: date,time,importance,currency,country,event,event_short
    # 注意！ みんかぶは日付が存在するデータを超えて日付を指定した場合、エラーではなく最終日のデータを表示。そのためその日付としてデータを取り込むエラーが起きる。修正が必要。
    def get_economy_indicators_from_minkabu(self,date):
        import pandas as pd

        URL= 'https://fx.minkabu.jp/indicators?date='+date.strftime('%Y-%m-%d')
        listdata = self.get_analyzed_html(URL)
        if date.strftime("%Y年%m月%d日") not in self.get_datecaption(listdata)[0]:
            return
        time_data = self.get_timedata(listdata)
        date_data=[date.strftime('%Y/%m/%d')]*len(time_data)
        
        title_data = self.get_eventdata(listdata)
        short_title=[item.split()[0] for item in title_data]    
        country_data = self.get_countrydata(listdata)
        currency_data = self.get_currencydata(country_data)
#        priority_data = self.get_prioritydata(listdata)

        df = pd.DataFrame({'date':date_data,
                        'time':time_data,
                        'currency':currency_data,
                        'country':country_data,
                        'event':title_data,
                        'event_short':short_title})
        # print(df)
        return df
    def get_datecaption(self,listdata):
        import re
        
        re_command = re.compile(r'<caption.+?</caption>')
        return re_command.findall(listdata)
        
    def get_analyzed_html(self,URL):
        import requests
        import bs4
        
        res = requests.get(URL)
        soup=bs4.BeautifulSoup(res.content,'lxml',from_encoding='utf-8')
        listdata=str(soup.select('body > div > main > section > div > table:nth-child(3)')) 
        return listdata
    
    def get_timedata(self,listdata):
        import re
        # 時刻データ
        re_command=re.compile(r'(?:>)?([\d]+?:[\d]+?|－|未定)(?:<br/>|</span>|</td>)')
        time_data=re_command.findall(listdata)
        time_data=['0:0' if time == "未定" else time for time in time_data]
    #    print('time_data:{}'.format(time_data))
        return time_data

    def get_eventdata(self,listdata):
        import re
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
        return title
    
    def get_countrydata(self, listdata):
        import re
        # 国名
        #    re_command=re.compile(r'(?:img alt=")(.+?|－)(?:" class="mt3)')
        re_command=re.compile(r'(?:grow fbd">)(.+?|－)(?:・)')
        country_data=re_command.findall(listdata)
        # print("country_data:{}".format(country_data))
        return country_data
    
    def get_currencydata(self, country_data):
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
        return currency
    
    # 重要指標はKeyEventsクラスで選択するためPrioritydataは未使用
    def get_prioritydata(self,listdata):
        import re
        
        re_command3=re.compile(r'<span><svg class="i-star.+?</span>')
        priority_string_list=re_command3.findall(listdata)
        priority=[]
        for priority_string in priority_string_list:
            priority_level=priority_string.count('i-star red')
            priority.append(priority_level)
        return priority
    
class KeyEvents:
    def __init__(self, events_df):
        self.events_df = events_df
        self.keywords = self.keyword()
        
    def extract(self):
        import pandas as pd
        df = pd.DataFrame()
        for dic in self.keywords:
            country = dic['country']
            keyword = dic['keyword']
            temp = self.events_df.loc[(self.events_df["country"]==country) & (self.events_df["event"].str.contains(keyword))]
            df = pd.concat([df, temp])
        return df
            
        
    def keyword(self):
        keywords = [
            {"country":"アメリカ","keyword":"実質ＧＤＰ"},
            {"country":"アメリカ","keyword":"新規失業保険"},
            {"country":"アメリカ","keyword":"ISM製造業景気指数"},
            {"country":"アメリカ","keyword":"ＡＤＰ雇用統計"},
            {"country":"アメリカ","keyword":"消費者物価指数"},
            {"country":"アメリカ","keyword":"FRB政策金利"},
            {"country":"ユーロ","keyword":"消費者物価指数"},
            {"country":"ユーロ","keyword":"ユーロ圏失業率"},
            {"country":"ユーロ","keyword":"小売売上高"},
            {"country":"ユーロ","keyword":"ECB政策金利"},
            {"country":"ユーロ","keyword":"実質ＧＤＰ"},
            {"country":"ドイツ","keyword":"実質ＧＤＰ"},
            {"country":"日本","keyword":"完全失業率"},
            {"country":"日本","keyword":"日銀政策金利"},
            {"country":"カナダ","keyword":"中銀政策金利"},
            {"country":"スイス","keyword":"中銀政策金利"},
            {"country":"英国","keyword":"中銀政策金利"},
            {"country":"豪","keyword":"中銀政策金利"},
            {"country":"NZ","keyword":"中銀政策金利"}
        ]
        return keywords

if __name__=="__main__":
    minkabu = Minkabu_EconomicIndicators()
    mode = "debug mode"
    if mode == "debug mode":
        URL="https://fx.minkabu.jp/indicators?date=2025-03-02"
        listdata = minkabu.get_analyzed_html(URL)
        with open("listdata.txt","w") as f:
            f.write(listdata)
        caption = minkabu.get_datecaption(listdata)
        time_data = minkabu.get_timedata(listdata)
        country_data = minkabu.get_countrydata(listdata)
        currency_data = minkabu.get_currencydata(country_data)
        title_data = minkabu.get_timedata(listdata)
        short_title = [item.split()[0] for item in title_data]
        print("capttion          {}".format(caption))
        print("time:       {}個, {}".format(len(time_data),time_data))
        print("country:    {}個, {}".format(len(country_data),country_data))
        print("currency:   {}個, {}".format(len(currency_data),currency_data))
        print("event:      {}個, {}".format(len(title_data),title_data))
        print("event_short:{}個, {}".format(len(short_title),short_title))
    else:
        df=minkabu.get_economiy_indicators_60days()
        keyevents = KeyEvents(df)
        print(keyevents.extract())
