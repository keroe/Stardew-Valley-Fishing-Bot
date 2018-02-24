from datetime import date, timedelta

days = dict()

for i in range(1, 7):
	day_name = 'day_{}'.format(i)
	day = date.today()-timedelta(days=(i-1))
	days[day_name] = day

days2 = {y:x for x,y in days.items()}

print(days)