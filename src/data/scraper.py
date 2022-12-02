import logging
import time
from concurrent.futures import ThreadPoolExecutor, wait
from functools import wraps
from pathlib import Path

import requests
from bs4 import BeautifulSoup
from scraper_utils import scrape_tag
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

TAGS = [
    "data-science",
    "machine-learning",
    "python",
    "programming",
    "technology",
]

# format must match YYYY/MM/DD
START_DATE = "2018/01/01"
END_DATE = "2022/10/01"


def get_proxies():
    url = "https://free-proxy-list.net/"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    proxies = []
    for i in soup.tbody.find_all("tr"):
        if len(proxies) == 5:
            break
        proxies.append(":".join([i.find_all("td")[0].string, i.find_all("td")[1].string]))
    return proxies


def get_driver():
    """Create a selenium driver"""
    options = webdriver.ChromeOptions()
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option("useAutomationExtension", False)
    options.add_argument("--disable-blink-features=AutomationControlled")
    s = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(options=options, service=s)

    driver.implicitly_wait(30)
    driver.execute_cdp_cmd(
        "Network.setUserAgentOverride",
        {
            "userAgent": (
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like"
                " Gecko) Chrome/91.0.4472.114 Safari/537.36"
            )
        },
    )
    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")

    return driver


def timeit(func):
    """a decorator to time a function"""

    @wraps(func)
    def timeit_wrapper(*args, **kwargs):
        start_time = time.perf_counter()
        result = func(*args, **kwargs)
        end_time = time.perf_counter()
        total_time = end_time - start_time
        logging.info(f"{func.__name__}{args} {kwargs} took {total_time:.4f} seconds")
        return result

    return timeit_wrapper


def single_scrape(path):
    """scrape with single driver"""
    for tag in TAGS:
        logging.info(f"Scraping tag: {tag}")
        logging.info("=====================================")
        driver = get_driver()
        scrape_tag(tag, driver, path, START_DATE, END_DATE)
        logging.info(f"Finished scraping {tag}")
        logging.info("done")


@timeit
def concurrent_scrape(path):
    """scrape with concurrent drivers"""

    drivers = [get_driver() for _ in range(5)]

    with ThreadPoolExecutor(max_workers=5) as executor:
        futures = [
            executor.submit(scrape_tag, tag, driver, path, START_DATE, END_DATE)
            for tag, driver in zip(TAGS, drivers)
        ]
        wait(futures)

    [driver.quit() for driver in drivers]


def main():
    project_dir = Path(__file__).resolve().parents[2]
    path = project_dir / "data" / "0_raw"

    try:
        path.mkdir(parents=True, exist_ok=False)
    except FileExistsError:
        logging.error("Folder is already there")

    single_scrape(path)

    # switching to concurrent scraping is faster but gets bot checked after a while
    # concurrent_scrape(path)


if __name__ == "__main__":
    log_fmt = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    logging.basicConfig(level=logging.INFO, format=log_fmt)

    main()
