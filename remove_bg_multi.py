import os
import io
import multiprocessing
from rembg import remove, new_session
from PIL import Image
from tqdm import tqdm  # tqdm 모듈 임포트

# 배경 제거 함수
def remove_background(args):
    image_path, output_dir = args  # unpacking 인자
    # 1. 이미지 가져오기
    with open(image_path, "rb") as img_file:
        input_img = img_file.read()
    
    # 2. 배경 제거
    model_name = "birefnet-portrait"
    session = new_session(model_name)

    out = remove(input_img, session=session)

    # 3. RGBA를 흰색 배경으로 변경
    out_img = Image.open(io.BytesIO(out))  # bytes 데이터를 PIL 이미지로 변환
    
    if out_img.mode == 'RGBA':
        # 흰색 배경을 가진 새로운 이미지 생성
        background = Image.new("RGB", out_img.size, (255, 255, 255))
        # 투명한 부분을 흰색으로 채움
        background.paste(out_img, (0, 0), out_img)
        out_img = background  # 흰색 배경을 가진 이미지로 대체
    
    # 4. 저장할 경로 지정
    img_name = os.path.basename(image_path)
    output_path = os.path.join(output_dir, img_name)

    # 5. 처리된 이미지 저장
    out_img.save(output_path, format='JPEG')  # JPEG로 저장

# 병렬 처리 함수
def process_images_in_parallel(image_paths, output_dir, num_workers=4):
    # 출력 디렉토리가 없다면 생성
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # 멀티프로세싱 풀 생성
    pool = multiprocessing.Pool(num_workers)
    
    # tqdm을 사용하여 진행 상황 표시
    # 각 인자를 튜플로 전달
    for _ in tqdm(pool.imap(remove_background, [(image_path, output_dir) for image_path in image_paths]), total=len(image_paths)):
        pass
    
    # 풀 종료
    pool.close()
    pool.join()

if __name__ == "__main__":
    # 이미지 파일이 들어 있는 디렉토리와 출력 디렉토리 설정
    input_dir = './data/training_image'  # 처리할 이미지가 있는 디렉토리
    output_dir = './data/training_image_birefnet'   # 처리된 이미지 저장할 디렉토리
    
    # 입력 디렉토리 내 모든 이미지 파일 경로 리스트 만들기
    image_paths = [os.path.join(input_dir, fname) for fname in os.listdir(input_dir) if fname.endswith(('.png', '.jpg', '.jpeg'))]
    
    # 병렬로 이미지 처리 (CPU 코어 수에 따라 조정 가능)
    process_images_in_parallel(image_paths, output_dir, num_workers=4)