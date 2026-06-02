# Sim-to-Real-to-Sim & AprilTag 학습 노트
**날짜:** 2026-06-02  
**주제:** S2R2S 루프, Robot Learning, AprilTag 메커니즘

---

## 1. Sim-to-Real-to-Sim (S2R2S) 루프

### 고전 방식 vs S2R2S

| 구분 | 고전 방식 | S2R2S |
|------|-----------|-------|
| 방향 | 단방향 (Sim → Real) | 양방향 (Sim ⇄ Real) |
| 피드백 | 수동, 단발성 | 자동, 지속적 |
| 목표 | 문제 발생 시 복귀 | Real 데이터로 Sim 지속 교정 |

### 최대 장점: Domain Gap 자동 축소

| 단계 | 내용 |
|------|------|
| Sim → Real | 학습된 정책을 실로봇에 배포 |
| Real → Sim | 실로봇 센서 데이터·오차·거동 수집 |
| Sim 업데이트 | 수집 데이터로 물리 파라미터 자동 보정 (System ID) |
| 재학습 | 보정된 Sim에서 더 나은 정책 학습 |

루프가 돌수록 **Sim이 Real의 디지털 트윈에 수렴**한다.

### Sim 고도화로 좋아지는 것

1. **물리 피델리티 향상** → 정책 전이율 상승 (Zero-shot 가능)
2. **Edge Case 무한 재현** → Real에서 한 번 발생한 실패를 Sim에서 수천 번 반복
3. **센서 모델 정밀화** → LiDAR 노이즈, IMU 드리프트 특성을 Sim에 주입

### Real 환경 변화에 대한 Sim의 대응 한계

```
✅ 대응 가능
   - 느린 변화 (관절 마모, 환경 레이아웃 변경)
   - 예측 가능한 변화 (공장 라인 변경, 물체 추가)

❌ 대응 어려움
   - 갑작스러운 동적 장애물 (루프 주기 latency 문제)
   - 물리 법칙 밖의 변화 (하드웨어 손상, 재질 변성)
   - 완전히 새로운 환경 (Out-of-Distribution)
```

> **NVIDIA Isaac Sim + Cosmos 2.0의 방향:**  
> 단순 물리 파라미터 튜닝을 넘어, 비디오 기반 세계 모델(World Model)이  
> 환경 변화 자체를 예측·학습하는 패러다임으로 발전 중.

---

## 2. Robot Learning 분야 키워드 맵

### 큰 그림

```
Embodied AI / Robot Learning
│
├── 학습 패러다임
│   ├── Reinforcement Learning (RL)
│   ├── Imitation Learning (IL)
│   └── Self-Supervised Learning
│
├── Sim ↔ Real
│   ├── Sim-to-Real Transfer
│   ├── S2R2S / Digital Twin
│   └── Domain Randomization / Adaptation
│
├── 정책(Policy) 구조
│   ├── End-to-End Learning
│   ├── Foundation Model for Robotics
│   └── World Models
│
└── 응용
    ├── Legged Locomotion
    ├── Dexterous Manipulation
    └── Autonomous Navigation
```

### 핵심 RL 알고리즘

| 키워드 | 내용 |
|--------|------|
| PPO (Proximal Policy Optimization) | 로봇 locomotion 학습의 표준 알고리즘 |
| SAC (Soft Actor-Critic) | 연속 행동공간에서 샘플 효율 높음 |
| Model-Based RL | 환경 모델을 함께 학습해 샘플 수 절감 |
| Curriculum Learning | 쉬운 과제 → 어려운 과제 자동 난이도 조절 |

### Foundation Models for Robotics (최신 트렌드)

| 키워드 | 설명 | 대표 연구 |
|--------|------|-----------|
| VLA (Vision-Language-Action) | 카메라+언어 지시 → 행동 직접 출력 | RT-2, π0 |
| World Model | 미래 상태 예측 신경망 내부 시뮬레이터 | DreamerV3, Cosmos |
| Diffusion Policy | Diffusion 모델로 로봇 행동 생성 | Chi et al. 2023 |
| GR00T | NVIDIA 휴머노이드 Foundation Model | Isaac Lab 기반 |

### Legged Locomotion 전문 키워드

| 키워드 | 내용 |
|--------|------|
| Whole-Body Control (WBC) | 전신 동역학 통합 제어 |
| Proprioceptive Feedback | 외부 센서 없이 관절 센서만으로 걷기 |
| Parkour / Agile Locomotion | 장애물 극복, 점프 등 동적 운동 학습 |
| Loco-Manipulation | 이동하면서 동시에 물건 집기 |

### 주요 도구 생태계

