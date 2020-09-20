import glob
import os
import sys
import time
import math
import weakref

try:
    sys.path.append(glob.glob('../carla/dist/carla-*%d.%d-%s.egg' % (
        sys.version_info.major,
        sys.version_info.minor,
        'win-amd64' if os.name == 'nt' else 'linux-x86_64'))[0])
except IndexError:
    pass

import carla

import argparse
import logging
import random
import csv


def main():
    client = carla.Client('127.0.0.1', 2000)
    client.set_timeout(10.0)

    try:

        world = client.get_world()
        ego_vehicle = None
        ego_cam = None
        depth_cam = None
        depth_cam02 = None
        sem_cam = None
        rad_ego = None
        lidar_sen = None

        # --------------
        # Query the recording
        # --------------
        """
        # Show the most important events in the recording.  
        print(client.show_recorder_file_info("~/tutorial/recorder/recording05.log",False))
        # Show actors not moving 1 meter in 10 seconds.  
        #print(client.show_recorder_actors_blocked("~/tutorial/recorder/recording04.log",10,1))
        # Show collisions between any type of actor.  
        #print(client.show_recorder_collisions("~/tutorial/recorder/recording04.log",'v','a'))
        """

        # --------------
        # Reenact a fragment of the recording
        # --------------
        """
        client.replay_file("~/tutorial/recorder/recording03.log",0,30,0)
        """

        # --------------
        # Set playback simulation conditions
        # --------------
        """
        ego_vehicle = world.get_actor(322) #Store the ID from the simulation or query the recording to find out
        """

        # --------------
        # Place spectator on ego spawning
        # --------------
        """
        spectator = world.get_spectator()
        world_snapshot = world.wait_for_tick() 
        spectator.set_transform(ego_vehicle.get_transform())
        """

        # --------------
        # Change weather conditions
        # --------------
        """
        weather = world.get_weather()
        weather.sun_altitude_angle = -30
        weather.fog_density = 65
        weather.fog_distance = 10
        world.set_weather(weather)
        """

        # --------------
        # Add a RGB camera to ego vehicle.
        # --------------
        """
        cam_bp = None
        cam_bp = world.get_blueprint_library().find('sensor.camera.rgb')
        cam_location = carla.Location(2,0,1)
        cam_rotation = carla.Rotation(0,180,0)
        cam_transform = carla.Transform(cam_location,cam_rotation)
        cam_bp.set_attribute("image_size_x",str(1920))
        cam_bp.set_attribute("image_size_y",str(1080))
        cam_bp.set_attribute("fov",str(105))
        ego_cam = world.spawn_actor(cam_bp,cam_transform,attach_to=ego_vehicle, attachment_type=carla.AttachmentType.Rigid)
        ego_cam.listen(lambda image: image.save_to_disk('~/tutorial/new_rgb_output/%.6d.jpg' % image.frame))
        """

        # --------------
        # Add a Logarithmic Depth camera to ego vehicle.
        # carla.Image:
        #   frame; timestamp; transform
        #   fov; height; width; raw_data
        #   convert(); save_to_disk()
        # --------------

        depth_cam = None
        depth_bp = world.get_blueprint_library().find('sensor.camera.depth')
        depth_bp.set_attribute("image_size_x", str(1920))
        depth_bp.set_attribute("image_size_y", str(1080))
        depth_bp.set_attribute("fov", str(105))
        depth_location = carla.Location(2, 0, 1)
        depth_rotation = carla.Rotation(0, 180, 0)
        depth_transform = carla.Transform(depth_location, depth_rotation)
        depth_cam = world.spawn_actor(depth_bp, depth_transform, attach_to=ego_vehicle,
                                      attachment_type=carla.AttachmentType.Rigid)
        with open('log_depth_cam_file.csv', mode='w', newline='') as log_depth_cam:
            log_depth_cam_writer = csv.writer(log_depth_cam, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
            log_depth_cam_writer.writerow(
                ['frame', 'timestamp', 'x', 'y', 'z', 'pitch', 'yaw', 'roll', 'field of view', 'height', 'width',
                 'raw data'])

        def Log_Depth_callback(image):
            print("Logarithmic Depth image detected:\n" + str(image) + '\n')
            with open('log_depth_cam_file.csv', mode='a', newline='') as log_depth_cam:
                log_depth_cam_app = csv.writer(log_depth_cam, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
                log_depth_cam_app.writerow(
                    [image.frame, image.timestamp, image.transform.location.x, image.transform.location.y,
                     image.transform.location.z, image.transform.rotation.pitch, image.transform.rotation.yaw,
                     image.transform.rotation.roll, image.fov, image.height, image.width, image.raw_data])

        # This time, a color converter is applied to the image, to get the semantic segmentation view
        depth_cam.listen(lambda image: Log_Depth_callback(image))

        # --------------
        # Add a Depth camera to ego vehicle.
        # carla.Image:
        #   frame; timestamp; transform
        #   fov; height; width; raw_data
        #   convert(); save_to_disk()
        # --------------

        depth_cam02 = None
        depth_bp02 = world.get_blueprint_library().find('sensor.camera.depth')
        depth_bp02.set_attribute("image_size_x", str(1920))
        depth_bp02.set_attribute("image_size_y", str(1080))
        depth_bp02.set_attribute("fov", str(105))
        depth_location02 = carla.Location(2, 0, 1)
        depth_rotation02 = carla.Rotation(0, 180, 0)
        depth_transform02 = carla.Transform(depth_location02, depth_rotation02)
        depth_cam02 = world.spawn_actor(depth_bp02, depth_transform02, attach_to=ego_vehicle,
                                        attachment_type=carla.AttachmentType.Rigid)
        with open('depth_cam_file.csv', mode='w', newline='') as depth_cam:
            depth_cam_writer = csv.writer(depth_cam, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
            depth_cam_writer.writerow(
                ['frame', 'timestamp', 'x', 'y', 'z', 'pitch', 'yaw', 'roll', 'field of view', 'height', 'width',
                 'raw data'])

        def depth_callback(image):
            print("Depth image detected:\n" + str(image) + '\n')
            with open('depth_cam_file.csv', mode='a', newline='') as depth_cam:
                depth_cam_app = csv.writer(depth_cam, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
                depth_cam_app.writerow(
                    [image.frame, image.timestamp, image.transform.location.x, image.transform.location.y,
                     image.transform.location.z, image.transform.rotation.pitch, image.transform.rotation.yaw,
                     image.transform.rotation.roll, image.fov, image.height, image.width, image.raw_data])

        # This time, a color converter is applied to the image, to get the semantic segmentation view
        depth_cam02.listen(lambda image: depth_callback(image))

        # --------------
        # Add a new semantic segmentation camera to ego vehicle
        # carla.Image:
        #   frame; timestamp; transform
        #   fov; height; width; raw_data
        #   convert(); save_to_disk()
        # --------------

        sem_cam = None
        sem_bp = world.get_blueprint_library().find('sensor.camera.semantic_segmentation')
        sem_bp.set_attribute("image_size_x", str(1920))
        sem_bp.set_attribute("image_size_y", str(1080))
        sem_bp.set_attribute("fov", str(105))
        sem_location = carla.Location(2, 0, 1)
        sem_rotation = carla.Rotation(0, 180, 0)
        sem_transform = carla.Transform(sem_location, sem_rotation)
        sem_cam = world.spawn_actor(sem_bp, sem_transform, attach_to=ego_vehicle,
                                    attachment_type=carla.AttachmentType.Rigid)
        with open('sem_cam_file.csv', mode='w', newline='') as sem_cam:
            sem_cam_writer = csv.writer(sem_cam, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
            sem_cam_writer.writerow(
                ['frame', 'timestamp', 'x', 'y', 'z', 'pitch', 'yaw', 'roll', 'field of view', 'height', 'width',
                 'raw data'])

        def sem_callback(image):
            print("Semantic segmentation image detected:\n" + str(image) + '\n')
            with open('sem_cam_file.csv', mode='a', newline='') as sem_cam:
                sem_cam_app = csv.writer(sem_cam, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
                sem_cam_app.writerow(
                    [image.frame, image.timestamp, image.transform.location.x, image.transform.location.y,
                     image.transform.location.z, image.transform.rotation.pitch, image.transform.rotation.yaw,
                     image.transform.rotation.roll, image.fov, image.height, image.width, image.raw_data])

        # This time, a color converter is applied to the image, to get the semantic segmentation view
        sem_cam.listen(lambda image: sem_callback(image))

        # --------------
        # Add a new radar sensor to ego vehicle
        # carla.RadarMeasurement:
        #   frame; timestamp; transform
        #   raw_data
        #   get_detection_count()
        # --------------

        rad_cam = None
        rad_bp = world.get_blueprint_library().find('sensor.other.radar')
        rad_bp.set_attribute('horizontal_fov', str(35))
        rad_bp.set_attribute('vertical_fov', str(20))
        rad_bp.set_attribute('range', str(20))
        rad_location = carla.Location(x=2.8, z=1.0)
        rad_rotation = carla.Rotation(pitch=5)
        rad_transform = carla.Transform(rad_location, rad_rotation)
        rad_ego = world.spawn_actor(rad_bp, rad_transform, attach_to=ego_vehicle,
                                    attachment_type=carla.AttachmentType.Rigid)
        with open('radar_data_file.csv', mode='w', newline='') as radar_data:
            radar_data_writer = csv.writer(radar_data, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
            radar_data_writer.writerow(
                ['frame', 'timestamp', 'x', 'y', 'z', 'pitch', 'yaw', 'roll', 'raw data'])

        def rad_callback(radar_data):
            # velocity_range = 7.5  # m/s
            # current_rot = radar_data.transform.rotation
            # for detect in radar_data:
            #     azi = math.degrees(detect.azimuth)
            #     alt = math.degrees(detect.altitude)
            #     # The 0.25 adjusts a bit the distance so the dots can
            #     # be properly seen
            #     fw_vec = carla.Vector3D(x=detect.depth - 0.25)
            #     carla.Transform(
            #         carla.Location(),
            #         carla.Rotation(
            #             pitch=current_rot.pitch + alt,
            #             yaw=current_rot.yaw + azi,
            #             roll=current_rot.roll)).transform(fw_vec)
            #
            #     def clamp(min_v, max_v, value):
            #         return max(min_v, min(value, max_v))
            #
            #     norm_velocity = detect.velocity / velocity_range  # range [-1, 1]
            #     r = int(clamp(0.0, 1.0, 1.0 - norm_velocity) * 255.0)
            #     g = int(clamp(0.0, 1.0, 1.0 - abs(norm_velocity)) * 255.0)
            #     b = int(abs(clamp(- 1.0, 0.0, - 1.0 - norm_velocity)) * 255.0)
            #     world.debug.draw_point(
            #         radar_data.transform.location + fw_vec,
            #         size=0.075,
            #         life_time=0.06,
            #         persistent_lines=False,
            #         color=carla.Color(r, g, b))

            with open('radar_data_file.csv', mode='a', newline='') as radar:
                radar_data_app = csv.writer(radar, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
                radar_data_app.writerow(
                    [radar_data.frame, radar_data.timestamp, radar_data.transform.location.x, radar_data.transform.location.y,
                     radar_data.transform.location.z, radar_data.transform.rotation.pitch, radar_data.transform.rotation.yaw,
                     radar_data.transform.rotation.roll, radar_data.raw_data])

        rad_ego.listen(lambda radar_data: rad_callback(radar_data))

        # --------------
        # Add a new LIDAR sensor to ego vehicle
        # carla.LidarMeasurement
        #   frame; timestamp; transform
        #   channels; horizontal_angle; raw_data
        #   save_to_disk(); get_point_count()
        # --------------

        lidar_cam = None
        lidar_bp = world.get_blueprint_library().find('sensor.lidar.ray_cast')
        lidar_bp.set_attribute('channels', str(32))
        lidar_bp.set_attribute('points_per_second', str(90000))
        lidar_bp.set_attribute('rotation_frequency', str(40))
        lidar_bp.set_attribute('range', str(20))
        lidar_location = carla.Location(0, 0, 2)
        lidar_rotation = carla.Rotation(0, 0, 0)
        lidar_transform = carla.Transform(lidar_location, lidar_rotation)
        lidar_sen = world.spawn_actor(lidar_bp, lidar_transform, attach_to=ego_vehicle,
                                      attachment_type=carla.AttachmentType.Rigid)
        with open('lidar_data_file.csv', mode='w', newline='') as lidar_data:
            lidar_data_writer = csv.writer(lidar_data, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
            lidar_data_writer.writerow(
                ['frame', 'timestamp', 'x', 'y', 'z', 'pitch', 'yaw', 'roll', 'channels', 'horizontal_angle', 'raw data'])

        def lidar_callback(point_cloud):
            print("Lidar detected:\n" + str(point_cloud) + '\n')
            with open('radar_data_file.csv', mode='a', newline='') as lidar_data:
                lidar_data_app = csv.writer(lidar_data, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
                lidar_data_app.writerow(
                    [point_cloud.frame, point_cloud.timestamp, point_cloud.transform.location.x, point_cloud.transform.location.y,
                     point_cloud.transform.location.z, point_cloud.transform.rotation.pitch, point_cloud.transform.rotation.yaw,
                     point_cloud.transform.rotation.roll, point_cloud.channels, point_cloud.horizontal_angle, point_cloud.raw_data])

        lidar_sen.listen(lambda point_cloud: lidar_callback(point_cloud))

        # --------------
        # Game loop. Prevents the script from finishing.
        # --------------
        while True:
            world_snapshot = world.wait_for_tick()

    finally:
        # --------------
        # Destroy actors
        # --------------
        if ego_vehicle is not None:
            if ego_cam is not None:
                ego_cam.stop()
                ego_cam.destroy()
            if depth_cam is not None:
                depth_cam.stop()
                depth_cam.destroy()
            if sem_cam is not None:
                sem_cam.stop()
                sem_cam.destroy()
            if rad_ego is not None:
                rad_ego.stop()
                rad_ego.destroy()
            if lidar_sen is not None:
                lidar_sen.stop()
                lidar_sen.destroy()
            ego_vehicle.destroy()
        print('\nNothing to be done.')


if __name__ == '__main__':

    try:
        main()
    except KeyboardInterrupt:
        pass
    finally:
        print('\nDone with tutorial_replay.')
