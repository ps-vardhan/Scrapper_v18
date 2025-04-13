# Web Scraping Projects

This repository contains two web scraping projects:

1. **E-commerce Product Scraper** (`Dynamic.py`)
2. **W3Schools Tutorial Scraper** (`Static.py`)

---

## Project Structure

```
Scrapper_v18/
├── data_Dynamic/       # Output directory for e-commerce product data
├── data_Static/        # Output directory for W3Schools tutorial content
├── myenv/              # Virtual environment (optional)
├── Dynamic.py          # E-commerce product scraper
├── Static.py           # W3Schools tutorial scraper
└── README.md           # This documentation file
```

---

## 1. E-commerce Product Scraper (`Dynamic.py`)

Scrapes product information from e-commerce websites like **Amazon** and **Flipkart**.

### Features
- Extracts product name, price, discount, and rating
- Supports pagination (up to 10 pages)
- Saves data in CSV format inside `data_Dynamic/`
- Uses **Selenium** for handling JavaScript-rendered content
- Configurable for different search URLs and categories

### Usage

```bash
python Dynamic.py
```

By default, it scrapes Samsung phones from Amazon.

To scrape another category, modify the `main()` function call inside `Dynamic.py`:

```python
main("https://www.flipkart.com/search?q=laptops", headless=True, debug=True)
```

### Output
- Format: `products_YYYYMMDD_HHMMSS.csv`
- Location: `data_Dynamic/`

---

## 2. W3Schools Tutorial Scraper (`Static.py`)

Scrapes static tutorial content from W3Schools HTML tutorial pages.

###  Features
- Extracts page titles and full tutorial content
- Follows pagination through tutorial series
- Saves each page as a `.txt` file
- Uses **Requests** and **BeautifulSoup** (no browser automation)

### Usage

```bash
python Static.py
```

By default, it scrapes the HTML tutorial series.

To scrape a different tutorial, update the `start_url` variable:

```python
start_url = "https://www.w3schools.com/python/default.asp"
```

### Output
- Format: `Page_Title.txt`
- Location: `data_Static/`

---

## Requirements

- Python 3.6 or higher
- Required packages:

```bash
pip install requests beautifulsoup4 selenium
```

- ChromeDriver (required for `Dynamic.py`)

---

## Setup Instructions

1. **Clone this repository:**

```bash
git clone https://github.com/your-username/scrapper_v18.git
cd scrapper_v18
```

2. **Install dependencies:**

```bash
pip install -r requirements.txt
```

3. **Setup ChromeDriver (for Dynamic Scraper):**
   - Download ChromeDriver: https://sites.google.com/chromium.org/driver/
   - Make sure it's in your system `PATH`

---

##  Notes

- Both scripts are designed to respect websites' `robots.txt` and terms of service.
- Introduce appropriate delays between requests to avoid server overload.
- Output directories are created automatically if they don’t exist.
- Always test scrapers with `headless=False` during development to debug UI issues.
- Logging and error handling can be extended for robustness.

---

## Optional Enhancements

You can expand this project by:
- Adding user-agent rotation and proxy support
- Exporting data to databases (SQLite, MongoDB, etc.)
- Adding CLI arguments for dynamic input
- Supporting more tutorial platforms or e-commerce sites

---

## Legal Disclaimer

This project is for educational purposes only. Ensure compliance with the terms of service of any website you scrape.

---

## Contributions

Contributions are welcome! Please submit a pull request or open an issue if you’d like to contribute or report bugs.

