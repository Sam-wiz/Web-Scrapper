from http.server import BaseHTTPRequestHandler, HTTPServer
import requests
from bs4 import BeautifulSoup
from urllib.parse import quote
import time

# Function to scrape data from Amazon
def scrape_amazon(product_name):
    amazon_url = f"https://www.amazon.in/s?k={quote(product_name)}"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36',
    }

    response = requests.get(amazon_url, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')

    # Extract data from Amazon
    product_list = soup.find_all('div', {'data-component-type': 's-search-result'})
    amazon_data = []

    for product in product_list:
        title_element = product.find('span', {'class': 'a-text-normal'})
        price_element = product.find('span', {'class': 'a-price-whole'})
        if title_element and price_element:
            title = title_element.text.strip()
            price = price_element.text.strip()
            amazon_data.append((title, price))

    return amazon_data

# Function to scrape data from Flipkart
def scrape_flipkart(product_name):
    max_retries = 3  # Maximum number of retry attempts
    retries = 0

    while retries < max_retries:
        flipkart_url = f"https://www.flipkart.com/search?q={quote(product_name)}"
        headers = { "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/119.0", 
           "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,/;q=0.8" }

        try:
            response = requests.get(flipkart_url, headers=headers)
            response.raise_for_status()  # Raise an exception for 4xx and 5xx HTTP status codes
        except requests.exceptions.RequestException as e:
            print(f"Failed to connect to Flipkart: {e}")
            retries += 1
            time.sleep(5)  # Wait for a few seconds before the next attempt
            continue

        soup = BeautifulSoup(response.content, 'html.parser')

        # Extract data from Flipkart using the updated class names
        product_list = soup.find_all('div', {'class': '_1AtVbE'})
        flipkart_data = []

        for product in product_list:
            title_element = product.find('div', {'class': '_4rR01T'})
            price_element = product.find('div', {'class': '_30jeq3'}) # Updated class name
            if title_element and price_element:
                title = title_element.text.strip()
                price =price_element.text.strip().replace('₹', '')
                flipkart_data.append((title, price))
        
        if flipkart_data:
            return flipkart_data  # If data is successfully scraped, return it

        retries += 1
        time.sleep(5)  # Wait for a few seconds before the next attempt

    return [] 

# HTML template for the form
form_template = """
<!DOCTYPE html>
<html>
<head>
    <title>Product Price Comparison</title>
    <style>
        h1
        {
            text-align: center;
            font-size: 50px;
            color: aliceblue;
        }
        .bg {
            animation:slide 3s ease-in-out infinite alternate;
            background-image: linear-gradient(-60deg, #000000 50%, rgb(31, 33, 33) 50%);
            bottom:0;
            left:-50%;
            opacity:.5;
            position:fixed;
            right:-50%;
            top:0;
            z-index:-1;
        }
        div
        {
            word-wrap: break-word;
        }
        .bg2 {
            animation-direction:alternate-reverse;
            animation-duration:4s;
        }
        
        .bg3 {
            animation-duration:3s;
        }
        
        
        @keyframes slide {
            0% {
            transform:translateX(-25%);
            }
            100% {
            transform:translateX(25%);
            }
        }
        form {
            margin-top: 10%;
            text-align: center;
        }

        label {
            color: aqua;
            font-size: 35px;
            margin-bottom: 10px;
        }

        input[type="text"] {
            display: block;
            margin: 30%;
            margin-top: 30px;
            margin-bottom: 30px;
            width: 50%;
            padding: 10px;
            font-size: 1em;
        }

        input[type="submit"] {
            margin-top: 10px;
            padding: 10px 20px;
            font-size: 1em;
            background-color: #4CAF50;
            color: white;
            border: none;
            cursor: pointer;
        }
        p
        {
            text-align: center;
            color: cyan;
            margin-top: 20%;
            font-size: 30px;
        }
    </style>
</head>
<body>
    <h1>Welcome to WebScrapper</h1>
    <div class="bg"></div>
    <div class="bg bg2"></div>
    <div class="bg bg3"></div>
    <form method="post">
        <label for="product_name">Enter Product Name:</label>
        <input type="text" name="product_name" id="product_name" required>
        <input type="submit" value="Search">
    </form>
    <div class="footer">
        <p>Made by Samrudh (A simple frontend page)</p>
    </div>
</body>
</html>
"""

# HTML template for displaying results in a table
# HTML template for displaying results in a table
results_template = """
<!DOCTYPE html>
<html>
<head>
    <title>Product Price Comparison</title>
    <style>
        .bg
        {{
            animation:slide 3s ease-in-out infinite alternate;
            background-image: linear-gradient(-60deg, #030303 50%, rgb(31, 33, 33) 50%);
            bottom:0;
            left:-50%;
            opacity:.5;
            position:fixed;
            right:-50%;
            top:0;
            z-index:-1;
        }}
        .bg2
        {{
            animation-direction:alternate-reverse;
            animation-duration:4s;
        }}
        .bg3
        {{
            animation-duration:3s;
        }}
        @keyframes slide {{
            0% {{
            transform:translateX(-25%);
            }}
            100% {{
            transform:translateX(25%);
            }}
        }}
        table {{
            color: aliceblue;
            border-collapse: collapse;
            width: 80%;
            align-items: center;
            margin: auto;
            border-color: aliceblue;
        }}
        th, td {{
            text-align: left;
            padding: 8px;
            word-wrap: break-word;
        }}
        th
        {{
            font-size: 15px;
        }}
        h2{{
            text-align: center;
            font-size: 35px;
            color: cyan;
            margin: 5%;
        }}
        p
        {{
            text-align: center;
            font-size: 25px;
            margin: 10%;
            margin-bottom: 40px;
            color: cyan;
        }}
        a
        {{
            text-decoration: none;
            color: aliceblue;
            margin-top: 20%;
            padding: 10px 20px;
            font-size: 1em;
            background-color: #4CAF50;
            color: white;
            border: none;
            cursor: pointer;
            align-items: center;
            margin-left: 49%;
        }}
        #search
        {{
            margin-top: 10%;
        }}
        form {{
            margin-top: 10%;
            text-align: center;
        }}

        label {{
            color: aqua;
            font-size: 35px;
            margin-bottom: 10px;
        }}

        input[type="text"] {{
            display: block;
            margin: 30%;
            margin-top: 30px;
            margin-bottom: 30px;
            width: 50%;
            padding: 10px;
            font-size: 1em;
        }}

        input[type="submit"] {{
            margin-top: 10px;
            padding: 10px 20px;
            font-size: 1em;
            background-color: #4CAF50;
            color: white;
            border: none;
            cursor: pointer;
            margin-bottom: 30%;
        }}
    </style>
</head>
<body>
    <div class="bg"></div>
    <div class="bg bg2"></div>
    <div class="bg bg3"></div>
    <h2>Amazon Results:</h2>
    <table>
        <tr>
            <th>Product Title</th>
            <th>Price</th>
        </tr>
        {}
    </table>
    <h2>Flipkart Results:</h2>
    <table>
        <tr>
            <th>Product Title</th>
            <th>Price</th>
        </tr>
        {}
    </table>
    <p> Search for other product </p>
    <div id="search">
        <form method="post">
            <label for="product_name">Enter Product Name:</label>
            <input type="text" name="product_name" id="product_name" required>
            <input type="submit" value="Search">
        </form>
    </div>
</body>
</html>
"""

# ...


class RequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(form_template.encode())

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length).decode('utf-8')
        product_name = post_data.split('=')[1]

        amazon_data = scrape_amazon(product_name)
        flipkart_data = scrape_flipkart(product_name)

        amazon_table = "\n".join([f"<tr><td>{title}</td><td>{price}</td></tr>" for title, price in amazon_data])
        flipkart_table = "\n".join([f"<tr><td>{title}</td><td>{price}</td></tr>" for title, price in flipkart_data])

        response = results_template.format(amazon_table, flipkart_table)

        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(response.encode())

if __name__ == '__main__':
    server = HTTPServer(('', 8000), RequestHandler)
    print('Starting server, use <Ctrl-C> to stop')
    server.serve_forever()
