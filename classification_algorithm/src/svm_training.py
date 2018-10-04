from sklearn import svm
from sklearn.metrics import f1_score
from sklearn.metrics import recall_score
from sklearn.metrics import precision_score
from sklearn.metrics import confusion_matrix
import csv
import numpy as np
import pickle

training_data = []
training_classes = []
test_data = []
test_classes = []

with open('C:\\Users\\pmant\\Documents\\Repositories\\' +
          'road-irregularity-detector\\data\\processed_data_2.csv', 'r') as p_data:
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
    classifier = svm.SVC(kernel='linear', C=0.1)
    classifier.fit(training_data, training_classes)
    predicted = classifier.predict(test_data)

    np.set_printoptions(precision=2, suppress=True)

    conf_matrix = np.transpose(confusion_matrix(test_classes, predicted))
    print('Confusion Matrix: ')
    print(str(conf_matrix))
    print('Precision Score: ' + str(precision_score(test_classes, predicted, average='macro')))
    print('Recall Score: ' + str(recall_score(test_classes, predicted, average='macro')))
    print('F1 Score: ' + str(f1_score(test_classes, predicted, average='macro')))

    # save model to file
    pickle.dump(classifier, open('../../data/model.sav', 'wb'))
