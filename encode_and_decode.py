import base64
from PIL import Image,ImageFile
import io
from datetime import datetime
import os

ImageFile.LOAD_TRUNCATED_IMAGES = True
def encode_image_to_base64(image_path):
    # 打开图片文件
    with Image.open(image_path) as img:
        # 将图片转换为字节流
        byte_arr = io.BytesIO()
        img.save(byte_arr, format=img.format)
        byte_arr = byte_arr.getvalue()

    # 将字节流转换为Base64编码
    return base64.b64encode(byte_arr).decode('utf-8')

# 示例
# image_path = 'dujuan.png'  # 或者 'example.png'
# encoded_image = encode_image_to_base64(image_path)
# print(encoded_image)

def decode_base64_to_image(base64_string,user_id):
    # length = len(base64_string)
    # if(length%3 == 1): 
    #     base64_string += "=="
    # elif(length%3 == 2): 
    #     base64_string += "=" 
    # 将Base64编码的字符串转换为字节
    base64_string = base64_string.replace(' ','+')
    # print(base64_string)
    decoded_data = base64.b64decode(base64_string)

    current_datetime = datetime.now()
    # 将字节流转换为图像对象
    image = Image.open(io.BytesIO(decoded_data))
    full_output_path = f'user_data/{user_id}/{current_datetime.year}/' \
                       f'{current_datetime.month}/{current_datetime.day}/' \
                       f'{current_datetime.hour}/{current_datetime.minute}_' \
                       f'{current_datetime.second}.jpg'
    
    # 确保输出目录存在
    output_dir = '/'.join(full_output_path.split('/')[:-1])
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # 保存图像
    image.save(full_output_path)
    return full_output_path
# 示例
# output_path = 'decoded_example.jpg'  # 或者 'decoded_example.png'
# decode_base64_to_image(encoded_image, output_path)