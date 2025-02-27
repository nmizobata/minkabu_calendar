import googlecalendar_lib as gcalendar

calendar = gcalendar.GoogleCalendar()
df = calendar.get_googlecalendar()
calendar.remove_googlecalendar(df)
df = calendar.get_googlecalendar()
print(df)
