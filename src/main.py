from scraper import fetch_html, extract_all_opinions

if __name__ == "__main__":
    product_id = input("Enter product ID: ")
    html = fetch_html(product_id)

    if html:
        opinions = extract_all_opinions(html)
        for opinion in opinions:
          print(opinion)
