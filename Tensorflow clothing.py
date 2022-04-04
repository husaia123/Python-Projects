from __future__ import absolute_import, division, print_function, unicode_literals
import sys
sys.path.insert(0, r"C:\Users\61422\AppData\Local\Packages\PythonSoftwareFoundation.Python.3.7_qbz5n2kfra8p0\LocalCache\local-packages\Python37\site-packages")#temporarily add modules to PATH
sys.path.insert(0, r"C:\Users\61422\AppData\Local\Packages\PythonSoftwareFoundation.Python.3.7_qbz5n2kfra8p0\LocalCache\local-packages\Python37\Scripts")

import tensorflow as tf
from tensorflow import keras

import numpy as np
import matplotlib.pyplot as plt#visualising items

fashion_mnist = keras.datasets.fashion_mnist#getting data set 
(train_images, train_labels), (test_images, test_labels) = fashion_mnist.load_data()



#9	Ankle boot
class_names = ['T-shirt/top', 'Trouser', 'Pullover', 'Dress', 'Coat','Sandal', 'Shirt', 'Sneaker', 'Bag', 'Ankle boot']


train_images.shape#(6000[items], 28, 28[28x28 pixles])
train_images = train_images / 255.0#pixles have value 0-1 instead of 0-225
test_images = test_images / 255.0

#plt.figure()
#plt.imshow(train_images[0])#what number of image to show
#plt.colorbar()
#plt.grid(False)
#plt.show()#show grid

model = keras.Sequential([
    keras.layers.Flatten(input_shape=(28, 28)),#flatten 28x28 pixles
    keras.layers.Dense(128, activation='relu'),#all 128 neurons (nodes) in first layer
    keras.layers.Dense(10, activation='softmax')#final result, 10 nodes for each possible answer
])

model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])#optimizer = This is how the model is updated based on the data it sees and its loss function
                                                                                             #loss = how accurate the model is during training
                                                                                             #metrics = monitor the training and testing steps
#you have done 3 main steps
#1  Feed the training data to the model. training data is train_images and train_labels arrays.
#2  The model learns to associate images and labels.
#3  You ask the model to make predictions about a test using the test_images array. Verify that the predictions match the labels from the test_labels array.

model.fit(train_images, train_labels, epochs=10)#runs the tests         epochs runs test 10 times to compare accuracy per run


test_loss, test_acc = model.evaluate(test_images,  test_labels, verbose=2)

print('\nTest accuracy:', test_acc*100, "%")

predictions = model.predict(test_images)



def plot_image(i, predictions_array, true_label, img):
  predictions_array, true_label, img = predictions_array, true_label[i], img[i]
  plt.grid(False)
  plt.xticks([])
  plt.yticks([])

  plt.imshow(img, cmap=plt.cm.binary)

  predicted_label = np.argmax(predictions_array)
  if predicted_label == true_label:
    color = 'blue'
  else:
    color = 'red'

  plt.xlabel("{} {:2.0f}% ({})".format(class_names[predicted_label],
                                100*np.max(predictions_array),
                                class_names[true_label]),
                                color=color)

def plot_value_array(i, predictions_array, true_label):
  predictions_array, true_label = predictions_array, true_label[i]
  plt.grid(False)
  plt.xticks(range(10))
  plt.yticks([])
  thisplot = plt.bar(range(10), predictions_array, color="#777777")
  plt.ylim([0, 1])
  predicted_label = np.argmax(predictions_array)

  thisplot[predicted_label].set_color('red')
  thisplot[true_label].set_color('blue')


for i in range (2):
    plt.figure(figsize=(6,3))
    plt.subplot(1,2,1)
    plot_image(i, predictions[i], test_labels, test_images)
    plt.subplot(1,2,2)
    plot_value_array(i, predictions[i],  test_labels)
    plt.show()
    print ("The prediction was",class_names[np.argmax(predictions[i])])


num_rows = 5
num_cols = 3
num_images = num_rows*num_cols
plt.figure(figsize=(2*2*num_cols, 2*num_rows))
for i in range(num_images):
  plt.subplot(num_rows, 2*num_cols, 2*i+1)
  plot_image(i, predictions[i], test_labels, test_images)
  plt.subplot(num_rows, 2*num_cols, 2*i+2)
  plot_value_array(i, predictions[i], test_labels)
plt.tight_layout()
plt.show()