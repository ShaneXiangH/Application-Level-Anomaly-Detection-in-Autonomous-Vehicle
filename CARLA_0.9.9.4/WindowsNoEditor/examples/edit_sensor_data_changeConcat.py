import os

import numpy as np
import pandas as pd
import math
import csv

# time_period = 2  # s
frame_period = 2


def main():
    tick = pd.DataFrame(pd.read_csv('./edit_sensor_data_filter.csv',
                                    keep_default_na=False,
                                    encoding='utf-8',
                                    delimiter=',',
                                    header=0,
                                    ))

    with open('edit_sensor_data_changeConcat.csv', mode='w', newline='') as sensor_data_concat:
        sensor_data_concat_writer = csv.writer(sensor_data_concat, delimiter=',', quotechar='|',
                                               quoting=csv.QUOTE_MINIMAL)

    with open('edit_sensor_data_changeConcat.csv', mode='a', newline='') as col:
        app = csv.writer(col, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        app.writerow(
            ['frame', 'timestamp', 'x', 'y', 'z', 'pitch', 'yaw', 'roll',  # 0-7
             'field of view', 'height', 'width', 'raw data',  # image; Radar M       #  8-11
             'altitude', 'latitude', 'longitude',  # Gnss M                       #  12-14
             'accelerometer x', 'accelerometer y', 'accelerometer z', 'compass', 'gyroscope x', 'gyroscope y',
             'gyroscope z',  # imu M
             'channels', 'horizontal_angle',  # Lidar M                           #  15-21   22-23（11）
             'actor id', 'crossed lane markings',  # Lane Invasion E              #  24-25
             'actor id', 'other actor id', 'distance',  # Obstacle Detection E    #  26-28
             'normal_impulse',  # Collision E                                     #  29 （26，27）
             '# of cars', '# of pedestrians',  # 30-31
             'label',  # 32
            ])  

    file = open('./data.txt', mode='r', encoding='utf-8')
    lines = file.readlines()
    file.close()
    # print(lines)
    # print(lines[2].split(',')[0])
    # print(lines[2].split(',')[1])

    len_col = len(tick)
    # start_time = math.trunc(float(tick.at[1, '2']))  # !!!!!!!
    # print(start_time)
    # temp_time = start_time + time_period

    start_frame = int(tick.at[1, '1'])
    temp_frame = start_frame + frame_period

    last_list = ['0', '0', '0', '0', '0', '0', '0',
                 '0', '0', '0', '0', '0', '0', '0',
                 '0', '0', '0', '0', '0', '0', '0',
                 '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0']

    mylist = ['0', '0', '0', '0', '0', '0', '0',
              '0', '0', '0', '0', '0', '0', '0',
              '0', '0', '0', '0', '0', '0', '0',
              '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0']

    change_list = ['', '', '', '', '', '', '',
                   '', '', '', '', '', '', '',
                   '', '', '', '', '', '', '',
                   '', '', '', '', '', '', '', '', '', '', '', '']
    colli_flag = 0

    i = 0
    j = 0
    while i < len_col:

        # print(i)
        try:
            # if math.trunc(float(tick.at[i + 1, '2'])) > temp_time:
            if int(tick.at[i + 1, '1']) > temp_frame:

                # temp_time = temp_time + time_period
                temp_frame = temp_frame + frame_period

                if colli_flag == 1:
                    mylist[32] = 1
                else:
                    mylist[32] = 0

                mylist[30] = lines[j].strip('\n').split(',')[0]
                mylist[31] = lines[j].strip('\n').split(',')[1]
                j = j + 1

                # print(float(mylist[2]) - float(last_list[2]))

                for k in range(2, 32):
                    if k != 28:
                        change_list[k] = float(mylist[k]) - float(last_list[k])

                change_list[0] = mylist[0]
                change_list[1] = mylist[1]
                change_list[28] = mylist[28]
                change_list[32] = mylist[32]
                
                # print(change_list)

                with open('edit_sensor_data_changeConcat.csv', mode='a', newline='') as col:
                    app = csv.writer(col, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
                    app.writerow(change_list)

                last_list = mylist
                mylist = ['0', '0', '0', '0', '0', '0', '0',
                        '0', '0', '0', '0', '0', '0', '0',
                        '0', '0', '0', '0', '0', '0', '0',
                        '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0']
                colli_flag = 0
                continue
        except ValueError:
            print(tick)
            tick.drop([i], inplace=True)
            i = i + 1
            continue

        if tick.at[i, '0'] == 'rgb_cam_file:':
            mylist[0] = tick.at[i + 1, '1']
            mylist[1] = tick.at[i + 1, '2']
            mylist[2] = tick.at[i + 1, '3']
            mylist[3] = tick.at[i + 1, '4']
            mylist[4] = tick.at[i + 1, '5']
            mylist[5] = tick.at[i + 1, '6']
            mylist[6] = tick.at[i + 1, '7']
            mylist[7] = tick.at[i + 1, '8']

            mylist[8] = tick.at[i + 1, '9']
            mylist[9] = tick.at[i + 1, '10']
            mylist[10] = tick.at[i + 1, '11']
            # mylist[11] = tick.at[i + 1, '12']

            i = i + 2

        elif tick.at[i, '0'] == 'cam_file:':
            mylist[0] = tick.at[i + 1, '1']
            mylist[1] = tick.at[i + 1, '2']
            mylist[2] = tick.at[i + 1, '3']
            mylist[3] = tick.at[i + 1, '4']
            mylist[4] = tick.at[i + 1, '5']
            mylist[5] = tick.at[i + 1, '6']
            mylist[6] = tick.at[i + 1, '7']
            mylist[7] = tick.at[i + 1, '8']

            mylist[8] = tick.at[i + 1, '9']
            mylist[9] = tick.at[i + 1, '10']
            mylist[10] = tick.at[i + 1, '11']
            # mylist[11] = tick.at[i + 1, '12']

            i = i + 2

        elif tick.at[i, '0'] == 'colli_file:':
            mylist[0] = tick.at[i + 1, '1']
            mylist[1] = tick.at[i + 1, '2']
            mylist[2] = tick.at[i + 1, '3']
            mylist[3] = tick.at[i + 1, '4']
            mylist[4] = tick.at[i + 1, '5']
            mylist[5] = tick.at[i + 1, '6']
            mylist[6] = tick.at[i + 1, '7']
            mylist[7] = tick.at[i + 1, '8']

            # mylist[26] = tick.at[i + 1, '9']
            # mylist[27] = tick.at[i + 1, '10']
            # mylist[29] = tick.at[i + 1, '11']

            colli_flag = 1

            i = i + 2

        elif tick.at[i, '0'] == 'lane_file:':
            mylist[0] = tick.at[i + 1, '1']
            mylist[1] = tick.at[i + 1, '2']
            mylist[2] = tick.at[i + 1, '3']
            mylist[3] = tick.at[i + 1, '4']
            mylist[4] = tick.at[i + 1, '5']
            mylist[5] = tick.at[i + 1, '6']
            mylist[6] = tick.at[i + 1, '7']
            mylist[7] = tick.at[i + 1, '8']

            mylist[24] = tick.at[i + 1, '9']
            mylist[25] = tick.at[i + 1, '10']

            i = i + 2

        elif tick.at[i, '0'] == 'obs_file:':
            mylist[0] = tick.at[i + 1, '1']
            mylist[1] = tick.at[i + 1, '2']
            mylist[2] = tick.at[i + 1, '3']
            mylist[3] = tick.at[i + 1, '4']
            mylist[4] = tick.at[i + 1, '5']
            mylist[5] = tick.at[i + 1, '6']
            mylist[6] = tick.at[i + 1, '7']
            mylist[7] = tick.at[i + 1, '8']

            # mylist[26] = tick.at[i + 1, '9']
            # mylist[27] = tick.at[i + 1, '10']
            mylist[28] = tick.at[i + 1, '11']

            i = i + 2

        elif tick.at[i, '0'] == 'gnss_file:':
            mylist[0] = tick.at[i + 1, '1']
            mylist[1] = tick.at[i + 1, '2']
            mylist[2] = tick.at[i + 1, '3']
            mylist[3] = tick.at[i + 1, '4']
            mylist[4] = tick.at[i + 1, '5']
            mylist[5] = tick.at[i + 1, '6']
            mylist[6] = tick.at[i + 1, '7']
            mylist[7] = tick.at[i + 1, '8']

            mylist[12] = tick.at[i + 1, '9']
            mylist[13] = tick.at[i + 1, '10']
            mylist[14] = tick.at[i + 1, '11']

            i = i + 2

        elif tick.at[i, '0'] == 'imu_file:':
            mylist[0] = tick.at[i + 1, '1']
            mylist[1] = tick.at[i + 1, '2']
            mylist[2] = tick.at[i + 1, '3']
            mylist[3] = tick.at[i + 1, '4']
            mylist[4] = tick.at[i + 1, '5']
            mylist[5] = tick.at[i + 1, '6']
            mylist[6] = tick.at[i + 1, '7']
            mylist[7] = tick.at[i + 1, '8']

            mylist[15] = tick.at[i + 1, '9']
            mylist[16] = tick.at[i + 1, '10']
            mylist[17] = tick.at[i + 1, '11']
            mylist[18] = tick.at[i + 1, '12']
            mylist[19] = tick.at[i + 1, '13']
            mylist[20] = tick.at[i + 1, '14']
            mylist[21] = tick.at[i + 1, '15']

            i = i + 2

        elif tick.at[i, '0'] == 'log_depth_cam_file:':
            mylist[0] = tick.at[i + 1, '1']
            mylist[1] = tick.at[i + 1, '2']
            mylist[2] = tick.at[i + 1, '3']
            mylist[3] = tick.at[i + 1, '4']
            mylist[4] = tick.at[i + 1, '5']
            mylist[5] = tick.at[i + 1, '6']
            mylist[6] = tick.at[i + 1, '7']
            mylist[7] = tick.at[i + 1, '8']

            mylist[8] = tick.at[i + 1, '9']
            mylist[9] = tick.at[i + 1, '10']
            mylist[10] = tick.at[i + 1, '11']
            # mylist[11] = tick.at[i + 1, '12']

            i = i + 2

        elif tick.at[i, '0'] == 'depth_cam_file:':
            mylist[0] = tick.at[i + 1, '1']
            mylist[1] = tick.at[i + 1, '2']
            mylist[2] = tick.at[i + 1, '3']
            mylist[3] = tick.at[i + 1, '4']
            mylist[4] = tick.at[i + 1, '5']
            mylist[5] = tick.at[i + 1, '6']
            mylist[6] = tick.at[i + 1, '7']
            mylist[7] = tick.at[i + 1, '8']

            mylist[8] = tick.at[i + 1, '9']
            mylist[9] = tick.at[i + 1, '10']
            mylist[10] = tick.at[i + 1, '11']
            # mylist[11] = tick.at[i + 1, '12']

            i = i + 2

        elif tick.at[i, '0'] == 'seg_cam_file:':
            mylist[0] = tick.at[i + 1, '1']
            mylist[1] = tick.at[i + 1, '2']
            mylist[2] = tick.at[i + 1, '3']
            mylist[3] = tick.at[i + 1, '4']
            mylist[4] = tick.at[i + 1, '5']
            mylist[5] = tick.at[i + 1, '6']
            mylist[6] = tick.at[i + 1, '7']
            mylist[7] = tick.at[i + 1, '8']

            mylist[8] = tick.at[i + 1, '9']
            mylist[9] = tick.at[i + 1, '10']
            mylist[10] = tick.at[i + 1, '11']
            # mylist[11] = tick.at[i + 1, '12']

            i = i + 2

        elif tick.at[i, '0'] == 'radar_data_file:':
            mylist[0] = tick.at[i + 1, '1']
            mylist[1] = tick.at[i + 1, '2']
            mylist[2] = tick.at[i + 1, '3']
            mylist[3] = tick.at[i + 1, '4']
            mylist[4] = tick.at[i + 1, '5']
            mylist[5] = tick.at[i + 1, '6']
            mylist[6] = tick.at[i + 1, '7']
            mylist[7] = tick.at[i + 1, '8']

            # mylist[11] = tick.at[i + 1, '9']

            i = i + 2

        elif tick.at[i, '0'] == 'lidar_data_file:':
            mylist[0] = tick.at[i + 1, '1']
            mylist[1] = tick.at[i + 1, '2']
            mylist[2] = tick.at[i + 1, '3']
            mylist[3] = tick.at[i + 1, '4']
            mylist[4] = tick.at[i + 1, '5']
            mylist[5] = tick.at[i + 1, '6']
            mylist[6] = tick.at[i + 1, '7']
            mylist[7] = tick.at[i + 1, '8']

            mylist[22] = tick.at[i + 1, '9']
            mylist[23] = tick.at[i + 1, '10']
            # mylist[11] = tick.at[i + 1, '11']

            i = i + 2

        else:
            print('there comes some errors')

        # i = i + 2

    if colli_flag == 1:
        mylist[32] = 1
    else:
        mylist[32] = 0

    mylist[30] = lines[j].strip('\n').split(',')[0]
    mylist[31] = lines[j].strip('\n').split(',')[1]

    for k in range(2, 32):
        change_list[k] = float(mylist[k]) - float(last_list[k])

    change_list[0] = mylist[0]
    change_list[1] = mylist[1]
    change_list[32] = mylist[32]

    with open('edit_sensor_data_changeConcat.csv', mode='a', newline='') as col:
        app = csv.writer(col, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        app.writerow(change_list)


if __name__ == '__main__':
    main()
    print("done!")
