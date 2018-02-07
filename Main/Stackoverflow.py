import re

string = 'Tracking Identification Number...1Z000000YW00000000\nasdasdasd'

no_dots = re.sub('\.', '', string) #Removes all points from the string

matchObj = re.search('^Tracking Identification Number(.*)', no_dots) #Matches anything after the "Tracking Identification Number"

try:
   print (matchObj.group(1))
except:
	print("No match!")