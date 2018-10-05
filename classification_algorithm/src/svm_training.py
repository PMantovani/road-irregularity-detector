import csv
import numpy as np
import pickle
import sys
from sklearn import svm
from sklearn.metrics import f1_score
from sklearn.metrics import recall_score
from sklearn.metrics import precision_score
from sklearn.metrics import confusion_matrix

training_data = []
training_classes = []
test_data = []
test_classes = []

axis_indep = False
two_classes = True

path = 'C:\\Users\\pmant\\Documents\\Repositories\\road-irregularity-detector\\data\\'
filename = path + 'processed_data'
if two_classes:
    filename += '_2'
if axis_indep:
    filename += '_axis_indep'
filename += '.csv'

with open(filename, 'r') as p_data:
    csv_reader = csv.reader(p_data)
    to_training_data = True
    first_row = True    

    for row in csv_reader:
        if not first_row:
            r = np.array(row, dtype=float)

            if to_training_data:
                training_classes.append(int(r[0]))
                if axis_indep:
                    training_data.append([r[1], r[2], r[3], r[4], r[5], r[6]])
                else:
                    training_data.append([r[1], r[2], r[3], r[4], r[5], r[6], r[7], 
                                        r[8], r[9], r[10], r[11], r[12], r[13], r[14]])
                # training_data.append([ r[1], r[2], r[3], r[4], r[5], r[6], r[8], r[10], r[12], r[13], r[14] ])
                to_training_data = False
            else:
                test_classes.append(int(r[0]))
                if axis_indep:
                    test_data.append([r[1], r[2], r[3], r[4], r[5], r[6]])
                else:
                    test_data.append([r[1], r[2], r[3], r[4], r[5], r[6], r[7], 
                                    r[8], r[9], r[10], r[11], r[12], r[13], r[14]])
                # test_data.append([ r[1], r[2], r[3], r[4], r[5], r[6], r[8], r[10], r[12], r[13], r[14] ])
                to_training_data = True
        first_row = False

    c_parameter = float(sys.argv[1])
    gamma_parameter = float(sys.argv[2])
    print('Parametros de classificacao: C='+str(c_parameter)+ ' gamma='+str(gamma_parameter))

    classifier = svm.SVC(gamma=gamma_parameter, C=c_parameter, kernel='poly', degree=2)
    # classifier = svm.SVC(kernel='linear', C=c_parameter)
    classifier.fit(training_data, training_classes)
    predicted = classifier.predict(test_data)

    np.set_printoptions(precision=2, suppress=True)

    conf_matrix = np.transpose(confusion_matrix(test_classes, predicted))
    print('Confusion Matrix: ')
    print(str(conf_matrix))
    print('Precision Score: ' + str(precision_score(test_classes, predicted, average='macro')))
    print('Recall Score: ' + str(recall_score(test_classes, predicted, average='macro')))
    print('F1 Score: ' + str(f1_score(test_classes, predicted, average='macro')))
    print('F1 Score (per class): ' + str(f1_score(test_classes, predicted, average=None)))

    # save model to file
    pickle.dump(classifier, open('../../data/model.sav', 'wb'))
