import csv
import pickle

needed_cols = [1, 2, 3, 4, 8, 10, 15, 16, 17]
years = [2008]

def ComputeDayofYear(row):
    """This function will return an integer to represent the day of the year given an integer
    representing month and an integer representing the day of the month.  This number will
    correspond to the ordered day of the year [0-365].  For instance, Jan 1st will be returned
    as 0.  Feb 29th will be returned as 59."""

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


def DiscretizeDepTime(row):
    """This function takes a scheduled departure time, classifies the departure time as:
    morning (0700 - 1259), afternoon (1300 - 1759), or evening (1800-0659).  The input value
    is assumed to be an integer in 24-hour time format.  These labels will correspond to
    variable values of 0 = morning, 1 = afternoon, 2 = evening.  The value is then returned.
    An error time is returned as morning."""

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


def AddDepVar(row):
    """This function adds a classification label based on the length of the recorded
    Departure Delay in the data set.  It assumes an input integer value of the delay in mins.
    By airline industry standards, flight delays are defined as departure delays greater than
    or equal to 15 minutes.  For delayed flights, this variable will have value "1".
    For on time flights, it will have value "0".  Default value will be set at "0"."""

    if(row[6] >= '15'):
        row[6] = '1'
    else:
        row[6] = '0'
    return row

def SaveData(data, pickle_file_name):
    """This function pickles each file."""

    f = open (pickle_file_name, "w")
    pickle.dump(data, f)
    f.close()



for i in years:
    data = []
    file_path='C:\data\airline' + str(i) + '.csv'
    pickle_file_name = 'data' + str(i)
    with open(file_path, 'r') as data_csv:
        csv_reader = csv.reader(data_csv, delimiter=',')
        for row in list(csv_reader):
            if row[21] == '0':
                if (row[16] == 'SFO' or row[16] == 'OAK'):
                    content = list(row[i] for i in needed_cols)
                    content2 = ComputeDayofYear(content)
                    content3 = DiscretizeDepTime(content2)
                    content4 = AddDepVar(content3)
                    data.append(content4)
    SaveData(data, pickle_file_name)


