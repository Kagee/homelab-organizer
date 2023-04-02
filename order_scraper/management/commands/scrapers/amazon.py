import re
import datetime
import os
from pathlib import Path
from getpass import getpass
from typing import Dict, Final, List
from lxml.html.soupparser import fromstring
from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import (TimeoutException)
from .base import BaseScraper


# Inspiration:
# https://github.com/tobiasmcnulty/amzscraper
# https://chase-seibert.github.io/blog/2011/01/15/backup-your-amazon-order-history-with-python.html

class AmazonScraper(BaseScraper):
    TLD: str = "test"
    LOGIN_PAGE_RE: Final[str]
    ORDER_LIST_URL_TEMPLATE: Final[str]
    ORDER_ARCHIVED_URL: Final[str]
    ORDER_DETAIL_URL_TEMPLATE: Final[str]
    YEARS: Final[List]
    ORDER_LIST_CACHE_FILENAME_TEMPLATE: str
    PDF_TEMP_FILE: str

    def __init__(self, command: BaseCommand, options: Dict):
        super().__init__(command, options)
        self.log = self.setup_logger(__name__)
        self.command = command
        self.cache_orderlist = options['cache_orderlist']

        # pylint: disable=invalid-name
        self.LOGIN_PAGE_RE = fr'^https://www\.amazon\.{self.TLD}/ap/signin'
        self.ORDER_LIST_URL_TEMPLATE = \
            (f'https://www.amazon.{self.TLD}/gp/css/order-history?'
                'orderFilter=year-{year}&startIndex={start_index}')
        self.ORDER_ARCHIVED_URL = \
            f'https://www.amazon.{self.TLD}/gp/your-account/order-history?&orderFilter=archived'
        # The double {{order_id}} is intentional
        self.ORDER_DETAIL_URL_TEMPLATE = \
            f'https://www.amazon.{self.TLD}/your-account/order-details?ie=UTF8&orderID={{order_id}}'

        options['year'] = [int(x) for x in options['year'].split(",")]
        if options['year'] != [-1] and \
            any((x > datetime.date.today().year or x < 2011) for x in options['year']):
            self.log.critical(
                "--year must be from %s to %s inclusive, or -1",
                2011, datetime.date.today().year)
            raise CommandError("Invalid --year")

        if options['year'] == [-1]:
            self.YEARS    = list(range(2011, datetime.date.today().year))
        else:
            self.YEARS = sorted(options['year'])

        self.YEARS = [2011, 2012, 2013]

    def setup_cache(self):
        cache = {
            "BASE": (Path(settings.SCRAPER_CACHE_BASE) / 
                     Path(f'amazon_{self.TLD.replace(".","_")}')).resolve()
        }
        cache.update({
            "ORDER_LISTS":  (cache['BASE'] / 
                             Path('order_lists')).resolve(),
            "ORDERS":  (cache['BASE'] / 
                        Path('orders')).resolve(),
        })
        for key in cache:  # pylint: disable=consider-using-dict-items
            self.log.debug("Cache folder %s: %s", key, cache[key])
            try:
                os.makedirs(cache[key])
            except FileExistsError:
                pass

        pdf_temp_file = cache['BASE'] / Path('temporary-pdf.pdf')
        order_list_cache_filename_template = \
            str(cache["ORDER_LISTS"] / Path("order-list-{year}-{start_index}.html"))
        return cache, pdf_temp_file, order_list_cache_filename_template

    def load_order_list_html(self) -> List[str]:
        '''
        Returns the order list html, eithter from disk
        cache or using Selenium to visit the url.

            Returns:
                order_list_html (List[str]): A list of the HTML from the order list pages
        '''
        order_list_html = {}
        missing_years = []
        for year in self.YEARS:
            found_year = False
            if self.cache_orderlist:
                start_index = 0
                while True:
                    html_file = \
                        self.ORDER_LIST_CACHE_FILENAME_TEMPLATE.format(
                        year=year,
                        start_index=start_index
                        )
                    self.log.debug("Looking for cache in: %s", html_file)
                    if os.access(html_file, os.R_OK):
                        found_year = True
                        self.log.debug("Found cache year %s, index %s", year, start_index)
                        with open(html_file, "r", encoding="utf-8") as olf:
                            order_list_html[year] = fromstring(olf.read())
                        start_index += 10
                    else:
                        break

            if not found_year:
                self.log.error("Tried to use order list cache "
                               "for year %s, but found none", year)
                missing_years.append(year)

        if missing_years:
            return order_list_html.update(self.browser_scrape_order_lists_html(missing_years))
        else:
            print(self.YEARS)
            self.log.debug("Found cache for all years: %s", ",".join(str(x) for x in self.YEARS))
        return order_list_html

    def browser_login(self):
        '''
        Uses Selenium to log in Amazon.
        Returns when the browser is at url, after login.

        Raises and alert in the browser if user action
        is required.
        '''
        # We (optionally) ask for this here and not earlier, since we
        # may not need to go live
        self.username = input(f"Enter Amazon.{self.TLD} username: ") \
                if not settings.SCRAPER_AMZ_USERNAME else settings.SCRAPER_AMZ_USERNAME
        self.password = getpass(f"Enter Amazon.{self.TLD} password: ") \
                if not settings.SCRAPER_AMZ_PASSWORD else settings.SCRAPER_AMZ_PASSWORD

        self.log.info(self.command.style.NOTICE("We need to log in to amazon.%s"), self.TLD)
        brws = self.browser_get_instance()

        wait = WebDriverWait(brws, 10)
        try:
            self.rand_sleep()
            username = wait.until(
                    EC.presence_of_element_located((By.ID, "ap_email"))
                    )
            username.send_keys(self.username)
            self.rand_sleep()
            wait.until(
                    EC.element_to_be_clickable(
                        ((By.ID, "continue"))
                        )
                    ).click()
            self.rand_sleep()
            password = wait.until(
                    EC.presence_of_element_located((By.ID, "ap_password"))
                    )
            password.send_keys(self.password)
            self.rand_sleep()
            remember = wait.until(
                    EC.presence_of_element_located((By.NAME, "rememberMe"))
                    )
            remember.click()
            self.rand_sleep()
            sign_in = wait.until(
                    EC.presence_of_element_located((By.ID, "auth-signin-button"))
                    )
            sign_in.click()
            self.rand_sleep()

        except TimeoutException:
            self.browser_safe_quit()
            # pylint: disable=raise-missing-from
            raise CommandError("Login to Amazon was not successful "
                               "because we could not find a expected element..")
        if re.match(self.LOGIN_PAGE_RE ,self.browser.current_url):
            raise CommandError('Login to Amazon was not successful.')
        self.log.info('Login to Amazon was probably successful.')

    def command_scrape(self) -> None:
        self.load_order_list_html()
        self.browser_safe_quit()

    # TypeError: Too few arguments for typing.Dict; actual 1, expected 2
    def browser_scrape_order_lists_html(self, years: List):
        '''
        Uses Selenium to visit, load, save and then
        return the HTML from the order list page

            Returns:
                order_lists_html (Dict[str]): A list of the HTML from the order list pages
        '''
        self.log.debug("Scraping %s using Selenium", years)
        order_list_html = {}
        for year in years:
            self.log.debug("Scraping order list")
            curr_url = self.ORDER_LIST_URL_TEMPLATE.format(
                year=year,
                start_index=0
                )
            brws = self.browser_visit_page(curr_url, goto_url_after_login=True)
            # wait10 = WebDriverWait(brws, 10)
            try:
                WebDriverWait(brws, 3).until(
                    EC.presence_of_element_located(
                        (By.XPATH,
                         '//div'
                         '[contains(@class, "a-text-center")]'
                         '[contains(@class, "a-section")]'
                        )
                    ))
                # No orders, save html and return
                cache_file = self.ORDER_LIST_CACHE_FILENAME_TEMPLATE.format(
                    year=year,
                    start_index=0
                    )
                self.log.info("No orders found, saving cache to %s", cache_file)
                order_list_html[year] = self.save_page_to_file(cache_file)
                continue
            except TimeoutException:
                pass
            # TODO
            self.log.debug("Page %s har orders, but we do not know how to scrape them", curr_url)
        return order_list_html
