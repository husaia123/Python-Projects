import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.model_selection import train_test_split
from matplotlib import cm
from mpl_toolkits.mplot3d import Axes3D

fruits = pd.read_table('fruit_data_with_colors.txt')
lookup_fruit_name = dict(zip(fruits.fruit_label.unique(),fruits.fruit_name.unique()))

X = fruits[['mass','width','height','color_score']]
y = fruits ['fruit_label']

X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=0)

def run_test():
    print (lookup_fruit_name,"\n")

    print (X_train,"\n")
    print (X_test,"\n")
    print (y_train,"\n")
    print (y_test,"\n")


def twoDmap():
    cmap= cm.get_cmap("gnuplot")
    scatter = pd.plotting.scatter_matrix(X_train, c= y_train, marker = 'o', s=40, hist_kwds={"bins":15},figsize=(12,12), cmap=cmap)
    plt.show()


def threeDmap():
    fig = plt.figure() 
    ax = fig.add_subplot (111,projection = "3d")
    ax.scatter(X_train['width'],X_train['height'],X_train['color_score'], c = y_train, marker = 'o', s=100)
    ax.set_xlabel("width")
    ax.set_xlabel("height")
    ax.set_zlabel("color_score")
    plt.show()

twoDmap()
threeDmap()
