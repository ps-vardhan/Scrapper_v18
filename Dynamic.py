import csv
import random
import time
import os
from datetime import datetime
from typing import List, Dict
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from urllib.parse import urlparse


def init_driver(headless=True):
    chrome_options = Options()
    if headless:
        chrome_options.add_argument("--headless=new")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/122.0.0.0 Safari/537.36")
    return webdriver.Chrome(options=chrome_options)


def get_max_page(driver, debug=False):
    try:
        pagination_links = driver.find_elements(By.CSS_SELECTOR, "a[href*='page=']")
        page_numbers = []

        for link in pagination_links:
            text = link.text.strip()
            if text.isdigit():
                page_numbers.append(int(text))

        max_page = min(max(page_numbers), 10) if page_numbers else 1
        if debug:
            print(f"[DEBUG] Detected max page: {max_page}")
        return max_page
    except Exception as e:
        print(f"[ERROR] Pagination detection failed: {str(e)}")
        return 1


def scrape_flipkart_product(product, debug=False) -> Dict[str, str]:
    try:
        name = product.find('div', class_='KzDlHZ') or product.find('a', class_='IRpwTa') or product.find('div', class_='_4rR01T')
        price = product.find('div', class_='Nx9bqj') or product.find('div', class_='_30jeq3')
        old_price = product.find('div', class_='yRaY8j') or product.find('div', class_='_3I9_wc')
        discount = product.find('div', class_='UkUFwK') or product.find('div', class_='_3Ay6Sb')
        rating = product.find('div', class_='XQDdHH') or product.find('div', class_='_3LWZlK')

        return {
            'Name': name.get_text(strip=True) if name else '',
            'Price': price.get_text(strip=True) if price else '',
            'Old Price': old_price.get_text(strip=True) if old_price else '',
            'Discount': discount.get_text(strip=True) if discount else '',
            'Rating': rating.get_text(strip=True) if rating else ''
        }

    except Exception as e:
        if debug:
            print(f"[DEBUG] Flipkart product error: {e}")
        return {}


def scrape_amazon_product(product, debug=False) -> Dict[str, str]:
    try:
        name = product.find('span', class_='a-text-normal') or product.find('h2')
        price_whole = product.select_one('span.a-price-whole')
        price_fraction = product.select_one('span.a-price-fraction')
        price = f"{price_whole.get_text(strip=True)}.{price_fraction.get_text(strip=True)}" if price_whole and price_fraction else ''
        rating = product.select_one('span.a-icon-alt')
        old_price = product.select_one('span.a-price.a-text-price')

        return {
            'Name': name.get_text(strip=True) if name else '',
            'Price': price,
            'Old Price': old_price.get_text(strip=True) if old_price else '',
            'Rating': rating.get_text(strip=True) if rating else ''
        }
    except Exception as e:
        if debug:
            print(f"[DEBUG] Amazon product error: {e}")
        return {}


def scrape_page(driver, debug=False) -> List[Dict[str, str]]:
    soup = BeautifulSoup(driver.page_source, 'html.parser')

    domain = urlparse(driver.current_url).netloc
    is_amazon = 'amazon' in domain
    is_flipkart = 'flipkart' in domain

    if is_flipkart:
        products = soup.find_all('div', {'data-id': True})
        return [scrape_flipkart_product(p, debug) for p in products]

    elif is_amazon:
        results = soup.select('div.s-result-item[data-asin]')
        return [scrape_amazon_product(p, debug) for p in results]

    else:
        print(f"[ERROR] Unsupported site: {domain}")
        return []

def save_to_csv(data_Dynamic, base_filename='products'):
    if not data_Dynamic:
        print("[INFO] No data to write.")
        return

    # Define the output directory path
    output_dir = os.path.join('Scrapper_v18', 'data_Dynamic')
    os.makedirs(output_dir, exist_ok=True)

    # Generate filename with timestamp
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = f"{base_filename}_{timestamp}.csv"
    filepath = os.path.join(output_dir, filename)

    # Save CSV
    with open(filepath, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=data_Dynamic[0].keys())
        writer.writeheader()
        writer.writerows(data_Dynamic)

    # Display only the relative path we want to show
    display_path = os.path.join('Scrapper_v18', 'data_Dynamic', filename)
    print(f"[INFO] Data saved to: {display_path}")
    return filepath



def main(search_url, headless=True, debug=False):
    driver = init_driver(headless)
    driver.get(search_url)
    time.sleep(2)

    all_data = []
    max_page = get_max_page(driver, debug)

    for page in range(1, max_page + 1):
        url = f"{search_url}&page={page}" if "flipkart" in search_url else f"{search_url}&page={page}"
        if debug:
            print(f"[DEBUG] Scraping: {url}")
        driver.get(url)
        time.sleep(random.uniform(2, 4))
        all_data.extend(scrape_page(driver, debug))

    driver.quit()
    save_to_csv(all_data)


# Example usage
if __name__ == '__main__':
    # test_url = "https://www.flipkart.com/search?q=samsung+phone"
    test_url = "https://www.amazon.in/s?k=samsung+phone"
    main(test_url, headless=True, debug=True)


