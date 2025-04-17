import subprocess
from pathlib import Path

from django.core.management.base import (
    BaseCommand,
    no_translations,
)


class Command(BaseCommand):
    requires_migrations_checks = True

    def add_arguments(self, parser):
        parser.add_argument("dump_read", choices=["dump", "read"])

    @no_translations
    def handle(self, *_, **options):
        db = Path(r"db\db-dev.sqlite3")
        tables = [
            "auth_user",
            "hlo_attachment",
            "hlo_shop",
            "hlo_order",
            "hlo_order_attachments",
            "hlo_orderitem",
            "hlo_orderitem_attachments",
        ]

        Path.mkdir("db/table_export/", parents=True)

        if "dump_read" in options and options["dump_read"] == "dump":
            for sql in Path("db").glob("*.sql"):
                sql.unlink()
            for table in tables:
                print(table)  # noqa: T201
                file = Path(rf"db\table_export\{table}.sql")
                subprocess.run(  # noqa: S603
                    [  # noqa: S607
                        "sqlite3",
                        f"{db}",
                        f".mode insert {table}",
                        f".output {file}",
                        f"select * from {table};",  # noqa: S608
                    ],
                    check=False,
                )
        else:
            for table in tables:
                print(table)  # noqa: T201
                file = Path(rf"db\table_export\{table}.sql")
                subprocess.run(  # noqa: S603
                    [  # noqa: S607
                        "sqlite3",
                        f"{db}",
                        f".read {file}",
                    ],
                    check=False,
                )
