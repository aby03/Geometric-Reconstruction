# -*- coding: utf-8 -*-
"""
Created on Fri Mar  9 09:17:24 2018

@author: DELL
"""

import numpy as np
import cv2
import matplotlib.pyplot as plt
import math
from RootSift import RootSIFT
import _pickle as pickle 

import img_tags
  
def get_img_res(test_img):
    count=0
    sift = cv2.xfeatures2d.SIFT_create()
    #test_img=cv2.imread("t5.jpg")
    # test_gray = cv2.cvtColor(test_img, cv2.COLOR_BGR2GRAY)
    kp2, des2 = sift.detectAndCompute(test_img,None)   

    rs = RootSIFT()
    kp2, des2 = rs.compute(test_img,kp2) 

    keypoint_db=pickle.load(open("keypoint_database.p","rb")) 
    db_size = len(keypoint_db)
    print(type(keypoint_db))
    print("Database size is ", db_size)

    # find the keypoints and descriptors with orb
    score_list=[]
    avg_score_list=[]
    for i in range(db_size):
        kp1=[]
        des1=[]
        for point in keypoint_db[i]:
            temp_feature = cv2.KeyPoint(x=point[0][0],y=point[0][1],_size=point[1], _angle=point[2], _response=point[3], _octave=point[4], _class_id=point[5])
            temp_descripter=point[6]
            kp1.append(temp_feature)
            des1.append(temp_descripter)
             
        des1=np.array(des1)        
        
        # FLANN parameters
        FLANN_INDEX_KDTREE = 1
        index_params = dict(algorithm = FLANN_INDEX_KDTREE, trees = 2)
        search_params = dict(checks=50)   # or pass empty dictionary
        flann = cv2.FlannBasedMatcher(index_params,search_params)
        matches = flann.knnMatch(des1,des2,k=2)
        # Need to draw only good matches, so create a mask
        matchesMask = [[0,0] for i in range(len(matches))]
        
               
        Dlist=[]
        for i,(m,n) in enumerate(matches):
            if m.distance < 0.7*n.distance:
                matchesMask[i]=[1,0]
                # score.append(math.exp(-a*m.distance))
                Dlist.append(m.distance)

        if len(Dlist)==0 :
            score=0.0
        else:
           score=len(Dlist)/(max(Dlist)+0.0001) 

        score_list.append(score)
    

    score_list=np.array(score_list)
    max_indices=score_list.argsort()[-15:][::-1]

    mx_scores=[]
    for ind in max_indices :
        mx_scores.append(score_list[ind])

    mx_scores=np.array(mx_scores)    
       
    # test_gray = cv2.cvtColor(test_img, cv2.COLOR_BGR2GRAY)
    # cv2.imshow('test image',test_img)
    # cv2.waitKey(1000)

    avg_filter_score=[]
    
    for t in max_indices :
        
        kp2_1=[]
        des2_1=[]
        for point in keypoint_db[t]:
            temp_feature = cv2.KeyPoint(x=point[0][0],y=point[0][1],_size=point[1], _angle=point[2], _response=point[3], _octave=point[4], _class_id=point[5])
            temp_descripter=point[6]
            kp2_1.append(temp_feature)
            des2_1.append(temp_descripter)
             
        des2_1=np.array(des2_1)

        FLANN_INDEX_KDTREE = 1
        index_params = dict(algorithm = FLANN_INDEX_KDTREE, trees = 2)
        search_params = dict(checks=50)   # or pass empty dictionary
        flann = cv2.FlannBasedMatcher(index_params,search_params)
        matches = flann.knnMatch(des2_1,des2,k=2)
        # Need to draw only good matches, so create a mask
        matchesMask = [[0,0] for i in range(len(matches))]
        
        a=0.5 # arbitrary positive real number to calculate the score 

        # ratio test as per Lowe's paper       
        filter_score=[]
        for i,(m,n) in enumerate(matches):
            if n.distance-m.distance>0.01:                
                matchesMask[i]=[1,0]
                filter_score.append(math.exp(-a*m.distance))                
                
        avg_filter_score.append((sum(filter_score)/(len(filter_score)+0.0001)))
        
    avg_filter_score=np.array(avg_filter_score)/100

    tot_score=np.add(avg_filter_score,mx_scores)
     
    best_matched=np.argmax(tot_score)
     
    target_img_index = max_indices[best_matched]
    max_score = 0
    tag = 'Location Info. ' + img_tags.img_tags[str(target_img_index)]

    return [target_img_index, tag]
           


