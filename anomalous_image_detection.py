import os
import numpy as np
from PIL import Image
import multiprocessing
from tqdm import tqdm

def is_anomalous(image_path, threshold=0.90):
    """
    배경 제거된 이미지에서 흰색 픽셀이 차지하는 비율이 특정 임계값을 넘으면 True를 반환.
    """
    image = Image.open(image_path).convert('RGB')  # 이미지 열기
    image_np = np.array(image)  # 이미지를 NumPy 배열로 변환

    # 흰색 픽셀 (255, 255, 255) 탐지
    white_pixels = np.all(image_np == [255, 255, 255], axis=-1)
    
    # 흰색 픽셀 비율 계산
    white_ratio = np.mean(white_pixels)
    
    return image_path if white_ratio > threshold else None  # 임계값 초과 시 이상치로 판단

def process_image(image_path_threshold_tuple):
    """
    Tuple을 받아 is_anomalous를 실행하는 함수. 
    multiprocessing을 사용할 때 필요.
    """
    image_path, threshold = image_path_threshold_tuple
    return is_anomalous(image_path, threshold)

def find_anomalous_images_parallel(image_paths, threshold=0.95, num_workers=4):
    """
    병렬로 이상치 이미지를 찾는 함수. tqdm으로 진행 상황을 표시.
    """
    # 각 이미지 경로와 threshold를 튜플로 묶어서 전달
    path_threshold_tuples = [(img, threshold) for img in image_paths]
    
    with multiprocessing.Pool(num_workers) as pool:
        # tqdm으로 병렬처리 진행 상황 표시
        results = list(tqdm(pool.imap(process_image, path_threshold_tuples), 
                            total=len(image_paths), desc="Checking for anomalies"))
    
    # 이상치 이미지만 필터링
    anomalous_images = [res for res in results if res is not None]
    
    return anomalous_images

def calculate_white_pixel_percentage(image_path):
    """
    단일 이미지에서 하얀색 픽셀이 차지하는 비율을 계산하는 함수.
    
    Args:
        image_path (str): 이미지 파일 경로
        
    Returns:
        float: 하얀색 픽셀 비율 (0.0 ~ 1.0)
    """
    # 이미지 열기 및 RGB로 변환
    image = Image.open(image_path).convert('RGB')
    
    # 이미지를 NumPy 배열로 변환
    image_np = np.array(image)
    
    # 흰색 픽셀 (255, 255, 255) 탐지
    white_pixels = np.all(image_np == [255, 255, 255], axis=-1)
    
    # 흰색 픽셀 비율 계산
    white_ratio = np.mean(white_pixels)
    
    return white_ratio


if __name__ == "__main__":
    # # 배경 제거된 이미지가 저장된 디렉토리
    # output_dir = './data/training_image_rembg'

    # # 디렉토리 내 모든 이미지 파일 경로 리스트 만들기
    # image_paths = [os.path.join(output_dir, fname) for fname in os.listdir(output_dir) if fname.endswith(('.png', '.jpg', '.jpeg'))]
    
    # # 병렬로 이상치 탐지 (임계값과 워커 수는 필요에 따라 조정 가능)
    # anomalies = find_anomalous_images_parallel(image_paths, threshold=0.90, num_workers=50)
    
    # # 이상치로 판단된 이미지 출력
    # if anomalies:
    #     print("Anomalous images found:", anomalies)
    # else:
    #     print("No anomalies found.")
    image_path = './data/training_image_rembg/W_01752_00_metrosexual_M.jpg'
    white_pixel_percentage = calculate_white_pixel_percentage(image_path)
    print(f"White pixel percentage for {os.path.basename(image_path)}: {white_pixel_percentage * 100:.2f}%")
