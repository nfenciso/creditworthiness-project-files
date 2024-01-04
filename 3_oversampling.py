from imblearn.over_sampling import SMOTENC
import csv
from random import shuffle

input=[]
label=[]
with open('encoded_training_dataset.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    for row in csv_reader:
        input_row=[]
        label_row=[]
        if line_count == 0:
            pass
        else:
            col_count = 0
            for col in row:
                if col_count == 27:
                    label_row.append(int(col))
                else:
                    input_row.append(float(col))
                col_count+=1
            input.append(input_row)
            label.append(label_row)
        line_count+=1

X = input
y = label

sm=SMOTENC(random_state=42, categorical_features=[0,1,2,5,6,7,8,9,10,11,12,13,14,15,18,19,20,21,22,23,24,25])
X_res, y_res = sm.fit_resample(X,y)

header = [
    "Gender","Car Owner","Property Owner","Children","Annual Income",
    "Type Income 1","Type Income 2","Education 1","Education 2","Education 3",
    "Marital Status 1","Marital Status 2","Marital Status 3","Housing Type 1","Housing Type 2",
    "Housing Type 3","Birthday Count","Employee Days","Work Phone","Phone",
    "Email","Type Occupation 1","Type Occupation 2","Type Occupation 3","Type Occupation 4",
    "Type Occupation 5","Family Members","Label"
]
oversampled_data = []

for i in range(0, len(X_res)):
    oversampled_row = X_res[i]
    oversampled_row.append(y_res[i])
    oversampled_data.append(oversampled_row)

shuffle(oversampled_data)
oversampled_data.insert(0, header)

with open('oversampled_training_dataset.csv', 'w', newline='') as csv_file:
    writer = csv.writer(csv_file)
    writer.writerows(oversampled_data)