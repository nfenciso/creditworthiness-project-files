import csv
from random import randrange

# Total Samples of Original Dataset: 1548
#   Approved: 175 (~11.3%)
#   Rejected: 1373 (~88.7%)

# 40% of Original Dataset: 620 -> Training Set
#   Approved: 70
#   Rejected: 550

# 30% of Original Dataset: 464 -> Each for Validation and Testing Sets
#   Approved: 52-53
#   Rejected: 411-412

data=[]
with open('filled_dataset.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    for row in csv_reader:
        if line_count == 0:
            header = row
        else:
            data.append(row)
        line_count+=1

MAX_APPR_TRAINING = 70
MAX_DECL_TRAINING = 550
MAX_APPR_VALIDATION = 52
MAX_DECL_VALIDATION = 412
MAX_APPR_TESTING = 52
MAX_DECL_TESTING = 412
num_samples=len(data)
#print(num_samples)

allotted=[]
training_set_appr=[]
training_set_decl=[]
validation_set_appr=[]
validation_set_decl=[]
testing_set_appr=[]
testing_set_decl=[]

curr_appr = 0
while (1):
    index = randrange(num_samples)
    if (index not in allotted):
        if (curr_appr < MAX_APPR_TRAINING):
            if (data[index][17] == '1'):
                training_set_appr.append(index)
                allotted.append(index)
                curr_appr+=1
        else:
            if (data[index][17] == '0'):
                training_set_decl.append(index)
                allotted.append(index)
            
            if (len(training_set_decl) == MAX_DECL_TRAINING):
                break

curr_appr = 0
while (1):
    index = randrange(num_samples)
    if (index not in allotted):
        if (curr_appr < MAX_APPR_VALIDATION):
            if (data[index][17] == '1'):
                validation_set_appr.append(index)
                allotted.append(index)
                curr_appr+=1
        else:
            if (data[index][17] == '0'):
                validation_set_decl.append(index)
                allotted.append(index)
            
            if (len(validation_set_decl) == MAX_DECL_VALIDATION):
                break

for index in range(0,num_samples):
    if (index not in allotted):
        allotted.append(index)
        if (data[index][17] == '1'):
            testing_set_appr.append(index)
        else:
            testing_set_decl.append(index)

training_set=training_set_appr
training_set.extend(training_set_decl)
validation_set=validation_set_appr
validation_set.extend(validation_set_decl)
testing_set=testing_set_appr
testing_set.extend(testing_set_decl)

# print(len(training_set_appr), len(training_set_decl))
# print(len(validation_set_appr), len(validation_set_decl))
# print(len(testing_set_appr), len(testing_set_decl))
# print(len(training_set))
# print(len(validation_set))
# print(len(testing_set))

with open('training_dataset.csv', 'w', newline='') as csv_file:
    writer = csv.writer(csv_file)
    training_data=[]
    training_data.append(header)
    for index in range(0,num_samples):
        if index in training_set:
            training_data.append(data[index])
    writer.writerows(training_data)

with open('validation_dataset.csv', 'w', newline='') as csv_file:
    writer = csv.writer(csv_file)
    validation_data=[]
    validation_data.append(header)
    for index in range(0,num_samples):
        if index in validation_set:
            validation_data.append(data[index])
    writer.writerows(validation_data)

with open('testing_dataset.csv', 'w', newline='') as csv_file:
    writer = csv.writer(csv_file)
    testing_data=[]
    testing_data.append(header)
    for index in range(0,num_samples):
        if index in testing_set:
            testing_data.append(data[index])
    writer.writerows(testing_data)