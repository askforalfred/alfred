import os
import sys
sys.path.append(os.path.join(os.environ['ALFRED_ROOT']))
sys.path.append(os.path.join(os.environ['ALFRED_ROOT'], 'gen'))

import json
import glob
import os
import constants
import cv2
import shutil
import numpy as np
import argparse
import threading
import time
import copy
import random
from utils.video_util import VideoSaver
from utils.py_util import walklevel
from env.thor_env import ThorEnv


TRAJ_DATA_JSON_FILENAME = "traj_data.json"
AUGMENTED_TRAJ_DATA_JSON_FILENAME = "augmented_traj_data.json"

ORIGINAL_IMAGES_FORLDER = "raw_images"
HIGH_RES_IMAGES_FOLDER = "high_res_images"
DEPTH_IMAGES_FOLDER = "depth_images"
INSTANCE_MASKS_FOLDER = "instance_masks"

IMAGE_WIDTH = 600
IMAGE_HEIGHT = 600

render_settings = dict()
render_settings['renderImage'] = True
render_settings['renderDepthImage'] = True
render_settings['renderObjectImage'] = True
render_settings['renderClassImage'] = True

video_saver = VideoSaver()


def get_image_index(save_path):
    return len(glob.glob(save_path + '/*.png'))


def save_image_with_delays(env, action,
                           save_path, direction=constants.BEFORE):
    im_ind = get_image_index(save_path)
    counts = constants.SAVE_FRAME_BEFORE_AND_AFTER_COUNTS[action['action']][direction]
    for i in range(counts):
        save_image(env.last_event, save_path)
        env.noop()
    return im_ind


def save_image(event, save_path):
    # rgb
    rgb_save_path = os.path.join(save_path, HIGH_RES_IMAGES_FOLDER)
    rgb_image = event.frame[:, :, ::-1]

    # depth
    depth_save_path = os.path.join(save_path, DEPTH_IMAGES_FOLDER)
    depth_image = event.depth_frame
    depth_image = depth_image * (255 / 10000)
    depth_image = depth_image.astype(np.uint8)

    # masks
    mask_save_path = os.path.join(save_path, INSTANCE_MASKS_FOLDER)
    mask_image = event.instance_segmentation_frame

    # dump images
    im_ind = get_image_index(rgb_save_path)
    cv2.imwrite(rgb_save_path + '/%09d.png' % im_ind, rgb_image)
    cv2.imwrite(depth_save_path + '/%09d.png' % im_ind, depth_image)
    cv2.imwrite(mask_save_path + '/%09d.png' % im_ind, mask_image)

    return im_ind


def save_images_in_events(events, root_dir):
    for event in events:
        save_image(event, root_dir)


def clear_and_create_dir(path):
    if os.path.exists(path):
        shutil.rmtree(path)
    os.mkdir(path)


