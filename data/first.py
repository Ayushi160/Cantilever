import pandas as pd
from bs4 import BeautifulSoup
import requests
def fetchAndSaveToFile(html, path):
    r= requests.get(html)
    r.raise_for_status()
    with open(path, "w", encoding='utf-8') as f:
        f.write(r.text)
        return r.text

html= "https://www.ajio.com/women-bags-belts-wallets/c/830301"

html_content=fetchAndSaveToFile(html,"data1.html")
soup = BeautifulSoup(html_content, 'html.parser')
spans= soup.find_all(class_="contentHolder")
prices= soup.select("span.price")
data ={"title":[], "price":[]}
for span in spans:
    print(span.get_text(strip=True))
    data["title"].append(span.get_text(strip=True))

for price in prices:
    print(price.get_text(strip=True))
    data["price"].append(price.get_text(strip=True))

df = pd.DataFrame.from_dict(data)
df.to_excel("data.xlsx", index=False)