
from playwright.sync_api import sync_playwright
import pandas as pd

def main():
    books_df = []

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        page.goto('https://www.nytimes.com/books/best-sellers/2022/09/11/combined-print-and-e-book-fiction/')
       
        for i in range(1, 20):    
            date = page.locator('[class="css-6068ga"]').inner_text()
            names = page.query_selector_all('[class="css-5pe77f"]')
            authors = page.query_selector_all('[class="css-hjukut"]')
            descriptions = page.query_selector_all('[class="css-14lubdp"]')
            images = page.query_selector_all('img')

            for j in range(len(names)):
                book_info = {
                    'date': date,
                    'name': names[j].inner_text(),
                    'author': authors[j].inner_text().removeprefix('by '),
                    'description': descriptions[j].inner_text(),
                    'image': images[j].get_attribute('src')
                }
                books_df.append(book_info)

            page.locator('[class="css-1g4pqde"]').click()
        browser.close()
    pd.DataFrame(books_df).to_csv('nyt.csv', index = False)


if __name__ == '__main__':
    main()