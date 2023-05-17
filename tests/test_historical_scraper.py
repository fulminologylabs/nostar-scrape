import pytest
from datetime import datetime
from services.scrapers.scraper import HistoricalScraper

# TODO Test case for initializing dates
test_params = [
    ("1/4/2020", "1/10/2020"),
    ("01/04/2020", "01/06/2020"),
    ("1/04/2020", "1/07/2020"),
    ("01/1/2020", "01/3/2020"),
    ("1/4/2020", "01/08/2020")
]
url = "wss://relay.com"
# TODO This will become the Bulk Process
class TestHistoricalScraper:
    def test_init_test_date_params(self):
        """
            Asserts the start and end init
            params can be parsed a variety of ways
        """
        for test in test_params:
            scraper = HistoricalScraper(url=url, start=test[0], end=test[1])
            # Assert that the value set is of type datetime
            assert datetime == type(scraper.start)
            assert datetime == type(scraper.end)

    def test_init_test_date_params_ver2(self):
        """
            Second set of date formats
        """
        for test in test_params:
            params = (test[0].replace("/", "-"), test[1].replace("/", "-"))
            scraper = HistoricalScraper(url=url, start=params[0], end=params[1])
            # Assert that the value set is of type datetime
            assert datetime == type(scraper.start)
            assert datetime == type(scraper.end)
            
    def test_init_no_params(self):
        """
            Asserts the default values are enough for initialization
        """
        scraper = HistoricalScraper(url=url)    
        # Assert that the value set is of type datetime
        assert datetime == type(scraper.start)   
        assert datetime == type(scraper.end)
