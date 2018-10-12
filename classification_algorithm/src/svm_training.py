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

path = '../../data/'
filename = path + 'processed_data'
out_filename = path + '/results/'

# parse number of classes
if '-t' in sys.argv or '--two' in sys.argv:
    two_classes = True
else:
    two_classes = False

# parse axis independence
if '-a' in sys.argv or '--axis-independent' in sys.argv:
    axis_indep = True
else:
    axis_indep = False

c_parameter = 1
# parse value of C
if '-c' in sys.argv:
    ind = sys.argv.index('-c')
    c_parameter = float(sys.argv[ind+1])

# parse value of gamma
gamma_parameter = 1
if '-g' in sys.argv:
    ind = sys.argv.index('-g')
    gamma_parameter = float(sys.argv[ind+1])

# parse kernel type
kernel_type = 'linear'
if '-k' in sys.argv:
    ind = sys.argv.index('-k')
    kernel_type = sys.argv[ind+1]


if two_classes:
    print 'Rodando classificador para 2 classes'
else:
    print 'Rodando classificador para 3 classes'
if axis_indep:
    print 'Rodando com independencia de eixo'
else:
    print 'Rodando sem independencia de eixo'
print 'Tipo de kernel: ' + str(kernel_type)
print 'Parametros de classificacao: C=' + str(c_parameter) + ' gamma=' + str(gamma_parameter)

if two_classes:
    filename += '_2'
    out_filename += '_2'
if axis_indep:
    filename += '_axis_indep'
    out_filename += '_axis_indep'

out_filename += kernel_type
out_filename += '_c_' + str(c_parameter)
out_filename += '_g_' + str(gamma_parameter)

filename += '.csv'
out_filename += '.csv'

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
                to_training_data = False
            else:
                test_classes.append(int(r[0]))
                if axis_indep:
                    test_data.append([r[1], r[2], r[3], r[4], r[5], r[6]])
                else:
                    test_data.append([r[1], r[2], r[3], r[4], r[5], r[6], r[7],
                                      r[8], r[9], r[10], r[11], r[12], r[13], r[14]])
                to_training_data = True
        first_row = False

    classifier = svm.SVC(gamma=gamma_parameter, C=c_parameter, kernel=kernel_type, degree=2)
    classifier.fit(training_data, training_classes)
    predicted = classifier.predict(test_data)

    np.set_printoptions(precision=2, suppress=True)

    conf_matrix = np.transpose(confusion_matrix(test_classes, predicted))
    print 'Confusion Matrix: '
    print str(conf_matrix)
    print 'Precision Score: ' + str(precision_score(test_classes, predicted, average='macro'))
    print 'Recall Score: ' + str(recall_score(test_classes, predicted, average='macro'))
    print 'F1 Score: ' + str(f1_score(test_classes, predicted, average='macro'))
    print 'F1 Score (per class): ' + str(f1_score(test_classes, predicted, average=None))

    with open(out_filename, 'w') as out_file:
        out_file.write('Confusion Matrix:\n')
        out_file.write(str(conf_matrix) + '\n')
        out_file.write('Precision Score: ' + str(precision_score(test_classes, predicted, average='macro')) + '\n')
        out_file.write('Recall Score: ' + str(recall_score(test_classes, predicted, average='macro')) + '\n')
        out_file.write('F1 Score: ' + str(f1_score(test_classes, predicted, average='macro')) + '\n')
        out_file.write('F1 Score (per class): ' + str(f1_score(test_classes, predicted, average=None)) + '\n')

    # save model to file
    # pickle.dump(classifier, open('../../data/model.sav', 'wb'))