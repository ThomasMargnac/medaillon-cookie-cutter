import subprocess
import os


def install_virtual_env():
    os.environ["POETRY_VIRTUALENVS_IN_PROJECT"] = "true"
    subprocess.run(
        args="poetry install",
        shell=True
    )

def init_git_repo():
    subprocess.run(
        args="git init --initial-branch=main",
        shell=True
    )
    subprocess.run(
        args="git add .",
        shell=True
    )
    subprocess.run(
        args="git commit -m 'Initial commit'",
        shell=True
    )

def main():
    install_virtual_env()
    init_git_repo()

if __name__ == "__main__":
    main()