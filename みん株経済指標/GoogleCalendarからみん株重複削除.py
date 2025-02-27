# みん株 経済指標スケジュール、Google Calendarに重複登録されているアイテムを削除
# 20241224 ver1.0 みん株 経済指標スケジュール ver1.4よりモジュールを分離
# 20250227 ver2.0 新構成で作成。

import googlecalendar_lib as googlecalendar

calendar = googlecalendar.GoogleCalendar()
df_currentdata = calendar.get_googlecalendar()
df_currentdata['duplicated']=df_currentdata.duplicated(subset=['start','end','event'])
calendar.remove_googlecalendar(df_currentdata.loc[df_currentdata["dupulicated"]])
