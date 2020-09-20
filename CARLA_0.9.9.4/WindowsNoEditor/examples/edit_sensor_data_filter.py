import os

import numpy as np
import pandas as pd
import math

# time_period = 2  # s
frame_period = 10


def main():
    tick = pd.DataFrame(pd.read_csv('./edit_sensor_data_sort.csv',
                                    keep_default_na=False,
                                    encoding='utf-8',
                                    delimiter=',',
                                    header=None,
                                    names=['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13',
                                           '14', '15', '16']))  # colunm INDEX. not NUM

    # tick_int = tick.astype('int32')
    len_col = len(tick)
    # len_raw = len(tick.values[1])

    # start_time = math.trunc(float(tick.at[1, '2']))
    # # final_time = int(tick.at[len_col - 1, '1'])
    # temp_time = start_time + time_period

    start_frame = int(tick.at[1, '1'])
    temp_frame = start_frame + frame_period

    rgb_cam_archive = [0, 0]  # [flag, data_row_index]
    cam_archive = [0, 0] 
    colli_archive = [0, 0]
    lane_archive = [0, 0]
    obs_archive = [0, 0]   # [flag for have data !0, data_row_index] 
    gnss_archive = [0, 0]
    imu_archive = [0, 0]
    log_depth_cam_archive = [0, 0]
    depth_cam_archive = [0, 0]
    seg_cam_archive = [0, 0]
    radar_data_archive = [0, 0]
    lidar_data_archive = [0, 0]

    i = 0
    j = 0  # index of obs..
    while i < len_col:

        print(i)
        try:
            # if math.trunc(float(tick.at[i + 1, '2'])) > temp_time:
            if int(tick.at[i + 1, '1']) > temp_frame:

                # temp_time = temp_time + time_period
                temp_frame = temp_frame + frame_period

                rgb_cam_archive = [0, 0]  # [flag, data_row_index]
                cam_archive = [0, 0]
                colli_archive = [0, 0]
                lane_archive = [0, 0]
                obs_archive = [0, 0]   # [flag for have data !0, data_row_index] 
                gnss_archive = [0, 0]
                imu_archive = [0, 0]
                log_depth_cam_archive = [0, 0]
                depth_cam_archive = [0, 0]
                seg_cam_archive = [0, 0]
                radar_data_archive = [0, 0]
                lidar_data_archive = [0, 0]
                continue
        except ValueError:
            print(tick)
            tick.drop([i], inplace=True)
            i = i + 1
            continue

        # print(tick.at[i, '0'])
        if tick.at[i, '0'] == 'rgb_cam_file:':
            if rgb_cam_archive[0] == 0:
                rgb_cam_archive = [1, i + 1]  # line INDEX
                i = i + 2
            else:
                tick.drop([rgb_cam_archive[1], rgb_cam_archive[1] - 1], inplace=True)
                rgb_cam_archive = [1, i + 1]
                i = i + 2

        elif tick.at[i, '0'] == 'cam_file:':
            if cam_archive[0] == 0:
                cam_archive = [1, i + 1]
                i = i + 2
            else:
                tick.drop([cam_archive[1], cam_archive[1] - 1], inplace=True)
                cam_archive = [1, i + 1]
                i = i + 2

        elif tick.at[i, '0'] == 'colli_file:':
            if colli_archive[0] == 0:
                colli_archive = [1, i + 1]
                i = i + 2
            else:
                tick.drop([colli_archive[1], colli_archive[1] - 1], inplace=True)
                colli_archive = [1, i + 1]
                i = i + 2

        elif tick.at[i, '0'] == 'lane_file:':
            if lane_archive[0] == 0:
                lane_archive = [1, i + 1]
                i = i + 2
            else:
                tick.drop([lane_archive[1], lane_archive[1] - 1], inplace=True)
                lane_archive = [1, i + 1]
                i = i + 2

        elif tick.at[i, '0'] == 'obs_file:':  # always store the smallest dis in that time slot

            # if obs_archive[0] == 0:
            #     obs_archive = [1, i + 1]
            #     i = i + 2
            # else:
            #     tick.drop([obs_archive[1], obs_archive[1] - 1], inplace=True)
            #     obs_archive = [1, i + 1]
            #     i = i + 2
            
            if (obs_archive[0] ==0) & (float(tick.at[i + 1, '11']) < 1):
                tick.drop([i, i + 1], inplace=True)
                i = i + 2
            elif (obs_archive[0] == 0) & (float(tick.at[i + 1, '11']) > 1):
                obs_archive = [1, i + 1]
                i = i + 2
            elif (obs_archive[0] == 1) & (float(tick.at[i + 1, '11']) > 1):
                if (float(tick.at[obs_archive[1], '11']) < float(tick.at[i + 1, '11'])):
                    tick.drop([i, i + 1], inplace=True)
                    i = i + 2
                else:
                    tick.drop([obs_archive[1], obs_archive[1] - 1], inplace=True)
                    obs_archive = [1, i + 1]
                    i = i + 2
            elif (obs_archive[0] == 1) & (float(tick.at[i + 1, '11']) < 1):
                tick.drop([obs_archive[1], obs_archive[1] - 1], inplace=True)
                obs_archive = [2, i + 1]
                tick.at[i + 1, '11'] = 0.1
                i = i + 2
            else:
                tick.drop([i, i + 1], inplace=True)
                i = i + 2


        elif tick.at[i, '0'] == 'gnss_file:':
            if gnss_archive[0] == 0:
                gnss_archive = [1, i + 1]
                i = i + 2
            else:
                tick.drop([gnss_archive[1], gnss_archive[1] - 1], inplace=True)
                gnss_archive = [1, i + 1]
                i = i + 2

        elif tick.at[i, '0'] == 'imu_file:':
            if imu_archive[0] == 0:
                imu_archive = [1, i + 1]
                i = i + 2
            else:
                tick.drop([imu_archive[1], imu_archive[1] - 1], inplace=True)
                imu_archive = [1, i + 1]
                i = i + 2

        elif tick.at[i, '0'] == 'log_depth_cam_file:':
            if log_depth_cam_archive[0] == 0:
                log_depth_cam_archive = [1, i + 1]
                i = i + 2
            else:
                tick.drop([log_depth_cam_archive[1], log_depth_cam_archive[1] - 1], inplace=True)
                log_depth_cam_archive = [1, i + 1]
                i = i + 2

        elif tick.at[i, '0'] == 'depth_cam_file:':
            if depth_cam_archive[0] == 0:
                depth_cam_archive = [1, i + 1]
                i = i + 2
            else:
                tick.drop([depth_cam_archive[1], depth_cam_archive[1] - 1], inplace=True)
                depth_cam_archive = [1, i + 1]
                i = i + 2

        elif tick.at[i, '0'] == 'seg_cam_file:':
            if seg_cam_archive[0] == 0:
                seg_cam_archive = [1, i + 1]
                i = i + 2
            else:
                tick.drop([seg_cam_archive[1], seg_cam_archive[1] - 1], inplace=True)
                seg_cam_archive = [1, i + 1]
                i = i + 2

        elif tick.at[i, '0'] == 'radar_data_file:':
            if radar_data_archive[0] == 0:
                radar_data_archive = [1, i + 1]
                i = i + 2
            else:
                tick.drop([radar_data_archive[1], radar_data_archive[1] - 1], inplace=True)
                radar_data_archive = [1, i + 1]
                i = i + 2

        elif tick.at[i, '0'] == 'lidar_data_file:':
            if lidar_data_archive[0] == 0:
                lidar_data_archive = [1, i + 1]
                i = i + 2
            else:
                tick.drop([lidar_data_archive[1], lidar_data_archive[1] - 1], inplace=True)
                lidar_data_archive = [1, i + 1]
                i = i + 2

        else:
            print('there comes some errors')

    tick.to_csv(path_or_buf='edit_sensor_data_filter.csv')
    print("done!")
    # data_concat(tick, start_time, time_period)


# def data_concat(tick, start_time, time_period):


if __name__ == '__main__':
    main()
