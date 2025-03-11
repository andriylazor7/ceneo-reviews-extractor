import requests
from bs4 import BeautifulSoup
import json

def fetch_html(product_id):
    url = f"https://www.ceneo.pl/{product_id}#tab=reviews"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36"
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.text
    except requests.RequestException as e:
        print(f"❌ Failed to fetch data for product {product_id}. Error: {e}")
        return None

def extract_all_opinions(html):
    soup = BeautifulSoup(html, "html.parser")
    opinions = soup.find_all("div", class_="user-post__card")

    if not opinions:
        print("⚠️ No opinions found. ")
        return []

    extracted_opinions = []
    for opinion in opinions:
        review_data = {
            "opinion_id": opinion.get("data-entry-id"),
            "author": opinion.find("span", class_="user-post__author-name").text.strip() if opinion.find("span", class_="user-post__author-name") else "Unknown",
            "recommendation": opinion.find("span", class_="user-post__author-recomendation").text.strip() if opinion.find("span", class_="user-post__author-recomendation") else "No recommendation",
            "score": opinion.find("span", class_="user-post__score-count").text.strip().replace(",", ".").split("/")[0] if opinion.find("span", class_="user-post__score-count") else "N/A",
            "content": opinion.find("div", class_="user-post__text").text.strip() if opinion.find("div", class_="user-post__text") else "No content",
            "advantages": ", ".join([feature.text.strip() for feature in opinion.find_all("div", class_="review-feature__item")]) if opinion.find("div", class_="review-feature__item") else "None",
            "disadvantages": ", ".join([feature.text.strip() for feature in opinion.find_all("div", class_="review-feature__item")]) if opinion.find("div", class_="review-feature__item") else "None",
            "helpful": opinion.find("button", class_="vote-yes").text.strip() if opinion.find("button", class_="vote-yes") else "0",
            "unhelpful": opinion.find("button", class_="vote-no").text.strip() if opinion.find("button", class_="vote-no") else "0",
            "publish_date": opinion.find("time", class_="user-post__published").get("datetime") if opinion.find("time", class_="user-post__published") else "N/A",
            "purchase_date": opinion.find("time", class_="user-post__published").text.strip() if opinion.find("time", class_="user-post__published") else "N/A"
        }
        extracted_opinions.append(json.dumps(review_data, indent=4, ensure_ascii=False))
    return extracted_opinions
