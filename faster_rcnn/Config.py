import math


class Config:
    def __init__(self):
        self.verbose = True
        self.network = 'resnet50'

        # setting for data augmentation
        self.use_horizontal_flips = False
        self.use_vertical_flips = False
        self.rot_90 = False
        # anchor box scales
        self.anchor_box_scales = [128, 256, 512]
        # anchor box ratios
        self.anchor_box_ratios = [[1, 1], [1. / math.sqrt(2), 2. / math.sqrt(2)],
                                  [2. / math.sqrt(2), 1. / math.sqrt(2)]]
        # size to resize the smallest side of the image
        self.im_size = 600
        # image channel-wise mean to subtract
        self.img_channel_mean = [103.939, 116.779, 123.68]
        self.img_scaling_factor = 1.0
        # number of ROIs at once
        self.num_rois = 4
        # stride at the RPN (this depends on the network configuration)
        self.rpn_stride = 16
        self.balanced_classes = False
        # scaling the stdev
        self.std_scaling = 4.0
        self.classifier_regr_std = [8.0, 8.0, 4.0, 4.0]
        # overlaps for RPN
        self.rpn_min_overlap = 0.3
        self.rpn_max_overlap = 0.7
        # overlaps for classifier ROIs
        self.classifier_min_overlap = 0.1
        self.classifier_max_overlap = 0.5
        self.class_mapping = None
        self.model_path = 'model_frcnn.vgg.hdf5'
        self.train_path = './traindataset.txt'
        self.input_weight_path = './resnet50_weights_tf_dim_ordering_tf_kernels.h5'
