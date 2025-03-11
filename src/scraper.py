import requests
from bs4 import BeautifulSoup
import json
import csv
import os

def fetch_html(product_id, page=1):
    if page == 1:
        url = f"https://www.ceneo.pl/{product_id}#tab=reviews"
    else:
        url = f"https://www.ceneo.pl/{product_id}/opinie-{page}"

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36"
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.text
    except requests.RequestException as e:
        print(f"❌ Failed to fetch page {page} for product {product_id}. Error: {e}")
        return None



def extract_all_opinions(html):
    soup = BeautifulSoup(html, "html.parser")
    opinions = soup.find_all("div", class_="user-post__card")

    if not opinions:
        print("⚠️ No opinions found. Maybe due to ceneo block")
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
        extracted_opinions.append(review_data)
    return extracted_opinions
  
  
def extract_all_pages(product_id):
    page = 1
    all_opinions = []
    seen_opinion_ids = set()

    while True:
        html = fetch_html(product_id, page)  # Pass page number correctly

        if not html:
            break

        opinions = extract_all_opinions(html)

        if not opinions:
            break  # Stop if no new opinions are found

        for opinion in opinions:
            if isinstance(opinion, dict) and "opinion_id" in opinion:  # Ensure correct format
                if opinion["opinion_id"] not in seen_opinion_ids:
                    seen_opinion_ids.add(opinion["opinion_id"])
                    all_opinions.append(opinion)

        page += 1  # Move to next page

    return all_opinions

def save_to_json(data, product_id):
    """Saves extracted data to a JSON file."""
    filename = f"data/{product_id}.json"

    with open(filename, "w", encoding="utf-8") as json_file:
        json.dump(data, json_file, indent=4, ensure_ascii=False)

    print(f"Data saved to {filename}")

def save_to_csv(data, product_id):
    """Saves extracted data to a CSV file."""
    if not data:
        print("⚠️ No data to save.")
        return
      
    filename = f"data/{product_id}.csv"

    keys = data[0].keys()
    with open(filename, "w", encoding="utf-8", newline="") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=keys)
        writer.writeheader()
        writer.writerows(data)

    print(f"Data saved to {filename}")


