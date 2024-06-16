import os
import sys
import datetime


def get_base_path():
    # 检查是否被打包
    if getattr(sys, 'frozen', False):
        # 如果被打包，使用 sys._MEIPASS 作为基路径
        return sys._MEIPASS
    else:
        # 否则，使用脚本文件的目录作为基路径
        return os.path.abspath(os.path.dirname(__file__))


Base_Path = get_base_path()
LogTime = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")

# 构建配置文件路径
command_config = os.path.join(Base_Path, 'fast_btn_config.ini')
instruction_config = os.path.join(Base_Path, 'instruction_config.csv')

# 创建 log 文件夹路径
log_folder_path = os.path.join(Base_Path, 'log')

# 检查 log 文件夹是否存在，如果不存在则创建
if not os.path.exists(log_folder_path):
    os.makedirs(log_folder_path)

# # 打印路径以供调试
# print(f"Base_Path: {Base_Path}")
# print(f"Command Config Path: {command_config}")
# print(f"Instruction Config Path: {instruction_config}")
