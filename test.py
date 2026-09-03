from datetime import date, timedelta


# Add one day to get tomorrow
tomorrow = date.today() + timedelta(days=1)

print(tomorrow)