| 도구 | 역할 |
|------|------|
| Isaac Lab | NVIDIA RL 학습 프레임워크 |
| MuJoCo | DeepMind 물리 엔진, 연구 표준 |
| Genesis | 2024년 신규, 초고속 물리 시뮬 |
| LeRobot | HuggingFace 로봇학습 오픈소스 |

---

## 3. 사람의 학습과 Robot Learning의 대응 구조

| 사람의 학습 | AI/로봇 학습 |
|------------|-------------|
| 처음엔 잘 안됨 | Random Policy 초기화 |
| 될 때까지 시행착오 | Reinforcement Learning |
| 머릿속에서 생각해봄 | World Model / Mental Simulation |
| 생각과 현실의 간격 파악 | Reality Gap / Domain Gap 측정 |
| 간격을 줄여감 | Sim-to-Real-to-Sim 루프 |

### 사람과 AI의 결정적 차이

```
사람:   시행착오 100번 → 자전거 습득
AI(RL): 시행착오 10,000,000번 필요 (Sample Inefficiency)
```

### 해결책들

| 방법 | 사람 학습과의 대응 |
|------|------------------|
| World Model | 머릿속에서 먼저 수백만 번 연습 |
| Imitation Learning | 전문가 시범 보고 시작 (유튜브 학습) |
| Curriculum Learning | 쉬운 것부터 순서대로 (교육과정) |
| Transfer Learning | 이미 배운 것을 다음 학습에 활용 |

### 진짜 효율적 학습이란

> **나쁜 효율:** 시간 대비 얼마나 많이 외웠는가  
> **좋은 효율:** 투자한 학습이 얼마나 오래, 넓게 전이되는가

학습에서 가장 중요한 것:
1. **실패를 데이터로 보는 관점** — 실패한 에피소드가 성공만큼 중요한 학습 신호
2. **내부 모델(World Model)의 정밀도** — "왜 그렇게 되는가"에 대한 인과 모델
3. **적절한 난이도 (Zone of Proximal Development)** — 너무 쉽거나 어려우면 성장 없음
4. **망각과 재학습 (Continual Learning)** — 적절한 망각이 일반화에 도움

---

## 4. 발표 프로젝트 분석 (충청 ICT이노베이션스퀘어)

### 프로젝트 핵심 구조

```
Isaac Sim (PhysX 5)
    ↓ Domain Randomization
ROS2 Bridge
    ↓ Image / LiDAR / IMU
TurtleBot3 + Jetson Orin Nano
    ↓ AprilTag 오차 측정
오차 프로필 (.yaml)
    ↓ 피드백
Isaac Sim 물리 파라미터 자동 업데이트
```

### 발표의 의미

1. **"우리는 지름길을 거부했다"**
   - Cosmos WFM → Custom USD 직접 제작으로 Pivot
   - 화려한 데모 대신 Reality Gap을 센티미터 단위로 측정하는 선택

2. **"S2R2S의 최소 단위를 증명했다"**
   - 측정(AprilTag) → 기록(.yaml) → 반영(Isaac Sim) 루프
   - NVIDIA, Boston Dynamics도 같은 구조를 더 크고 빠르게 돌릴 뿐

3. **"완성이 아닌 과정 자체가 학습이다"**

> **발표 클로징 한 문장:**  
> "Nav2가 아직 완전하지 않지만, 우리는 오차가 왜 생기는지는 압니다.  
> 그게 이 프로젝트의 실제 성과입니다."

---

## 5. AprilTag 메커니즘

### 동작 흐름

```
카메라 촬영
    ↓
① 이진화 (Threshold)
② 외곽선 추출
③ 사각형 후보 탐색
④ ID 비트 디코딩
⑤ 4개 꼭짓점 확정
    ↓
PnP (Perspective-n-Point) 풀이
    ↓
출력: Translation (x,y,z) + Rotation (roll,pitch,yaw)
```

### 핵심 원리: PnP 알고리즘

마커의 실제 크기(고정) + 이미지상 4 꼭짓점 픽셀 좌표  
→ 카메라와 마커 사이의 **6-DOF Pose**를 수학적으로 역산

딥러닝 없음. 순수 카메라 기하학 + 행렬 연산.

### 내부 구조 (3겹)

| 영역 | 역할 |
|------|------|
| 외곽 검정 테두리 | 마커 감지 + 4 꼭짓점 확정 |
| 흰색 여백 (Quiet Zone) | 배경과 마커 경계 분리 |
| 데이터 비트 (격자) | 마커 고유 ID 저장 (검정=1, 흰색=0) |

> **내부 패턴 = 마커의 ID(숫자)를 이진 코드로 새긴 것**  
> QR코드가 URL을 저장하듯, AprilTag는 정수 ID 하나만 저장.  
> 위치 계산은 패턴이 아닌 테두리의 4 꼭짓점 기하학으로 수행.

### AprilTag 패밀리 비교

