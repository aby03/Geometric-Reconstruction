import numpy as np
import cv2
import matplotlib.pyplot as plt
import math
from RootSift import RootSIFT

import img_tags
  
def get_img_res(test_img):
    count=0
    match_error = False
    sift = cv2.xfeatures2d.SIFT_create()
    kp2, des2 = sift.detectAndCompute(test_img,None)   

    rs = RootSIFT()
    kp2, des2 = rs.compute(test_img,kp2) 

    train_img = []
    for i in range(0,84):
        fp = "Main_Database/SIT1stfloor/"+str(i)+".jpg"
        frame = cv2.imread(fp)
        train_img.append(frame)
    print("All images read")          
    count+=1
    # find the keypoints and descriptors with SIFT
    score_list=[]
    img_count=0
    for img in train_img :
        img_count+=1
        # gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        kp1, des1 = sift.detectAndCompute(img,None) 
        kp1, des1 = rs.compute(img,kp1)        
        
        # FLANN parameters
        FLANN_INDEX_KDTREE = 1
        index_params = dict(algorithm = FLANN_INDEX_KDTREE, trees = 2)
        search_params = dict(checks=50)   # or pass empty dictionary
        flann = cv2.FlannBasedMatcher(index_params,search_params)
        try:
            match_error = True
            matches = flann.knnMatch(des1,des2,k=2)
            match_error = False
        except:
            print("No location found")
        finally:
            if (match_error):
                return [-1, "Could not locate.", -1]
        # Need to draw only good matches, so create a mask
        matchesMask = [[0,0] for i in range(len(matches))]
        
        a=1.5 # arbitrary positive real number to calculate the score 
        # ratio test as per Lowe's paper
       
        Dlist=[]
        for i,(m,n) in enumerate(matches):
            if m.distance < 0.7*n.distance:
                matchesMask[i]=[1,0]
                # score.append(math.exp(-a*m.distance))
                Dlist.append(m.distance)

        # sum_score=sum(score)
        # avg_score=sum_score/(len(score)+1)
        if len(Dlist)==0 :
            score=0.0
        else:
           score=len(Dlist)/(max(Dlist)+0.0001) 

        #print("img :",img_count," score :",score)                  
        
        # avg_score_list.append(avg_score)
        score_list.append(score)


    score_list=np.array(score_list)
    # score_list2 = sorted(score_list,reverse=True)
    max_indices=score_list.argsort()[-15:][::-1]
    # mx_scores=[]
    # for ind in max_indices :
    #     mx_scores.append(score_list[ind])

    # mx_scores=np.array(mx_scores)

    score_list2 = score_list[max_indices]
    # print(max_indices)  
    print('==== CALC 1 BEST MATCH ',max_indices[0])
    test_gray = cv2.cvtColor(test_img, cv2.COLOR_BGR2GRAY)
    # cv2.imshow('test image',test_img)
    # cv2.waitKey(1000)

    SSIM_score=[]
    avg_filter_score=[]
    print('Max indices ', max_indices)
    for t in max_indices :
        kp2_1,des2_1=sift.detectAndCompute(train_img[t],None)
        kp2_1, des2_1 = rs.compute(train_img[t],kp2_1)      
        FLANN_INDEX_KDTREE = 1
        index_params = dict(algorithm = FLANN_INDEX_KDTREE, trees = 2)
        search_params = dict(checks=50)   # or pass empty dictionary
        flann = cv2.FlannBasedMatcher(index_params,search_params)
        try:
            matches = flann.knnMatch(des2_1,des2,k=2)
        except cv2.error as e:
            print('Error caught')
            return [-1, "Could not localize", 0]
        # Need to draw only good matches, so create a mask
        matchesMask = [[0,0] for i in range(len(matches))]
        
        a=0.5 # arbitrary positive real number to calculate the score 
        # ratio test as per Lowe's paper
       
        filter_score=[]
        #print('Enumerate ',enumerate(matches))
        # for i,(m,n) in enumerate(matches):
            #print('m distance ',m.distance, ' n distance ',n.distance)
            # if m.distance < 0.7 * n.distance:
            #     # print('FS Coming')
            #     matchesMask[i]=[1,0]
            #     filter_score.append(math.exp(-a*m.distance))
                
                
        avg_filter_score.append((sum(filter_score)/(len(filter_score)+0.0001)))
        
    avg_filter_score=np.array(avg_filter_score)
    # tot_score=np.add(avg_filter_score,mx_scores)

     
    #print(avg_filter_score)
    best_matched=np.argmax(avg_filter_score)
    print('==== CALC 2 ', avg_filter_score)

    #print(best_matched) 
    # cv2.imshow('best image',train_img[max_indices[best_matched]])
    # cv2.waitKey(3000)              
    # cv2.destroyAllWindows()
    sorted_avg_score_i = avg_filter_score.argsort()[::-1]
    sorted_avg_score = avg_filter_score[sorted_avg_score_i]

    target_img_index = max_indices[best_matched]
    print('==== IMG INDEX ', target_img_index)
    #max_score = avg_filter_score
    tag = 'Location Info. ' + img_tags.img_tags[str(target_img_index)]
    return [target_img_index, tag]           


