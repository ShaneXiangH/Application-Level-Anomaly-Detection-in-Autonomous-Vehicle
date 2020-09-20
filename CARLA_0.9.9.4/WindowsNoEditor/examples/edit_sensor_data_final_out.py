import os

import numpy as np
import pandas as pd
import math
import csv

def main():

    tick = pd.DataFrame(pd.read_csv('./edit_sensor_data_concat.csv',
                                    keep_default_na=False,
                                    encoding='utf-8',
                                    delimiter=',',
                                    header=0,
                                    ))
    # print(tick)

    with open('edit_sensor_data_final_out.csv', mode='w', newline='') as sensor_data_concat:
        sensor_data_concat_writer = csv.writer(sensor_data_concat, delimiter=',', quotechar='|',
                                               quoting=csv.QUOTE_MINIMAL)

    with open('edit_sensor_data_final_out.csv', mode='a', newline='') as col:
        app = csv.writer(col, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        app.writerow(
            ['accelerometer','gyroscope','distance',  # 0-2
             'label',  # 3
            ])

    len_col = len(tick)
    # print(len_col)
    mylist = ['0','0','0','0']
    i = 1

    while i < len_col:

        mylist[0] = math.sqrt(float(tick.at[i, 'accelerometer x']) ** 2 + float(tick.at[i, 'accelerometer y']) ** 2 + float(tick.at[i, 'accelerometer z']) ** 2)
        mylist[1] = math.sqrt(float(tick.at[i, 'gyroscope x']) ** 2 + float(tick.at[i, 'gyroscope y']) ** 2 + float(tick.at[i, 'gyroscope z']) ** 2)
        mylist[2] = tick.at[i, 'distance']
        mylist[3] = tick.at[i, 'label']

        with open('edit_sensor_data_final_out.csv', mode='a', newline='') as col:
                    app = csv.writer(col, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
                    app.writerow(mylist)
        
        i = i + 1


if __name__ == '__main__':
    main()
    print("done!")