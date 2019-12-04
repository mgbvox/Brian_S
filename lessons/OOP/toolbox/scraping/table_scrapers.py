import requests
import pandas as pd


def scrape_tables(url):
    # From https://stackoverflow.com/questions/43590153/http-error-403-forbidden-when-reading-html

    # Pretend to be a browser
    header = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.75 Safari/537.36",
        "X-Requested-With": "XMLHttpRequest"
    }
    r = requests.get(url, headers=header)
    dfs = pd.read_html(r.text)

    # Only return DF if more than one row.
    return dfs