import requests
from bs4 import BeautifulSoup
import csv
from flask import Flask, render_template, request, send_file

app = Flask(__name__)

def scrape_data(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    # Add code here to scrape data from the page and return the result as a list
    # For example, let's assume we are scraping the titles of articles
    result = []
    articles = soup.find_all('h2', class_='article-title')
    for article in articles:
        result.append(article.text.strip())
    return result

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/scrape', methods=['POST'])
def scrape():
    url = request.form['url']
    data = scrape_data(url)
    return render_template('index.html', data=data)

@app.route('/export', methods=['POST'])
def export():
    url = request.form['url']
    data = scrape_data(url)
    filename = 'scraped_data.csv'
    with open(filename, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['Title'])  # Modify this line based on your scraped data
        writer.writerows(data)
    return send_file(filename, as_attachment=True, mimetype='text/csv')

if __name__ == '__main__':
    app.run()

