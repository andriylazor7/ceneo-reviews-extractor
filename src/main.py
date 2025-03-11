from scraper import extract_all_pages, save_to_json, save_to_csv

if __name__ == "__main__":
    product_id = input("Enter product ID: ")
    opinions = extract_all_pages(product_id)

    print(f"Total opinions extracted: {len(opinions)}")

    if opinions:
        save_to_json(opinions, product_id)

        save_to_csv(opinions, product_id)