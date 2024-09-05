import os
import re
import shutil

# 设置要遍历的文件夹路径
source_folder_path = r'G:\Data\AudioClassification\ESC-50-master\audio'
target_folder_path = 'G:\Data\AudioClassification\dataset'

# 音频分类索引
ClassName = {0: 'Dog', 10: 'Rain', 25: 'Footsteps', 26: 'Laughing', 31: 'MouseClick', 43: 'CarHorn'}


# 遍历文件夹中的所有文件
for filename in os.listdir(source_folder_path):
    # 检查文件扩展名是否为.wav
    if filename.endswith('.wav'):
        # 匹配文件名中的数字1-数字2-字母-数字3的模式
        match = re.match(r'(\d+)-(\d+)-[a-zA-Z]-(\d+)\.wav', filename)
        if match:
            number = int(match.group(3))
            if number in ClassName:
                # 为每个类别创建一个新的计数器
                category = ClassName[number]
                counter = 1  # 初始化计数器
                new_folder_path = os.path.join(target_folder_path, category)
                # 确保新文件夹存在
                os.makedirs(new_folder_path, exist_ok=True)
                # 构建源文件的完整路径
                source_file_path = os.path.join(source_folder_path, filename)
                while True:
                    # 构建新文件名
                    new_filename = f"{category}({counter}).wav"
                    target_file_path = os.path.join(new_folder_path, new_filename)
                    # 如果文件名不存在，则进行复制，否则递增计数器
                    if not os.path.exists(target_file_path):
                        shutil.copy2(source_file_path, target_file_path)
                        print(f'Copied "{filename}" to "{target_file_path}"')
                        break
                    else:
                        counter += 1
            else:
                print(f"No class name found for number {number}")

