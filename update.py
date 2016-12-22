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
    for index, repo in enumerate(full_repositories):
        print("Updating {}".format(repo))
        try:
            os.chdir(repo)
        except:
            raise WhatTheHellError(repo)
        sb = subprocess.Popen([git, "stash"], stdout=subprocess.PIPE)
        sb.wait()
        with subprocess.Popen([git, "pull"], stdout=subprocess.PIPE) as git_process:
            exit = git_process.wait()
            if exit == 0:
                print("OK")

    sys.exit(0)