# import matplotlib.pyplot as plt
import numpy as np
import random
import pickle
import sys

def loadData(fileName):
	x = pickle.load(open(fileName, "rb"))
	y = x[:, -1:].copy() # last col is y value (delay or not)
	x[:, -1:] = 1.
	return x, y

def gradientDescent(x, y, numIterations, dimension):
	theta = np.zeros(dimension)[np.newaxis].transpose()
	for i in range(1, numIterations):
		randIdx = random.randint(0, len(x) - 1)
		xTrans = x[randIdx][np.newaxis].transpose()
		u = 1 / (1 + np.exp(np.dot(theta.transpose() * (-1), xTrans)))
		loss = y[randIdx] - u
		gradient = np.dot(loss[0][0], xTrans)
		# update
		theta = theta + gradient / i
	return theta

def graph(formula, x_range):  
	x = np.array(x_range)  
	y = eval(formula)
	plt.plot(x, y)


# def getData(fileName):
# 	f = open(fileName, 'r')
# 	x = np.array([0,0,0])
# 	x0 = []
# 	x1 = []
# 	y = np.array([0])
# 	for line in f:
# 		arr = line.strip().split(' ')
# 		x = np.vstack((x, [float(arr[0]), float(arr[1]), 1.]))
# 		y = np.vstack((y, [float(arr[2])]))
# 		if arr[2] == '0':
# 			x0.append((float(arr[0]), float(arr[1])))
# 		else:
# 			x1.append((float(arr[0]), float(arr[1])))

# 	x = np.delete(x, 0, 0)
# 	y = np.delete(y, 0, 0)
# 	f.close()

# 	return x, x0, x1, y




def main():
	arg = sys.argv
	if len(arg) < 2:
		print 'USE: $ python logisticRegression.py [dataset_file]'
		return
	x, y = loadData(arg[1])

	# x, x0, x1, y = getData('classification.dat')
	print 'x shape ', x.shape

	theta = gradientDescent(x, y, 100000, x.shape[1])
	# # print theta
	# graph('(-1) * theta[2][0] / theta[1][0] - (theta[0][0] / theta[1][0]) * x', range(-3, 5))
	print 'asdf'



if __name__ == '__main__':
	main()