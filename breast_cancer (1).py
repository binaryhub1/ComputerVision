# -*- coding: utf-8 -*-
"""Breast_cancer.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1LNY-dVrgrIzyuImHrnEPpBjmtiPiF4qF
"""

import tensorflow as tf
from tensorflow.keras import layers, models
from sklearn.model_selection import train_test_split
import numpy as np
#   DataGenerator to read images and rescale images
from tensorflow.keras.preprocessing.image import ImageDataGenerator
import matplotlib.pyplot as plt
from sklearn.metrics import classification_report, confusion_matrix, roc_auc_score
from sklearn.metrics import precision_recall_curve, auc
from tensorflow.keras.callbacks import Callback
#   Optimizer
from tensorflow.keras.optimizers import SGD

import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from tensorflow import keras
from tensorflow.keras import layers
from tensorflow.keras.applications import ResNet50
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Input, Convolution2D, ReLU, AveragePooling2D, Dropout, Flatten, Dense, Softmax
from tensorflow.keras.initializers import glorot_uniform
from tensorflow.keras.applications import VGG16

## Set Path Here before running the code
WORKING_DIRECTORY =  "/content/drive/MyDrive/Breast_Cancer_Patients_MRI/Breast Cancer Patients MRI/Breast Cancer Patients MRI_s/train"

##  Name of classes
CLASSES = ['Healthy',
           'Sick']

X, y = [], []

## Images rescaling
datagen = ImageDataGenerator(rescale=1.0/255.0)

#   Load images by resizing and shuffling randomly
train_dataset = datagen.flow_from_directory(WORKING_DIRECTORY, target_size=(150, 150),batch_size=6400, shuffle=True)
### Seperate Dataset from  Data Genrator
X, y = train_dataset.next()

#   Number of samples in classes
from collections import Counter
print("Number of samples in each class:\t", sorted(Counter(np.argmax(y, axis=1)).items()))

#   class labels as per indices
print("Classes Names according to index:\t", train_dataset.class_indices)

# Split the data into training, validation, and test sets
X_train, X_temp, y_train, y_temp = train_test_split(X, y, test_size=0.3, random_state=42)
X_val, X_test, y_val, y_test = train_test_split(X_temp, y_temp, test_size=0.2, random_state=42)


# Number of samples after train test split
print("Number of samples after splitting into Training, validation & test set\n")

print("Train     \t",sorted(Counter(np.argmax(y_train, axis=1)).items()))
print("Validation\t",sorted(Counter(np.argmax(y_val, axis=1)).items()))
print("Test      \t",sorted(Counter(np.argmax(y_test, axis=1)).items()))

print("X_train shape:", X_train.shape)
print("y_train shape:", y_train.shape)
print("X_val shape:", X_val.shape)
print("y_val shape:", y_val.shape)

import matplotlib.pyplot as plt
import numpy as np
from sklearn.metrics import confusion_matrix

# Function to train and plot accuracy
def train_and_plot(model, X_train, y_train, X_val, y_val, epochs=80):

    history = model.fit(X_train, y_train, epochs=epochs, validation_data=(X_val, y_val), verbose=2)
    # Calculate and plot confusion matrix
    y_pred = np.argmax(model.predict(X_val), axis=1)
    y_true = np.argmax(y_val, axis=1)
    cm = confusion_matrix(y_true, y_pred)
    plot_confusion_matrix(cm, classes=['Healthy', 'Sick'])
    plt.show()

    # Plot training history
    plot_training_history(history)


def plot_training_history(history):
    plt.figure(figsize=(12, 4))
    plt.subplot(1, 2, 1)
    plt.plot(history.history['accuracy'], label='Train Accuracy')
    plt.plot(history.history['val_accuracy'], label='Validation Accuracy')
    plt.title('Training and Validation Accuracy')
    plt.xlabel('Epoch')
    plt.ylabel('Accuracy')
    plt.legend()

    plt.subplot(1, 2, 2)
    plt.plot(history.history['loss'], label='Train Loss')
    plt.plot(history.history['val_loss'], label='Validation Loss')
    plt.title('Training and Validation Loss')
    plt.xlabel('Epoch')
    plt.ylabel('Loss')
    plt.legend()

    plt.tight_layout()
    plt.savefig('history_plot.png')
    plt.show()


    plt.tight_layout()


def plot_confusion_matrix(cm, classes, figsize=(8, 6)):
    plt.figure(figsize=figsize)
    plt.imshow(cm, interpolation='nearest', cmap=plt.cm.Blues)
    plt.title('Confusion Matrix')
    plt.colorbar()
    # Add labels to the plot
    for i in range(cm.shape[0]):
        for j in range(cm.shape[1]):
             plt.text(j, i, cm[i, j], horizontalalignment='center', verticalalignment='center', color='black')

    plt.xticks(np.arange(2), ['Healthy', 'Sick'], rotation=45)
    plt.yticks(np.arange(2), ['Healthy', 'Sick'])
    tick_marks = np.arange(len(classes))
    plt.xticks(tick_marks, classes, rotation=45)
    plt.yticks(tick_marks, classes)

    plt.ylabel('True label')
    plt.xlabel('Predicted label')
    plt.tight_layout()

# Define a function to create the CNN model
def create_cnn_model(input_shape=(150, 150, 3)):
    seed_value = 42
  # Define the initializer
    init = glorot_uniform(seed=seed_value)
    model = Sequential()

    model.add(Input(shape=input_shape))

    model.add(Convolution2D(16, 5, kernel_initializer=init))
    model.add(ReLU())
    model.add(AveragePooling2D(pool_size=(2,2)))

    model.add(Convolution2D(32, 5, kernel_initializer=init))
    model.add(ReLU())
    model.add(AveragePooling2D(pool_size=(2,2)))

    model.add(Convolution2D(64, 5, kernel_initializer=init))
    model.add(ReLU())
    model.add(AveragePooling2D(pool_size=(2,2)))

    model.add(Convolution2D(128, 5, kernel_initializer=init))
    model.add(ReLU())
    model.add(AveragePooling2D(pool_size=(2,2)))


    model.add(Dropout(0.01))

    model.add(Flatten())

    model.add(Dense(256, kernel_initializer=init))
    model.add(ReLU())
    model.add(Dropout(0.03))

    model.add(Dense(2, activation='sigmoid'))

    model.compile(optimizer='SGD', loss='binary_crossentropy', metrics=['accuracy'])
    return model

# Input shape
input_shape = ( 150, 150, 3)

# Create CNN model
cnn_model = create_cnn_model(input_shape)
cnn_model.summary()

train_and_plot(cnn_model, X_train, y_train, X_val, y_val)

# Save the model
cnn_model.save('my_model.h5')

# Evaluate the model on the test data
score = cnn_model.evaluate(X_test, y_test, verbose=0)

# Print the test accuracy
print('Test accuracy:', score[1])

# Generate predictions on the test data
predictions = cnn_model.predict(X_test)

# Get the predicted class for each image
predicted_classes = np.argmax(predictions, axis=1)

# Get the true class for each image
true_classes = np.argmax(y_test, axis=1)

# Print the first 10 predictions and true labels
for i in range(10):
    print("Predicted class:", predicted_classes[i], "True class:", true_classes[i])

# Plot the first 10 images and their predictions
for i in range(10):
    plt.figure(figsize=(5,5))
    plt.imshow(X_test[i])
    plt.title("Predicted class: {}, True class: {}".format(predicted_classes[i], true_classes[i]))
    plt.show()

from google.colab import drive
drive.mount('/content/drive')



