from flask import Flask, render_template, request, redirect, url_for, send_file
from scraper import Scraper
import os
import json
import pandas as pd
import io
from visualizer import Visualizer

app = Flask(__name__, template_folder="my_templates")

if not os.path.exists("data"):
  os.makedirs("data")
  
DATA_FOLDER = os.path.join(os.getcwd(), "data")
  
def load_products():
    products = []
    for filename in os.listdir(DATA_FOLDER):
        if filename.endswith(".json"):
            product_id = filename.replace(".json", "")
            with open(os.path.join(DATA_FOLDER, filename), "r", encoding="utf-8") as file:
                opinions = json.load(file)

                num_opinions = len(opinions)
                num_with_pros = sum(1 for op in opinions if op.get("advantages") and op["advantages"] != "None")
                num_with_cons = sum(1 for op in opinions if op.get("disadvantages") and op["disadvantages"] != "None")

                valid_scores = [float(op["score"]) for op in opinions if op.get("score") not in (None, "N/A")]
                avg_score = round(sum(valid_scores) / len(valid_scores), 2) if valid_scores else 0
                
                scraper = Scraper(product_id)
                product_name = scraper.get_product_name()

                products.append({
                    "product_name": product_name,
                    "product_id": product_id,
                    "num_opinions": num_opinions,
                    "num_with_pros": num_with_pros,
                    "num_with_cons": num_with_cons,
                    "avg_score": avg_score
                })
    return products
  
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
  
  with open(json_file, "r", encoding="utf-8") as file:
    opinions = json.load(file)
    
  scraper = Scraper(product_id)
  product_name = scraper.get_product_name()
  
  return render_template("product.html", product_id=product_id, opinions=opinions, product_name=product_name, enumerate=enumerate)

@app.route('/product_list')
def product_list():
    products = load_products()
    return render_template("product_list.html", products=products)
  
@app.route('/author_page')
def author_page():
  return render_template("author.html")
  
@app.route("/download/<product_id>/<file_type>")
def download_file(product_id, file_type):
    json_path = os.path.join(DATA_FOLDER, f"{product_id}.json")

    if file_type == "xlsx":
        if not os.path.exists(json_path):
            return "Product data not found", 404

        with open(json_path, "r", encoding="utf-8") as file:
            data = json.load(file)

        df = pd.DataFrame(data)

        output = io.BytesIO()
        with pd.ExcelWriter(output, engine="openpyxl") as writer:
            df.to_excel(writer, index=False)
        output.seek(0)

        return send_file(output, as_attachment=True, download_name=f"{product_id}.xlsx", mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")

    file_path = os.path.join(DATA_FOLDER, f"{product_id}.{file_type}")
    
    if os.path.exists(file_path):
        return send_file(file_path, as_attachment=True)
    
    return "File not found", 404
  
@app.route("/product/<product_id>/charts")
def show_charts(product_id):
    file_path = f"{DATA_FOLDER}/{product_id}.json"

    try:
        with open(file_path, "r", encoding="utf-8") as file:
            opinions = json.load(file)
    except FileNotFoundError:
        return "Product data not found", 404
      
    visualizer = Visualizer(opinions)

    pie_chart = visualizer.plot_recommendation_pie_base64()
    bar_chart = visualizer.plot_ratings_bar_base64()
    
    scraper = Scraper(product_id)
    product_name = scraper.get_product_name()

    return render_template("charts.html", product_id=product_id, product_name=product_name, pie_chart=pie_chart, bar_chart=bar_chart)


if __name__ == "__main__":
  app.run(debug=True)

