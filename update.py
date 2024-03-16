#! /usr/bin/env python3
from bootstrap import python_checks

python_checks()

# pylint: disable=wrong-import-position,wrong-import-order
import shutil  # noqa: E402
import subprocess  # noqa: E402
import sys  # noqa: E402
from pathlib import Path  # noqa: E402

from environs import Env  # noqa: E402

env = Env()
with env.prefixed("UPDATE_HLO_"):
    env.read_env(".env", recurse=False, verbose=True)
    SUPERUSER_NAME = env("SUPERUSER_NAME")
    SUPERUSER_EMAIL = env("SUPERUSER_EMAIL")


def main(auto_answer: bool) -> None:
    if auto_answer or input("Upgrade pip? (Y/n): ").lower() != "n":
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

    if auto_answer or input("Pip install && upgrade? (Y/n): ").lower() != "n":
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

    db_deleted = False
    migrations_ran = False

    if auto_answer or input("Delete DB? (y/N): ").lower() == "y":
        p = Path("db/db-dev.sqlite3")
        if p.is_file():
            p.unlink()
        db_deleted = True

    if (
        auto_answer
        or input("Delete, recreate and apply migrations? (y/N): ").lower()
        == "y"
    ):
        shutil.rmtree(Path("hlo/migrations"))
        subprocess.run(
            [  # noqa: S603
                sys.executable,
                "manage.py",
                "makemigrations",
                "hlo",
            ],
            check=False,
        )
        subprocess.run(
            [  # noqa: S603
                sys.executable,
                "manage.py",
                "migrate",
            ],
            check=False,
        )
        migrations_ran = True

    if db_deleted and migrations_ran:
        print("Database deleted, must recreate superuser.V")  # noqa: T201
        print(f"Username: {SUPERUSER_NAME}")  # noqa: T201
        print(f"Email: {SUPERUSER_EMAIL}")  # noqa: T201
        subprocess.run(
            [  # noqa: S603
                sys.executable,
                "manage.py",
                "createsuperuser",
                "--username",
                SUPERUSER_NAME,
                "--email",
                SUPERUSER_EMAIL,
            ],
            check=False,
        )

    if auto_answer or input("Init shops? (Y/n): ").lower() != "n":
        subprocess.run(
            [  # noqa: S603
                sys.executable,
                "manage.py",
                "hlo",
                "--init-shops",
            ],
            check=False,
        )

    if (
        auto_answer
        or input("Init order metadata without attachements? (Y/n): ").lower()
        != "n"
    ):
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

    if input("Init order metadata with attachements ?  (Y/n): ").lower() != "n":
        subprocess.run(
            [sys.executable, "manage.py", "hlo", "--import-shop", "all"],  # noqa: S603
            check=False,
        )


if __name__ == "__main__":
    do_it = False
    if len(sys.argv) > 1:
        do_it = sys.argv[1] == "-y"
    main(auto_answer=do_it)
