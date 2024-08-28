import os
import random

def get_random_image_from_folder(folder_path):
    # 检查文件夹是否存在
    if not os.path.isdir(folder_path):
        return "文件夹不存在，请检查路径是否正确"

    # 获取文件夹下的所有文件
    files = os.listdir(folder_path)
    
    # 筛选出图片文件
    images = [file for file in files if file.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif'))]
    
    # 如果没有找到任何图片，则返回提示信息
    if not images:
        return "文件夹中没有找到任何支持的图片文件"
    
    # 随机选择一张图片
    random_image = random.choice(images)
    
    return os.path.join(folder_path, random_image)

# 使用示例
# folder_path = 'path/to/your/folder'  # 替换为实际的文件夹路径
# print(get_random_image_from_folder(folder_path))