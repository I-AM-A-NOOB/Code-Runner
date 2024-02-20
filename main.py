import json
from pathlib import Path
import subprocess
from rich.console import Console
from rich.table import Table

fileTable = Table()
commandTable = Table()
console = Console(color_system="256", style=None)

with open("filetype.json") as configure_file:
    config = json.load(configure_file)
# file = sys.argv[1].split(".")
file_source = ".\\test\\a.cpp"
file_source = str(Path(file_source).resolve())
file = str(Path(file_source).name)
file_name = str(Path(file_source).stem)
file_type = str(Path(file_source).suffix)[1:]
file_dir = str(Path(file_source).parent)
exec_cmd = []

fileTable.add_column("[bold]Item")
fileTable.add_column("[red]Value")
fileTable.add_row("File source", file_source)
fileTable.add_row("File", file)
fileTable.add_row("File name", file_name)
fileTable.add_row("File type", file_type)
fileTable.add_row("File dir", file_dir)
console.print(fileTable)

for i in config:
    for j in config[i]["filetype"]:
        if j == file_type:
            exec_cmd = config[i]["command"]
            break
    if exec_cmd:
        break

commandTable.add_column("")
commandTable.add_column("[bold]Command")
if exec_cmd:
    for i in range(len(exec_cmd)):
        cmd = exec_cmd[i].replace("$$", "\n\n$\n\n")
        cmd = (
            cmd.replace("$file", file)
            .replace("$name", file_name)
            .replace("$type", file_type)
            .replace("$path", file_dir)
            .replace("$dir", file_dir)
        )
        cmd = cmd.replace("\n\n$\n\n", "$")
        commandTable.add_row(str(i + 1), cmd)
        exec_cmd[i] = cmd

    console.print(commandTable)
    for i in exec_cmd:
        console.rule()
        console.print(">", i, style="cyan")
        subprocess.run(i, cwd=file_dir, shell=True)
else:
    console.print(
        "No execution command found for file type: .", file_type, style="white on red"
    )
