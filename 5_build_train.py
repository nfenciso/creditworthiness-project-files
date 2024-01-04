import csv
import numpy as np
import tensorflow as tf
import random

NUM_INPUT_NODES = 27
NUM_HIDDEN_NODES = 108
NUM_OUTPUT_NODES = 1

min_val_loss = 1

with open('new_weights.csv', 'w', newline='') as csv_file:
    writer = csv.writer(csv_file)
    c = []
    writer.writerows(c)

with open('loss_history.csv', 'w', newline='') as csv_file:
    writer = csv.writer(csv_file)
    c = []
    writer.writerows(c)

class GetWeightsCallback(tf.keras.callbacks.Callback):
    def __init__(self):
        super(GetWeightsCallback, self).__init__()

    def on_epoch_end(self, epoch, logs=None):
        if epoch % 10 == 0:
            # Get the model weights at the end of each epoch
            current_weights = self.model.get_weights()
            # Append the weights
            filename = "new_weights" 
            #"actual_weights_to_use"
            with open(filename+'.csv', 'a', newline='') as csv_file:
                writer = csv.writer(csv_file)
                c = [[],["EPOCH",epoch]]
                d2 = []
                d3 = []
                d4 = []

                layer_cntr = 0
                for i, layer_weights in enumerate(current_weights):
                    #print(layer_weights)
                    for j in enumerate(layer_weights):
                        #print("::::\t",j)
                        
                        for k in range(len(j)):
                            if k == 1:
                                #print(j[k])
                                #c.append(j[k])
                                if layer_cntr == 0:
                                    d = []
                                    for m in j[k]:
                                        d.append(m)
                                    c.append(d)
                                elif layer_cntr == 1:
                                    d2.append(j[k])
                                elif layer_cntr == 2:
                                    d3.append(j[k][0])
                                else:
                                    d4.append(j[k])

                    layer_cntr+=1
                c.append(d2)
                c.append(d3)
                c.append(d4)
                writer.writerows(c)
            
class LossHistory(tf.keras.callbacks.Callback):
    def on_train_begin(self, logs={}):
        with open('loss_history.csv', 'a', newline='') as csv_file:
            writer = csv.writer(csv_file)
            writer.writerows([["Epoch","Loss","Validation Loss"]])

    def on_epoch_end(self, epoch, logs={}):
        global min_val_loss
        with open('loss_history.csv', 'a', newline='') as csv_file:
            writer = csv.writer(csv_file)
            writer.writerows([[epoch,logs.get('loss'),logs.get('val_loss')]])
        
        if logs.get('val_loss') < min_val_loss:
            min_val_loss = logs.get('val_loss')

            current_weights = self.model.get_weights()
            # Append the weights
            filename = "actual_weights_to_use" 
            with open(filename+'.csv', 'w', newline='') as csv_file:
                writer = csv.writer(csv_file)
                c = []
                d2 = []
                d3 = []
                d4 = []

                layer_cntr = 0
                for i, layer_weights in enumerate(current_weights):
                    #print(layer_weights)
                    for j in enumerate(layer_weights):
                        #print("::::\t",j)
                        
                        for k in range(len(j)):
                            if k == 1:
                                #print(j[k])
                                #c.append(j[k])
                                if layer_cntr == 0:
                                    d = []
                                    for m in j[k]:
                                        d.append(m)
                                    c.append(d)
                                elif layer_cntr == 1:
                                    d2.append(j[k])
                                elif layer_cntr == 2:
                                    d3.append(j[k][0])
                                else:
                                    d4.append(j[k])

                    layer_cntr+=1
                c.append(d2)
                c.append(d3)
                c.append(d4)
                c.append([epoch])
                writer.writerows(c)


def hidden_initializer(shape, dtype=None):
    return tf.random.uniform(shape, minval=-0.5, maxval=0.5, dtype=dtype)

def output_weight_initializer(shape, dtype=None):
    weight_counter = 0

    rows, cols = shape
    weights = np.zeros((rows, cols))
    
    for i in range(len(weights)):
        if (weight_counter < NUM_HIDDEN_NODES/2):
            weights[i] = 1
            weight_counter+=1
        else:
            weights[i] = -1

    return tf.constant(weights, dtype=dtype)

def output_bias_initializer(shape, dtype=None):
    return tf.zeros(shape, dtype=dtype)

data=[]
label=[]
with open('oversampled_training_dataset.csv') as csv_file:
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
                    label.append(int(col))
                else:
                    data_row.append(float(col))
                col_count+=1
            data.append(data_row)
            #label.append(label_row)
        line_count+=1


hidden_weights = np.zeros((NUM_HIDDEN_NODES, NUM_INPUT_NODES))
hidden_bias = np.zeros((NUM_HIDDEN_NODES,))

with open('initial_weights.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    for row in csv_reader:
        if line_count in [0,1]:
            pass
        else:
            for i in range(0,NUM_INPUT_NODES+2):
                if i == 0:
                    pass
                elif i == 1:
                    hidden_bias[line_count-2] = float(row[i])
                else:
                    hidden_weights[line_count-2][i-2] = float(row[i])
        line_count+=1

hidden_weights = np.array(hidden_weights).T
hidden_bias = np.array(hidden_bias).T

def hidden_weight_initializer(shape, dtype=None):
    return tf.constant(hidden_weights, dtype=dtype)

def hidden_bias_initializer(shape, dtype=None):
    return tf.constant(hidden_bias, dtype=dtype)

data_val=[]
label_val=[]
with open('encoded_validation_dataset.csv') as csv_file:
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
                    label_val.append(int(col))
                else:
                    data_row.append(float(col))
                col_count+=1
            data_val.append(data_row)
            #label.append(label_row)
        line_count+=1

# Build the neural network model
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

get_weights_callback = GetWeightsCallback()
loss_history = LossHistory()
#model.summary()

# Train the model
history = model.fit(data, label, epochs=10000, batch_size=len(label), validation_data=(data_val,label_val), callbacks=[get_weights_callback,loss_history])

# initial_weights = model.get_weights()
# for i, w in enumerate(initial_weights):
#     print(f"Initial weights of layer {i}:")
#     print(np.shape(w))
#     print(w)
#     print("\n")