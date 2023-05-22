import csv
import pandas as pd
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

websites_file = 'websites.parquet'
output_file = 'addresses.csv'
errors_file = 'errors.csv'


def extract_addresses(url):
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            address = {}

            # Extract country
            address_element = soup.find('span', class_=['contact-text', 'et_pb_text_inner', 'sqs-block-content'])
            if address_element:
                country_text = address_element.get_text(strip=True)
                if country_text:
                    address['country'] = country_text

            # Extract region
            address_element = soup.find('span', class_=['region-text', 'location', 'region'])
            if address_element:
                region_text = address_element.get_text(strip=True)
                if region_text:
                    address['region'] = region_text

            # Extract city
            address_element = soup.find('span', class_=['city-text', 'city', 'town-text'])
            if address_element:
                city_text = address_element.get_text(strip=True)
                if city_text:
                    address['city'] = city_text

            # Extract postcode
            address_element = soup.find('span', class_=['postcode-text', 'postcode', 'postcode_text'])
            if address_element:
                postcode_text = address_element.get_text(strip=True)
                if postcode_text:
                    address['postcode'] = postcode_text

            # Extract road
            address_element = soup.find('span', class_=['street-text', 'road', 'street'])
            if address_element:
                road_text = address_element.get_text(strip=True)
                if road_text:
                    address['road'] = road_text

            # Extract road number
            address_element = soup.find('span', class_=['streetNr', 'street_nr', 'roadNr'])
            if address_element:
                roadNr_text = address_element.get_text(strip=True)
                if roadNr_text:
                    address['road number'] = roadNr_text

            if address:
                return address

    except requests.RequestException:
        pass

    return None


def process_website(website):
    base_url = f"http://{website}"
    subdomains = ['homepage', 'home', 'contact', 'index.php/contact']
    error_code = None
    addresses = []

    for subdomain in subdomains:
        url = urljoin(base_url, subdomain)
        address = extract_addresses(url)
        if address:
            addresses.append({
                'Website': website,
                'Country': address.get('country'),
                'Region': address.get('region'),
                'City': address.get('city'),
                'Postcode': address.get('postcode'),
                'Road': address.get('road'),
                'Road Number': address.get('road number')
            })

    if not addresses:
        try:
            response = requests.get(base_url, timeout=10)
            error_code = response.status_code
        except requests.RequestException:
            error_code = 'Error'

    return website, addresses, error_code


def main():
    # Read websites from the file
    df = pd.read_parquet(websites_file)
    df = df.head(5)  # Limit the number of websites for testing purposes
    websites = df['domain'].tolist()

    addresses = []
    errors = []

    # Process each website
    for website in websites:
        website, address, error_code = process_website(website)
        if address:
            if isinstance(address, list):
                for addr in address:
                    addresses.append({
                        'Website': website,
                        'Country': addr.get('country'),
                        'Region': addr.get('region'),
                        'City': addr.get('city'),
                        'Postcode': addr.get('postcode'),
                        'Road': addr.get('road'),
                        'Road Number': addr.get('road number')
                    })
            else:
                addresses.append({
                    'Website': website,
                    'Country': address.get('country'),
                    'Region': address.get('region'),
                    'City': address.get('city'),
                    'Postcode': address.get('postcode'),
                    'Road': address.get('road'),
                    'Road Number': address.get('road number')
                })
        if error_code and error_code != 200:
            errors.append({'Website': website, 'Error': error_code})

    # Write addresses to CSV file
    if addresses:
        with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['Website', 'Country', 'Region', 'City', 'Postcode', 'Road', 'Road Number']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(addresses)

    # Write errors to CSV file
    if errors:
        with open(errors_file, 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['Website', 'Error']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(errors)


if __name__ == '__main__':
    main()
