from decimal import Decimal

from djmoney.money import Money
from faker.providers import BaseProvider  # , ElementsType


class MoneyProvider(BaseProvider):
    # settings.CURRENCIES
    def money(self, text: str | None = None):
        return Money(Decimal(self.numerify(text=text).replace(",", ".")), "NOK")
