import logging

from django.contrib.contenttypes.models import ContentType
from django.core.management.base import BaseCommand, CommandError

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = (
        "List all permissions for models. "
        "Will by default not list results for the admin, auth, "
        "contenttypes or sessions apps."
    )

    def add_arguments(self, parser):
        parser.add_argument(
            "app_label_model",
            help="[app_label.]model(s) to show permissions for.",
            nargs="*",
        )
        parser.add_argument(
            "--all",
            help=(
                "Include results for admin, auth, auth, contenttypes "
                "and sessions"
            ),
            action="store_true",
        )
        parser.add_argument(
            "--app-label",
            help="App label to dump permissions for.",
        )

    def handle(self, *_args, **options):
        if options["all"]:
            logger.debug("Getting absolutely all available content types")
            content_types = ContentType.objects.order_by("app_label", "model")
        elif options["app_label"]:
            app_label = options["app_label"].lower()
            logger.debug(
                "Getting all content types with app label '%s'",
                app_label,
            )
            content_types = ContentType.objects.filter(
                app_label=app_label,
            ).order_by("app_label", "model")
            if not content_types:
                msg = (
                    "There are no content types "
                    f'with the "{app_label}" app label.'
                )
                raise CommandError(msg)
        elif not bool(options["app_label_model"]):
            logger.debug(
                "Getting all content types excluding admin, "
                "auth, contenttypes and session apps",
            )
            content_types = ContentType.objects.exclude(
                app_label__in=["admin", "auth", "contenttypes", "sessions"],
            ).order_by("app_label", "model")
        else:
            logger.debug(
                (
                    "Getting all content types with "
                    "app_label/model name matching %s"
                ),
                ", ".join(options["app_label_model"]),
            )
            content_types = []
            for content_type in options["app_label_model"]:
                orm_filter = {"model": content_type}
                if "." in content_type:
                    app_label, model = content_type.split(".")
                    orm_filter = {"app_label": app_label, "model": model}
                logger.debug("Getting content types with filter %s", orm_filter)
                result = ContentType.objects.filter(**orm_filter)
                if not result:
                    msg = (
                        f"Could not find content type using filter {orm_filter}"
                    )
                    raise CommandError(msg)
                content_types += result

        for content_type in content_types:
            self.stdout.write(
                f"Permissions for {content_type}",
            )
            for permission in content_type.permission_set.all():
                self.stdout.write(
                    f"\t {content_type.app_label}.{permission.codename} | {permission.name}"
                )
