import csv
import requests
from bs4 import BeautifulSoup

# Function to scrape data from the provided URL
def scrape_data(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')

    product_details = []
    for item in soup.find_all('div', class_='s-result-item'):
        product_name_elem = item.find('span', class_='a-size-base-plus a-color-base a-text-normal')
        product_name = product_name_elem.get_text().strip() if product_name_elem else "Not Available"

        product_price_elem = item.find('span', class_='a-price')
        product_price = product_price_elem.get_text().strip() if product_price_elem else "Not Available"

        product_url_elem = item.find('a', class_='a-link-normal')
        product_url = 'https://www.amazon.in' + product_url_elem['href'] if product_url_elem and 'href' in product_url_elem.attrs else "Not Available"

        product_rating_elem = item.find('span', class_='a-icon-alt')
        product_rating = product_rating_elem.get_text().strip() if product_rating_elem else "Not Available"

        product_reviews_elem = item.find('span', class_='a-size-base')
        product_reviews = product_reviews_elem.get_text().strip() if product_reviews_elem else "Not Available"

        product_details.append([product_name, product_price, product_url, product_rating, product_reviews])

    return product_details

# Define the URL
url = "https://www.amazon.in/s?k=bags&crid=2M096C61O4MLT&qid=1653308124&sprefix=ba%2Caps%2C283&ref=sr_pg_1"

# Perform the scraping
all_product_details = []
for page in range(1, 21):  
    current_url = url + f'&page={page}'
    all_product_details.extend(scrape_data(current_url))

# Write the scraped data to a CSV file
with open('scraped_data.csv', mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(["Product Name", "Product Price", "Product URL", "Product Rating", "Product Reviews"])
    for product in all_product_details:
        writer.writerow(product)
