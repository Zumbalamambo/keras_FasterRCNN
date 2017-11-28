"""

"""

import xml.etree.ElementTree as ET
import os
from optparse import OptionParser


def get_classes_and_index(path):
    D = {}
    f = open(os.path.abspath(path))
    for line in f:
        temp = line.rstrip().split(',', 2)
        print("temp[0]:" + temp[0] + "\n")
        print("temp[1]:" + temp[1] + "\n")
        D[temp[1].replace(' ', '')] = temp[0]
    return D


def convert(size, box):
    dw = 1. / size[0]
    dh = 1. / size[1]
    x = (box[0] + box[1]) / 2.0
    y = (box[2] + box[3]) / 2.0
    w = box[1] - box[0]
    h = box[3] - box[2]
    x = x * dw
    w = w * dw
    y = y * dh
    h = h * dh
    return (x, y, w, h)


def convert_annotation(path, image_id):
    in_file = open('%s/%s.xml' % (os.path.abspath(path), image_id))
    tree = ET.parse(in_file)
    root = tree.getroot()
    size = root.find('size')
    w = int(size.find('width').text)
    h = int(size.find('height').text)

    for obj in root.iter('object'):
        cls = obj.find('name').text.replace(' ', '')
        if cls not in classes:
            continue
        cls_id = classes[cls]  # 获取该类物体在yolo训练列表中的id
        xmlbox = obj.find('bndbox')
        b = (float(xmlbox.find('xmin').text), float(xmlbox.find('xmax').text), float(xmlbox.find('ymin').text),
             float(xmlbox.find('ymax').text))
        bb = convert((w, h), b)


def convert_annotation_train(trainfile, imagedir, path, image_id):
    in_file = open('%s/%s.xml' % (os.path.abspath(path), image_id))
    tree = ET.parse(in_file)
    root = tree.getroot()
    size = root.find('size')
    w = int(size.find('width').text)
    h = int(size.find('height').text)

    for obj in root.iter('object'):
        cls = obj.find('name').text.replace(' ', '')
        # 如果该类物体不在我们的yolo训练列表中，跳过
        if cls not in classes:
            continue
        cls_id = classes[cls]  # 获取该类物体在yolo训练列表中的id
        xmlbox = obj.find('bndbox')
        b = (float(xmlbox.find('xmin').text), float(xmlbox.find('ymin').text), float(xmlbox.find('xmax').text),
             float(xmlbox.find('ymax').text))
        # bb = convert((w, h), b)
        trainfile.write(imagedir + "," + ",".join([str(a) for a in b]) + "," + cls + '\n')


def IsSubString(SubStrList, Str):
    flag = True
    for substr in SubStrList:
        if not (substr in Str):
            flag = False

    return flag


# 获取FindPath路径下指定格式（FlagStr）的文件名（不包含后缀名）列表
def GetFileList(FindPath, FlagStr=[]):
    import os
    FileList = []
    FileNames = os.listdir(os.path.abspath(FindPath))
    if (len(FileNames) > 0):
        for fn in FileNames:
            if (len(FlagStr) > 0):
                if (IsSubString(FlagStr, fn)):
                    FileList.append(fn[:-4])
            else:
                FileList.append(fn)

    if (len(FileList) > 0):
        FileList.sort()

    return FileList


# 获取目录下子目录的目录名列表
def get_dirs(time):
    dirs = []
    dirs_temp = os.listdir(time)
    for dir_name in dirs_temp:
        dirs.append(time + '/' + dir_name)
    return dirs


parser = OptionParser()

parser.add_option("-c", "--class", dest="class_path", help="Path to class in training data.", default='./class.txt')
parser.add_option("-a", "--annotations", dest="annotations", help="your images' annotations created by voctool",
                  default="./annotations")
parser.add_option("-i", "--images", dest="images", help="the training images",
                  default="./images")

(options, args) = parser.parse_args()

if not options.class_path:  # if filename is not given
    parser.error('Error: path to training class data must be specified.')

if not options.annotations:  # if filename is not given
    parser.error('Error: path to training annotations data must be specified.')

if not options.images:  # if filename is not given
    parser.error('Error: path to training images data must be specified.')

classes = get_classes_and_index(options.class_path)
trainfile = open('traindataset.txt', 'w')

image_ids = GetFileList(options.annotations, ['xml'])
for image_id in image_ids:
    imagedir = '%s/%s.jpg' % (options.images, image_id)
    convert_annotation(options.annotations, image_id)
    convert_annotation_train(trainfile, imagedir, options.annotations, image_id)
