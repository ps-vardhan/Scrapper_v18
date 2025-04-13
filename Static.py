import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import os
import re

def sanitize_filename(title):
    """Convert title to a safe filename"""
    return re.sub(r'[\\/*?:"<>|]', "", title).strip()

def scrape_w3schools_page(url, output_dir='data_Static'):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Extract page title
        title_tag = soup.find('title')
        title = title_tag.text.strip() if title_tag else 'Untitled'
        safe_title = sanitize_filename(title)
        
        # Create output directory if it doesn't exist
        os.makedirs(output_dir, exist_ok=True)
        
        # Extract main content
        main_content = soup.find('div', id='main') or soup.find('main') or soup.find('body')
        content_text = main_content.get_text('\n', strip=True) if main_content else "Content not found"
        
        # Save to file
        filename = f"{safe_title}.txt"
        filepath = os.path.join(output_dir, filename)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(f"URL: {url}\n")
            f.write(f"Title: {title}\n\n")
            f.write(content_text)
        
        # Display only the relative path we want to show
        display_path = os.path.join('data_Static', filename)
        print(f"Saved: {display_path}")
        return True
        
    except Exception as e:
        print(f"Error scraping {url}: {e}")
        return False

def get_next_page_url(current_url, soup):
    """Find the URL for the next page in the tutorial"""
    next_button = soup.find('a', class_='w3-right w3-btn')
    if next_button and 'Next ❯' in next_button.text:
        return urljoin(current_url, next_button['href'])
    return None

def scrape_w3schools_tutorial(start_url, max_pages=10):
    current_url = start_url
    pages_scraped = 0
    
    while current_url and pages_scraped < max_pages:
        print(f"\nScraping page {pages_scraped + 1}: {current_url}")
        
        # Scrape the current page
        success = scrape_w3schools_page(current_url)
        if not success:
            break
        
        # Get the next page URL
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }
            response = requests.get(current_url, headers=headers)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')
            
            current_url = get_next_page_url(current_url, soup)
            pages_scraped += 1
            
        except Exception as e:
            print(f"Error getting next page: {e}")
            break
    
    print(f"\nCompleted! Scraped {pages_scraped} pages. Files saved in data_Static")

# Start scraping from the HTML tutorial homepage
start_url = "https://www.w3schools.com/html/default.asp"
scrape_w3schools_tutorial(start_url, max_pages=10)