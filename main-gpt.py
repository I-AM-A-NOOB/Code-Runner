import json
import subprocess
from pathlib import Path

# 读取配置文件
with open("filetype.json") as configure_file:
    config = json.load(configure_file)

# 解析文件信息
file_path = Path("./test/a.cpp").resolve()
file_name = file_path.stem
file_type = file_path.suffix[1:]
file_dir = str(file_path.parent)

# 获取命令行
exec_cmd = []
for i in config:
    for j in config[i]["filetype"]:
        if j == file_type:
            exec_cmd = config[i]["command"]
            break
    if exec_cmd:
        break

# 执行命令行
if exec_cmd:
    for cmd_template in exec_cmd:
        cmd = cmd_template.replace("$file", file_name) \
                           .replace("$name", file_name) \
                           .replace("$type", file_type) \
                           .replace("$path", file_dir) \
                           .replace("$dir", file_dir)
        print(cmd)
        subprocess.run(["powershell", "-Command", cmd], cwd=file_dir, shell=True)
else:
    print(f"No execution command found for file type: {file_type}")
