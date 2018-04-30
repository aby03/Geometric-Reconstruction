# Usage
# python xml_to_csv.py --image_path <IMGS DIR> --csv_file <Name of csv file>
# Example Usage
# python xml_to_csv.py --image_path Database/1_A/labelled_images --csv_file labels.csv
import os
import glob
import pandas as pd
import xml.etree.ElementTree as ET

import argparse

def xml_to_csv(path):
    xml_list = []
    for xml_file in glob.glob(path + '/*.xml'):
        tree = ET.parse(xml_file)
        root = tree.getroot()
        for member in root.findall('object'):
            value = (root.find('filename').text,
                     int(root.find('size')[0].text),
                     int(root.find('size')[1].text),
                     member[0].text,
                     int(member[4][0].text),
                     int(member[4][1].text),
                     int(member[4][2].text),
                     int(member[4][3].text)
                     )
            xml_list.append(value)
    column_name = ['filename', 'width', 'height', 'class', 'xmin', 'ymin', 'xmax', 'ymax']
    xml_df = pd.DataFrame(xml_list, columns=column_name)
    return xml_df


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-i','--image_path', required=True, action='store', dest='image_path', help='foo help')
    parser.add_argument('-c','--csv_file', required=True, action='store', dest='csv_file', help='foo help')
    args = parser.parse_args()
    print('Image Path = ' + args.image_path)
    print('CSV File = ' + args.csv_file)
    
    image_path = os.path.join(os.getcwd(), args.image_path)
    xml_df = xml_to_csv(image_path)
    xml_df.to_csv(args.csv_file, index=None)
    print('Successfully converted xml to csv.')

main()
