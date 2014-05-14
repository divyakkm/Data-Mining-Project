import csv

with open('C:\\Dropbox\\Naive Bayes\\Analysis1.csv', 'r') as data:
    csv_reader = csv.reader(data, delimiter=',')
    SFO_count = 0
    OAK_count = 0
    for row in csv_reader:
        origin = row[1]
        if(origin == '270'):
            SFO_count += int(row[3])
        elif(origin == '215'):
            OAK_count += int(row[3])
        else:
            continue

print OAK_count
print SFO_count
