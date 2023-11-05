import fitz
from loader.models import OrderItem
import logging
from django.conf import settings
from django.core.management.base import (
    BaseCommand,
    no_translations,
)


class Command(BaseCommand):
    help = "Extract text from all item PDFs"
    requires_migrations_checks = True



    @no_translations
    def handle(self, *_, **options):
        options["verbosity"] = 3  # Force debug output
        self.setup_logger(options)
        self.log.debug(options)
        for itemobj in OrderItem.objects.all():
            if itemobj.attachements.count() > 0:
                pdfs = itemobj.attachements.filter(file__endswith=".pdf")
                for pdf in pdfs:
                    self.log.debug("Processing %s", pdf.file.path)
                    doc = fitz.open(pdf.file.path)
                    text = ''
                    for i, page in enumerate(doc):
                        text += page.get_text()
                    pdf.text = text
                    pdf.save()

    #def add_arguments(self, parser):
    #    scraper = parser.add_argument_group()
    #    scraper.add_argument(
    #        "--init-shops",
    #        action="store_true",
    #        help=(
    #            "Initialize database with shop data from JSON files. Will"
    #            " update existing data."
    #        ),
    #    )

    def setup_logger(self, options):
        log = logging.getLogger(__name__)
        if options["verbosity"] == 0:
            # 0 = minimal output
            log.setLevel(logging.ERROR)
        elif options["verbosity"] == 1:
            # 1 = normal output
            log.setLevel(logging.WARNING)
        elif options["verbosity"] == 2:
            # 2 = verbose output
            log.setLevel(logging.INFO)
        elif options["verbosity"] == 3:
            # 3 = very verbose output
            log.setLevel(logging.DEBUG)
        # pylint: disable=attribute-defined-outside-init
        self.log = log