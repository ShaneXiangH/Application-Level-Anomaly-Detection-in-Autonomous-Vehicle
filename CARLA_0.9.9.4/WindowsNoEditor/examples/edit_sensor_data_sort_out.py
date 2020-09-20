import glob
import os
import sys
import time

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
    argparser = argparse.ArgumentParser(
        description=__doc__)
    argparser.add_argument(
        '--host',
        metavar='H',
        default='127.0.0.1',
        help='IP of the host server (default: 127.0.0.1)')
    argparser.add_argument(
        '-p', '--port',
        metavar='P',
        default=2000,
        type=int,
        help='TCP port to listen to (default: 2000)')
    args = argparser.parse_args()

    logging.basicConfig(format='%(levelname)s: %(message)s', level=logging.INFO)

    client = carla.Client(args.host, args.port)
    client.set_timeout(10.0)

    try:

        world = client.get_world()
        # world_set = world.get_settings()
        # world_set.synchronous_mode = True
        # world_set.fixed_delta_seconds = 0.1
        # world.apply_settings(world_set)

        ego_vehicle = None
        ego_cam = None
        ego_col = None
        ego_lane = None
        ego_obs = None
        ego_gnss = None
        ego_imu = None

        depth_cam = None
        depth_cam02 = None
        sem_cam = None
        rad_ego = None
        lidar_sen = None

        # --------------
        # Start recording
        # --------------
        """
        client.start_recorder('~/tutorial/recorder/recording01.log')
        """

        with open('edit_sensor_data_sort.csv', mode='w', newline='') as sensor_data_sort:
            sensor_data_sort_writer = csv.writer(sensor_data_sort, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)

        # --------------
        # Spawn ego vehicle
        # --------------

        ego_bp = world.get_blueprint_library().find('vehicle.tesla.model3')
        ego_bp.set_attribute('role_name', 'ego')
        print('\nEgo role_name is set')
        ego_color = random.choice(ego_bp.get_attribute('color').recommended_values)
        ego_bp.set_attribute('color', ego_color)
        print('\nEgo color is set')

        spawn_points = world.get_map().get_spawn_points()
        number_of_spawn_points = len(spawn_points)

        if 0 < number_of_spawn_points:
            random.shuffle(spawn_points)
            ego_transform = spawn_points[0]
            ego_vehicle = world.spawn_actor(ego_bp, ego_transform)
            print('\nEgo is spawned')
        else:
            logging.warning('Could not found any spawn points')

        # world.tick()

        # --------------
        # Add a RGB camera sensor to ego vehicle.
        # carla.Image:
        #   frame; timestamp; transform
        #   fov; height; width; raw_data
        #   convert(); save_to_disk()
        # --------------

        # cam_bp = None
        # cam_bp = world.get_blueprint_library().find('sensor.camera.rgb')
        # cam_bp.set_attribute("image_size_x", str(1920))
        # cam_bp.set_attribute("image_size_y", str(1080))
        # cam_bp.set_attribute("fov", str(105))
        # cam_location = carla.Location(2, 0, 1)
        # cam_rotation = carla.Rotation(0, 180, 0)
        # cam_transform = carla.Transform(cam_location, cam_rotation)
        # ego_cam = world.spawn_actor(cam_bp, cam_transform, attach_to=ego_vehicle,
        #                             attachment_type=carla.AttachmentType.Rigid)

        # def cam_callback(image):
        #     # world.tick()
        #     print("RGB image detected:\n" + str(image))
        #     # print("frame: " + str(image.frame) + "; "
        #     #       + "timestamp: " + str(image.timestamp) + "; \n"
        #     #       + "transform: " + str(image.transform) + "; \n"
        #     #       + "field of view: " + str(image.fov) + "; \n"
        #     #       + "height: " + str(image.height) + "; \n"
        #     #       + "width: " + str(image.width) + "; \n"
        #     #       + "raw data: " + str(image.raw_data) + "; \n"
        #     #       )
        #     with open('edit_sensor_data_sort.csv', mode='a', newline='') as rgb_cam:
        #         rgb_cam_app = csv.writer(rgb_cam, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        #         rgb_cam_app.writerow(
        #             ['rgb_cam_file:', 'frame', 'timestamp', 'x', 'y', 'z', 'pitch', 'yaw', 'roll', 'field of view',
        #              'height', 'width',
        #              'raw data'])
        #         rgb_cam_app.writerow(
        #             ['', image.frame, image.timestamp, image.transform.location.x, image.transform.location.y,
        #              image.transform.location.z, image.transform.rotation.pitch, image.transform.rotation.yaw,
        #              image.transform.rotation.roll, image.fov, image.height, image.width, image.raw_data])

        # ego_cam.listen(lambda image: cam_callback(image))

        # --------------
        # Add collision sensor to ego vehicle.
        # carla.CollisionEvent:
        #   frame; timestamp; transform
        #   actor; other_actor; normal_impulse
        # --------------

        col_bp = world.get_blueprint_library().find('sensor.other.collision')
        col_location = carla.Location(0, 0, 0)
        col_rotation = carla.Rotation(0, 0, 0)
        col_transform = carla.Transform(col_location, col_rotation)
        ego_col = world.spawn_actor(col_bp, col_transform, attach_to=ego_vehicle,
                                    attachment_type=carla.AttachmentType.Rigid)

        def col_callback(colli):
            # world.tick()
            print("Collision detected:\n" + str(colli) + '\n')
            with open('edit_sensor_data_sort.csv', mode='a', newline='') as col:
                colli_app = csv.writer(col, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
                colli_app.writerow(
                    ['colli_file:', 'frame', 'timestamp', 'x', 'y', 'z', 'pitch', 'yaw', 'roll', 'actor', 'other_actor',
                     'normal_impulse'])
                colli_app.writerow(
                    ['', colli.frame, colli.timestamp, colli.transform.location.x, colli.transform.location.y,
                     colli.transform.location.z, colli.transform.rotation.pitch, colli.transform.rotation.yaw,
                     colli.transform.rotation.roll, colli.actor, colli.other_actor, colli.normal_impulse])

        ego_col.listen(lambda colli: col_callback(colli))

        # --------------
        # Add Lane invasion sensor to ego vehicle.
        # carla.LaneInvasionEvent:
        #   frame; timestamp; transform
        #   actor; crossed_lane_markings
        # --------------
        
        # lane_bp = world.get_blueprint_library().find('sensor.other.lane_invasion')
        # lane_location = carla.Location(0, 0, 0)
        # lane_rotation = carla.Rotation(0, 0, 0)
        # lane_transform = carla.Transform(lane_location, lane_rotation)
        # ego_lane = world.spawn_actor(lane_bp, lane_transform, attach_to=ego_vehicle,
        #                              attachment_type=carla.AttachmentType.Rigid)
        
        # def lane_callback(lane):
        #     # world.tick()
        #     print("Lane invasion detected:\n" + str(lane) + '\n')
        #     with open('edit_sensor_data_sort.csv', mode='a', newline='') as lan:
        #         lane_app = csv.writer(lan, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        #         lane_app.writerow(
        #             ['lane_file:', 'frame', 'timestamp', 'x', 'y', 'z', 'pitch', 'yaw', 'roll', 'actor id', 'crossed lane markings'])
        #         lane_app.writerow(
        #             ['', lane.frame, lane.timestamp, lane.transform.location.x, lane.transform.location.y,
        #              lane.transform.location.z, lane.transform.rotation.pitch, lane.transform.rotation.yaw,
        #              lane.transform.rotation.roll, lane.actor.id, lane.crossed_lane_markings])
        
        # ego_lane.listen(lambda lane: lane_callback(lane))

        # --------------
        # Add Obstacle sensor to ego vehicle.
        # carla.ObstacleDetectionEvent:
        #   frame; timestamp; transform
        #   actor; other_actor; distance
        # --------------

        obs_bp = world.get_blueprint_library().find('sensor.other.obstacle')
        obs_bp.set_attribute("only_dynamics", str(True))
        obs_location = carla.Location(0, 0, 0)
        obs_rotation = carla.Rotation(0, 0, 0)
        obs_transform = carla.Transform(obs_location, obs_rotation)
        ego_obs = world.spawn_actor(obs_bp, obs_transform, attach_to=ego_vehicle,
                                    attachment_type=carla.AttachmentType.Rigid)

        def obs_callback(obs):
            # world.tick()
            print("Obstacle detected:\n" + str(obs) + '\n')
            with open('edit_sensor_data_sort.csv', mode='a', newline='') as obsta:
                obs_app = csv.writer(obsta, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
                obs_app.writerow(
                    ['obs_file:', 'frame', 'timestamp', 'x', 'y', 'z', 'pitch', 'yaw', 'roll', 'actor id', 'other actor id', 'distance'])
                obs_app.writerow(
                    ['', obs.frame, obs.timestamp, obs.transform.location.x, obs.transform.location.y,
                     obs.transform.location.z, obs.transform.rotation.pitch, obs.transform.rotation.yaw,
                     obs.transform.rotation.roll, obs.actor.id, obs.other_actor.id, obs.distance])

        ego_obs.listen(lambda obs: obs_callback(obs))

        # --------------
        # Add GNSS sensor to ego vehicle.
        # carla.GnssMeasurement:
        #   frame; timestamp; transform
        #   altitude; latitude; longitude
        # --------------

        # gnss_bp = world.get_blueprint_library().find('sensor.other.gnss')
        # gnss_location = carla.Location(0, 0, 0)
        # gnss_rotation = carla.Rotation(0, 0, 0)
        # gnss_transform = carla.Transform(gnss_location, gnss_rotation)
        # gnss_bp.set_attribute("sensor_tick", str(3.0))
        # ego_gnss = world.spawn_actor(gnss_bp, gnss_transform, attach_to=ego_vehicle,
        #                              attachment_type=carla.AttachmentType.Rigid)

        # def gnss_callback(gnss):
        #     # world.tick()
        #     print("GNSS measure:\n" + str(gnss) + '\n')
        #     with open('edit_sensor_data_sort.csv', mode='a', newline='') as gns:
        #         gnss_app = csv.writer(gns, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        #         gnss_app.writerow(
        #             ['gnss_file:', 'frame', 'timestamp', 'x', 'y', 'z', 'pitch', 'yaw', 'roll', 'altitude', 'latitude', 'longitude'])
        #         gnss_app.writerow(
        #             ['', gnss.frame, gnss.timestamp, gnss.transform.location.x, gnss.transform.location.y,
        #              gnss.transform.location.z, gnss.transform.rotation.pitch, gnss.transform.rotation.yaw,
        #              gnss.transform.rotation.roll, gnss.altitude, gnss.latitude, gnss.longitude])

        # ego_gnss.listen(lambda gnss: gnss_callback(gnss))

        # --------------
        # Add IMU sensor to ego vehicle.
        # carla.IMUMeasurement:
        #   frame; timestamp; transform
        #   accelerometer; compass; gyroscope
        # --------------

        # imu_bp = world.get_blueprint_library().find('sensor.other.imu')
        # imu_location = carla.Location(0, 0, 0)
        # imu_rotation = carla.Rotation(0, 0, 0)
        # imu_transform = carla.Transform(imu_location, imu_rotation)
        # imu_bp.set_attribute("sensor_tick", str(3.0))
        # ego_imu = world.spawn_actor(imu_bp, imu_transform, attach_to=ego_vehicle,
        #                             attachment_type=carla.AttachmentType.Rigid)

        # def imu_callback(imu):
        #     # world.tick()
        #     print("IMU measure:\n" + str(imu) + '\n')
        #     with open('edit_sensor_data_sort.csv', mode='a', newline='') as imuu:
        #         imu_app = csv.writer(imuu, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        #         imu_app.writerow(
        #             ['imu_file:', 'frame', 'timestamp', 'x', 'y', 'z', 'pitch', 'yaw', 'roll', 'accelerometer x', 'accelerometer y',
        #              'accelerometer z', 'compass', 'gyroscope x', 'gyroscope y', 'gyroscope z'])
        #         imu_app.writerow(
        #             ['', imu.frame, imu.timestamp, imu.transform.location.x, imu.transform.location.y,
        #              imu.transform.location.z, imu.transform.rotation.pitch, imu.transform.rotation.yaw,
        #              imu.transform.rotation.roll, imu.accelerometer.x, imu.accelerometer.y, imu.accelerometer.z,
        #              imu.compass, imu.gyroscope.x, imu.gyroscope.y, imu.gyroscope.z])

        # ego_imu.listen(lambda imu: imu_callback(imu))

        # --------------
        # Add a Logarithmic Depth camera to ego vehicle.
        # carla.Image:
        #   frame; timestamp; transform
        #   fov; height; width; raw_data
        #   convert(); save_to_disk()
        # --------------

        # depth_bp = world.get_blueprint_library().find('sensor.camera.depth')
        # depth_bp.set_attribute("image_size_x", str(1920))
        # depth_bp.set_attribute("image_size_y", str(1080))
        # depth_bp.set_attribute("fov", str(105))
        # depth_location = carla.Location(2, 0, 1)
        # depth_rotation = carla.Rotation(0, 180, 0)
        # depth_transform = carla.Transform(depth_location, depth_rotation)
        # depth_cam = world.spawn_actor(depth_bp, depth_transform, attach_to=ego_vehicle,
        #                               attachment_type=carla.AttachmentType.Rigid)

        # def Log_Depth_callback(image):
        #     # world.tick()
        #     print("Logarithmic Depth image detected:\n" + str(image) + '\n')
        #     with open('edit_sensor_data_sort.csv', mode='a', newline='') as log_depth_ca:
        #         log_depth_cam_app = csv.writer(log_depth_ca, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        #         log_depth_cam_app.writerow(
        #             ['log_depth_cam_file:', 'frame', 'timestamp', 'x', 'y', 'z', 'pitch', 'yaw', 'roll', 'field of view', 'height', 'width',
        #              'raw data'])
        #         log_depth_cam_app.writerow(
        #             ['', image.frame, image.timestamp, image.transform.location.x, image.transform.location.y,
        #              image.transform.location.z, image.transform.rotation.pitch, image.transform.rotation.yaw,
        #              image.transform.rotation.roll, image.fov, image.height, image.width, image.raw_data])

        # # This time, a color converter is applied to the image, to get the semantic segmentation view
        # depth_cam.listen(lambda image: Log_Depth_callback(image))

        # --------------
        # Add a Depth camera to ego vehicle.
        # carla.Image:
        #   frame; timestamp; transform
        #   fov; height; width; raw_data
        #   convert(); save_to_disk()
        # --------------

        # depth_bp02 = world.get_blueprint_library().find('sensor.camera.depth')
        # depth_bp02.set_attribute("image_size_x", str(1920))
        # depth_bp02.set_attribute("image_size_y", str(1080))
        # depth_bp02.set_attribute("fov", str(105))
        # depth_location02 = carla.Location(2, 0, 1)
        # depth_rotation02 = carla.Rotation(0, 180, 0)
        # depth_transform02 = carla.Transform(depth_location02, depth_rotation02)
        # depth_cam02 = world.spawn_actor(depth_bp02, depth_transform02, attach_to=ego_vehicle,
        #                                 attachment_type=carla.AttachmentType.Rigid)

        # def depth_callback(image):
        #     # world.tick()
        #     print("Depth image detected:\n" + str(image) + '\n')
        #     with open('edit_sensor_data_sort.csv', mode='a', newline='') as depth_cam:
        #         depth_cam_app = csv.writer(depth_cam, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        #         depth_cam_app.writerow(
        #             ['depth_cam_file:', 'frame', 'timestamp', 'x', 'y', 'z', 'pitch', 'yaw', 'roll', 'field of view', 'height', 'width',
        #              'raw data'])
        #         depth_cam_app.writerow(
        #             ['', image.frame, image.timestamp, image.transform.location.x, image.transform.location.y,
        #              image.transform.location.z, image.transform.rotation.pitch, image.transform.rotation.yaw,
        #              image.transform.rotation.roll, image.fov, image.height, image.width, image.raw_data])

        # # This time, a color converter is applied to the image, to get the semantic segmentation view
        # depth_cam02.listen(lambda image: depth_callback(image))

        # --------------
        # Add a new semantic segmentation camera to ego vehicle
        # carla.Image:
        #   frame; timestamp; transform
        #   fov; height; width; raw_data
        #   convert(); save_to_disk()
        # --------------

        # sem_bp = world.get_blueprint_library().find('sensor.camera.semantic_segmentation')
        # sem_bp.set_attribute("image_size_x", str(1920))
        # sem_bp.set_attribute("image_size_y", str(1080))
        # sem_bp.set_attribute("fov", str(105))
        # sem_location = carla.Location(2, 0, 1)
        # sem_rotation = carla.Rotation(0, 180, 0)
        # sem_transform = carla.Transform(sem_location, sem_rotation)
        # sem_cam = world.spawn_actor(sem_bp, sem_transform, attach_to=ego_vehicle,
        #                             attachment_type=carla.AttachmentType.Rigid)

        # def sem_callback(image):
        #     # world.tick()
        #     print("Semantic segmentation image detected:\n" + str(image) + '\n')
        #     with open('edit_sensor_data_sort.csv', mode='a', newline='') as sem:
        #         sem_cam_app = csv.writer(sem, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        #         sem_cam_app.writerow(
        #             ['seg_cam_file:', 'frame', 'timestamp', 'x', 'y', 'z', 'pitch', 'yaw', 'roll', 'field of view', 'height', 'width',
        #              'raw data'])
        #         sem_cam_app.writerow(
        #             ['', image.frame, image.timestamp, image.transform.location.x, image.transform.location.y,
        #              image.transform.location.z, image.transform.rotation.pitch, image.transform.rotation.yaw,
        #              image.transform.rotation.roll, image.fov, image.height, image.width, image.raw_data])

        # # This time, a color converter is applied to the image, to get the semantic segmentation view
        # sem_cam.listen(lambda image: sem_callback(image))

        # --------------
        # Add a new radar sensor to ego vehicle
        # carla.RadarMeasurement:
        #   frame; timestamp; transform
        #   raw_data
        #   get_detection_count()
        # --------------

        # rad_bp = world.get_blueprint_library().find('sensor.other.radar')
        # rad_bp.set_attribute('horizontal_fov', str(35))
        # rad_bp.set_attribute('vertical_fov', str(20))
        # rad_bp.set_attribute('range', str(20))
        # rad_location = carla.Location(x=2.8, z=1.0)
        # rad_rotation = carla.Rotation(pitch=5)
        # rad_transform = carla.Transform(rad_location, rad_rotation)
        # rad_ego = world.spawn_actor(rad_bp, rad_transform, attach_to=ego_vehicle,
        #                             attachment_type=carla.AttachmentType.Rigid)

        # def rad_callback(radar_data):
        #     # world.tick()
        #     # velocity_range = 7.5  # m/s
        #     # current_rot = radar_data.transform.rotation
        #     # for detect in radar_data:
        #     #     azi = math.degrees(detect.azimuth)
        #     #     alt = math.degrees(detect.altitude)
        #     #     # The 0.25 adjusts a bit the distance so the dots can
        #     #     # be properly seen
        #     #     fw_vec = carla.Vector3D(x=detect.depth - 0.25)
        #     #     carla.Transform(
        #     #         carla.Location(),
        #     #         carla.Rotation(
        #     #             pitch=current_rot.pitch + alt,
        #     #             yaw=current_rot.yaw + azi,
        #     #             roll=current_rot.roll)).transform(fw_vec)
        #     #
        #     #     def clamp(min_v, max_v, value):
        #     #         return max(min_v, min(value, max_v))
        #     #
        #     #     norm_velocity = detect.velocity / velocity_range  # range [-1, 1]
        #     #     r = int(clamp(0.0, 1.0, 1.0 - norm_velocity) * 255.0)
        #     #     g = int(clamp(0.0, 1.0, 1.0 - abs(norm_velocity)) * 255.0)
        #     #     b = int(abs(clamp(- 1.0, 0.0, - 1.0 - norm_velocity)) * 255.0)
        #     #     world.debug.draw_point(
        #     #         radar_data.transform.location + fw_vec,
        #     #         size=0.075,
        #     #         life_time=0.06,
        #     #         persistent_lines=False,
        #     #         color=carla.Color(r, g, b))

        #     with open('edit_sensor_data_sort.csv', mode='a', newline='') as radar:
        #         radar_data_app = csv.writer(radar, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        #         radar_data_app.writerow(
        #             ['radar_data_file:', 'frame', 'timestamp', 'x', 'y', 'z', 'pitch', 'yaw', 'roll', 'raw data'])
        #         radar_data_app.writerow(
        #             ['', radar_data.frame, radar_data.timestamp, radar_data.transform.location.x,
        #              radar_data.transform.location.y, radar_data.transform.location.z,
        #              radar_data.transform.rotation.pitch, radar_data.transform.rotation.yaw,
        #              radar_data.transform.rotation.roll, radar_data.raw_data])

        # rad_ego.listen(lambda radar_data: rad_callback(radar_data))

        # --------------
        # Add a new LIDAR sensor to ego vehicle
        # carla.LidarMeasurement
        #   frame; timestamp; transform
        #   channels; horizontal_angle; raw_data
        #   save_to_disk(); get_point_count()
        # --------------

        # lidar_bp = world.get_blueprint_library().find('sensor.lidar.ray_cast')
        # lidar_bp.set_attribute('channels', str(32))
        # lidar_bp.set_attribute('points_per_second', str(90000))
        # lidar_bp.set_attribute('rotation_frequency', str(40))
        # lidar_bp.set_attribute('range', str(20))
        # lidar_location = carla.Location(0, 0, 2)
        # lidar_rotation = carla.Rotation(0, 0, 0)
        # lidar_transform = carla.Transform(lidar_location, lidar_rotation)
        # lidar_sen = world.spawn_actor(lidar_bp, lidar_transform, attach_to=ego_vehicle,
        #                               attachment_type=carla.AttachmentType.Rigid)

        # def lidar_callback(point_cloud):
        #     # world.tick()
        #     print("Lidar detected:\n" + str(point_cloud) + '\n')
        #     with open('edit_sensor_data_sort.csv', mode='a', newline='') as lidar_data:
        #         lidar_data_app = csv.writer(lidar_data, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        #         lidar_data_app.writerow(
        #             ['lidar_data_file:', 'frame', 'timestamp', 'x', 'y', 'z', 'pitch', 'yaw', 'roll', 'channels', 'horizontal_angle',
        #              'raw data'])
        #         lidar_data_app.writerow(
        #             ['', point_cloud.frame, point_cloud.timestamp, point_cloud.transform.location.x,
        #              point_cloud.transform.location.y,
        #              point_cloud.transform.location.z, point_cloud.transform.rotation.pitch,
        #              point_cloud.transform.rotation.yaw,
        #              point_cloud.transform.rotation.roll, point_cloud.channels, point_cloud.horizontal_angle,
        #              point_cloud.raw_data])

        # lidar_sen.listen(lambda point_cloud: lidar_callback(point_cloud))

        # --------------
        # Place spectator on ego spawning
        # --------------

        spectator = world.get_spectator()
        world_snapshot = world.wait_for_tick()
        spectator.set_transform(ego_vehicle.get_transform())

        # --------------
        # Enable autopilot for ego vehicle
        # --------------

        ego_vehicle.set_autopilot(False)

        # --------------
        # Game loop. Prevents the script from finishing.
        # --------------
        while True:
            world_snapshot = world.wait_for_tick()

    finally:
        # --------------
        # Stop recording and destroy actors
        # --------------
        client.stop_recorder()
        if ego_vehicle is not None:
            if ego_cam is not None:
                ego_cam.stop()
                ego_cam.destroy()
            if ego_col is not None:
                ego_col.stop()
                ego_col.destroy()
            if ego_lane is not None:
                ego_lane.stop()
                ego_lane.destroy()
            if ego_obs is not None:
                ego_obs.stop()
                ego_obs.destroy()
            if ego_gnss is not None:
                ego_gnss.stop()
                ego_gnss.destroy()
            if ego_imu is not None:
                ego_imu.stop()
                ego_imu.destroy()

            if depth_cam is not None:
                depth_cam.stop()
                depth_cam.destroy()
            if depth_cam02 is not None:
                depth_cam02.stop()
                depth_cam02.destroy()
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


if __name__ == '__main__':

    try:
        main()
    except KeyboardInterrupt:
        pass
    finally:
        print('\nDone with tutorial_ego.')
