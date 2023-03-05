import argparse
# script to download a file from a url with an iframe
from icecream import ic
import time
import os
from tqdm import tqdm
from cad_tickers.sedar.tsx import get_ticker_filings, get_news_and_events
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium import webdriver
from selenium.webdriver.common.by import By
import requests


def make_webdriver(build_name="stonk_doc_search"):
    remote_url = os.environ.get("REMOTE_SELENIUM_URL")
    if remote_url == None:
        raise Exception("Missing REMOTE_SELENIUM_URL in env vars")
    desired_cap = {
        "os_version": "10",
        "resolution": "1920x1080",
        "browser": "Chrome",
        "browser_version": "latest",
        "os": "Windows",
        "name": "stonk_reports-[Python]",  # test name
        "build": build_name,  # CI/CD job or build name
    }
    driver = webdriver.Remote(
        command_executor=remote_url,
        desired_capabilities=desired_cap,
    )
    return driver

# make directory if it doesn't exist

def mk_dir(dir_name: str):
    if not os.path.exists(dir_name):
        os.makedirs(dir_name)

def get_stonk_data(stock_name: str = "PKK", start_date = "2020-09-03", end_date = "2021-12-03"):
    ic("Eating ice cream")
    filings_data = get_ticker_filings(stock_name, start_date, end_date, 2000)
    filings = filings_data.get("filings")
    ic(filings)
    if filings is None:
        return
    mk_dir(f"docs/{stock_name}")
    total_downloads = 0
    startTime = time.time()
    # use tqdm to show progress bar
    for filing in tqdm(filings, desc = f'Downloading PDFs for {stock_name}'):
        # get data tp
        filing_date = filing.get("filingDate")
        description = filing.get("description", "")
        description = description.replace(" ", "_")
        name = filing.get("name", "")
        name = name.replace("-", " ").replace(" ", "_").replace("/", "_")
        pdf_url = filing.get("urlToPdf")
        pdf_name = f"docs/{stock_name}/{filing_date}_{name}.pdf"
        # if file exists skip
        if os.path.exists(pdf_name):
            ic(f"Skipping {pdf_name}")
            continue
        else:
            total_downloads += 1
            ic(f"Downloading {pdf_name}")
            try:
                get_pdf_from_url(pdf_url, pdf_name)
            except Exception as e:
                print(e)
                print(f"Skipping {pdf_name}")
                continue

    # get all urls from data
    executionTime = (time.time() - startTime)
    print('Execution time in seconds: ' + str(executionTime))
    print(f"Total downloads: {total_downloads}")
    if total_downloads == 0:
        print("No filings found")
    else:
        print(f"Average dl time: {executionTime / total_downloads}")



def get_stonk_data_news(stock_name: str = "PKK", start_date = "2020-09-03", end_date = "2021-12-03"):
    ic("Eating ice cream")
    filings_data = get_news_and_events(stock_name, 1, 1000)
    filings = filings_data.get("news")
    if filings is None:
        ic("NO FILINGS")
        return
    ic(filings)
    mk_dir(f"../docs/{stock_name}")
    total_downloads = 0
    startTime = time.time()
    # use tqdm to show progress bar
    for filing in tqdm(filings, desc = f'Downloading PDFs for {stock_name}'):
        # get data tp
        filing_date = filing.get("filingDate")
        description = filing.get("description", "")
        description = description.replace(" ", "_")
        name = filing.get("name", "")
        name = name.replace("-", " ").replace(" ", "_").replace("/", "_")
        pdf_url = filing.get("urlToPdf")
        pdf_name = f"docs/{stock_name}/pdf/{filing_date}_{name}.pdf"
        # if file exists skip
        if os.path.exists(pdf_name):
            ic(f"Skipping {pdf_name}")
            continue
        else:
            total_downloads += 1
            ic(f"Downloading {pdf_name}")
            try:
                get_pdf_from_url(pdf_url, pdf_name)
            except Exception as e:
                print(e)
                print(f"Skipping {pdf_name}")
                continue

    # get all urls from data
    executionTime = (time.time() - startTime)
    print('Execution time in seconds: ' + str(executionTime))
    print(f"Total downloads: {total_downloads}")
    if total_downloads == 0:
        print("No filings found")
    else:
        print(f"Average dl time: {executionTime / total_downloads}")


def get_pdf_from_url(
    investorx_url: str = "https://www.investorx.ca/doc/2111300436476926",
    pdf_name: str = "test.pdf",
):
    driver = make_webdriver()
    # driver = webdriver.Chrome(options=options)

    driver.get(investorx_url)
    try:
        WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.TAG_NAME, 'iframe')))
    except TimeoutException:
        time.sleep(2)
    pdf_url = driver.find_element(By.TAG_NAME, 'iframe').get_attribute("src")
    driver.quit()
    chunk_size  = 2000
    r = requests.get(pdf_url, stream=True)
    with open(pdf_name, 'wb') as fd:
        for chunk in r.iter_content(chunk_size):
            fd.write(chunk)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--stock', help='Target stock name must be for webmoney', default="BRAG")
    parser.add_argument('--start_date', help='Start date for filings', default="2019-09-03")
    parser.add_argument('--end_date', help='End date for filings', default="2023-02-20")
    args = parser.parse_args()
    ic("Running script with args: {}".format(args))
    get_stonk_data(args.stock, args.start_date, args.end_date)