def augment_traj(env, json_file):
    # load json data
    with open(json_file) as f:
        traj_data = json.load(f)

    # make directories
    root_dir = json_file.replace(TRAJ_DATA_JSON_FILENAME, "")

    orig_images_dir = os.path.join(root_dir, ORIGINAL_IMAGES_FORLDER)
    high_res_images_dir = os.path.join(root_dir, HIGH_RES_IMAGES_FOLDER)
    depth_images_dir = os.path.join(root_dir, DEPTH_IMAGES_FOLDER)
    instance_masks_dir = os.path.join(root_dir, INSTANCE_MASKS_FOLDER)
    augmented_json_file = os.path.join(root_dir, AUGMENTED_TRAJ_DATA_JSON_FILENAME)

    # fresh images list
    traj_data['images'] = list()

    clear_and_create_dir(high_res_images_dir)
    clear_and_create_dir(depth_images_dir)
    clear_and_create_dir(instance_masks_dir)

    # scene setup
    scene_num = traj_data['scene']['scene_num']
    object_poses = traj_data['scene']['object_poses']
    object_toggles = traj_data['scene']['object_toggles']
    dirty_and_empty = traj_data['scene']['dirty_and_empty']

    # reset
    scene_name = 'FloorPlan%d' % scene_num
    env.reset(scene_name)
    env.restore_scene(object_poses, object_toggles, dirty_and_empty)

    env.step(dict(traj_data['scene']['init_action']))
    print("Task: %s" % (traj_data['template']['task_desc']))

    # setup task
    env.set_task(traj_data, args, reward_type='dense')
    rewards = []

    for ll_idx, ll_action in enumerate(traj_data['plan']['low_actions']):
        # next cmd under the current hl_action
        cmd = ll_action['api_action']
        hl_action = traj_data['plan']['high_pddl'][ll_action['high_idx']]

        # remove unnecessary keys
        cmd = {k: cmd[k] for k in ['action', 'objectId', 'receptacleObjectId', 'placeStationary', 'forceAction'] if k in cmd}

        if "MoveAhead" in cmd['action']:
            if args.smooth_nav:
                save_image(env.last_event, root_dir)
                events = env.smooth_move_ahead(cmd, render_settings)
                save_images_in_events(events, root_dir)
                event = events[-1]
            else:
                save_image(env.last_event, root_dir)
                event = env.step(cmd)

        elif "Rotate" in cmd['action']:
            if args.smooth_nav:
                save_image(env.last_event, root_dir)
                events = env.smooth_rotate(cmd, render_settings)
                save_images_in_events(events, root_dir)
                event = events[-1]
            else:
                save_image(env.last_event, root_dir)
                event = env.step(cmd)

        elif "Look" in cmd['action']:
            if args.smooth_nav:
                save_image(env.last_event, root_dir)
                events = env.smooth_look(cmd, render_settings)
                save_images_in_events(events, root_dir)
                event = events[-1]
            else:
                save_image(env.last_event, root_dir)
                event = env.step(cmd)

        # handle the exception for CoolObject tasks where the actual 'CoolObject' action is actually 'CloseObject'
        # TODO: a proper fix for this issue
        elif "CloseObject" in cmd['action'] and \
             "CoolObject" in hl_action['planner_action']['action'] and \
             "OpenObject" in traj_data['plan']['low_actions'][ll_idx + 1]['api_action']['action']:
            if args.time_delays:
                cool_action = hl_action['planner_action']
                save_image_with_delays(env, cool_action, save_path=root_dir, direction=constants.BEFORE)
                event = env.step(cmd)
                save_image_with_delays(env, cool_action, save_path=root_dir, direction=constants.MIDDLE)
                save_image_with_delays(env, cool_action, save_path=root_dir, direction=constants.AFTER)
            else:
                save_image(env.last_event, root_dir)
                event = env.step(cmd)

        else:
            if args.time_delays:
                save_image_with_delays(env, cmd, save_path=root_dir, direction=constants.BEFORE)
                event = env.step(cmd)
                save_image_with_delays(env, cmd, save_path=root_dir, direction=constants.MIDDLE)
                save_image_with_delays(env, cmd, save_path=root_dir, direction=constants.AFTER)
            else:
                save_image(env.last_event, root_dir)
                event = env.step(cmd)

        # update image list
        new_img_idx = get_image_index(high_res_images_dir)
        last_img_idx = len(traj_data['images'])
        num_new_images = new_img_idx - last_img_idx
        for j in range(num_new_images):
            traj_data['images'].append({
                'low_idx': ll_idx,
                'high_idx': ll_action['high_idx'],
                'image_name': '%09d.png' % int(last_img_idx + j)
            })

        if not event.metadata['lastActionSuccess']:
            raise Exception("Replay Failed: %s" % (env.last_event.metadata['errorMessage']))

        reward, _ = env.get_transition_reward()
        rewards.append(reward)

    # save 10 frames in the end as per the training data
    for _ in range(10):
        save_image(env.last_event, root_dir)

    # store color to object type dictionary
    color_to_obj_id_type = {}
    all_objects = env.last_event.metadata['objects']
    for color, object_id in env.last_event.color_to_object_id.items():
        for obj in all_objects:
            if object_id == obj['objectId']:
                color_to_obj_id_type[str(color)] = {
                    'objectID': obj['objectId'],
                    'objectType': obj['objectType']
                }

    augmented_traj_data = copy.deepcopy(traj_data)
    augmented_traj_data['scene']['color_to_object_type'] = color_to_obj_id_type
    augmented_traj_data['task'] = {'rewards': rewards, 'reward_upper_bound': sum(rewards)}

    with open(augmented_json_file, 'w') as aj:
        json.dump(augmented_traj_data, aj, sort_keys=True, indent=4)

    # save video
    images_path = os.path.join(high_res_images_dir, '*.png')
    video_save_path = os.path.join(high_res_images_dir, 'high_res_video.mp4')
    video_saver.save(images_path, video_save_path)

    # check if number of new images is the same as the number of original images
    if args.smooth_nav and args.time_delays:
        orig_img_count = get_image_index(high_res_images_dir)
        new_img_count = get_image_index(orig_images_dir)
        print ("Original Image Count %d, New Image Count %d" % (orig_img_count, new_img_count))
        if orig_img_count != new_img_count:
            raise Exception("WARNING: the augmented sequence length doesn't match the original")


def run():
    '''
    replay loop
    '''
    # start THOR env
    env = ThorEnv(player_screen_width=IMAGE_WIDTH,
                  player_screen_height=IMAGE_HEIGHT)

    skipped_files = []

    while len(traj_list) > 0:
        lock.acquire()
        json_file = traj_list.pop()
        lock.release()

        print ("Augmenting: " + json_file)
        try:
            augment_traj(env, json_file)
        except Exception as e:
            import traceback
            traceback.print_exc()
            print ("Error: " + repr(e))
            print ("Skipping " + json_file)
            skipped_files.append(json_file)

    env.stop()
    print("Finished.")

    # skipped files
    if len(skipped_files) > 0:
        print("Skipped Files:")
        print(skipped_files)


traj_list = []
lock = threading.Lock()

# parse arguments
parser = argparse.ArgumentParser()
parser.add_argument('--data_path', type=str, default="data/2.1.0")
parser.add_argument('--smooth_nav', dest='smooth_nav', action='store_true')
parser.add_argument('--time_delays', dest='time_delays', action='store_true')
parser.add_argument('--shuffle', dest='shuffle', action='store_true')
parser.add_argument('--num_threads', type=int, default=1)
parser.add_argument('--reward_config', type=str, default='../models/config/rewards.json')
args = parser.parse_args()

# make a list of all the traj_data json files
for dir_name, subdir_list, file_list in walklevel(args.data_path, level=3):
    if "trial_" in dir_name:
        json_file = os.path.join(dir_name, TRAJ_DATA_JSON_FILENAME)
        if not os.path.isfile(json_file) or 'tests' in dir_name:
            continue
        traj_list.append(json_file)

# random shuffle
if args.shuffle:
    random.shuffle(traj_list)

# start threads
threads = []
for n in range(args.num_threads):
    thread = threading.Thread(target=run)
    threads.append(thread)
    thread.start()
    time.sleep(1)
