import os
import io
from rembg import remove, new_session
from PIL import Image

# 단일 이미지 배경 제거 함수
def remove_background_single(image_path, output_dir):
    """
    단일 이미지의 배경을 제거하고, 투명 배경을 흰색으로 변경하여 저장하는 함수.
    
    Args:
        image_path (str): 배경을 제거할 이미지 파일 경로
        output_dir (str): 처리된 이미지를 저장할 디렉토리 경로
    """
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

# 사용 예시
if __name__ == "__main__":
    # 단일 이미지 파일 경로와 출력 디렉토리 지정
    image_path = './data/training_image/W_24352_70_hippie_M.jpg'  # 처리할 이미지 경로
    output_dir = './data/training_image_rembg_anormal'              # 저장할 디렉토리

    # 출력 디렉토리가 없다면 생성
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # 배경 제거 및 처리된 이미지 저장
    remove_background_single(image_path, output_dir)

    print(f"Processed image saved to: {output_dir}")
