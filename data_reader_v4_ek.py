#
# data_reader_v4_ek.py
# author: eunkwang joo
# description: This code prepares dataset for logistic regression algorithm, which is written by myself.
#


import csv
import pickle
import time
import os
from boto.s3.connection import S3Connection
from boto.s3.key import Key


timestr = time.strftime("%Y%m%d-%H%M%S")
print timestr

needed_cols = [1, 2, 3, 4, 8, 10, 15, 16, 17]
years = [2001, 2002, 2003, 2004, 2005, 2006, 2007, 2008]
j = 0

#
# function: ComputeDayofYear()
# description: This function will return an integer to represent the day of the year given an integer
#    representing month and an integer representing the day of the month.  This number will
#    correspond to the ordered day of the year [0-365].  For instance, Jan 1st will be returned
#    as 0.  Feb 29th will be returned as 59.
# input: row of csv file, a raw dataset
# output: row of csv file, date of year value of which is encoded.
#


def ComputeDayofYear(row):
    if(row[0] == '1'):
        calc = 0 + int(row[1]) - 1
        row[1] = str(calc)
    elif(row[0] == '2'):
        calc = 31 + int(row[1]) - 1
        row[1] = str(calc)
    elif(row[0] == '3'):
        calc = 60 + int(row[1]) - 1
        row[1] = str(calc)
    elif(row[0] == '4'):
        calc = 91 + int(row[1]) - 1
        row[1] = str(calc)
    elif(row[0] == '5'):
        calc = 121 + int(row[1]) - 1
        row[1] = str(calc)
    elif(row[0] == '6'):
        calc = 152 + int(row[1]) - 1
        row[1] = str(calc)
    elif(row[0] == '7'):
        calc = 182 + int(row[1]) - 1
        row[1] = str(calc)
    elif(row[0] == '8'):
        calc = 213 + int(row[1]) - 1
        row[1] = str(calc)
    elif(row[0] == '9'):
        calc = 244 + int(row[1]) - 1
        row[1] = str(calc)
    elif(row[0] == '10'):
        calc = 274 + int(row[1]) - 1
        row[1] = str(calc)
    elif(row[0] == '11'):
        calc = 305 + int(row[1]) - 1
        row[1] = str(calc)
    elif(row[0] == '12'):
        calc = 335 + int(row[1]) - 1
        row[1] = str(calc)
    return row


#
# function: DiscretizeDepTime()
# description: This function takes a scheduled departure time, classifies the departure time as:
#    morning (0700 - 1259), afternoon (1300 - 1759), or evening (1800-0659).  The input value
#    is assumed to be an integer in 24-hour time format.  These labels will correspond to
#    variable values of 0 = morning, 1 = afternoon, 2 = evening.  The value is then returned.
#    An error time is returned as morning.
# input: row of csv file, a raw dataset
# output: row of csv file, departure time value of which is encoded.
#

def DiscretizeDepTime(row):

    if(int(row[3]) <= 559):
        row[3] = '2'
    elif(int(row[3]) >= 600 and int(row[3]) <= 1259):
        row[3] = '0'
    elif(int(row[3]) >= 1300 and int(row[3]) <= 1759):
        row[3] = '1'
    elif(int(row[3]) >= 1800):
        row[3] = '2'
    else:
        row[3] = '0'
    return row

#
# function: AddDepVar()
# description: This function adds a classification label based on the length of the recorded
#    Departure Delay in the data set.  It assumes an input integer value of the delay in mins.
#    By airline industry standards, flight delays are defined as departure delays greater than
#    or equal to 15 minutes.  For delayed flights, this variable will have value "1".
#    For on time flights, it will have value "0".  Default value will be set at "0".
# input: row of csv file, a raw dataset
# output: row of csv file, delay value of which is encoded as binary.
#


def AddDepVar(row):

    if(row[6] >= '15'):
        row[6] = '1'
    else:
        row[6] = '0'
    return row

#
# function: SaveData()
# description: This function pickles each file. Also, due to the lack of storage space on local server, it stores data to S3 server as well.
# input: data= data structure which will be stored for future uses
#        pickle_file_name= file name to be used to store data
# output: null
#


def SaveData(data, pickle_file_name):

    f = open(pickle_file_name, "wb")
    try:
        pickle.dump(data, f, protocol=pickle.HIGHEST_PROTOCOL)
    except Exception as e:
        print e
    f.close()

    conn = S3Connection(
        'AKIAJ3S6FFCVZ7NZPPPA', 'egDauV1C6HY3Q31tjpQg4IiMwSq/Sm4ATASYVl+7')
    bucket = conn.get_bucket('i290-aero')
    k = Key(bucket)
    k.key = pickle_file_name
    k.set_contents_from_filename(pickle_file_name)

    os.remove(pickle_file_name)


# it reads raw datset of every year, encodes variables, drop unused
# variables, and pickle trimmed dataset in file system.

for i in years:
    data = []
    '''
    conn = S3Connection('AKIAJ3S6FFCVZ7NZPPPA', 'egDauV1C6HY3Q31tjpQg4IiMwSq/Sm4ATASYVl+7')
    bucket = conn.get_bucket('i290-aero')
    k = Key(bucket)
    k.key = 'data2001.csv'
    file_path = k.get_contents_as_string()
    '''
    file_path = 'data' + str(i) + '.csv'
    pickle_file_name = timestr + '-data-' + str(i)
    with open(file_path, 'r') as data_csv:
        csv_reader = csv.reader(data_csv, delimiter=',')
        j = 0
        for row in csv_reader:
            # and j<80000000: #and (row[16] == 'SFO' or row[16] == 'OAK'):
            if row[21] == '0':
#                 if (row[16] == 'SFO' or row[16] == 'OAK'):
                    content = [row[i] for i in needed_cols]
                    content2 = ComputeDayofYear(content)
                    content3 = DiscretizeDepTime(content2)
                    content4 = AddDepVar(content3)
                    data.append(content4)
                    # print 'content4', content4
                    # print 'data', data
                    # fff = raw_input()
                    j = j + 1
                    if j % 2000000 == 0:
                        print j
                        SaveData(data, pickle_file_name + '-' + str(j))
                        data = []
    SaveData(data, pickle_file_name)
