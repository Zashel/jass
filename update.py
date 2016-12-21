import argparse
import subprocess
import os
import sys

username = os.environ["USERNAME"]
proxy = "10.166.8.4:8080"
this_path = os.getcwd()
git = os.path.join(this_path, r"Git\bin\git.exe")
print(git)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Initialize J-Ass Updater")
    parser.add_argument("-p", type=str, help="Network Password")
    args = parser.parse_args()
    password = args.p
    setting = subprocess.Popen(
            [git, "config", "--global", "http.proxy", "http://{}:{}@{}".format(username, password, proxy)])
    try:
        setting.wait(2)
    except subprocess.TimeoutExpired:
        pass
    git = subprocess.Popen(["git", "reset", "--hard", "HEAD"])
    git.wait()
    with subprocess.Popen([git, "pull", os.path.join(this_path, r"Python/Lib/site-packages/zashel/Utils"), "--allow-unrelated-histories"]) as git:
        exit = git.wait()
        print(exit)