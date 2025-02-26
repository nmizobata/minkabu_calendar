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
# Replace Chart Parameterのクラス
from abc import ABC, abstractmethod

# Interface
class LayoutParameters(ABC):
    @abstractmethod
    def main_dic(self):
        pass

    @abstractmethod
    def indicator_dic(self):
        pass

    @abstractmethod
    def object_dic(self):
        pass



# +
# Concrete
class Layout_6(LayoutParameters):
    def __init__(self, mt4, timeframe):
        self.mt4 = mt4
        self.timeframe = timeframe

    def main_dic(self):
        background_color='16777215'  # White
        left,top,right,bottom = self.__get_left_top_right_bottom_info(self.mt4, 
                                                                      self.__get_timeframe_layout_no(self.timeframe))
        main_parameter_dic={'window_left':str(left),'window_top':str(top),'window_right':str(right),
                            'window_bottom':str(bottom),'background_color':background_color}
        return main_parameter_dic

    def object_dic(self):
        object_parameter_dic={}
        return object_parameter_dic

    def indicator_dic(self):
        indicator_parameter_dic={}
        return indicator_parameter_dic

#################################### 共通ライブラリ系 ####################################
    def __get_timeframe_layout_no(self,timeframe):
        timeframe_layout_no={'MN':3, 'W1':4,'D1':5,'H4':2,'H1':1,'M30':1}
        return timeframe_layout_no[self.timeframe]

    # チャートウィンドウの座標(LEFT,TOP,RIGHT,BOTTOM)を返す
    # timeframe_layout_no: 通時間足レイアウト番号
    def __get_left_top_right_bottom_info(self, mt4, timeframe_layout_no):
        MT4_TATE=mt4.TATE
        MT4_YOKO=mt4.YOKO
        TATE_2=MT4_TATE/2  #468
        YOKO_M30=1030
        YOKO_3=MT4_YOKO/3
        if timeframe_layout_no==1:
            TOP=0
            BOTTOM=TATE_2
            LEFT=0
            RIGHT=YOKO_M30
        elif timeframe_layout_no==2:
            TOP=0
            BOTTOM=TATE_2
            LEFT=YOKO_M30
            RIGHT=MT4_YOKO
        else:
            TOP=TATE_2
            BOTTOM=MT4_TATE
            LEFT=YOKO_3*(timeframe_layout_no-3)
            RIGHT=YOKO_3*(timeframe_layout_no-2)
        return int(LEFT),int(TOP),int(RIGHT),int(BOTTOM)


# -

# Concrete
class Layout_16watch(LayoutParameters):
    pass


# +
# Concrete
class Layout_07Cross(LayoutParameters):
    def __init__(self, mt4, currencyname, timeframe, order_name="1st_currency"):
        self.mt4 = mt4
        self.order_name = order_name
        self.currencyname = currencyname
        self.timeframe = timeframe

    def main_dic(self):
        if self.order_name=='1st_currency':
            currency_layout_no=self.__get_currency_layout_no1(self.currencyname)
            background_color='15136253'  # Oldlace
        elif self.order_name=='2nd_currency':
            currency_layout_no=self.__get_currency_layout_no2(self.currencyname)
            background_color='16775408'  # AliceBlue
        left,top,right,bottom = self.__get_left_top_right_bottom_info(self.mt4, currency_layout_no,
                                                                      self.__get_timeframe_layout_no(self.timeframe))

        main_parameter_dic={}
        if self.currencyname=='JPN225':
            main_parameter_dic={'window_left':str(left),'window_top':str(top),'window_right':str(right),
                                'window_bottom':str(bottom),'background_color':'16777215'}  # White
        elif self.currencyname=='XAUUSD':
            main_parameter_dic={'window_left':str(left),'window_top':str(top),'window_right':str(right),
                                'window_bottom':str(bottom),'background_color':'16777215'}  # White
        else:
            main_parameter_dic={'window_left':str(left),'window_top':str(top),'window_right':str(right),
                                'window_bottom':str(bottom),'background_color':background_color}
        return main_parameter_dic

    def object_dic(self):
        from MT4_common_lib import mt4_lib as mt

        object_parameter_dic={}

        # オブジェクト表示制限定数
        object_parameter_dic={'StampText':{'period_flags':mt.object_display_timeframe_dic()[self.timeframe]}}
        return object_parameter_dic

    def indicator_dic(self):
        indicator_parameter_dic={}
        if self.timeframe=='M30':
            indicator_parameter_dic={'Mi_TimeStamp_v06':{'adjust_y':'-100'},
                                     'VT_Chart':{'jpn_flag':'false'}}
        elif self.timeframe=='D1':
            indicator_parameter_dic={'Mi_TimeStamp_v06':{'adjust_y':'3'},
                                     'SyncPeriod':{'ichart_text':'#pair','fontsize2':'20','xshift2':'10','yshift2':'15'}}
        elif self.timeframe=='H4':
            indicator_parameter_dic={'VT_Chart':{'jpn_flag':'true','offset_time':'1'}}
        return indicator_parameter_dic

