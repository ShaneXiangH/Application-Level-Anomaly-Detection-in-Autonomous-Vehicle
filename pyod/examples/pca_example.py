# -*- coding: utf-8 -*-
"""Example of using PCA for outlier detection
"""
# Author: Yue Zhao <zhaoy@cmu.edu>
# License: BSD 2 clause

from __future__ import division
from __future__ import print_function

import os
import sys

import csv
import numpy as np

# temporary solution for relative imports in case pyod is not installed
# if pyod is installed, no need to use the following line
sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname("__file__"), '..')))

from pyod.models.pca import PCA
from pyod.utils.data import generate_data
from pyod.utils.data import evaluate_print
from pyod.utils.example import visualize

from sklearn.model_selection import train_test_split
from sklearn import metrics

if __name__ == "__main__":
    contamination = 0.1  # percentage of outliers
    # n_train = 200  # number of training points
    # n_test = 100  # number of testing points

    # Generate sample data

    # csv_file = open('edit_sensor_data_concat.csv')
    # csv_file = open('edit_sensor_data_changeConcat.csv')
    csv_file = open('edit_sensor_data_final_out.csv')

    csv_reader_lines = csv.reader(csv_file)
    data = []
    n = 0

    for one_line in csv_reader_lines:
        if n == 0:
            n = n + 1
            continue
        else:
            row = []
            for item in one_line:
                if item == '':
                    item = 0
                row.append(item)
            data.append(row)

    # np.save('edit_sensor_data_concat.npy',data)
    # np.save('edit_sensor_data_changeConcat.npy',data)
    np.save('edit_sensor_data_final_out.npy',data)
    # shape_data = np.load('edit_sensor_data_concat.npy')
    # shape_data = np.load('edit_sensor_data_changeConcat.npy')
    shape_data = np.load('edit_sensor_data_final_out.npy')
    shape_data = shape_data.astype(np.float)

    data = shape_data[:, :2]
    target = shape_data[:, 3]

    X_train, X_test, y_train, y_test = train_test_split(data, target, test_size=0.25, random_state = 4)

    # train PCA detector
    clf_name = 'PCA'
    clf = PCA(n_components=1)
    clf.fit(X_train)

    # get the prediction labels and outlier scores of the training data
    y_train_pred = clf.labels_  # binary labels (0: inliers, 1: outliers)
    y_train_scores = clf.decision_scores_  # raw outlier scores

    # get the prediction on the test data
    y_test_pred = clf.predict(X_test)  # outlier labels (0 or 1)
    y_test_scores = clf.decision_function(X_test)  # outlier scores

    # evaluate and print the results
    print("\nOn Training Data:")
    print(y_train)
    print(y_train_pred)
    print(y_train_scores)
    print("F1 Score",round(metrics.f1_score(y_train, y_train_pred),2))
    evaluate_print(clf_name, y_train, y_train_scores)

    print("\nOn Test Data:")
    print(y_test)
    print(y_test_pred)
    print(y_test_scores)
    print("F1 Score",round(metrics.f1_score(y_test, y_test_pred),2))
    evaluate_print(clf_name, y_test, y_test_scores)

    # visualize the results
    # Note: the original dimension has to be 2 for visualization
    # visualize(clf_name, X_train, y_train, X_test, y_test, y_train_pred,
    #           y_test_pred, show_figure=True, save_figure=False)
