#!/usr/local/bin/python3

import subprocess
from pathlib import Path


def main():
    command = subprocess.Popen(
        ["pip3", "--version"], stdout=subprocess.PIPE)
    output = int(command.communicate()[0].decode()[4:10].replace(".", ""))

    if output != 2024:
        subprocess.run(
            ["curl", "https://bootstrap.pypa.io/get-pip.py", "-o", "get-pip.py"])

    root = str(Path(__file__).parents[0])
    subprocess.run('pip3 install -r requirements.txt', shell=True, cwd=root)

    subprocess.run('python3 saaq.py', shell=True, cwd=root)


if __name__ == "__main__":
    main()
