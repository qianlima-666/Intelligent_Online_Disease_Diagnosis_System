from flask import Blueprint

app_plugins = Blueprint('plugins', __name__)

import os
import glob
import importlib

# 获取当前目录路径
dir_path = os.path.dirname(os.path.realpath(__file__))

# 获取所有 Python 文件的路径
file_paths = glob.glob(dir_path + "/*.py")

# 导入所有 Python 文件中的公共变量和函数
for file_path in file_paths:
    module_name = os.path.splitext(os.path.basename(file_path))[0]
    if module_name != "__init__":
        module = importlib.import_module("web.plugins." + module_name)
        globals().update(module.__dict__)
