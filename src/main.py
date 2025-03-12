from scraper import Scraper
from visualizer import plot_recommendation_pie, plot_ratings_bar

if __name__ == "__main__":
    product_id = input("Enter product ID: ")
    
    scraper = Scraper(product_id)
    product = scraper.scrape_all_pages() 

    print(f"Total opinions extracted: {len(product.opinions)}")

    if product.opinions:
        product.save_to_json()
        product.save_to_csv()

        stats = product.get_statistics()
        print("\n📊 Statistics:")
        for key, value in stats.items():
            print(f"{key.replace('_', ' ').capitalize()}: {value}")

        plot_recommendation_pie(product.opinions)
        plot_ratings_bar(product.opinions)
