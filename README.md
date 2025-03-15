# Ceneo Reviews Extractor

The **Ceneo Reviews Extractor** collects product reviews from [Ceneo.pl](https://www.ceneo.pl), analyzes the data, and provides insights through visualizations. The project is built using Python, **BeautifulSoup**, **Flask**, and **Matplotlib**, and allows users to download reviews in multiple formats (CSV, JSON, Excel). For handling and manipulating data, **pandas** was used, and for reading/writing Excel files, **openpyxl** was utilized.

## How application works
Application extracts opinions about products from the Ceneo.pl website. For product, the code of which will be given as a parameter, its name and all available opinions about it is extracted. For each review applications extracts:
  - opinion ID
  - opinion’s author
  - author’s recommendation
  - score expressed in number of stars
  - opinion’s content
  - list of product advantages
  - list of product disadvantages
  - how many users think that opinion was helpful
  - how many users think that opinion was unhelpful
  - publishing date
  - purchase date

In addition, the application allows to display:
  - extracted opinions with all its components
  - statistics about extracted reviews
  - charts showing these statistics

## Project Structure
```
.
├── data/
├── src/
    ├── my_templates/
        ├── author.html
        ├── charts.html
        ├── extract.html
        ├── index.html
        ├── product_list.html
        ├── product.html
    ├── app.py
    ├── models.py
    ├── scraper.py
    ├── visualizer.py
└── .gitignore  
└── README.md
└── requirements.txt
```

## Installation
### Prerequisites
- Python 3.10+
- Virtual environment

### Steps
1. Clone the repository:
```bash
git clone https://github.com/andriylazor7/ceneo-reviews-extractor.git
```

2. Navigate to the project directory:
```bash
cd ceneo-reviews-extractor
```

3. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Linux or macOS
venv\Scripts\activate    # On Windows
```

4. Install the dependencies:
```bash
pip install -r requirements.txt
```

## Running
Run the main script to start the extraction and web interface:
```bash
python src/app.py
```
Access the web interface at `http://127.0.0.1:5000`.

