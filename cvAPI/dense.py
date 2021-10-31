# import base64
# import math
# from os import confstr
# import time
# import cv2
# import sys

# sys.path.append('/opt/mycroft/skills/sandbox-git-skill.yuyang0828/cvAPI')
# from util import callAPI, encode_image_from_file

# image_file = '/opt/mycroft/skills/sandbox-git-skill.yuyang0828/photo/1.jpeg'
# image_base64 = encode_image_from_file(image_file)
# response = callAPI(image_base64, 'LOC')
# print(response)

import numpy as np
cost = np.array([[4, 1, 3], [2, 0, 5], [3, 2, 2]])

from scipy.optimize import linear_sum_assignment
row_ind, col_ind = linear_sum_assignment(cost)
print(col_ind)
print(row_ind)
# array([1, 0, 2])
a = cost[row_ind, col_ind].sum()
print(a)
