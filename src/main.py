from scraper import extract_all_pages

if __name__ == "__main__":
    product_id = input("Enter product ID: ")
    opinions = extract_all_pages(product_id)

    print(f"Total opinions extracted: {len(opinions)}")
    for opinion in opinions:
      print(opinion)