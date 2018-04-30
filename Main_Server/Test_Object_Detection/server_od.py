import sys
sys.path.append('/home/aby03/Desktop/COP/1_A/Main_Server/Test_Object_Detection')
from models import object_detection
from config import config
import cv2
import tensorflow as tf

import imutils
import urllib.request
import numpy as np
import time

def init_net():
    model_name = config.models["3"]
    net = object_detection.Net(graph_fp='Test_Object_Detection/%s/frozen_inference_graph.pb' % model_name,
                               labels_fp='Test_Object_Detection/data/label.pbtxt',
                               num_classes=90,
                               threshold=0.6)
    return net

def replace_last(source_string, replace_what, replace_with):
    head, _sep, tail = source_string.rpartition(replace_what)
    return head + replace_with + tail

def get_obj_str(p_class):    
    obj_str = "There "
    p_class.sort()
    prev = None
    prev_count = 0
    tmp_str = ""
    first = True
    if len(p_class) == 0:
        obj_str = ""
    else:
        for i in p_class:
            tmp_str += str(i)
            if prev == i:
                prev_count += 1
            else:
                if prev != None:
                    if first:
                        if prev_count == 1:
                            obj_str += "is a " + prev
                        else:
                            obj_str += "are " + str(prev_count)+ " " + prev
                        first = False
                    else:
                        if prev_count == 1:
                            obj_str += ", a " + prev
                        else:
                            obj_str += ", " + str(prev_count)+ " " + prev
                prev = i
                prev_count = 1
        if first:
            if prev_count == 1:
                obj_str += "is a " + prev
            else:
                obj_str += "are " + str(prev_count)+ " " + prev
            first = False
        else:
            if prev_count == 1:
                obj_str += ", a " + prev
            else:
                obj_str += ", " + str(prev_count)+ " " + prev
        obj_str += " in view"
        obj_str = replace_last(obj_str, ',', ' and')
        if obj_str.startswith(' and'):
            obj_str = obj_str[4:]
    return obj_str

def get_objects(img, net):


    #img_fp = 'test_images/b.jpg'
    #img = cv2.imread(img_fp)
    start = time.time()
    [p_class, p_score, disp_img] = net.predict(img=img, display_img=img)
    stop = time.time()
    print("obj det Time = ", stop-start)
    # cv2.waitKey(5000)
    #cv2.destroyAllWindows()
    return [p_class, get_obj_str(p_class), p_score, disp_img]

# imgg = cv2.imread("aa.png")
# net = init_net()
# [pcl, psc] = get_objects(imgg, net)
# ss = get_obj_str(pcl)
# print(pcl, type(pcl))
# print(ss)



# s = "1,2,31,2,3"
# r = replace_last(s, ',', ' and ')
# print(r)
# [p_class, p_score] = get_objects(cv2.imread('test_images/i.jpg'))
# print(p_class)
#print(p_class, score)
