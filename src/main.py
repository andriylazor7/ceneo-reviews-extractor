from scraper import fetch_html, extract_single_opinion

if __name__ == "__main__":
    product_id = input("Enter product ID: ")
    html = fetch_html(product_id)

    if html:
        opinion = extract_single_opinion(html)
        print(opinion)
