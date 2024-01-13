#! /usr/bin/env python3
from bootstrap import python_checks

python_checks()

# pylint: disable=wrong-import-position,wrong-import-order
import subprocess  # noqa: E402
import sys  # noqa: E402

nuke = input("Upgrade pip? (Y/n): ")
if nuke.lower() != "n":
    subprocess.run(
        [  # noqa: S603
            sys.executable,
            "-m",
            "pip",
            "install",
            "--require-virtualenv",
            "--no-user",
            "--upgrade",
            "pip",
        ],
        check=False,
    )

nuke = input("Pip install? (Y/n): ")
if nuke.lower() != "n":
    subprocess.run(
        [  # noqa: S603
            sys.executable,
            "-m",
            "pip",
            "install",
            "--require-virtualenv",
            "--no-user",
            "--upgrade",
            "-r",
            "requirements-dev.txt",
        ],
        check=False,
    )

nuke = input("Init shops? (Y/n): ")
if nuke.lower() != "n":
    subprocess.run(
        [  # noqa: S603
            sys.executable,
            "manage.py",
            "hlo",
            "--init-shops",
        ],
        check=False,
    )

nuke = input("Init order metadata without attachements? (Y/n): ")
if nuke.lower() != "n":
    subprocess.run(
        [  # noqa: S603
            sys.executable,
            "manage.py",
            "hlo",
            "--import-shop",
            "all",
            "--skip-attachements",
        ],
        check=False,
    )

nuke = input("Init order metadata with attachements ?  (Y/n): ")
if nuke.lower() != "n":
    subprocess.run(
        [sys.executable, "manage.py", "hlo", "--import-shop", "all"],  # noqa: S603
        check=False,
    )
