import time
import requests
from bs4 import BeautifulSoup
import pandas as pd

# Define headers to mimic a real browser request
HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36"
    )
}

def fetching_content(url):
    """
    Sends a GET request to the provided URL and returns the response content if successful.
    """
    session = requests.Session()
    response = session.get(url, headers=HEADERS)
    try:
        response.raise_for_status()
        return response.content
    except requests.exceptions.RequestException as e:
        print(f"Error requesting {url}: {e}")
        return None

def extract_product_data(article):
    """
    Extracts product information from an article element.
    """
    product_title = article.find('h3', class_='product-title').text
    product_element = article.find('div', class_='price-container')
    price = product_element.find('span', class_='price').text

    details = product_element.find_all('p')
    if len(details) >= 5:
        rating = details[1].text
        colors = details[2].text
        size = details[3].text
        gender = details[4].text
    else:
        rating = colors = size = gender = "N/A"

    products = {
        "Title": product_title,
        "Price": price,
        "Rating": rating,
        "Colors": colors,
        "Size": size,
        "Gender": gender,
    }

    return products


def scrape_product(base_url, start_page=1, delay=2):
    """
    Scrapes product data from the paginated product pages of the given base URL.

    Args:
        base_url (str): Base URL with a placeholder for page number (used from page 2 onward).
        start_page (int): Page number to start scraping from.
        delay (int): Delay in seconds between page requests.

    Returns:
        list: List of dictionaries containing product data.
    """
    data = []
    page_number = start_page

    while True:
        if page_number == 1:
            url = 'https://fashion-studio.dicoding.dev/'  # First page
        else:
            url = base_url.format(page_number)  # Subsequent pages

        print(f"Scraping page: {url}")

        content = fetching_content(url)
        if content:
            soup = BeautifulSoup(content, "html.parser")
            articles_element = soup.find_all('div', {"id": "collectionList"}, class_='collection-grid')
            for article in articles_element:
                product = extract_product_data(article)
                data.append(product)

            next_button = soup.find('li', class_='page-item next')
            if next_button:
                page_number += 1
                time.sleep(delay)
            else:
                break
        else:
            break

    return data


def main():
    """
    Main function to execute the entire scraping process and display the results as a DataFrame.
    """
    BASE_URL = 'https://fashion-studio.dicoding.dev/page{}'
    all_products = scrape_product(BASE_URL)
    df = pd.DataFrame(all_products)
    print(df)

if __name__ == '__main__':
    main()
