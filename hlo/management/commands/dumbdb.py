import os
import subprocess
from pathlib import Path

from django.core.management.base import (
    BaseCommand,
    no_translations,
)


class Command(BaseCommand):
    requires_migrations_checks = True

    def add_arguments(self, parser):
        parser.add_argument("dump_read", choices=["dump","read"])

    @no_translations
    def handle(self, *_, **options):
        db = Path(r"db\db-dev.sqlite3")
        tables = [
            "auth_user",
            "hlo_attachement",
            "hlo_shop",
            "hlo_order",
            "hlo_order_attachements",
            "hlo_orderitem",
            "hlo_orderitem_attachements",
        ]

        os.makedirs("db/table_export/", exist_ok=True)

        if "dump_read" in options and options["dump_read"] == "dump":
            for sql in Path("db").glob("*.sql"):
                sql.unlink()
            for table in tables:
                print(table)
                file = Path(fr"db\table_export\{table}.sql")
                subprocess.run(
                    [
                        "sqlite3",
                        f"{db}",
                        f".mode insert {table}",
                        f".output {file}",
                        f"select * from {table};",
                    ],
                    check=False,
                )
        else:
            for table in tables:
                print(table)
                file = Path(fr"db\table_export\{table}.sql")
                subprocess.run(
                    [
                        "sqlite3",
                        f"{db}",
                        f".read {file}",
                    ],
                    check=False,
                )
