#
# date_graph2.py
# Author: Ryan Jung
# Description: This function takes a date and calculates the probability of delay at SFO
# and at OAK for the date and the 6 days prior.  It then graphs these probabilities as
# side-by-side bars for each day.
# Dependencies:  Run the Naive Bayes classification code in Crossval_r.py file. Ensure that the file _dfTest2008.csv is in the
# same folder.
#

from __future__ import division
import sys
import csv
import datetime
import matplotlib.pyplot as plt
plt.rcdefaults()
import numpy as np

#
# These are the hard codes of the "look back" period (set at 6 days) and airport codes
# from our Naive Bayes dictionary.
#

TIME_DELTA = 6
SFO_AIRPORT_CODE = '270'
OAK_AIRPORT_CODE = '215'
JFK_AIRPORT_CODE = '160'
ORD_AIRPORT_CODE = '225'
ATL_AIRPORT_CODE = '25'
LAX_AIRPORT_CODE = '168'
LGA_AIRPORT_CODE = '174'
DFW_AIRPORT_CODE = '85'

#
# Main Function
# The function first takes an argument from the command line of the form:
#			python date_graph2.py m-d-yy
# It then calculates the bounds of our query for probability of delay by day.
#

for arg in sys.argv:
    if(arg != 'date_graph2.py'):
        start_date = datetime.datetime.strptime(arg, '%m-%d-%y')
        start_date = datetime.date(
            start_date.year, start_date.month, start_date.day)

delta = datetime.timedelta(days=TIME_DELTA)
begin = start_date - delta
end = start_date

#
# This block of code sets up a hash for each airport of the form {key: value} => {day:
# [predict label,...]}.  This is a list of the predicted labels for each flight on a
# particular day from the origin airport to the destination airport.  It iterates over
# the days in our query range and constructs the hash.
#

SFO_Hash = {}
OAK_Hash = {}
with open('_dfTest2008.csv', 'r') as data:
    csv_reader = csv.reader(data, delimiter=',')
    for row in csv_reader:
        if(row[0] != 'Year'):
            year = int(row[0])
            month = int(row[1])
            date = int(row[2])
            curr_date = datetime.date(year, month, date)
            if(curr_date >= begin and curr_date <= end):
                origin = row[7]
                dest = row[8]
                if(origin == SFO_AIRPORT_CODE and dest == LAX_AIRPORT_CODE):
                    label = int(row[10])
                    if(curr_date not in SFO_Hash):
                        SFO_Hash[curr_date] = [label]
                    else:
                        SFO_Hash[curr_date].append(label)
                if(origin == OAK_AIRPORT_CODE and dest == LAX_AIRPORT_CODE):
                    label = int(row[10])
                    if(curr_date not in OAK_Hash):
                        OAK_Hash[curr_date] = [label]
                    else:
                        OAK_Hash[curr_date].append(label)

#
# This block of code initializes values for day "steps" for our iterator later.
# We also initialize lists which will have the number of delays, on-time flights, and
# percentage of predicted delays for the days in our query.
#

iterator = datetime.timedelta(days=1)
two_iterator = datetime.timedelta(days=2)
three_iterator = datetime.timedelta(days=3)
four_iterator = datetime.timedelta(days=4)
five_iterator = datetime.timedelta(days=5)
six_iterator = datetime.timedelta(days=6)

day_values = []
SFO_Delays = []
SFO_On_Time = []
SFO_Flights = []
SFO_Pct = []
SFO_Comp = []
OAK_Delays = []
OAK_On_Time = []
OAK_Flights = []
OAK_Pct = []
OAK_Comp = []

#
# We then loop through the query date range and populate the lists, counting number of
# delayed flights, number of on-time flights, and percent of flights delayed.  Each
# list item corresponds to a date in our query range.
#

while begin <= end:
    if(begin not in SFO_Hash):
        SFO_Delays.append(0)
        SFO_On_Time.append(0)
        SFO_Pct.append(0.00)
    else:
        SFO_Flights = SFO_Hash[begin]
        delays = sum(SFO_Flights)
        num_flights = len(SFO_Flights)
        pct = float(delays) / (num_flights + delays)
        SFO_Delays.append(delays)
        SFO_On_Time.append(num_flights - delays)
        SFO_Pct.append(pct)
        SFO_Comp.append(1)

    if(begin not in OAK_Hash):
        OAK_Delays.append(0)
        OAK_On_Time.append(0)
        OAK_Pct.append(0.00)
    else:
        OAK_Flights = OAK_Hash[begin]
        delays = sum(OAK_Flights)
        num_flights = len(OAK_Flights)
        pct = float(delays) / (num_flights + delays)
        OAK_Delays.append(delays)
        OAK_On_Time.append(num_flights - delays)
        OAK_Pct.append(pct)
        OAK_Comp.append(1)

    day_values.append(begin)
    begin += iterator

#
# This block of code then graphs the percentage of delays by day as a side-by-side bar
# graph for each day in the query.
#

Y1 = SFO_Pct
Y2 = OAK_Pct
Y3 = SFO_Comp
Y4 = OAK_Comp

N = 7
ind = np.arange(N)  # the x locations for the groups
width = 0.35       # the width of the bars

fig, ax = plt.subplots()
rects1 = ax.bar(ind, Y1, width, color='blue')
rects2 = ax.bar(ind + width, Y2, width, color='grey')

fig.suptitle(
    'Probability of Flight Delays at SFO vs. OAK Given Specific Date Through t-7 Days')
ax.legend((rects1[0], rects2[0]), ('SFO', 'OAK'), loc='upper center')


def autolabel(rects):
    for rect in rects:
        height = rect.get_height()
        ax.text(
            rect.get_x() + rect.get_width() /
            2., 1.05 * height, '%.2f' % float(height),
            ha='center', va='bottom', rotation='vertical')

autolabel(rects1)
autolabel(rects2)
ax.set_xticklabels(
    [start_date - six_iterator, start_date - five_iterator, start_date - four_iterator,
     start_date - three_iterator, start_date - two_iterator, start_date - iterator, start_date], rotation=45)
ax.set_ylabel('Probability of Delay')

plt.show()
