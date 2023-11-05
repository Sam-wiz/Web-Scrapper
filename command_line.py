import requests
from bs4 import BeautifulSoup

# Function to scrape data from Amazon
def scrape_amazon(product_name):
    amazon_url = f"https://www.amazon.in/s?k={product_name.replace(' ', '+')}"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36',  # Set your User Agent
    }

    response = requests.get(amazon_url, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')

    # Extract data from Amazon
    product_list = soup.find_all('div', {'data-component-type': 's-search-result'})
    amazon_data = []

    for product in product_list:
        title = product.find('span', {'class': 'a-text-normal'}).text.strip()
        price = product.find('span', {'class': 'a-price-whole'}).text.strip()
        amazon_data.append((title, price))

    return amazon_data

# Function to scrape data from Flipkart
def scrape_flipkart(product_name):
    flipkart_url = f"https://www.flipkart.com/search?q={product_name.replace(' ', '+')}"
    headers = { "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/119.0", 
           "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,/;q=0.8" }

    try:
        response = requests.get(flipkart_url, headers=headers)
        response.raise_for_status()  # Raise an exception for 4xx and 5xx HTTP status codes
    except requests.exceptions.RequestException as e:
        print(f"Failed to connect to Flipkart: {e}")
        return []

    soup = BeautifulSoup(response.content, 'html.parser')

    # Extract data from Flipkart using the updated class names
    product_list = soup.find_all('div', {'class': '_1AtVbE'})
    flipkart_data = []

    for product in product_list:
        title_element = product.find('div', {'class': '_4rR01T'})
        price_element = product.find('div', {'class': '_30jeq3'}) # Updated class name
        if title_element and price_element:
            title = title_element.text.strip()
            price = price_element.text.strip()
            flipkart_data.append((title, price))
    return flipkart_data


# Main function to scrape and display data
def main():
    product_name = input("Enter the product name: ")

    amazon_data = scrape_amazon(product_name)
    flipkart_data = scrape_flipkart(product_name)

    print("Amazon Results:")
    for i, (title, price) in enumerate(amazon_data, start=1):
        print(f"{i}. {title} - {price}")

    print("\nFlipkart Results:")
    for i, (title, price) in enumerate(flipkart_data, start=1):
        print(f"{i}. {title} - {price}")

if __name__ == "__main__":
    main()
