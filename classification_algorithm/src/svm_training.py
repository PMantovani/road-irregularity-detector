from sklearn import svm
import csv
import numpy as np

training_data = []
training_classes = []
test_data = []
test_classes = []

with open('C:\\Users\\pmant\\Documents\\Repositories\\' +
          'road-irregularity-detector\\data\\processed_data.csv', 'r') as p_data:
    csv_reader = csv.reader(p_data)
    to_training_data = True
    first_row = True    

    for row in csv_reader:
        if not first_row:
            r = np.array(row, dtype=float)

            if to_training_data:
                training_classes.append(int(r[0]))
                training_data.append([r[1], r[2], r[3], r[4], r[5], r[6], r[7], 
                                      r[8], r[9], r[10], r[11], r[12], r[13], r[14]])
                # training_data.append([ r[6], r[13], r[14] ])
                to_training_data = False
            else:
                test_classes.append(int(r[0]))
                test_data.append([r[1], r[2], r[3], r[4], r[5], r[6], r[7], 
                                  r[8], r[9], r[10], r[11], r[12], r[13], r[14]])
                # test_data.append([ r[6], r[13], r[14] ])
                to_training_data = True
        first_row = False

    classifier = svm.SVC(gamma=0.00001, C=1000000, kernel='rbf')
    # classifier = svm.SVC(kernel='linear')
    classifier.fit(training_data, training_classes)
    predicted = classifier.predict(test_data)

    error_matrix = {}
    # error_matrix[1] = [0, 0]
    # error_matrix[2] = [0, 0] 
    error_matrix[1] = [0, 0, 0]
    error_matrix[2] = [0, 0, 0] 
    error_matrix[3] = [0, 0, 0]

    for i in xrange(len(test_classes)):
        error_matrix[int(test_classes[i])][int(predicted[i])-1] += 1

    for i in xrange(len(error_matrix)):
        index = i+1
        total = error_matrix[index][0] + error_matrix[index][1] + error_matrix[index][2]
        # total = error_matrix[index][0] + error_matrix[index][1]
        if total != 0:
            for j in xrange(len(error_matrix[index])):
                error_matrix[index][j] *= 100./total

    print error_matrix