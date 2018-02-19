import numpy as np
import cv2
from sklearn.neighbors import KNeighborsClassifier
from sklearn import svm
from sklearn.neural_network import MLPClassifier

img = cv2.imread('''digits.png''')
#print(img.shape)
gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
#print(gray.shape)

#Split image into 50 rows and each row into 100 column to get a digit
cells = [np.hsplit(row,100) for row in np.vsplit(gray,50)]

x = np.array(cells) #(50, 100, 20, 20)

train = x[:,:50].reshape(-1,400).astype(np.float32) #(2500,400)
test = x[:,50:100].reshape(-1,400).astype(np.float32) #(2500,400)

k = np.arange(10)
train_labels = np.repeat(k,250)
test_labels = np.repeat(k,250)


#Using kNN with n = 5
knn = KNeighborsClassifier(n_neighbors=5)
knn.fit(train, train_labels)
result = knn.predict(test)

matches = result==test_labels
correct = np.count_nonzero(matches)
accuracy = correct*100.0/result.size
print("The accuracy of kNN algorithm with k = 5 is: " + str(accuracy) + "%")

#Using kNN with n = 3
knn = KNeighborsClassifier(n_neighbors=3)
knn.fit(train, train_labels)
result = knn.predict(test)

matches = result==test_labels
correct = np.count_nonzero(matches)
accuracy = correct*100.0/result.size
print("The accuracy of kNN algorithm with k = 3 is: " + str(accuracy) + "%")


#Using kNN with n = 1
knn = KNeighborsClassifier(n_neighbors=1)
knn.fit(train, train_labels)
result = knn.predict(test)

matches = result==test_labels
correct = np.count_nonzero(matches)
accuracy = correct*100.0/result.size
print("The accuracy of kNN algorithm with k = 1 is: " + str(accuracy) + "%")

#Using SVM
vm = svm.LinearSVC()
vm.fit(train, train_labels)
result = vm.predict(test)

matches = result==test_labels
correct = np.count_nonzero(matches)
accuracy = correct*100.0/result.size
print("The accuracy of SVM algorithm is: " + str(accuracy) + "%")

#Using Neural Network: (400,400,10)
nn = MLPClassifier(solver='lbfgs', alpha=1e-5,
                    hidden_layer_sizes=(400), random_state=1)
nn.fit(train, train_labels)
result = nn.predict(test)
matches = result==test_labels
correct = np.count_nonzero(matches)
accuracy = correct*100.0/result.size
print("The accuracy of a neural network with structure (400,400,10) " + 
                 "is: " + str(accuracy) + "%")

#Using Neural Network: (400,800,10)
nn = MLPClassifier(solver='lbfgs', alpha=1e-5,
                    hidden_layer_sizes=(800), random_state=1)
nn.fit(train, train_labels)
result = nn.predict(test)
matches = result==test_labels
correct = np.count_nonzero(matches)
accuracy = correct*100.0/result.size
print("The accuracy of a neural network with structure (400,800,10) " + 
                 "is: " + str(accuracy) + "%")

#Using Neural Network: (400,400,400,10)
nn = MLPClassifier(solver='lbfgs', alpha=1e-5,
                    hidden_layer_sizes=(400, 400), random_state=1)
nn.fit(train, train_labels)
result = nn.predict(test)
matches = result==test_labels
correct = np.count_nonzero(matches)
accuracy = correct*100.0/result.size
print("The accuracy of a neural network with structure (400,400,400,10) " + 
                 "is: " + str(accuracy) + "%")

#Using Neural Network: (400,400,10) and sigmoid function
nn = MLPClassifier(activation = 'logistic', solver='lbfgs', alpha=1e-5,
                    hidden_layer_sizes=(400), random_state=1)
nn.fit(train, train_labels)
result = nn.predict(test)
matches = result==test_labels
correct = np.count_nonzero(matches)
accuracy = correct*100.0/result.size
print("The accuracy of a neural network with structure (400,400,10) " + 
                 "and sigmoid function is: " + str(accuracy) + "%")

#Using Neural Network: (400,400,400,10) and sigmoid function
nn = MLPClassifier(activation = 'logistic', solver='lbfgs', alpha=1e-5,
                    hidden_layer_sizes=(400, 400), random_state=1)
nn.fit(train, train_labels)
result = nn.predict(test)
matches = result==test_labels
correct = np.count_nonzero(matches)
accuracy = correct*100.0/result.size
print("The accuracy of a neural network with structure (400,400,400,10) " + 
                 "and sigmoid function is: " + str(accuracy) + "%")

#Using Neural Network: (400,400,10), sigmoid function and stochastic gradient descent
nn = MLPClassifier(activation = 'logistic', solver='adam', alpha=1e-5,
                    hidden_layer_sizes=(400), random_state=1)
nn.fit(train, train_labels)
result = nn.predict(test)
matches = result==test_labels
correct = np.count_nonzero(matches)
accuracy = correct*100.0/result.size
print("The accuracy of a neural network with structure (400,400,10) " + 
                "and sigmoid function and  stochastic " + 
                " gradient descent is: " + str(accuracy) + "%")

#Using Neural Network: (400,400,400,10), sigmoid function and stochastic gradient descent
nn = MLPClassifier(activation = 'logistic', solver='adam', alpha=1e-5,
                    hidden_layer_sizes=(400,400), random_state=1)
nn.fit(train, train_labels)
result = nn.predict(test)
matches = result==test_labels
correct = np.count_nonzero(matches)
accuracy = correct*100.0/result.size
print("The accuracy of a neural network with structure (400,400,400,10) " + 
                "and sigmoid function and  stochastic " + 
                " gradient descent is: " + str(accuracy) + "%")

