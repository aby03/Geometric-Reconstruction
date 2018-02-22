from models import object_detection
from config import config
import cv2
import tensorflow as tf

import imutils
import urllib.request
import numpy as np

url='http://10.194.51.143:8080/shot.jpg'


model_name = config.models["2"]
net = object_detection.Net(graph_fp='%s/frozen_inference_graph.pb' % model_name,
                           labels_fp='data/label.pbtxt',
                           num_classes=90,
                           threshold=0.3)
CAMERA_MODE = 'camera'
STATIC_MODE = 'static'
IP_CAMERA_MODE = 'ip camera'
VIDEO_MODE = 'video'
IMAGE_SIZE = 320

def rotateImage(image, angle):
    image0 = image
    if hasattr(image, 'shape'):
        image_center = tuple(np.array(image.shape)/2)
        shape = tuple(image.shape)
    elif hasattr(image, 'width') and hasattr(image, 'height'):
        image_center = tuple(np.array((image.width/2, image.height/2)))
        shape = (image.width, image.height)
    else:
        print('Unable to acquire dimensions of image for type %s.' % (type(image),))
    rot_mat = cv2.getRotationMatrix2D(image_center, angle,1.0)
    image = np.asarray( image[:,:] )

    rotated_image = cv2.warpAffine(image, rot_mat, shape, flags=cv2.INTER_LINEAR)

    # Copy the rotated data back into the original image object.
    cv2.SetData(image0, rotated_image.tostring())

    return image0

def demo(mode=CAMERA_MODE):
    if mode == STATIC_MODE:
        img_fp = 'test_images/2.jpg'
        img = cv2.imread(img_fp)
        net.predict(img=img, display_img=img)
        cv2.waitKey()
        cv2.destroyAllWindows()
    elif mode == VIDEO_MODE:
        video_file = 'Database_Link/v1.mp4'
        cap = cv2.VideoCapture(video_file)

        while True:
            with tf.device('/gpu:0'):
                ret, frame = cap.read()
                frame = imutils.rotate(frame, -90)
                in_progress = net.get_status()
                if ret and (not in_progress):
                    resize_frame = cv2.resize(frame, (IMAGE_SIZE, IMAGE_SIZE))
                    net.predict(img=resize_frame, display_img=frame)
                else:
                    print('[Warning] drop frame or in progress')
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break

        cap.release()
        cv2.destroyAllWindows()
    elif mode == CAMERA_MODE:
        cap = cv2.VideoCapture(0)

        while True:
            with tf.device('/gpu:0'):
                ret, frame = cap.read()
                in_progress = net.get_status()
                if ret and (not in_progress):
                    resize_frame = cv2.resize(frame, (IMAGE_SIZE, IMAGE_SIZE))
                    net.predict(img=resize_frame, display_img=frame)
                else:
                    print('[Warning] drop frame or in progress')
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break

        cap.release()
        cv2.destroyAllWindows()
    elif mode == IP_CAMERA_MODE:
        while True:
            with tf.device('/gpu:0'):
                # IP Camera
                imgResp=urllib.request.urlopen(url)
                imgNp=np.array(bytearray(imgResp.read()),dtype=np.uint8)
                frame=cv2.imdecode(imgNp,-1)
                ret = True
                # Camera end
                in_progress = net.get_status()
                if ret and (not in_progress):
                    resize_frame = cv2.resize(frame, (IMAGE_SIZE, IMAGE_SIZE))
                    net.predict(img=resize_frame, display_img=frame)
                else:
                    print('[Warning] drop frame or in progress')
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break

        cap.release()
        cv2.destroyAllWindows()


if __name__ == '__main__':
    demo(mode=VIDEO_MODE)
