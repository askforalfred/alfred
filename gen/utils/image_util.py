import numpy as np
import constants

def bbox_to_mask(bbox):
    '''
    bbox to rectangle pixelwise mask
    '''
    x1, y1, x2, y2 = bbox
    mask = np.zeros((constants.DETECTION_SCREEN_HEIGHT, constants.DETECTION_SCREEN_WIDTH)).astype(int)
    mask[y1:y2, x1:x2] = 1
    return mask


def point_to_mask(point):
    '''
    single point to dense pixelwise mask
    '''
    x, y = point
    mask = np.zeros((constants.DETECTION_SCREEN_HEIGHT, constants.DETECTION_SCREEN_WIDTH)).astype(int)
    mask[y, x] = 1
    return mask


def decompress_mask(compressed_mask):
    '''
    decompress compressed mask array
    '''
    mask = np.zeros((constants.DETECTION_SCREEN_WIDTH, constants.DETECTION_SCREEN_HEIGHT))
    for start_idx, run_len in compressed_mask:
        for idx in range(start_idx, start_idx + run_len):
            mask[idx // constants.DETECTION_SCREEN_WIDTH, idx % constants.DETECTION_SCREEN_HEIGHT] = 1
    return mask
