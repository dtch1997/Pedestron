# -*- coding: utf-8 -*-
"""
Created on Mon Jul 27 04:37:01 2020

@author: Daniel Tan
"""


input_size = 128
# Model config adapted from https://github.com/hasanirtiza/Pedestron/blob/master/configs/ssd300_coco.py
model = dict(
    type='SingleStageDetector',
    pretrained=None,
    backbone=dict(
        type='MobilenetV2',
        width_mult=1.0,
        inverted_residual_setting=None,
        round_nearest=8,
        block=None),
    neck=None,
    bbox_head=dict(
        type='SSDHead',
        input_size=input_size,
        in_channels=(512, 1024, 512, 256, 256, 256),
        num_classes=81,
        anchor_strides=(8, 16, 32, 64, 100, 300),
        basesize_ratio_range=(0.15, 0.9),
        anchor_ratios=([2], [2, 3], [2, 3], [2, 3], [2], [2]),
        target_means=(.0, .0, .0, .0),
        target_stds=(0.1, 0.1, 0.2, 0.2)))
cudnn_benchmark = True
train_cfg = dict(
    assigner=dict(
        type='MaxIoUAssigner',
        pos_iou_thr=0.5,
        neg_iou_thr=0.5,
        min_pos_iou=0.,
        ignore_iof_thr=-1,
        gt_max_assign_all=False),
    smoothl1_beta=1.,
    allowed_border=-1,
    pos_weight=-1,
    neg_pos_ratio=3,
    debug=False)
test_cfg = dict(
    nms=dict(type='nms', iou_thr=0.45),
    min_bbox_size=0,
    score_thr=0.02,
    max_per_img=200)
# model training and testing settings
# dataset settings copied from https://github.com/hasanirtiza/Pedestron/blob/master/configs/elephant/crowdhuman/cascade_hrnet.py
dataset_type = 'CocoDataset'
data_root = 'datasets/CrowdHuman/'
img_norm_cfg = dict(
    mean=[123.675, 116.28, 103.53],
    std=[58.395, 57.12, 57.375],
    to_rgb=True)
data = dict(
    imgs_per_gpu=1,
    workers_per_gpu=5,
    train=dict(
        type=dataset_type,
	ann_file=data_root + 'train.json',
 	img_prefix=data_root + 'Images',
	img_scale=[(1216, 608),(2048, 1024)],
        multiscale_mode='range',
        img_norm_cfg=img_norm_cfg,
        size_divisor=32,
        flip_ratio=0.5,
        with_mask=True,
        with_crowd=True,
        with_label=True,
        extra_aug=dict(
            photo_metric_distortion=dict(brightness_delta=180, contrast_range=(0.5, 1.5),
                 saturation_range=(0.5, 1.5), hue_delta=18),
             random_crop=dict(min_ious=(0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9), min_crop_size=0.1),
         ),
    ),
    test=dict(
        type=dataset_type,
	    ann_file=data_root + 'val.json',
        img_prefix=data_root + 'Images_val',
        img_scale=(2048, 1024),
        img_norm_cfg=img_norm_cfg,
        size_divisor=32,
        flip_ratio=0,
        with_mask=False,
        with_label=False,
        test_mode=True))
# optimizer
optimizer = dict(type='SGD', lr=2e-3, momentum=0.9, weight_decay=5e-4)
optimizer_config = dict()
# learning policy
lr_config = dict(
    policy='step',
    warmup='linear',
    warmup_iters=500,
    warmup_ratio=1.0 / 3,
    step=[16, 22])
checkpoint_config = dict(interval=1)    
# yapf:disable
log_config = dict(
    interval=50,
    hooks=[
        dict(type='TextLoggerHook'),
        # dict(type='TensorboardLoggerHook')
    ])
# yapf:enable
# runtime settings
total_epochs = 24
dist_params = dict(backend='nccl')
log_level = 'INFO'
work_dir = './work_dirs/ssd_mobilenet_128_crowdhuman'
load_from = None
resume_from = None
workflow = [('train', 1)]