import json
import argparse
from pathlib import Path
import subprocess
from rich.console import Console
from rich.table import Table


class RunnerApp:
    def __init__(self) -> None:
        self.fileTable = Table()  # 用于显示文件信息的表格
        self.commandTable = Table()  # 用于显示执行的命令的表格

    def ParseFile(self, debugMode: bool, file: Path) -> None:
        """
        解析文件信息并添加到表格中
        """
        self.file_source = str(file.resolve())  # 获取文件的绝对路径
        self.file = file.name  # 文件名
        self.file_name = file.stem  # 文件名（不包含扩展名）
        self.file_type = file.suffix[1:]  # 文件扩展名
        self.file_dir = str(file.parent)  # 文件所在目录的路径
        self.exec_cmd = []  # 存储要执行的命令

        # 添加文件信息到表格
        if debugMode:
            self.fileTable.add_column("[bold]Item")
            self.fileTable.add_column("[red]Value")
            self.fileTable.add_row("File source", self.file_source)
            self.fileTable.add_row("File", self.file)
            self.fileTable.add_row("File name", self.file_name)
            self.fileTable.add_row("File type", self.file_type)
            self.fileTable.add_row("File dir", self.file_dir)
            console.print(self.fileTable)

    def ExecCode(self, debugMode: bool, fileConfig: dict) -> None:
        """
        根据文件类型执行相应的命令，并将命令添加到表格中
        """
        for i in fileConfig:
            for j in fileConfig[i]["extension"]:
                if j == self.file_type:
                    self.exec_cmd = fileConfig[i]["command"]  # 查找执行命令
                    break
            if self.exec_cmd:
                break

        # 解析命令并将其添加到表格
        self.commandTable.add_column("")
        self.commandTable.add_column("[bold]Command")
        if self.exec_cmd:
            for i in range(len(self.exec_cmd)):
                cmd = self.exec_cmd[i].replace("$$", "\n\n$\n\n")
                cmd = (
                    cmd.replace("$file", self.file)
                    .replace("$name", self.file_name)
                    .replace("$type", self.file_type)
                    .replace("$path", self.file_dir)
                    .replace("$dir", self.file_dir)
                )
                cmd = cmd.replace("\n\n$\n\n", "$")
                self.commandTable.add_row(str(i + 1), cmd)
                self.exec_cmd[i] = cmd
            if debugMode:
                console.print(self.commandTable)

            # 执行命令
            for i in self.exec_cmd:
                console.rule()
                console.print(">", i, style="cyan")
                subprocess.run(i, cwd=self.file_dir, shell=True)
        else:
            console.print(
                "No execution command found for file type: .",
                self.file_type,
                style="white on red",
            )


# 解析命令行参数
parser = argparse.ArgumentParser(add_help=False)
parser.add_argument("file", type=str)
parser.add_argument("-v", "--verbosity", type=int, help="increase output verbosity")  # 增加输出详细程度的选项
parser.add_argument("-d", "--debug", action="store_true")  # 启用调试模式的选项
parser.add_argument("-h", "--help", action="store_true")  # 显示帮助信息的选项
args = parser.parse_args()

with open("filetype.json") as configure_file:
    config = json.load(configure_file)  # 从filetype.json文件中加载配置信息

if args.debug:
    config["debug"] = True

console = Console(color_system="256", style=None)  # 创建控制台对象

App = RunnerApp()
file = Path(args.file)
if file.exists():
    # 文件存在，继续执行逻辑
    App.ParseFile(config["debug"], file)
    App.ExecCode(config["debug"], config["filetype"])
else:
    console.print('"%s" is NOT a valid file path.' % args.file, style="white on red")
