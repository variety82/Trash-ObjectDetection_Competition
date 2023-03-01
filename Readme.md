## 진행기간
2022.03.21 ~ 2022.04.07 19:00

## 프로젝트 개요

산업혁명 이후로 대량 생산 시대가 찾아오면서 쓰레기 처리문제, 매립지 문제 등은 끊임없이 인류를 괴롭히는 문제 중 하나가 되었습니다. 최근에는 코로나 이슈로 쓰레기 문제는 점점 더 심각해지고 있는 상황입니다.

![image-20220413165645988](https://raw.githubusercontent.com/variety82/imgForTypora/forUpload/img/image-20220413165645988.png)



이러한 상황 속에서 분리수거의 중요성은 더 커지고 있습니다. 쓰레기 양이 많아지는 만큼 분리수거가 제대로 되지 않는 쓰레기들도 많아지는 것은 당연한 결과입니다.

이를 해결하기 위해 우리는 사진에서 쓰레기를 Detection 하는 모델을 만들어보려고 합니다. 모델에 필요한 데이터셋은 일반 쓰레기, 플라스틱, 종이, 유리 등 10 종류의 쓰레기가 찍힌 사진들이 제공됩니다.

- **Input :** 쓰레기 객체가 담긴 이미지와 bbox 정보(좌표, 카테고리)
- **Output :** 모델은 bbox 좌표, 카테고리, score 값을 리턴

|  이름  | 역할                                                         | github                         |
| :----: | ------------------------------------------------------------ | ------------------------------ |
| 강소망  | yolox, yolov5x6 실험                                         | https://github.com/Somang-Kang |
| 김기태  | htc_Swin_L(22K), yolov5l6 + TTA 실험, EDA 수행               | https://github.com/kkt4828/    |
| 김창현  | Swin_L_Cascade R-CNN 실험, Oversampling 실험                 | https://github.com/variety82   |
| 박기련  | Swin-T, L 기반 Cascade R-CNN, HTC 실험                       | https://github.com/parkgr95    |
| 박민수  | Centernet2, DyHead, Universenet 실험Augmentation 실험, Ensenble(WBF) 코드 | https://github.com/mata1139    |

# File Directory

```
baseline
├── mmdetection
│   ├── config
│   └── ...
├── requirements.txt
│
└── yolo
		├── dataset
		│   ├── images
		│   └── labels
		└── cocotrash.yaml
```



# Dataset

- 전체 이미지 개수 : 9754장 (train : 4883 장 , test : 4871 장)
- 10 class : General trash, Paper, Paper pack, Metal, Glass, Plastic, Styrofoam, Plastic bag, Battery, Clothing
- 이미지 크기 : (1024, 1024)
- COCO Format

![image-20220413170311282](https://raw.githubusercontent.com/variety82/imgForTypora/forUpload/img/image-20220413170311282.png)



## 모델 아키텍쳐

![image-20220413170349773](https://raw.githubusercontent.com/variety82/imgForTypora/forUpload/img/image-20220413170349773.png)



# Augmentation

### 공통

```markdown
💡 Albumentation

- RandomRotate90 , RandomFlip ( Horizion, Vertical )
  - Rotate 를 시켜도 Object 의 형태는 동일하므로 데이터 증강의 목적으로 사용
- HueSaturationValue, RandomGamma, CLAHE [One of]
  - 여러가지 밝기에 따른 일반화 성능 향상 도모
- Blur, GaussianNoise, MotionBlur [One of]
  - 초점이 흐린 Image가 들어올 것을 대비
  
TTA

- HorizionFlip, VerticalFlip 적용 
```

### Yolov5

```markdown
 💡 Albumentation

- RandomRotate90 , RandomFlip ( Horizion, Vertical )
  - Rotate 를 시켜도 Object 의 형태는 동일하므로 데이터 증강의 목적으로 사용
- HueSaturationValue, RandomGamma, CLAHE [One of]
  - 여러가지 밝기에 따른 일반화 성능 향상 도모
- Blur, GaussianNoise, MotionBlur [One of]
  - 초점이 흐린 Image가 들어올 것을 대비

Yolov5 내부 Augmentation

- Translate, scale, mosaic, mixup

TTA

- HorizionFlip, VerticalFlip, Multi scale 적용
```



## 모델별 결과 테이블 (Hyperparameter, TTA 적용 등 내용 추가)



|      | BackBone    | Model         | Val mAP50 | LB Score |
| ---- | ----------- | ------------- | --------- | -------- |
| 1    | Resnet101   | Cascade R-CNN | 0.5290    |          |
| 2    |             | Grid R-CNN    | 0.5054    |          |
| 3    |             | ATSS + DyHead | 0.4934    |          |
| 4    |             | UniverseNet   | 0.6070    | 0.6134   |
| 5    |             | Centernet2    | 0.5860    | 0.5927   |
| 6    | Swin_T      | Cascade R-CNN | 0.5810    | 0.5949   |
| 7    |             | HTC           | 0.5899    | 0.6003   |
| 8    | Swin_L (1K) | Cascade R-CNN | 0.6520    | 0.6849   |
| 9    |             | HTC           | 0.6660    | 0.6819   |
| 10   |             | Centernet2    | 0.6160    | 0.6184   |
| 11   |             | ATSS + DyHead | 0.6450    | 0.6660   |
| 12   | Swin_L(22K) | HTC           | 0.6510    | 0.6722   |
| 13   | YOLO        | YOLOx         | 0.4280    |          |
| 14   |             | YOLOv5x6      | 0.5600    |          |
| 15   |             | YOLOv5l6      | 0.5900    |          |

# Ensemble

- WBF ( Weighted Box Fusion)
- Threshold 0.65

![image-20220413171235163](https://raw.githubusercontent.com/variety82/imgForTypora/forUpload/img/image-20220413171235163.png)



# 최종결과 (마무리)

- **최종 LB Score**

  **Public : 0.7207** (5등 / 19 team)    **Private : 0.7059 ** (5등 / 19 team)



## Reference

swin transformer - [microsoft](https://github.com/microsoft)/**[Swin-Transformer](https://github.com/microsoft/Swin-Transformer)**

yolov5 github - https://github.com/ultralytics/yolov5

mmdetection docs - https://mmdetection.readthedocs.io/en/latest/

mmdetection github - https://github.com/open-mmlab/mmdetection

universenet - https://github.com/shinya7y/UniverseNet

centernet2 - https://github.com/xingyizhou/CenterNet2

data - Upstage 제공

albumentation - https://github.com/albumentations-team/albumentations
