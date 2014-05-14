import matplotlib.pyplot as plt; plt.rcdefaults()

# Divya and Eunkwang to provide [precision, recall, accuracy] for each of their 8 results.
# This script will graph the models against each other and select the best model.

TEST_DATA = [[0.4,0.6,0.8] , [0.5,0.3,0.69], [0.8, 0.2, 0.75], [0.3, 0.9, 0.72], [0.8, 0.95, 0.9]]

def calc_f1_score(precision, recall, accuracy):
	return (float(2 * (precision * recall) / (precision + recall)))

precision_array = []
recall_array = []
best_f1 = 0.00000000000000000
index = 0

for each in TEST_DATA:
	precision_array.append(each[0])
	recall_array.append(each[1])
	
	f1 = calc_f1_score(each[0], each[1], each[2])
	#print f1
	if(f1 > best_f1):
		best_f1 = f1
		best_index = index
	index +=1

print "The Best Model is: Model " + str(best_index)

fig = plt.subplot(111)
fig.scatter(precision_array, recall_array)
fig.set_xlabel('Recall')
fig.set_ylabel('Precision')

plt.show()