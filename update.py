#! /usr/bin/env python3
from bootstrap import python_checks

python_checks()
# ruff: noqa: T201  # This is a simple script, we use print
# pylint: disable=wrong-import-position,wrong-import-order
import shutil  # noqa: E402
import subprocess  # noqa: E402
import sys  # noqa: E402
from pathlib import Path  # noqa: E402

environs_loaded = False
try:
    from environs import Env

    env = Env()
    with env.prefixed("UPDATE_HLO_"):
        env.read_env(".env", recurse=False, verbose=True)
        SUPERUSER_NAME = env("SUPERUSER_NAME")
        SUPERUSER_EMAIL = env("SUPERUSER_EMAIL")
    environs_loaded = True
except ModuleNotFoundError:
    pass


def _01_upgrade_pip():
    if not only_input and (
        auto_answer or input("Upgrade pip? (Y/n): ").lower() != "n"
    ):
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
            check=True,
        )


def _02_pip_install_upgrade():
    if not only_input and (
        auto_answer or input("Pip install && upgrade? (Y/n): ").lower() != "n"
    ):
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
            check=True,
        )

    if not environs_loaded:
        print("Restart script to load environs module")
        sys.exit(0)


def _03_delete_db():
    db_deleted = False
    if not only_input and (
        auto_answer or input("Delete DB? (y/N): ").lower() == "y"
    ):
        p = Path("db/db-dev.sqlite3")
        if p.is_file():
            p.unlink()
        db_deleted = True
    return db_deleted


def _04_migrations(db_deleted=None):
    if db_deleted is None:
        db_deleted = _03_delete_db()
    migrations_ran = False
    if not only_input and (
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
            check=True,
        )
        subprocess.run(
            [  # noqa: S603
                sys.executable,
                "manage.py",
                "migrate",
            ],
            check=True,
        )
        migrations_ran = True
    return (db_deleted, migrations_ran)


def _05_superuser(db_deleted=None, migrations_ran=None):
    if db_deleted is None and migrations_ran is None:
        db_delete, migrations_ran = _04_migrations()

    if db_deleted and migrations_ran:
        print("Database deleted, must recreate superuser.V")
        print(f"Username: {SUPERUSER_NAME}")
        print(f"Email: {SUPERUSER_EMAIL}")
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
            check=True,
        )


def _06_init_shops():
    if only_input or auto_answer or input("Init shops? (Y/n): ").lower() != "n":
        subprocess.run(
            [  # noqa: S603
                sys.executable,
                "manage.py",
                "hlo",
                "--init-shops",
            ],
            check=True,
        )


def _07_order_metadata():
    if (
        only_input
        or auto_answer
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
            check=True,
        )


def _08_order_attachements():
    if (
        only_input
        or auto_answer
        or input("Init order metadata with attachements ?  (Y/n): ").lower()
        != "n"
    ):
        subprocess.run(
            [sys.executable, "manage.py", "hlo", "--import-shop", "all"],  # noqa: S603
            check=True,
        )


def main() -> None:
    print(f"{auto_answer=}, {only_input=}")
    _01_upgrade_pip()
    _02_pip_install_upgrade()
    # _03_delete_db
    # _04_migrations
    _05_superuser(_04_migrations(_03_delete_db()))
    _06_init_shops()
    _07_order_metadata()
    _08_order_attachements()


if __name__ == "__main__":
    # YES I KNOW; SUE ME!!
    print_help = "-h" in sys.argv or "--help" in sys.argv
    auto_answer = "-y" in sys.argv or "--yes" in sys.argv
    only_input = "-i" in sys.argv or "--import" in sys.argv

    import inspect
    import types

    funcs = inspect.getmembers(
        sys.modules[__name__],
        predicate=lambda x: isinstance(x, types.FunctionType)
        and x.__module__ == __name__
        and x.__name__.startswith("_0"),
    )
    funcs = [(x[4:], y) for (x, y) in funcs]
    any_func_called = False
    if print_help:
        any_func_called = True
        print("-y\t\tAuto answer yes to every question")
        print("-i\t\tOnly run nondestructive import functions")
        print("")
        print("Call functions directly (may use multiple)")
        for fname, _ in funcs:
            print(f"\t--{fname}")
    else:
        for fname, func in funcs:
            if f"--{fname}" in sys.argv:
                any_func_called = True
                func()

    if not any_func_called:
        main()
