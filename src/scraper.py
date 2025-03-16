import requests
from bs4 import BeautifulSoup
from models import Opinion, Product

class Scraper:
    HEADERS = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36"
    }

    def __init__(self, product_id):
        self.product = Product(product_id)

    def fetch_html(self, page=1):
        if page == 1:
            url = f"https://www.ceneo.pl/{self.product.product_id}#tab=reviews"
        else:
            url = f"https://www.ceneo.pl/{self.product.product_id}/opinie-{page}"

        try:
            response = requests.get(url, headers=self.HEADERS)
            response.raise_for_status()
            return response.text
        except requests.RequestException as e:
            print(f"❌ Failed to fetch page {page}: {e}")
            return None
        
    def get_product_name(self):
        url = f'https://www.ceneo.pl/{self.product.product_id}'

        response = requests.get(url)

        if response.status_code != 200:
            print(f"Failed to retrieve product page for {self.product.product_id}")
            return None

        soup = BeautifulSoup(response.text, 'html.parser')

        product_name_tag = soup.find('h1', class_='product-top__product-info__name')
        
        if product_name_tag:
            product_name = product_name_tag.get_text(strip=True)
            return product_name
        else:
            print(f"Product name not found for {self.product.product_id}")
            return None

    def extract_opinions(self, html):
        soup = BeautifulSoup(html, "html.parser")
        opinions = soup.find_all("div", class_="user-post__card")

        if not opinions:
            print("⚠️ No opinions found. Maybe Ceneo blocked the request.")
            return []

        for opinion in opinions:
            review_data = Opinion(
                opinion_id=opinion.get("data-entry-id"),
                author=opinion.find("span", class_="user-post__author-name").text.strip() if opinion.find("span", class_="user-post__author-name") else "Unknown",
                recommendation=opinion.find("span", class_="user-post__author-recomendation").text.strip() if opinion.find("span", class_="user-post__author-recomendation") else "No recommendation",
                score=opinion.find("span", class_="user-post__score-count").text.strip().replace(",", ".").split("/")[0] if opinion.find("span", class_="user-post__score-count") else "N/A",
                content=opinion.find("div", class_="user-post__text").text.strip() if opinion.find("div", class_="user-post__text") else "No content",
                advantages = ", ".join([item.text.strip() for item in opinion.find_all("div", class_="review-feature__item") if item.find_previous("div", class_="review-feature__title") and "Zalety" in item.find_previous("div", class_="review-feature__title").text]) or "None",
                disadvantages = ", ".join([item.text.strip() for item in opinion.find_all("div", class_="review-feature__item") if item.find_previous("div", class_="review-feature__title") and "Wady" in item.find_previous("div", class_="review-feature__title").text]) or "None",
                helpful=opinion.find("button", class_="vote-yes").text.strip() if opinion.find("button", class_="vote-yes") else "0",
                unhelpful=opinion.find("button", class_="vote-no").text.strip() if opinion.find("button", class_="vote-no") else "0",
                publish_date = (opinion.find("span", class_="user-post__published").find_all("time")[0].get("datetime") if opinion.find("span", class_="user-post__published") else "N/A"),
                purchase_date = (opinion.find("span", class_="user-post__published").find_all("time")[1].get("datetime") if opinion.find("span", class_="user-post__published") and len(opinion.find("span", class_="user-post__published").find_all("time")) > 1 else "N/A")
            )

            self.product.add_opinion(review_data)

    def scrape_all_pages(self):
        page = 1
        consecutive_empty_pages = 0  

        while True:
            html = self.fetch_html(page)
            if not html:
                print(f"❌ Stopping: No HTML content on page {page}.")
                break

            opinions_count_before = len(self.product.opinions) 
            self.extract_opinions(html)
            opinions_count_after = len(self.product.opinions)  

            if opinions_count_after == opinions_count_before:  
                consecutive_empty_pages += 1
                print(f"⚠️ No opinions found on page {page}. ({consecutive_empty_pages} empty pages)")
            else:
                consecutive_empty_pages = 0  

            if consecutive_empty_pages >= 2:  
                print("🚫 Stopping scraping: No more reviews available.")
                break

            page += 1  

        return self.product

