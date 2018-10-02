from sklearn import svm
import csv
import numpy as np
import pickle

def find_recall(confusion_matrix):
    recall = [0] * len(confusion_matrix)
    for i in xrange(len(confusion_matrix)):
        total = 0
        for j in xrange(len(confusion_matrix[i])):
            total += confusion_matrix[j][i]

        recall[i] = 100.*confusion_matrix[i][i]/total

    return recall

def find_precision(confusion_matrix):
    precision = [0] * len(confusion_matrix)
    for i in xrange(len(confusion_matrix)):
        total = 0
        for j in xrange(len(confusion_matrix[i])):
            total += confusion_matrix[i][j]

        precision[i] = 100.*confusion_matrix[i][i]/total

    return precision

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
                # training_data.append([ r[1], r[2], r[3], r[4], r[5], r[6], r[8], r[10], r[12], r[13], r[14] ])
                to_training_data = False
            else:
                test_classes.append(int(r[0]))
                test_data.append([r[1], r[2], r[3], r[4], r[5], r[6], r[7], 
                                  r[8], r[9], r[10], r[11], r[12], r[13], r[14]])
                # test_data.append([ r[1], r[2], r[3], r[4], r[5], r[6], r[8], r[10], r[12], r[13], r[14] ])
                to_training_data = True
        first_row = False

    # classifier = svm.SVC(gamma=0.00001, C=10000, kernel='rbf')
    classifier = svm.SVC(kernel='linear', C=10000)
    classifier.fit(training_data, training_classes)
    predicted = classifier.predict(test_data)

    np.set_printoptions(precision=2, suppress=True)
    confusion_matrix = np.zeros((3,3))

    for i in xrange(len(test_classes)):
        confusion_matrix[int(predicted[i])-1][int(test_classes[i])-1] += 1
        

    print confusion_matrix
    precision = find_precision(confusion_matrix)
    recall = find_recall(confusion_matrix)

    denom = 0
    for element in precision:
        denom += (1./element)
    precision_harm_mean = len(precision) / denom
    
    denom = 0
    for element in recall:
        denom += (1./element)
    recall_harm_mean = len(recall) / denom

    f1_score = 2.*precision_harm_mean*recall_harm_mean/(precision_harm_mean+recall_harm_mean)

    print('Precision Harmonic Mean: ' + str(precision_harm_mean))
    print('Recall Harmonic Mean: ' + str(recall_harm_mean))
    print('F1 Score: ' + str(f1_score))

    # save model to file
    pickle.dump(classifier, open('../../data/model.sav', 'wb'))

