import numpy as np
import cv2
import matplotlib.pyplot as plt
import math
import _pickle as pickle
import time
  
import img_tags

def get_img_res(inp_img):
	start = time.time()
	tags = img_tags.img_tags

	orb = cv2.ORB_create()
	kp2, des2=orb.detectAndCompute(inp_img,None)

	# Load Database
	keypoint_db=pickle.load(open("keypoint_database.p","rb")) 
	db_size = len(keypoint_db)
	print(type(keypoint_db))
	print("Database size is ", db_size)

	# find the keypoints and descriptors with orb
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
	    FLANN_INDEX_LSH = 1
	    #index_params = dict(algorithm = FLANN_INDEX_KDTREE, trees = 5)
	    index_params = dict(algorithm = FLANN_INDEX_LSH, table_number = 6, key_size = 12, multi_probe_level = 1)
	    search_params = dict(checks=50)   # or pass empty dictionary
	    flann = cv2.FlannBasedMatcher(index_params,search_params)

	    matches = flann.knnMatch(np.asarray(des1,np.float32),np.asarray(des2,np.float32), 2)

	    # Need to draw only good matches, so create a mask
	    matchesMask = [[0,0] for i in range(len(matches))]
	    score =[0]*len(matches)
	    a=0.5 # arbitrary positive real number to calculate the score 
	    # ratio test as per Lowe's paper
	    sum_score=0.0
	    for i,(m,n) in enumerate(matches):
	        if m.distance < 0.7*n.distance:
	            matchesMask[i]=[1,0]
	            score.append(math.exp(-a*m.distance))  
	            # score[i]=math.exp(-a*m.distance)
	            # sum_score+=score[i]            
	    
	    
	    sum_score=sum(score)
	    if len(score)==0:     
	    	avg_score=sum_score/(len(score)+1)
	    else :
	    	avg_score=sum_score+len(score)

	    #print(avg_score)
	    avg_score_list.append(avg_score)

	max_score=0.0 

	for i in range(db_size):
	    if avg_score_list[i]>max_score:
	        max_score=avg_score_list[i]
	        t_img_index=i
	img_index = t_img_index + 1
	if (img_index <= len(tags)):
		tag = tags[str(t_img_index+1)]
	else:
		tag = "NOT FOUND"
	score = max_score
	stop = time.time()
	print("Orb Time = ", stop-start)
	cv2.imshow('a',)
	return [t_img_index, tag, max_score]


#test_img=cv2.imread("3.jpg")
#print(type(test_img))
'''
test_img=cv2.imread("3.jpg")  
[a, b, c] = get_img_res(test_img)
print(a)
print(b)
'''

#         draw_params = dict(matchColor = (0,255,0),
#                        singlePointColor = (255,0,0),
#                        matchesMask = matchesMask,
#                        flags = 0)
#     # img3 = cv2.drawMatchesKnn(img1,kp1,img2,kp2,matches,None,**draw_params)
#         fin_img = cv2.drawMatchesKnn(img,kp1,test_img,kp2,matches,None,**draw_params)


# #*******************changed by P**********************    
#     cv2.imshow('image',fin_img)
#     cv2.waitKey(100)
#*****************************************************    

#plt.imshow(img3,),plt.show()
#    if cv2.waitKey(1) & 0xFF == ord('q'):
#        break
    
#cap.release()
#cv2.destroyAllWindows()

