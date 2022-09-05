
from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
import pandas as pd

def main():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        page.goto('https://www.baseball-reference.com/')

        urls = []
        for league in ['AL','NL']:
            table = page.locator(f'[id="standings_{league}"]').inner_html()
            soup = BeautifulSoup(table, features='lxml')
            links = soup.find_all('a')
            links = [l.get("href") for l in links] # get reference urls for those links
            links = [f"https://www.baseball-reference.com{l}" for l in links] 
            urls = urls + links
        print(urls)

        
        browser.close()


if __name__ == '__main__':
    main()