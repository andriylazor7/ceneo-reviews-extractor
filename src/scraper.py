import requests
from bs4 import BeautifulSoup

def fetch_html(product_id):
    url = f"https://www.ceneo.pl/{product_id}#tab=reviews"
    response = requests.get(url)
    
    if response.status_code == 200:
        return response.text
    else:
        print(f"Failed to fetch data for product {product_id}. Status code: {response.status_code}")
        return None