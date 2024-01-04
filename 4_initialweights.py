import csv
import random
import numpy as np

NUM_INPUT_NODES = 27
NUM_HIDDEN_NODES = 108
NUM_OUTPUT_NODES = 1

input=[]
label=[]
with open('oversampled_training_dataset.csv') as csv_file:
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

x = np.array(input)
x_mean = x.mean(axis=0)

a_weights = [["a_"+str(i)+"_"+str(j) for j in range(NUM_HIDDEN_NODES+1)] for i in range(NUM_INPUT_NODES+1)]
b_weights = ["b_"+str(i) for i in range(NUM_HIDDEN_NODES+1)]

# Get weights from input to hidden
for i in range(1,NUM_INPUT_NODES+1): # 1 to 27
    for j in range(1,NUM_HIDDEN_NODES+1): # 1 to 60
        a_weights[i][j] = random.uniform(0, 1)
        #print(i,j,"\t==\t",a_weights[i][j])

# Get bias weights of hidden nodes
for j in range(1,NUM_HIDDEN_NODES+1):
    sum_a_times_x = 0
    for k in range(1,NUM_INPUT_NODES+1):
        a_times_x = a_weights[k][j] * x_mean[k-1]
        sum_a_times_x += a_times_x
    
    bias = (abs(sum_a_times_x) - random.uniform(0,0.5))
    if (sum_a_times_x > 0 and bias > 0) or (sum_a_times_x < 0 and bias < 0):
        bias *= -1
    
    #print(j,":\t",sum_a_times_x, "\t\t", bias)
    a_weights[0][j] = bias
    #a_weights[0][j] = random.uniform(0, 1)

# Get weights from hidden to output and bias weight of output node
for i in range(0,NUM_HIDDEN_NODES+1):
    if i == 0:
        b_weights[i] = 0
    elif i < 31:
        b_weights[i] = 1
    else:
        b_weights[i] = -1
    #b_weights[i] = random.uniform(0.5, 1)

# for i in a_weights:
#     print(i)

# for i in b_weights:
#     print(i)

header1 = ["" for i in range(0,30)]
header1[0] = "j"
header1[1] = "Input Nodes"
header1[29] = "Output Node"
#print(header1)

header2 = []
for i in range(0,31):
    if i == 0:
        header2.append("")
    elif i >= 1 and i < 29:
        header2.append("a_"+str(i-1)+"j")
    elif i == 29:
        header2.append("b_j")
    else:
        header2.append("b_0")

#print(header2)

tabular = []
for i in range(1,NUM_HIDDEN_NODES+1):
    row = []
    row.append(i)
    for j in range(0,NUM_INPUT_NODES+1+1):
        if j == 0:
            row.append(a_weights[0][i])
        elif j < NUM_INPUT_NODES+1:
            #print(i,j)
            row.append(a_weights[j][i])
        else:
            row.append(b_weights[i])

            if i == 1:
                row.append(b_weights[0])

    tabular.append(row)

tabular.insert(0, header2)
tabular.insert(0, header1)
# for i in a_weights:
#     print(i)

with open('initial_weights.csv', 'w', newline='') as csv_file:
    writer = csv.writer(csv_file)
    writer.writerows(tabular)