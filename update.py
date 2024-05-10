#! /usr/bin/env python3
import logging

from bootstrap import python_checks

logging.basicConfig(
    level=logging.DEBUG,
    style="{",
    format="{asctime} [{levelname}] {message} ({name}:{module})",
    handlers=[logging.StreamHandler()],
)

logger = logging.getLogger(__name__)

python_checks()
# ruff: noqa: T201,E402  # This is a simple script, we use print
# pylint: disable=wrong-import-position,wrong-import-order
import argparse
import shutil
import subprocess
import sys
from pathlib import Path

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


def upgrade_pip(args: argparse.Namespace) -> None:
    if args.yes or input("Upgrade pip? (Y/n): ").lower() != "n":
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


def install_upgrade_packages(args: argparse.Namespace) -> None:
    if args.yes or input("Pip install && upgrade? (Y/n): ").lower() != "n":
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


def delete_db(args: argparse.Namespace) -> None:
    if args.yes or input("Delete DB? (y/N): ").lower() == "y":
        p = Path("db/db-dev.sqlite3")
        if p.is_file():
            p.unlink()


def delete_migrations(args: argparse.Namespace) -> None:
    if args.yes or input("Delete migrations? (y/N): ").lower() == "y":
        migrations = Path("hlo/migrations")
        if migrations.is_dir():
            shutil.rmtree(migrations)


def make_run_migrations(args: argparse.Namespace) -> None:
    if args.yes or input("Make and apply migrations? (y/N): ").lower() == "y":
        try:
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
        except subprocess.CalledProcessError as cpe:
            logger.error("Error when running %s", "".join(cpe.cmd))  # noqa: TRY400
            sys.exit(1)


def create_superuser(_args: argparse.Namespace) -> None:
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
            # We are using Apache for auth, don't need password
            "--noinput",
        ],
        check=True,
    )


def import_shops(args: argparse.Namespace) -> None:
    if args.yes or input("Init shops? (Y/n): ").lower() != "n":
        subprocess.run(
            [  # noqa: S603
                sys.executable,
                "manage.py",
                "hlo",
                "--init-shops",
            ],
            check=True,
        )


def import_orders(args: argparse.Namespace) -> None:
    if (
        args.yes
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


def import_attachements(args: argparse.Namespace) -> None:
    if (
        args.yes
        or input("Init order metadata with attachements ?  (Y/n): ").lower()
        != "n"
    ):
        subprocess.run(
            [sys.executable, "manage.py", "hlo", "--import-shop", "all"],  # noqa: S603
            check=True,
        )


def _argparse() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    default_loglevel = "WARNING"
    parser.add_argument(
        "--loglevel",
        dest="loglevel",
        choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
        help="Set the logging level",
        type=str.upper,
        default=default_loglevel,
    )
    # logging.getLevelNamesMapping is 3.12
    default_loglevel = logging.getLevelName(default_loglevel)
    func_args = [
        "upgrade-pip",
        "install-upgrade_packages",
        "make_run_migrations",
        "create-superuser",
        "import-shops",
        "import-orders",
        "import-attachements",
    ]

    for arg in func_args:
        parser.add_argument(
            f"--{arg}",
            action="store_true",
            help=f"Run function {arg}()",
        )

    parser.add_argument(
        "--import-all",
        action="store_true",
        help="Run all import-functions.",
    )

    parser.add_argument(
        "--all",
        action="store_true",
        help="Run *all* functions.",
    )

    parser.add_argument(
        "-y",
        "--yes",
        action="store_true",
        help="Answer yes to all (most?) questions",
    )

    args = parser.parse_args()

    logger.setLevel(args.loglevel)

    if logger.getEffectiveLevel() != default_loglevel:
        logger.debug(
            "Loglevel changed from %s to %s",
            logging.getLevelName(default_loglevel),
            logging.getLevelName(logger.getEffectiveLevel()),
        )

    if args.all:
        for _arg in func_args:
            arg = _arg.replace("-", "_")
            logger.debug("Setting %s to True", arg)
            setattr(args, arg, True)

    if args.import_all:
        for _arg in [x for x in func_args if "import" in x]:
            arg = _arg.replace("-", "_")
            logger.debug("Setting %s to True", arg)
            setattr(args, arg, True)

    return args


def main() -> None:
    args = _argparse()

    logger.debug("Command line args: %s", args)

    if args.upgrade_pip:
        upgrade_pip(args)
    if args.install_upgrade_packages:
        install_upgrade_packages(args)
    if args.make_run_migrations:
        make_run_migrations(args)
    if args.create_superuser:
        create_superuser(args)
    if args.import_shops:
        import_shops(args)
    if args.import_orders:
        import_orders(args)
    if args.import_attachements:
        import_attachements(args)


if __name__ == "__main__":
    main()