| 패밀리 | 비트 | ID 수 | 특징 |
|--------|------|-------|------|
| tag16h5 | 4×4 | 30개 | 원거리 인식 유리 |
| tag36h11 | 6×6 | 587개 | 오류 정정 강함 **(권장)** |
| tagStandard41h12 | — | 2115개 | 최신 표준 |

> `isaac_ros_apriltag` 기본값 = **tag36h11**

### 해밍코드 오류 정정

16비트 전부를 ID에 쓰지 않고 일부를 오류 정정에 할당  
→ 마커가 일부 가려지거나 훼손돼도 ID 복원 가능

---

## 6. 카메라 각도와 인식 정확도

| 방식 | 정밀도 | 비고 |
|------|--------|------|
| TOP view (수직) | ±2~3mm @ 1m | 이상적, 원근 왜곡 없음 |
| 측면 경사 view | ±1~3cm @ 1m | 각도 클수록 z축 오차 급증 |

**권장 인식 각도:** 수직(90°) 기준 ±45° 이내

### 배치 전략 (소형 공간 120×155cm 기준)

```
┌─────────────────────┐
│  [ID:0]      [ID:1] │  ← 코너 4개: 공간 좌표계 정렬용
│                     │
│       [ID:4]        │  ← 중앙: 주행 오차 측정용
│                     │
│  [ID:2]      [ID:3] │
└─────────────────────┘
```

- **코너 4개:** Sim ↔ Real 원점 정렬
- **중앙 1개:** Odometry 슬립 오차 측정

---

## 7. AprilTag 이미지 생성 Python 코드

### 의존성 설치

```bash
pip install opencv-contrib-python numpy
```

### 핵심 코드

```python
import cv2
import numpy as np

# 패밀리 선택
aruco_dict = cv2.aruco.getPredefinedDictionary(
    cv2.aruco.DICT_APRILTAG_36H11
)

# 마커 생성 (ID, 픽셀 크기)
marker_img = cv2.aruco.generateImageMarker(aruco_dict, tag_id=0, sidePixels=400)

# 흰색 여백 추가 (인쇄 필수)
margin = 60
canvas = np.ones((400 + margin*2, 400 + margin*2), dtype=np.uint8) * 255
canvas[margin:margin+400, margin:margin+400] = marker_img

cv2.imwrite("tag36h11_id000.png", canvas)
```

