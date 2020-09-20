# -*- coding: utf-8 -*-
"""Example of using kNN for outlier detection
"""
# Author: Yue Zhao <zhaoy@cmu.edu>
# License: BSD 2 clause

from __future__ import division
from __future__ import print_function

import os
import sys

import csv
import numpy as np
import pandas as pd

# temporary solution for relative imports in case pyod is not installed
# if pyod is installed, no need to use the following line
sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname("__file__"), '..')))

from pyod.models.knn import KNN
from pyod.utils.data import generate_data
from pyod.utils.data import evaluate_print
from pyod.utils.example import visualize

from sklearn.model_selection import train_test_split
from sklearn import metrics

if __name__ == "__main__":

    tick = pd.DataFrame(pd.read_csv('./edit_sensor_data_changeConcat.csv',
                                    keep_default_na=False,
                                    encoding='utf-8',
                                    delimiter=',',
                                    header=0,
                                    ))
    
    len_col = len(tick)
    # print(len_col)
    # print(tick.at[27, 'label'])
    bad = 0
    for i in range(0, len_col):
        if tick.at[i, 'label'] == 1:
            bad = bad + 1

    contamination = bad / len_col  # percentage of outliers
    print(bad)
    print(contamination)
    # n_train = 200  # number of training points
    # n_test = 100  # number of testing points

    # Generate sample data

    # csv_file = open('edit_sensor_data_concat.csv')
    csv_file = open('edit_sensor_data_changeConcat.csv')
    # csv_file = open('edit_sensor_data_final_out.csv')

    csv_reader_lines = csv.reader(csv_file)
    data = []
    n = 0
    # print(csv_reader_lines)
    # headers = next(csv_reader_lines, None)
    # print(headers)
    for one_line in csv_reader_lines:
        # print(one_line)
        if n == 0:
            n = n + 1
            continue
        else:
            row = []
            for item in one_line:
                # print(item)
                if item == '':
                    item = 0
                row.append(item)
            # print(row)
            data.append(row)

    # print(data)
    # np.save('edit_sensor_data_concat.npy',data)
    # np.save('edit_sensor_data_changeConcat.npy',data)
    np.save('edit_sensor_data_final_out.npy',data)
    # print(data.shape)
 
    # shape_data = np.load('edit_sensor_data_concat.npy')
    # shape_data = np.load('edit_sensor_data_changeConcat.npy')
    shape_data = np.load('edit_sensor_data_final_out.npy')
    shape_data = shape_data.astype(np.float)
    # print(shaped_data)
    # print(shaped_data.shape)

    # print(shaped_data[:,:31])
    data = shape_data[:, :31]
    target = shape_data[:, 32]

    X_train, X_test, y_train, y_test = train_test_split(data, target, test_size=0.2, random_state = 4)
    # print(X_train)
    # print(y_train)
    # print(X_test)
    # print(y_test)

    # XX_train, yy_train, XX_test, yy_test = \
    #     generate_data(n_train=n_train,
    #                   n_test=n_test,
    #                   n_features=2,
    #                   contamination=contamination,
    #                   random_state=42)
    # print(XX_train)
    # print(yy_train)
    # print(XX_test)
    # print(yy_test)

    # train kNN detector
    clf_name = 'KNN'
    clf = KNN(contamination=contamination, n_neighbors=5, method='largest', radius=1)
    clf.fit(X_train)
    # print(clf)

    # get the prediction labels and outlier scores of the training data
    y_train_pred = clf.labels_  # binary labels (0: inliers, 1: outliers)
    y_train_scores = clf.decision_scores_  # raw outlier scores
    # print(y_train_pred)
    # print(y_train_scores)

    # get the prediction on the test data
    y_test_pred = clf.predict(X_test)  # outlier labels (0 or 1)
    y_test_scores = clf.decision_function(X_test)  # outlier scores
    # print(y_test_pred)
    # print(y_test_scores)

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
    # visualize(clf_name, X_train, y_train, X_test, y_test, y_train_pred,
    #           y_test_pred, show_figure=True, save_figure=True)
    
