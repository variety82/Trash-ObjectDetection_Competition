# optimizer
optimizer = dict(type='AdamW', lr=2e-5, weight_decay=1e-8)
optimizer_config = dict(grad_clip=dict(max_norm=10, norm_type=2))
# learning policy
lr_config = dict(
    policy='CosineAnnealing',
    warmup='linear',
    warmup_iters=300,
    warmup_ratio=0.1,
    min_lr_ratio=2e-7)
runner = dict(type='EpochBasedRunner', max_epochs=20)
