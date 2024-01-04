import csv
import numpy as np
import tensorflow as tf
import random

NUM_INPUT_NODES = 27
NUM_HIDDEN_NODES = 108
NUM_OUTPUT_NODES = 1

hidden_weights = np.zeros((NUM_INPUT_NODES, NUM_HIDDEN_NODES))
hidden_bias = np.zeros((NUM_HIDDEN_NODES,))
output_weights = np.zeros((NUM_HIDDEN_NODES,1))
output_bias = np.zeros((1,))

with open('actual_weights_to_use.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    for row in csv_reader:
        if line_count < 27:
            for j in range(NUM_HIDDEN_NODES):
                hidden_weights[line_count][j] = row[j]
        elif line_count == 27:
            for j in range(NUM_HIDDEN_NODES):
                hidden_bias[j] = row[j]
        elif line_count == 28:
            for j in range(NUM_HIDDEN_NODES):
                output_weights[j][0] = row[j]
        elif line_count == 29:
            output_bias[0] = row[0]
        line_count+=1

# hidden_weights = np.array(hidden_weights).T
hidden_bias = np.array(hidden_bias).T

def hidden_weight_initializer(shape, dtype=None):
    return tf.constant(hidden_weights, dtype=dtype)

def hidden_bias_initializer(shape, dtype=None):
    return tf.constant(hidden_bias, dtype=dtype)

def output_weight_initializer(shape, dtype=None):
    return tf.constant(output_weights, dtype=dtype)

def output_bias_initializer(shape, dtype=None):
    return tf.constant(output_bias, dtype=dtype)

data_test=[]
label_test=[]
# encoded_training_dataset
# oversampled_training_dataset
# encoded_validation_dataset
# encoded_testing_dataset
filename = "encoded_testing_dataset"
with open(filename+'.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    for row in csv_reader:
        data_row=[]
        #label_row=[]
        if line_count == 0:
            pass
        else:
            col_count = 0
            for col in row:
                if col_count == 27:
                    #label_row.append(int(col))
                    label_test.append(int(col))
                else:
                    data_row.append(float(col))
                col_count+=1
            data_test.append(data_row)
            #label.append(label_row)
        line_count+=1

# # Build the neural network model
model = tf.keras.Sequential([
    tf.keras.layers.Dense(NUM_HIDDEN_NODES, activation='sigmoid', input_shape=(NUM_INPUT_NODES,),
                          kernel_initializer=hidden_weight_initializer,
                          bias_initializer=hidden_bias_initializer),
    tf.keras.layers.Dense(NUM_OUTPUT_NODES, activation='sigmoid',
                          kernel_initializer=output_weight_initializer,
                          bias_initializer=output_bias_initializer)
])

# Compile the model
optimizer = tf.keras.optimizers.Adam(learning_rate=0.001)
model.compile(optimizer=optimizer, loss='mean_squared_error')  # Using Adam optimizer and mean squared error loss
# print(hidden_weights)
# print(hidden_bias)
# print(output_weights)
# print(output_bias)

predictions = model.predict(data_test)

correct_count = 0
true_positives = 0
true_negatives = 0
false_positives = 0
false_negatives = 0
for i in range(len(predictions)):
    if predictions[i] > 0.5:
        print("1",label_test[i],1==label_test[i], predictions[i])
        if 1==label_test[i]:
            correct_count+=1
            true_positives+=1
        else:
            false_positives+=1
    else:
        print("0",label_test[i],0==label_test[i],predictions[i])
        if 0==label_test[i]:
            correct_count+=1
            true_negatives+=1
        else:
            false_negatives+=1

print()
print("=================================================")
print("Dataset File: "+filename+".csv")
print("\tTrue Positives:",true_positives)
print("\tTrue Negatives:",true_negatives)
print("\tFalse Positives:",false_positives)
print("\tFalse Negatives:",false_negatives)
print("\tTotal Correct:",correct_count,"out of",len(predictions))
print("\tAccuracy:",correct_count/len(predictions)*100,"%")
print("=================================================")
print()