```
"""
AprilTag 이미지 생성기
=====================
의존성: opencv-contrib-python, numpy
설치:   pip install opencv-contrib-python numpy

사용법:
    python generate_apriltags.py                   # 기본 (tag36h11, ID 0~4)
    python generate_apriltags.py --family tag16h5  # 패밀리 변경
    python generate_apriltags.py --ids 0 1 2 3     # ID 지정
    python generate_apriltags.py --ids 0 9 --size 600 --grid  # 크기 + 그리드
    python generate_apriltags.py --all-families    # 모든 패밀리 생성
"""

import cv2
import numpy as np
import os
import argparse


# ── 지원 패밀리 ──────────────────────────────────────────────────────────────
FAMILIES = {
    "tag16h5":  cv2.aruco.DICT_APRILTAG_16H5,   # 30개  ID, 4x4 비트, 원거리 인식 유리
    "tag25h9":  cv2.aruco.DICT_APRILTAG_25H9,   # 35개  ID, 5x5 비트
    "tag36h10": cv2.aruco.DICT_APRILTAG_36H10,  # 2320개 ID, 6x6 비트
    "tag36h11": cv2.aruco.DICT_APRILTAG_36H11,  # 587개 ID, 6x6 비트, 오류정정 강함 (권장)
}

# isaac_ros_apriltag 기본값 = tag36h11
DEFAULT_FAMILY = "tag36h11"
DEFAULT_IDS    = [0, 1, 2, 3, 4]
DEFAULT_SIZE   = 400   # 마커 픽셀 크기
DEFAULT_MARGIN = 60    # 흰색 여백 (인쇄 시 필수)


def generate_marker(aruco_dict, tag_id: int, size: int, margin: int,
                    family_name: str) -> np.ndarray:
    """마커 1개를 생성하고 여백 + 라벨을 추가한 이미지를 반환."""
    marker = cv2.aruco.generateImageMarker(aruco_dict, tag_id, size)

    canvas_size = size + margin * 2
    canvas = np.ones((canvas_size, canvas_size), dtype=np.uint8) * 255
    canvas[margin:margin + size, margin:margin + size] = marker

    label = f"{family_name}  ID: {tag_id}"
    font_scale = max(0.4, size / 700)
    cv2.putText(canvas, label,
                (margin, canvas_size - 16),
                cv2.FONT_HERSHEY_SIMPLEX,
                font_scale, 0, 1, cv2.LINE_AA)

    return canvas


def make_grid(images: list, cols: int = 5) -> np.ndarray:
    """마커 이미지 리스트를 그리드 한 장으로 합침."""
    rows = (len(images) + cols - 1) // cols
    h, w = images[0].shape[:2]
    grid = np.ones((h * rows, w * cols), dtype=np.uint8) * 255
    for idx, img in enumerate(images):
        r, c = divmod(idx, cols)
        grid[r * h:(r + 1) * h, c * w:(c + 1) * w] = img
    return grid


def run(family_name: str, ids: list, size: int, margin: int,
        output_dir: str, save_grid: bool, grid_cols: int):

    if family_name not in FAMILIES:
        raise ValueError(f"지원하지 않는 패밀리: {family_name}\n"
                         f"선택 가능: {list(FAMILIES.keys())}")

    aruco_dict = cv2.aruco.getPredefinedDictionary(FAMILIES[family_name])
    save_dir = os.path.join(output_dir, family_name)
    os.makedirs(save_dir, exist_ok=True)

    images = []
    for tag_id in ids:
        img = generate_marker(aruco_dict, tag_id, size, margin, family_name)
        path = os.path.join(save_dir, f"{family_name}_id{tag_id:03d}.png")
        cv2.imwrite(path, img)
        images.append(img)
        print(f"  저장: {path}")

    if save_grid and len(images) > 1:
        grid = make_grid(images, cols=min(grid_cols, len(images)))
        grid_path = os.path.join(
            output_dir,
            f"{family_name}_grid_id{ids[0]}-{ids[-1]}.png"
        )
        cv2.imwrite(grid_path, grid)
        print(f"  그리드: {grid_path}")

    print(f"  완료: {len(images)}개 마커 생성\n")


def main():
    parser = argparse.ArgumentParser(description="AprilTag 이미지 생성기")
    parser.add_argument("--family",  default=DEFAULT_FAMILY,
                        choices=list(FAMILIES.keys()),
                        help=f"AprilTag 패밀리 (기본: {DEFAULT_FAMILY})")
    parser.add_argument("--ids",     nargs="+", type=int,
                        default=DEFAULT_IDS,
                        help="생성할 ID 목록 (기본: 0 1 2 3 4)")
    parser.add_argument("--size",    type=int, default=DEFAULT_SIZE,
                        help=f"마커 픽셀 크기 (기본: {DEFAULT_SIZE})")
    parser.add_argument("--margin",  type=int, default=DEFAULT_MARGIN,
                        help=f"흰색 여백 px (기본: {DEFAULT_MARGIN})")
    parser.add_argument("--output",  default="apriltags",
                        help="출력 디렉토리 (기본: apriltags/)")
    parser.add_argument("--grid",    action="store_true",
                        help="그리드 이미지도 생성")
    parser.add_argument("--grid-cols", type=int, default=5,
                        help="그리드 열 수 (기본: 5)")
    parser.add_argument("--all-families", action="store_true",
                        help="모든 패밀리 동시 생성")
    args = parser.parse_args()

    print("=" * 50)
    print("  AprilTag 이미지 생성기")
    print("=" * 50)

    if args.all_families:
        for fam in FAMILIES:
            print(f"\n[{fam}]")
            run(fam, args.ids, args.size, args.margin,
                args.output, args.grid, args.grid_cols)
    else:
        print(f"\n[{args.family}]  ID: {args.ids}")
        run(args.family, args.ids, args.size, args.margin,
            args.output, args.grid, args.grid_cols)


if __name__ == "__main__":
    main()

```


### 사용법 (generate_apriltags.py)

```bash
# 기본 실행 (tag36h11, ID 0~4)
python generate_apriltags.py

# ID 지정 + 그리드 이미지 생성
python generate_apriltags.py --ids 0 1 2 3 4 --grid

# 인쇄용 고해상도
python generate_apriltags.py --ids 0 1 2 3 4 --size 800 --grid

# 모든 패밀리 한 번에 생성
python generate_apriltags.py --all-families --grid
```

<img src="tag36h11_grid_id0-4.png">

<img src="tag36h11_id000.png">

---

## 참고 자료

- [NVIDIA Isaac Sim Documentation](https://docs.omniverse.nvidia.com/isaacsim/)
- [isaac_ros_apriltag GitHub](https://github.com/NVIDIA-ISAAC-ROS/isaac_ros_apriltag)
- [AprilTag 공식 사이트](https://april.eecs.umich.edu/software/apriltag)
- [Isaac Sim Korea Cafe](https://cafe.naver.com/isaacsimkr)
- [ROS2 TurtleBot3 URDF Import](https://nvidia-isaac-ros.github.io/)

---

*생성일: 2026-06-02 | Claude Sonnet 4.6*

