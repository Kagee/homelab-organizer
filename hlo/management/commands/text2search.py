import logging
from whoosh.fields import *
from whoosh.index import open_dir
from whoosh.qparser import QueryParser
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
        if options["init"] and options["search"]:
            self.print_help("manage.py", "text2search")
        #elif options["init"]:
        #    schema = Schema(att_id=ID(stored=True),item_id=ID(stored=True), content=TEXT)
        #    ix = create_in("whoosh_index", schema)
        #    writer = ix.writer()
        #    for itemobj in OrderItem.objects.all():
        #        if itemobj.attachements.count() > 0:
        #            pdfs = itemobj.attachements.filter(file__endswith=".pdf")
        #            for pdf in pdfs:
        #                if len(pdf.text) > 0:
        #                    self.log.debug("Processing item %s, attachement %s", itemobj.id, pdf.id)
        #                    writer.add_document(att_id=str(pdf.id), item_id=str(itemobj.id), content=pdf.text)
        #    writer.commit()
        elif options["search"]:
            ix = open_dir("whoosh_index")
            with ix.searcher() as searcher:
                query = QueryParser("content", ix.schema).parse(options["search"])
                results = searcher.search(query)
                print(results[0], len(results))

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

    def add_arguments(self, parser):
        cmd = parser.add_argument_group()
        cmd.add_argument(
            "--init",
            action="store_true",
            help=(
                "Initialize search index from DB"
            ),
        )

        cmd.add_argument(
            "-s",
            "--search",
            help="Search query",
        )