from sklearn import svm
import csv


data = []
target = []

with open('C:\\Users\\pmant\\Documents\\Repositories\\' +
          'road-irregularity-detector\\data\\processed_data.csv', 'r') as p_data:

    csv_reader = csv.reader(p_data)
    first_row = True

    for row in csv_reader:
        if first_row:
            first_row = False
        else:
            target.append(float(row[0]))
            data.append([float(row[1]), float(row[2]), float(row[3]),
                         float(row[4]), float(row[5]), float(row[6])])

    classifier = svm.SVC(gamma=0.001, C=100)

    classifier.fit(data, target)

    print classifier.predict([data[0]])
