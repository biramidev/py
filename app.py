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

        # Print the scraped data for debugging purposes
        print('Emails:', [email['href'][7:] for email in email_elements])
        print('Contact Info:', [info.get_text(strip=True) for info in contact_info_elements])
        print('Phone Numbers:', [phone.get_text(strip=True) for phone in phone_elements])
        print('Websites:', [website['href'] for website in website_elements])
        print('Addresses:', [address.get_text(strip=True) for address in address_elements])
        print('Twitter Profiles:', [twitter['href'] for twitter in twitter_elements])

        return None  # Return None to indicate no error occurred
    else:
        print('Request failed with status code:', response.status_code)
        return response.status_code  # Return the status code indicating an error occurred



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
