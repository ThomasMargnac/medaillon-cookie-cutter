import subprocess
import os


def install_virtual_env():
    os.environ["POETRY_VIRTUALENVS_IN_PROJECT"] = "true"
    subprocess.run(
        args="poetry install",
        shell=True
    )

def main():
    install_virtual_env()

if __name__ == "__main__":
    main()