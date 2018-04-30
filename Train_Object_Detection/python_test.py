from object_detection.utils import label_map_util

label_map_dict = label_map_util.get_label_map_dict('label.pbtxt')
rev_label_map_dict = {y:x for x,y in label_map_dict.items()}
print(label_map_dict)
print(label_map_dict['door'])
print(rev_label_map_dict)
