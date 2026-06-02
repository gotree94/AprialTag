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
