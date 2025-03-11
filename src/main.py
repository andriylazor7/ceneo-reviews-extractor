from scraper import extract_all_pages, save_to_json, save_to_csv
from analyzer import analyze_reviews

if __name__ == "__main__":
    product_id = input("Enter product ID: ")
    opinions = extract_all_pages(product_id)

    print(f"Total opinions extracted: {len(opinions)}")

    if opinions:
        # Save to JSON & CSV
        save_to_json(opinions, product_id)
        save_to_csv(opinions, product_id)

        # Analyze data
        stats = analyze_reviews(opinions)
        print("\nStatistics:")
        for key, value in stats.items():
            print(f"{key.replace('_', ' ').capitalize()}: {value}")