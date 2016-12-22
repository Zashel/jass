import argparse
import subprocess
import os
import sys

username = os.environ["USERNAME"]
proxy = "10.166.8.4:8080"
this_path = os.getcwd()
git = os.path.join(this_path, r"Git\bin\git.exe")
print(git)
repositories = [
    r"zashel\utils",
    r"zashel\websocket",
    r"zashel\virtualgpio",
    r"zashel\signal",
    r"zashel\basehandler",
    "uAgentAPI",
    "KenanFX"
    ]
repositories.sort()
full_repositories = [os.path.join(this_path, r"Python\Lib\site-packages", repo) for repo in repositories]
full_repositories.append(this_path)

class WhatTheHellError(Exception):
    pass

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
    for index, repo in enumerate(full_repositories):
        print("Updating {}".format(repo))
        try:
            os.chdir(repo)
        except:
            raise WhatTheHellError(repo)
        with subprocess.Popen([git, "pull"], stdout=subprocess.PIPE) as git_process:
            exit = git_process.wait()
            print("Exit: {}".format(exit))
            if exit == 1:
                sys.exit(1)

    sys.exit(0)