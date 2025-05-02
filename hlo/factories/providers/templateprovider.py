import logging

from faker.providers import BaseProvider  # , ElementsType

logger = logging.getLogger(__name__)


class TemplateProvider(BaseProvider):
    def template(self, template, values: dict[str]) -> str:
        return template.format(**values)
