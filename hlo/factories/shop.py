import factory
from django.conf import settings
from factory import fuzzy
from factory.django import DjangoModelFactory
from faker_file.providers.image.pil_generator import PilImageGenerator
from faker_file.providers.png_file import (
    GraphicPngFileProvider,
    PngFileProvider,
)
from faker_file.storages.filesystem import FileSystemStorage

from hlo.models import Shop

# FAKER = Faker()  # Initialize Faker
# FAKER.add_provider(PngFileProvider)  # Register PngFileProvider

# Generate PNG file using `imgkit`
# pdf_file = FAKER.png_file(image_generator_cls=ImgkitImageGenerator)#
# factory.Faker.add_provider(PngFileProvider)
factory.Faker.add_provider(GraphicPngFileProvider)


class ShopFactory(DjangoModelFactory):
    class Meta:
        model = Shop
        exclude = ("_branch", "_order_url", "_item_url")

    name = factory.Faker("company")
    _branch = fuzzy.FuzzyChoice(
        [".no", ".com", " South Branch", " China"],
    )
    branch_name = factory.LazyAttribute(
        lambda p: f"{p.name}{p._branch}",  # noqa: SLF001
    )

    _order_url = factory.Faker("url")
    order_url_template = factory.LazyAttribute(
        lambda p: f"{p._order_url}/{{order_id}}/view",  # noqa: SLF001
    )
    item_url_template = factory.LazyAttribute(
        lambda p: f"{p._order_url}{{order_id}}/view/{{item_id}}",  # noqa: SLF001
    )
    manual_input = False

    icon = factory.Faker(
        "graphic_png_file",
        image_generator_cls=PilImageGenerator,
        storage=FileSystemStorage(
            root_path=settings.MEDIA_ROOT,
            rel_path="faker",
            size=(200, 200),
        ),
    )