#################################### 共通ライブラリ系 ####################################
    # 通貨ペア文字列→レイアウト番号(1～7)を返す
    def __get_currency_layout_no1(self,currencyname):   # 第一通貨  EUR*** など
        currency_layout_no={'EURGBP':1,'EURAUD':2,'EURNZD':3,'EURUSD':4,'EURCAD':5,'EURCHF':6,'EURJPY':7,
                                       'GBPAUD':2,'GBPNZD':3,'GBPUSD':4,'GBPCAD':5,'GBPCHF':6,'GBPJPY':7,
                                                  'AUDNZD':3,'AUDUSD':4,'AUDCAD':5,'AUDCHF':6,'AUDJPY':7,
                                                             'NZDUSD':4,'NZDCAD':5,'NZDCHF':6,'NZDJPY':7,
                                                                        'USDCAD':5,'USDCHF':6,'USDJPY':7,
                                                                                   'CADCHF':6,'CADJPY':7,
                                                                                              'CHFJPY':7,
                                                                                   'JPN225':6,
                                                                                   'XAUUSD':6}
        return currency_layout_no[currencyname]

    def __get_currency_layout_no2(self,currencyname):   # 第二通貨  ***EURなど
        currency_layout_no={'EURGBP':1,
                            'EURAUD':1,'GBPAUD':2,
                            'EURNZD':1,'GBPNZD':2,'AUDNZD':3,
                            'EURUSD':1,'GBPUSD':2,'AUDUSD':3,'NZDUSD':4,
                            'EURCAD':1,'GBPCAD':2,'AUDCAD':3,'NZDCAD':4,'USDCAD':5,
                            'EURCHF':1,'GBPCHF':2,'AUDCHF':3,'NZDCHF':4,'USDCHF':5,'CADCHF':6,
                            'EURJPY':1,'GBPJPY':2,'AUDJPY':3,'NZDJPY':4,'USDJPY':5,'CADJPY':6,'CHFJPY':7,
                                                                                   'JPN225':6,
                                                                                   'XAUUSD':6}
        return currency_layout_no[currencyname]

    def __get_timeframe_layout_no(self,timeframe):
        timeframe_layout_no={'MN':0, 'W1':0,'D1':1,'H4':0,'H1':0,'M30':0}
        return timeframe_layout_no[self.timeframe]

    # チャートウィンドウの座標(LEFT,TOP,RIGHT,BOTTOM)を返す
    # currency_klayout_no: 通貨レイアウト番号
    # timeframe_layout_no: 通時間足レイアウト番号
    def __get_left_top_right_bottom_info(self,mt4, currency_layout_no,timeframe_layout_no):
        MT4_TATE=mt4.TATE
        MT4_YOKO=mt4.YOKO
        TATE_2=MT4_TATE/2  #468
        TATE_3=MT4_TATE/3  #312
        YOKO_D1=MT4_YOKO/3
        if currency_layout_no<=4:
            TOP=TATE_2*((currency_layout_no-1)%2)
            BOTTOM=TATE_2*((currency_layout_no-1)%2+1)
            LEFT=YOKO_D1*((currency_layout_no-1)//2)
            RIGHT=YOKO_D1*((currency_layout_no+1)//2)
        else:
            TOP=TATE_3*(currency_layout_no-5)
            BOTTOM=TATE_3*(currency_layout_no-4)
            LEFT=YOKO_D1*2
            RIGHT=YOKO_D1*3
        return int(LEFT),int(TOP),int(RIGHT),int(BOTTOM)

# +
# Concrete
class Layout_14Cross(LayoutParameters):
    def __init__(self, mt4, currencyname, timeframe, order_name="1st_currency"):
        self.mt4 = mt4
        self.order_name = order_name
        self.currencyname = currencyname
        self.timeframe = timeframe

    def main_dic(self):
        if self.order_name=='1st_currency':
            currency_layout_no=self.__get_currency_layout_no1(self.currencyname)
            background_color='15136253'  # Oldlace
        elif self.order_name=='2nd_currency':
            currency_layout_no=self.__get_currency_layout_no2(self.currencyname)
            background_color='16775408'  # AliceBlue
        left,top,right,bottom=self.__get_left_top_right_bottom_info(self.mt4, currency_layout_no,
                                                                    self.__get_timeframe_layout_no(self.timeframe))

        main_parameter_dic={}
        if self.currencyname=='JPN225':
            main_parameter_dic={'window_left':str(left),'window_top':str(top),'window_right':str(right),
                                'window_bottom':str(bottom),'background_color':'16777215'}  # White
        elif self.currencyname=='XAUUSD':
            main_parameter_dic={'window_left':str(left),'window_top':str(top),'window_right':str(right),
                                'window_bottom':str(bottom),'background_color':'16777215'}  # White
        else:
            main_parameter_dic={'window_left':str(left),'window_top':str(top),'window_right':str(right),
                                'window_bottom':str(bottom),'background_color':background_color}
        return main_parameter_dic

    def object_dic(self):
        from MT4_common_lib import mt4_lib as mt
        import datetime

        object_parameter_dic={}
        object_parameter_dic={'StampText':{'period_flags':mt.object_display_timeframe_dic()[self.timeframe]},
                              'TesterLine':{'selectable':'0','time_0':mt.get_VTchart_date_parameter(datetime.datetime.now())}}
        return object_parameter_dic

    def indicator_dic(self):
        from MT4_common_lib import mt4_lib as mt

        if self.order_name=='1st_currency':
            currency_layout_no=self.__get_currency_layout_no1(self.currencyname)
        elif self.order_name=='2nd_currency':
            currency_layout_no=self.__get_currency_layout_no2(self.currencyname)

        indicator_parameter_dic={}
        if self.timeframe=='M30':
            indicator_parameter_dic={'Mi_TimeStamp_v06':{'adjust_y':'-100'},
                                     'VT_Chart':{'jpn_flag':'false'}}
        elif self.timeframe=='D1':
            indicator_parameter_dic={'Mi_TimeStamp_v06':{'adjust_y':'3'},
                                     'SyncPeriod':{'ichart_text':'#pair','fontsize2':'18','xshift2':'10','yshift2':'15'},
                                     }
        elif self.timeframe=='H4':
            indicator_parameter_dic={'CustomCandle2':{'yousen_color':'15453831','insen_color':'12695295','even_color':'13959039',
                                                      'yousen_color2':'13959039','insen_color2':'14804223','even_color2':'65280',
                                                      'candle_type':'3','hige_width':'2',
                                                      'iuse_lock_tf':'true','ilock_tf_h04':'17','ilock_tf_d01':'18','ilock_tf_w01':'19'},
                                     'CustomCandleTester':{'yousen_color':'15453831','insen_color':'12695295','even_color':'13959039',
                                                      'yousen_color2':'13959039','insen_color2':'14804223','even_color2':'65280',
                                                      'candle_type':'3','hige_width':'2',
                                                      'iuse_lock_tf':'true','ilock_tf_h04':'17','ilock_tf_d01':'18','ilock_tf_w01':'19'},
                                     'VT_Chart':{'jpn_flag':'true','offset_time':'1'}}
        return indicator_parameter_dic

#################################### 共通ライブラリ系 ####################################
    # 通貨ペア文字列→レイアウト番号(1～7)を返す
    def __get_currency_layout_no1(self,currencyname):   # 第一通貨  EUR*** など
        currency_layout_no={'EURGBP':1,'EURAUD':2,'EURNZD':3,'EURUSD':4,'EURCAD':5,'EURCHF':6,'EURJPY':7,
                                       'GBPAUD':2,'GBPNZD':3,'GBPUSD':4,'GBPCAD':5,'GBPCHF':6,'GBPJPY':7,
                                                  'AUDNZD':3,'AUDUSD':4,'AUDCAD':5,'AUDCHF':6,'AUDJPY':7,
                                                             'NZDUSD':4,'NZDCAD':5,'NZDCHF':6,'NZDJPY':7,
                                                                        'USDCAD':5,'USDCHF':6,'USDJPY':7,
                                                                                   'CADCHF':6,'CADJPY':7,
                                                                                              'CHFJPY':7,
                                                                                   'JPN225':6,
                                                                                   'XAUUSD':6}
        return currency_layout_no[currencyname]

    def __get_currency_layout_no2(self,currencyname):   # 第二通貨  ***EURなど
        currency_layout_no={'EURGBP':1,
                            'EURAUD':1,'GBPAUD':2,
                            'EURNZD':1,'GBPNZD':2,'AUDNZD':3,
                            'EURUSD':1,'GBPUSD':2,'AUDUSD':3,'NZDUSD':4,
                            'EURCAD':1,'GBPCAD':2,'AUDCAD':3,'NZDCAD':4,'USDCAD':5,
                            'EURCHF':1,'GBPCHF':2,'AUDCHF':3,'NZDCHF':4,'USDCHF':5,'CADCHF':6,
                            'EURJPY':1,'GBPJPY':2,'AUDJPY':3,'NZDJPY':4,'USDJPY':5,'CADJPY':6,'CHFJPY':7,
                                                                                   'JPN225':6,
                                                                                   'XAUUSD':6}
        return currency_layout_no[currencyname]

    def __get_timeframe_layout_no(self,timeframe):
        timeframe_layout_no={'MN':0, 'W1':0,'D1':0,'H4':1,'H1':0,'M30':0}
        return timeframe_layout_no[self.timeframe]

    # チャートウィンドウの座標(LEFT,TOP,RIGHT,BOTTOM)を返す
    # currency_klayout_no: 通貨レイアウト番号
    # timeframe_layout_no: 通時間足レイアウト番号
    def __get_left_top_right_bottom_info(self,mt4, currency_layout_no, timeframe_layout_no):
        MT4_TATE=mt4.TATE
        MT4_YOKO=mt4.YOKO
        TATE_3=MT4_TATE/3  #312
        TATE_4=MT4_TATE/4  #234
        YOKO_D1_H4=1916/4
        if currency_layout_no<=3:
            TOP=TATE_3*(currency_layout_no-1)
            BOTTOM=TATE_3*(currency_layout_no)
            LEFT=YOKO_D1_H4*timeframe_layout_no
            RIGHT=YOKO_D1_H4*(timeframe_layout_no+1)
        else:
            TOP=TATE_4*(currency_layout_no-4)
            BOTTOM=TATE_4*(currency_layout_no-3)
            LEFT=MT4_YOKO/2+YOKO_D1_H4*timeframe_layout_no
            RIGHT=MT4_YOKO/2+YOKO_D1_H4*(timeframe_layout_no+1)
        return int(LEFT),int(TOP),int(RIGHT),int(BOTTOM)



# -

# Concrete
class Layout_21Cross(LayoutParameters):
    pass


# +
# Concrete
class Layout_28Cross(LayoutParameters):
    def __init__(self, mt4, currencyname, timeframe="H4", order_name="1st_currency"):
        self.mt4 = mt4
        self.order_name = order_name
        self.currencyname = currencyname
        self.timeframe = timeframe

    def main_dic(self):
        left,top,right,bottom=self.__get_left_top_right_bottom_info(self.mt4, self.__get_currency_layout_no()[self.currencyname])
        
        main_parameter_dic={}
        if self.__get_currency_layout_no()[self.currencyname] in [17,18,19,20,12]:
            background_color='16775408'
        elif self.__get_currency_layout_no()[self.currencyname] in [21,22,23,24,8,7]:
            background_color='15794175'
        elif self.__get_currency_layout_no()[self.currencyname] in [25,26,27,28,4,3,2]:
            background_color='16449525'
        else:
            background_color='16777215'
    
        if self.currencyname=='JPN225':
            main_parameter_dic={'window_left':str(left),'window_top':str(top),'window_right':str(right),
                                'window_bottom':str(bottom),'background_color':'15136253'}        
        elif self.currencyname=='XAUUSD':
            main_parameter_dic={'window_left':str(left),'window_top':str(top),'window_right':str(right),
                                'window_bottom':str(bottom),'background_color':'15136253'}  
        else:
            main_parameter_dic={'window_left':str(left),'window_top':str(top),'window_right':str(right),
                                'window_bottom':str(bottom),'background_color':background_color}
        return main_parameter_dic

    def object_dic(self):
        import datetime
        from MT4_common_lib import mt4_lib as mt
        
        object_parameter_dic={}
        object_parameter_dic={'StampText':{'period_flags':mt.object_display_timeframe_dic()[self.timeframe]},
                              'TesterLine':{'selectable':'0','time_0':mt.get_VTchart_date_parameter(datetime.datetime.now())},
                              'H4 Trendline':{'period_flags':mt.object_display_timeframe_dic()['H4-']},
                              'Daily Trendline':{'period_flags':mt.object_display_timeframe_dic()['D1-']},
                              'Weekly Trendline':{'period_flags':mt.object_display_timeframe_dic()['W1-']}}
        return object_parameter_dic

    def indicator_dic(self):
        indicator_parameter_dic={}
        indicator_parameter_dic={'CustomCandle2':{'yousen_color':'15453831','insen_color':'12695295','even_color':'13959039',
                                                  'yousen_color2':'13959039','insen_color2':'14804223','even_color2':'65280',
                                                  'candle_type':'3','hige_width':'2',
                                                  'iuse_lock_tf':'true','ilock_tf_h04':'17','ilock_tf_d01':'18','ilock_tf_w01':'19'},
                                 'CustomCandleTester':{'yousen_color':'15453831','insen_color':'12695295','even_color':'13959039',
                                                  'yousen_color2':'13959039','insen_color2':'14804223','even_color2':'65280',
                                                  'candle_type':'3','hige_width':'2',
                                                  'iuse_lock_tf':'true','ilock_tf_h04':'17','ilock_tf_d01':'18','ilock_tf_w01':'19'},
                                 'VT_Chart':{'jpn_flag':'true','offset_time':'1','xshift':'5'}}  
        return indicator_parameter_dic

#################################### 共通ライブラリ系 ####################################
    # 通貨ペア文字列→レイアウト番号(1～28)を返す
    def __get_currency_layout_no(self):
        return {'EURGBP':1,'EURAUD':5,'EURNZD': 9,'EURUSD':13,'EURCAD':17,'EURCHF':21,'EURJPY':25,
                            'GBPAUD':6,'GBPNZD':10,'GBPUSD':14,'GBPCAD':18,'GBPCHF':22,'GBPJPY':26,
                                       'AUDNZD':11,'AUDUSD':15,'AUDCAD':19,'AUDCHF':23,'AUDJPY':27,
                                                   'NZDUSD':16,'NZDCAD':20,'NZDCHF':24,'NZDJPY':28,
                                                               'USDCAD':12,'USDCHF':8 ,'USDJPY': 4,
                                                                           'CADCHF':7 ,'CADJPY': 3,
                                                                                       'CHFJPY': 2,
                                                                           'JPN225':7 ,'XAUUSD': 7}


    # チャートウィンドウの座標(LEFT,TOP,RIGHT,BOTTOM)を返す
    # currency_klayout_no: 通貨レイアウト番号
    def __get_left_top_right_bottom_info(self, mt4, currency_layout_no):
        MT4_TATE=mt4.TATE
        MT4_YOKO=mt4.YOKO
        TATE_4=MT4_TATE/4  #234
        YOKO_7=int(MT4_YOKO/7)  #274
        
        TOP=TATE_4*((currency_layout_no-1)%4)
        BOTTOM=TATE_4*((currency_layout_no-1)%4+1)
        LEFT=YOKO_7*((currency_layout_no-1)//4)
        RIGHT=YOKO_7*((currency_layout_no-1)//4+1)
        return int(LEFT),int(TOP),int(RIGHT),int(BOTTOM)
    
# -

# Concrete
class Layout_35Cross(LayoutParameters):
    pass


