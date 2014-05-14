#
# date_iterator_plot2.py
# Author: Ryan Jung
# Description: This function reads the predicted results from one of our models.  It then
# aggregates the probability of delay by week and graphs the probability of delay at
# both airports (SFO and OAK).  Lastly, it calculates the t-score of the difference in
# means of both airports to help determine if the difference is statistically significant.
#

import datetime
import csv
import matplotlib.pyplot as plt
plt.rcdefaults()
import numpy

# Hard code of airport codes in our dictionary that correspond to Naive
# Bayes model
SFO_AIRPORT_CODE = '270'
OAK_AIRPORT_CODE = '215'

#
# Function: ComputeDayofYear(month, day)
# Description: This function takes a month and day of month and outputs a number which
# corresponds to the day of year.  This will be a number between 0 and 365.
# Input: Integer values for month and day
# Output: Integer value for day of year
#


def ComputeDayofYear(month, day):
    if(month == 1):
        numDays = 0
    if(month == 2):
        numDays = 31
    if(month == 3):
        numDays = 60
    if(month == 4):
        numDays = 91
    if(month == 5):
        numDays = 121
    if(month == 6):
        numDays = 152
    if(month == 7):
        numDays = 182
    if(month == 8):
        numDays = 213
    if(month == 9):
        numDays = 244
    if(month == 10):
        numDays = 274
    if(month == 11):
        numDays = 305
    if(month == 12):
        numDays = 335

    return (numDays + day - 1)

#
# Main Function
# This block of code reads from the output of the Naive Bayes model and creates a hash
# for SFO and OAK that corresponds to {key: value} = {week #: [predicted label,...]}.
# The idea here is to create a list of all flights that are scheduled to leave SFO or OAK
# by week (52 weeks in the year).  The list will be 1's and 0's based on our prediction of
# whether the flight will be delayed (1) or not delayed (0).
#

with open('_dfTest2008.csv', 'r') as data:
    csv_reader = csv.reader(data, delimiter=',')
    SFO_DM_Hash = {}
    OAK_DM_Hash = {}
    for row in csv_reader:
        origin = row[7]
        if(origin == SFO_AIRPORT_CODE):
            month = int(row[1])
            date = int(row[2])
            DayofYear = ComputeDayofYear(month, date)
            key = DayofYear / 7
            label = int(row[10])
            if(key not in SFO_DM_Hash):
                SFO_DM_Hash[key] = [label]
            else:
                SFO_DM_Hash[key].append(label)
        elif(origin == OAK_AIRPORT_CODE):
            month = int(row[1])
            date = int(row[2])
            DayofYear = ComputeDayofYear(month, date)
            key = DayofYear / 7
            label = int(row[10])
            if(key not in OAK_DM_Hash):
                OAK_DM_Hash[key] = [label]
            else:
                OAK_DM_Hash[key].append(label)
        else:
            continue

#
# This block of code separates out the value list of flights from the previous block of
# code into a list of the number of delays and the number of on-time flights from SFO
# and OAK by week.  In other words, SFO_DM_Delays[14] will be the number of delayed
# flights we predict at SFO in week 14.  We create a 3rd list which is the percent of
# flights that are delayed by week.
#

week_values = []
SFO_DM_Delays = []
SFO_DM_On_Time = []
SFO_DM_Pct = []
OAK_DM_Delays = []
OAK_DM_On_Time = []
OAK_DM_Pct = []

d = 0
while d <= 51:
    if(d not in SFO_DM_Hash):
        SFO_DM_Delays.append(0)
        SFO_DM_On_Time.append(0)
        SFO_DM_Pct.append(0.00)
    else:
        SFO_DM_Flights = SFO_DM_Hash[d]
        delays = sum(SFO_DM_Flights)
        num_flights = len(SFO_DM_Flights)
        pct = float(delays) / (num_flights + delays)
        SFO_DM_Delays.append(delays)
        SFO_DM_On_Time.append(num_flights - delays)
        SFO_DM_Pct.append(pct)

    if(d not in OAK_DM_Hash):
        OAK_DM_Delays.append(0)
        OAK_DM_On_Time.append(0)
        OAK_DM_Pct.append(0.00)
    else:
        OAK_DM_Flights = OAK_DM_Hash[d]
        delays = sum(OAK_DM_Flights)
        num_flights = len(OAK_DM_Flights)
        pct = float(delays) / (num_flights + delays)
        OAK_DM_Delays.append(delays)
        OAK_DM_On_Time.append(num_flights - delays)
        OAK_DM_Pct.append(pct)

    week_values.append(d)
    d += 1

#
# This block of code calculates the mean and standard deviation of the percent of flights
# that are predicted to be delayed.  It uses these to calculate a t-score of the
# difference in means which can be used to determine if the difference is statistically
# significant.
#

SFO_mean = numpy.mean(SFO_DM_Pct)
OAK_mean = sum(OAK_DM_Pct) / len(OAK_DM_Pct)
SFO_std = numpy.std(SFO_DM_Pct)
OAK_std = numpy.std(OAK_DM_Pct)
SFO_n = len(SFO_DM_Pct)
OAK_n = len(OAK_DM_Pct)
Diff = OAK_mean - SFO_mean
std_err = (((SFO_std ** 2) / SFO_n) + ((OAK_std ** 2) / OAK_n)) ** 0.5

print "Standard Error", std_err
print "t = ", Diff / std_err

#
# Graphic visualization of the probability of delay by week at SFO and OAK.  SFO will be
# the green line and OAK will be the blue line in the graph.  X-axis is the week of 2008
# and y-axis is probability of delay.
#

ax1 = plt.subplot(111)
p1 = ax1.plot(week_values, SFO_DM_Pct, color='green')
p2 = ax1.plot(week_values, OAK_DM_Pct, color='blue')
ax1.set_title('Proportion of flights delayed in SFO (green) vs. OAK (blue)')
ax1.set_xticklabels(
    ['Jan 2008', 'Mar 2008', 'May 2008', 'Jul 2008', 'Sep 2008', 'Nov 2008'])
ax1.set_ylabel('Probability of Delay')
ax1.legend((p1[0], p2[0]), ('SFO', 'OAK'), loc='upper center')

plt.show()
