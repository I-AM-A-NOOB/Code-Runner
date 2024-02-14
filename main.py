import json
from pathlib import Path
import subprocess
# import sys
# using "pathlib" to get folder & file & filetype

with open("filetype.json") as configure:
    cfg = configure.read()
    cfg = json.loads(cfg)
print(cfg)
# file = sys.argv[1].split(".")
file_source = ".\\test\\a.cpp"
file_source = str(Path(file_source).resolve())
file = str(Path(file_source).name)
file_name = str(Path(file_source).stem)
file_type = str(Path(file_source).suffix)[1:]
file_dir = str(Path(file_source).parent)
exec_cmd = []
print("file_type: "+file_type)
print("file_dir:  "+file_dir)

for i in cfg:
    print(i)
    for j in cfg[i]["filetype"]:
        if j == file_type:
            exec_cmd = cfg[i]["command"]
            print(exec_cmd)
            break
    if exec_cmd != []:
        break
# subprocess.call("cd \"%s\"" % file_locate)
for i in exec_cmd:
    cmd = i.replace("$$", "\\$\\")
    cmd = cmd.replace("$file", file).replace("$name", file_name).replace("$type", file_type).replace("$path", file_dir)
    cmd = cmd.replace("\\$\\", "$")
    print(cmd)
    cmd.replace("$dir", file_dir)
    # print("powershell -Command \"& cd '%s' ; %s \"" % (file_dir, cmd))
    subprocess.call("powershell -Command \"& cd '%s' ; %s \"" % (file_dir, cmd))
    # subprocess.call("cmd -c \"cd \"%s\"\";\"%s\"" % (file_locate, cmd))
