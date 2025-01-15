from flask import Flask, render_template, request, jsonify
from bs4 import BeautifulSoup
import requests
import csv

app = Flask(__name__)

def scrape_data(url):
    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')

        # Extract data
        emails = [email['href'][7:] for email in soup.select('a[href^=mailto]')]
        contact_info = [info.get_text(strip=True) for info in soup.select('.contact-info')]
        phones = [phone.get_text(strip=True) for phone in soup.select('.phone-number')]
        websites = [website['href'] for website in soup.select('a[href^=http]')]
        addresses = [address.get_text(strip=True) for address in soup.select('.address')]
        twitters = [twitter['href'] for twitter in soup.select('a[href^=https://twitter]')]

        return {
            'emails': emails,
            'contact_info': contact_info,
            'phones': phones,
            'websites': websites,
            'addresses': addresses,
            'twitters': twitters
        }
    else:
        return None

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        url = request.form['url']
        data = scrape_data(url)

        if data:
            # Export data to CSV
            with open('scraped_data.csv', 'w', newline='', encoding='utf-8') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(['Emails', 'Contact Info', 'Phone Numbers', 'Websites', 'Addresses', 'Twitter Profiles'])
                rows = zip(data['emails'], data['contact_info'], data['phones'], data['websites'], data['addresses'], data['twitters'])
                writer.writerows(rows)

            return jsonify(data)
        else:
            return jsonify({'error': 'Failed to scrape data.'})

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
