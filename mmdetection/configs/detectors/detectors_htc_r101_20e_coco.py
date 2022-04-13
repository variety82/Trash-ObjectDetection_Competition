_base_ = '../htc/htc_without_semantic_r50_fpn_1x_coco.py'
conv_cfg = dict(type='ConvAWS')
model = dict(
    backbone=dict(
        type='DetectoRS_ResNeXt',
        conv_cfg=dict(type='ConvAWS'),
        sac=dict(type='SAC', use_deform=True),
        stage_with_sac=(False, True, True, True),
        output_img=True),
    neck=dict(
        type='RFP',
        rfp_steps=2,
        aspp_out_channels=64,
        aspp_dilations=(1, 3, 6, 1),
        rfp_backbone=dict(
            rfp_inplanes=256,
            type='DetectoRS_ResNeXt',
            depth=101,
            groups=64,
            base_width=4,
            num_stages=4,
            out_indices=(0, 1, 2, 3),
            frozen_stages=1,
            pretrained='open-mmlab://resnext101_64x4d',
            conv_cfg=conv_cfg,
            sac=dict(type='SAC', use_deform=True),
            stage_with_sac=(False, True, True, True),
            norm_cfg=dict(type='BN', requires_grad=True),
            style='pytorch')))


    
# optimizer
optimizer = dict(type='AdamW', lr=0.005,weight_decay=0.0001)
# learning policy
lr_config = dict(
    policy='step',
    warmup='linear',
    warmup_iters=500,
    warmup_ratio=0.001,
    step=[10, 20])
runner = dict(type='EpochBasedRunner', max_epochs=25)

optimizer_config = dict(
    grad_clip=None)