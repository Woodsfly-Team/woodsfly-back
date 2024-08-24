import base64
from PIL import Image
import io
from datetime import datetime

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
    # 将Base64编码的字符串转换为字节
    decoded_data = base64.b64decode(base64_string)

    # 将字节流转换为图像对象
    image = Image.open(io.BytesIO(decoded_data))
    output_path = 'user_data/'+str(user_id)+'/'
    # 保存图像
    image.save(output_path)

# 示例
# output_path = 'decoded_example.jpg'  # 或者 'decoded_example.png'
# decode_base64_to_image(encoded_image, output_path)