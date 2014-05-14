#
# model_selector.py
# Author:  Ryan Jung
# Description:  This script graphs the results of validation tests with precision on the
# y-axis and recall on the x-axis.
# Because we only used 8-fold validation for the Naive Bayes model, this model is only
# used for the testing results of that validation.
#

import matplotlib.pyplot as plt
plt.rcdefaults()

# Hard code of testing results of form [precision, recall, accuracy, title]
DM_TEST_DATA = [
    [0.59, 0.61, 0.61, 'NB 2008'], [0.60, 0.61, 0.60, 'NB 2007'], [
        0.60, 0.63, 0.62, 'NB 2006'], [0.62, 0.64, 0.64, 'NB 2005'],
    [0.63, 0.66, 0.66, 'NB 2004'], [0.65, 0.70, 0.70, 'NB 2003'], [0.60, 0.65, 0.65, 'NB 2002'], [0.58, 0.62, 0.61, 'NB 2001']]

#
# Function: calc_f1_score(precision, recall, accuracy)
# Description: This function calculates the F1 score = 2*(precision * recall) / (precision + recall)
# Input: Floating point values of precision, recall, and accuracy (not used)
# Output: Floating point F1 score
#


def calc_f1_score(precision, recall, accuracy):
    return (float(2 * (precision * recall) / (precision + recall)))

#
# Main Function
# Description: Creates array of precision and array of recall values.  Uses best values to
# track highest F1 score and title of test with best result.
#

precision_dm_array = []
recall_dm_array = []
dm_best_f1 = 0.00000000000000000
index = 0
dm_best_title = 'None'

for each in DM_TEST_DATA:
    precision_dm_array.append(each[0])
    recall_dm_array.append(each[1])

    f1 = calc_f1_score(each[0], each[1], each[2])
    if(f1 > dm_best_f1):
        dm_best_f1 = f1
        best_index = index
        dm_best_title = each[3]
    index += 1

# prints title of Best performing model by F1 score
# print "The Best Naive Bayes Model is: Model " + str(dm_best_title)

# Scatter plot visualization of results with precision on y-axis and
# recall on x-axis
fig = plt.subplot(111)
fig.scatter(precision_dm_array, recall_dm_array, color='blue')
fig.set_xlabel('Recall')
fig.set_ylabel('Precision')

plt.show()
