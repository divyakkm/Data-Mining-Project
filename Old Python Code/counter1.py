import csv

with open('C:\\Dropbox\\Naive Bayes\\_dfTest2008\\_dfTest2008.csv', 'r') as data:
    csv_reader = csv.reader(data, delimiter=',')
    SFO_count = 0
    OAK_count = 0
    for row in csv_reader:
        origin = row[7]
        if(origin == '270'):
            SFO_count += 1
        elif(origin == '215'):
            OAK_count += 1
        else:
            continue

print OAK_count
print SFO_count
