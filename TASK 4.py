import csv
import requests
from bs4 import BeautifulSoup

def scrape_product_info(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }

    # Send GET request to the URL
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')

    # Find all product containers (adjust based on HTML structure of the target site)
    products = soup.find_all('div', {'class': 's-result-item'})

    product_data = []
    for product in products:
        try:
            name = product.find('span', {'class': 'a-size-base-plus a-color-base a-text-normal'}).text.strip()
            price = product.find('span', {'class': 'a-price-whole'}).text.strip()
            rating = product.find('span', {'class': 'a-icon-alt'}).text.strip().split()[0]
            product_data.append((name, price, rating))
        except AttributeError:
            continue

    return product_data

def save_to_csv(data, filename):
    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['Name', 'Price', 'Rating'])
        writer.writerows(data)
    print(f'Saved {len(data)} products to {filename}')

if __name__ == "__main__":
    # Example URL to scrape (Amazon search results)
    url = 'https://www.amazon.com/s?k=laptop'

    # Scrape product information
    product_info = scrape_product_info(url)

    # Save data to CSV
    save_to_csv(product_info, 'products.csv')
