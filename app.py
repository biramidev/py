from flask import Flask, render_template, request, jsonify
from bs4 import BeautifulSoup
import requests
import csv

app = Flask(__name__)

def scrape_data(url):
    # Make a request to the provided URL
    response = requests.get(url)

    # Check if the request was successful
    if response.status_code == 200:
        # Parse the HTML content of the page
        soup = BeautifulSoup(response.content, 'html.parser')

        # Find the elements containing the desired data
        email_elements = soup.select('a[href^=mailto]')
        contact_info_elements = soup.select('.contact-info')
        phone_elements = soup.select('.phone-number')
        website_elements = soup.select('a[href^=http]')
        address_elements = soup.select('.address')
        twitter_elements = soup.select('a[href^=https://twitter]')

        # Extract the text from the elements
        emails = [email['href'][7:] for email in email_elements]
        contact_info = [info.get_text(strip=True) for info in contact_info_elements]
        phones = [phone.get_text(strip=True) for phone in phone_elements]
        websites = [website['href'] for website in website_elements]
        addresses = [address.get_text(strip=True) for address in address_elements]
        twitters = [twitter['href'] for twitter in twitter_elements]

        # Return the scraped data as a dictionary
        scraped_data = {
            'emails': emails,
            'contact_info': contact_info,
            'phones': phones,
            'websites': websites,
            'addresses': addresses,
            'twitters': twitters
        }

        return scraped_data
    else:
        return None


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        url = request.form['url']
        data = scrape_data(url)

        if data is not None:
            # Export data to CSV file
            with open('scraped_data.csv', 'w', newline='', encoding='utf-8') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(['Emails', 'Contact Info', 'Phone Numbers', 'Websites', 'Addresses', 'Twitter Profiles'])
                writer.writerows(zip(data['emails'], data['contact_info'], data['phones'], data['websites'], data['addresses'], data['twitters']))

            return jsonify(data)
        else:
            return jsonify({'error': 'Failed to scrape data.'})

    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)
