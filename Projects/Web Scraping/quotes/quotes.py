
from playwright.sync_api import sync_playwright

def main():
    quotes_df = []

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
       
        for i in range(1,10):    
            page.goto(f'https://www.goodreads.com/quotes?page={i}')
            quotes = page.query_selector_all('[class="quoteText"]')
            for quote in quotes:
                quotes_df.append(quote.inner_text())

        browser.close()
    print(len(quotes_df))


if __name__ == '__main__':
    main()