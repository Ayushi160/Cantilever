import pandas as pd
from bs4 import BeautifulSoup
import requests
from flask import Flask, render_template, request

app = Flask(__name__)


def fetch_and_save_to_file(url):
    try:
        r = requests.get(url)
        r.raise_for_status()
        return r.text
    except requests.RequestException as e:
        print(f"Error fetching data: {e}")
        return None


def search_items(search_term):
    search_url = f"https://www.ajio.com/search/?query={search_term}"
    html_content = fetch_and_save_to_file(search_url)

    if not html_content:
        return [], []

    soup = BeautifulSoup(html_content, 'html.parser')
    spans = soup.find_all(class_="contentHolder")
    prices = soup.select("span.price")

    data = {"title": [], "price": []}

    for span in spans:
        title = span.get_text(strip=True)
        if title:
            data["title"].append(title)

    for price in prices:
        price_text = price.get_text(strip=True)
        if price_text:
            data["price"].append(price_text)

    return data["title"], data["price"]


@app.route('/', methods=['GET', 'POST'])
def index():
    titles = []
    prices = []
    if request.method == 'POST':
        search_term = request.form['search_term']
        titles, prices = search_items(search_term)

    return render_template('index.html', titles=titles, prices=prices)


if __name__ == '__main__':
    app.run(debug=True)
