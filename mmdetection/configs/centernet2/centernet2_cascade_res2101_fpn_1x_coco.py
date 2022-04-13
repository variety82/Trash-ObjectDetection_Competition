_base_ = [
    '../_base_/models/centernet2_cascade_r50_fpn.py',
    '../_base_/datasets/coco_detection_mstrain_480_960.py',
    '../_base_/schedules/schedule_1x.py', '../_base_/default_runtime.py'
]

pretrained = 'https://github.com/SwinTransformer/storage/releases/download/v1.0.0/swin_large_patch4_window12_384_22kto1k.pth'  # noqa
model = dict(
    type='MaskRCNN',
    backbone=dict(
        
        type='SwinTransformer',
        embed_dims=192,
        depths=[2, 2, 18, 2],
        num_heads=[6, 12, 24, 48],
        window_size=12,
        mlp_ratio=4,
        qkv_bias=True,
        qk_scale=None,
        drop_rate=0.,
        attn_drop_rate=0.,
        drop_path_rate=0.2,
        patch_norm=True,
        out_indices=(0, 1, 2, 3),
        with_cp=False,
        convert_weights=True,
        init_cfg=dict(type='Pretrained', checkpoint=pretrained)),
    neck=dict(in_channels=[192, 384, 768, 1536])
)




# optimizer
optimizer_config = dict(_delete_=True,grad_clip=dict(max_norm=35, norm_type=2))
optimizer = dict(type='SGD', lr=0.005, momentum=0.9, weight_decay=0.0001)

lr_config = dict(
    policy='step',
    warmup='linear',
    warmup_iters=1000,
    warmup_ratio=0.0001,
    step=[18, 30])
runner = dict(type='EpochBasedRunner', max_epochs=36)







