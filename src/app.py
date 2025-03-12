from flask import Flask, render_template, request, redirect, url_for
from scraper import Scraper
import os

app = Flask(__name__, template_folder="my_templates")

if not os.path.exists("data"):
  os.makedirs("data")
  
@app.route("/")
def home():
  return render_template("index.html")

@app.route("/extract", methods=["GET", "POST"])
def extract():
  if request.method == "POST":
    product_id = request.form.get("product_id")
    
    if not product_id:
      return render_template("extract.html", error="Please enter a product ID.")
    
    if not product_id.isdigit():
      return render_template("extract.html", error="Please enter valid product ID. ")
      
    
    scraper = Scraper(product_id)
    product = scraper.scrape_all_pages()
    
    if not product.opinions:
      return render_template("extract.html", error="No opinions found for this product.")
    
    product.save_to_json()
    product.save_to_csv()
    
    return redirect(url_for("product", product_id=product_id))
  
  return render_template("extract.html")

@app.route("/product/<product_id>")
def product(product_id):
  json_file = f"data/{product_id}.json"
  
  if not os.path.exists(json_file):
    return "Product data not found.", 404
  
  return render_template("product.html", product_id=product_id)


if __name__ == "__main__":
  app.run(debug=True)

