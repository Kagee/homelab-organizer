import logging
from decimal import Decimal

logger = logging.getLogger(__name__)
from django.conf import settings
from djmoney.money import Money
from faker.providers import BaseProvider  # , ElementsType


class MoneyProvider(BaseProvider):
    # settings.CURRENCIES
    def djmoney(
        self,
        text: str | None = None,
        currency: str | None = None,
        multiplier: Decimal = 1,
        money: Money | list[Money] | None = None,
    ) -> Money:
        if money:
            # Use the input currency
            if isinstance(money, Money):
                logger.debug("Money is Money: %s / %s", money, type(money))
                new_money = Money(
                    amount=money.amount * Decimal(multiplier),
                    currency=money.currency,
                )
            else:
                logger.debug("Money is not Money: %s", money)
                new_money = Money(amount=0, currency=money[0].currency)
                for m in money:
                    new_money += m
                new_money = new_money * Decimal(multiplier)
            logger.debug("Money: %s, New money: %s", money, new_money)
            return new_money
        if not currency:
            currency = self.random_choices(settings.CURRENCIES, length=1)[0]
            # logger.debug("Random currency: %s", currency)
        else:
            # logger.debug("Spesified currency: %s", currency)
            pass
        if not text:
            # For USD and EUR
            text = "@%#,##"
            if currency == "NOK":
                # 10 NOK ~1 USD, add a digit
                text = "@%##,##"
            if currency == "JPY":
                # 100 NOK ~.7 USD, add two digits and no decimals
                text = "@%###"
        m = Money(
            amount=Decimal(self.numerify(text=text).replace(",", "."))
            * Decimal(multiplier),
            currency=currency,
        )
        logger.debug("Money returned: %s", m)
        return m
