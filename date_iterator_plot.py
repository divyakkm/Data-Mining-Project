import datetime
import csv
import random
import matplotlib.pyplot as plt; plt.rcdefaults()

# Eunkwang data:  SFO = 1; OAK = 2
# Divya data: SFO = 136; OAK = 141

# Need to change row indexes to make sure they match data from Eunkwang.

'''with open('EunkwangSampleData.csv', 'r') as data:
	csv_reader = csv.reader(data, delimiter=',')
	SFO_EJ_Hash = {}
	OAK_EJ_Hash = {}
	for row in csv_reader:
		origin = row[8]
		if(origin == '1'):
			year = int(row[0])
			month = int(row[1])
			date = int(row[2])
			key = datetime.date(year, month, date)
			label = int(row[9])
			if(key not in SFO_EJ_Hash):
				SFO_EJ_Hash[key] = [label]
			else:
				SFO_EJ_Hash[key].append(label)
		elif(origin == '2'):
			year = int(row[0])
			month = int(row[1])
			date = int(row[2])
			key = datetime.date(year, month, date)
			label = int(row[9])
			if(key not in OAK_EJ_Hash):
				OAK_EJ_Hash[key] = [label]
			else:
				OAK_EJ_Hash[key].append(label)
		else:
			continue'''		

with open('DivyaSampleData.csv', 'r') as data:
	csv_reader = csv.reader(data, delimiter=',')
	SFO_DM_Hash = {}
	OAK_DM_Hash = {}
	for row in csv_reader:
		origin = row[8]
		if(origin == '136'):
			year = int(row[0])
			month = int(row[1])
			date = int(row[2])
			key = datetime.date(year, month, date)
			label = int(row[9])
			if(key not in SFO_DM_Hash):
				SFO_DM_Hash[key] = [label]
			else:
				SFO_DM_Hash[key].append(label)
		elif(origin == '141'):
			year = int(row[0])
			month = int(row[1])
			date = int(row[2])
			key = datetime.date(year, month, date)
			label = int(row[9])
			if(key not in OAK_DM_Hash):
				OAK_DM_Hash[key] = [label]
			else:
				OAK_DM_Hash[key].append(label)
		else:
			continue				

start_date = datetime.date(2008, 1, 1)
end_date = datetime.date(2008, 1,31)
date_values = []
SFO_DM_Delays = []
SFO_DM_On_Time = []
OAK_DM_Delays = []
OAK_DM_On_Time = []
SFO_EJ_Delays = []
SFO_EJ_On_Time = []
OAK_EJ_Delays = []
OAK_EJ_On_Time = []

d = start_date
delta = datetime.timedelta(days=1)
while d <= end_date:
	'''if(d not in SFO_EJ_Hash):
		SFO_EJ_Values.append([0,0])
	else:
		SFO_EJ_Flights = SFO_EJ_Hash[d]
		delays = sum(SFO_EJ_Flights)
		num_flights = len(SFO_EJ_Flights)
		SFO_EJ_Delays.append(delays)
		SFO_EJ_On_Time.append(num_flights - delays)
	
	if(d not in OAK_EJ_Hash):
		OAK_EJ_Values.append([0,0])
	else:
		OAK_EJ_Flights = OAK_EJ_Hash[d]
		delays = sum(OAK_EJ_Flights)
		num_flights = len(OAK_EJ_Flights)
		OAK_EJ_Delays.append(delays)
		OAK_EJ_On_Time.append(num_flights - delays)'''
	
	if(d not in SFO_DM_Hash):
		SFO_DM_Values.append([0,0])
	else:
		SFO_DM_Flights = SFO_DM_Hash[d]
		delays = sum(SFO_DM_Flights)
		num_flights = len(SFO_DM_Flights)
		SFO_DM_Delays.append(delays)
		SFO_DM_On_Time.append(num_flights - delays)
	
	if(d not in OAK_DM_Hash):
		OAK_DM_Values.append([0,0])
	else:
		OAK_DM_Flights = OAK_DM_Hash[d]
		delays = sum(OAK_DM_Flights)
		num_flights = len(OAK_DM_Flights)
		OAK_DM_Delays.append(delays)
		OAK_DM_On_Time.append(num_flights - delays)
	
	date_values.append(d)
	d += delta

plt.title('Probability of Flight Delays at SFO vs. OAK')

ax1 = plt.subplot(211)
ax1.bar(date_values, SFO_DM_Delays, bottom = SFO_DM_On_Time, color = 'green')
ax1.bar(date_values, SFO_DM_On_Time, color = 'blue')
ax1.set_xticklabels(['Jan 1 2008', '', '', '', '', '', '','','','','','','','','Jan 15 2008', '','','','','','','','','','','','','','','','Jan 31 2008'])
#ax1.set_xticklabels(['Jan 2008','','','','','Jun 2008','','','','','','Dec 2008'])
ax1.set_yticks([0, 50, 100])
ax1.set_title('On-Time Flights and Delayed Flights at SFO')

ax2 = plt.subplot(212)
ax2.bar(date_values, OAK_DM_Delays, bottom = OAK_DM_On_Time, color = 'red')
ax2.bar(date_values, OAK_DM_On_Time, color = 'grey')
ax2.set_xticklabels(['Jan 1 2008', '', '', '', '', '', '','','','','','','','','Jan 15 2008', '','','','','','','','','','','','','','','','Jan 31 2008'])
#ax2.set_xticklabels(['Jan 2008','','','','','Jun 2008','','','','','','Dec 2008'])
ax2.set_yticks([0, 50, 100])
ax2.set_title('On-Time Flights and Delayed Flights at OAK')

plt.show()